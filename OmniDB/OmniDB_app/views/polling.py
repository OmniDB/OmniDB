from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from datetime import datetime
from math import ceil
import json
import time
import threading
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB.startup import clean_temp_folder

from enum import IntEnum
from django.utils.timezone import make_aware
from OmniDB import settings
import sys
import os
import sqlparse

import paramiko
import OmniDB_app.include.custom_paramiko_expect as custom_paramiko_expect

from django.contrib.auth.models import User
from OmniDB_app.models.main import Tab, QueryHistory, Connection, ConsoleHistory

from OmniDB_app.views.memory_objects import clear_client_object, get_client_object, close_tab_handler, create_tab_object, get_database_tab_object

import traceback

import logging
logger = logging.getLogger('OmniDB_app.QueryServer')

class requestType(IntEnum):
    Login          = 0
    Query          = 1
    Execute        = 2
    Script         = 3
    QueryEditData  = 4
    SaveEditData   = 5
    CancelThread   = 6
    Debug          = 7
    CloseTab       = 8
    AdvancedObjectSearch     = 9
    Console        = 10
    Terminal       = 11
    Ping           = 12

class response(IntEnum):
    LoginResult         = 0
    QueryResult         = 1
    QueryEditDataResult = 2
    SaveEditDataResult  = 3
    SessionMissing      = 4
    PasswordRequired    = 5
    QueryAck            = 6
    MessageException    = 7
    DebugResponse       = 8
    RemoveContext       = 9
    AdvancedObjectSearchResult    = 10
    ConsoleResult       = 11
    TerminalResult      = 12
    Pong                = 13

class debugState(IntEnum):
    Initial  = 0
    Starting = 1
    Ready    = 2
    Step     = 3
    Finished = 4
    Cancel   = 5

class StoppableThread(threading.Thread):
    def __init__(self,p1,p2):
        super(StoppableThread, self).__init__(target=p1, args=(self,p2,))
        self.cancel = False
    def stop(self):
        self.cancel = True

def clear_client(request):
    clear_client_object(
        p_client_id = request.session.session_key
    )
    return JsonResponse(
        {}
    )

def client_keep_alive(request):
    client_object = get_client_object(request.session.session_key)
    client_object['last_update'] = datetime.now()

    return JsonResponse(
        {}
    )

def long_polling(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    startup = json_object['p_startup']

    #get client attribute in global object or create if it doesn't exist
    client_object = get_client_object(request.session.session_key)

    if startup:
        try:
            client_object['polling_lock'].release()
        except Exception:
            None

    # Acquire client polling lock to read returning data
    client_object['polling_lock'].acquire()

    v_returning_data = []

    client_object['returning_data_lock'].acquire()

    while len(client_object['returning_data'])>0:
        v_returning_data.append(client_object['returning_data'].pop(0))

    client_object['returning_data_lock'].release()

    return JsonResponse(
        {
            'returning_rows': v_returning_data
        }
    )

def queue_response(p_client_object, p_data):

    p_client_object['returning_data_lock'].acquire()

    p_client_object['returning_data'].append(p_data)

    try:
        # Attempt to release client polling lock so that the polling thread can read data
        p_client_object['polling_lock'].release()
    except Exception as exc:
        None
    p_client_object['returning_data_lock'].release()


def create_request(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_code = json_object['v_code']
    v_context_code = json_object['v_context_code']
    v_data = json_object['v_data']

    client_object = get_client_object(request.session.session_key)

    # Release lock to avoid dangling ajax polling requests
    try:
        client_object['polling_lock'].release()
    except Exception:
        None

    #Cancel thread
    if v_code == requestType.CancelThread:
        try:
            thread_data = client_object['tab_list'][v_data]
            if thread_data:
                if thread_data['type'] == 'advancedobjectsearch':
                    def callback(self):
                        try:
                            self.tag['lock'].acquire()

                            for v_activeConnection in self.tag['activeConnections']:
                                v_activeConnection.Cancel(False)
                        finally:
                            self.tag['lock'].release()

                    thread_data['thread_pool'].stop(p_callback=callback)
                else:
                    thread_data['thread'].stop()
                    thread_data['omnidatabase'].v_connection.Cancel(False)
        except Exception as exc:
            print(str(exc))
            None

    #Close Tab
    elif v_code == requestType.CloseTab:
        for v_tab_close_data in v_data:
            close_tab_handler(client_object,v_tab_close_data['tab_id'])
            #remove from tabs table if db_tab_id is not null
            if v_tab_close_data['tab_db_id']:
                try:
                    tab = Tab.objects.get(id=v_tab_close_data['tab_db_id'])
                    tab.delete()
                except Exception as exc:
                    None

    else:

        #Check database prompt timeout
        if v_data['v_db_index'] is not None:
            v_timeout = v_session.DatabaseReachPasswordTimeout(v_data['v_db_index'])
            if v_timeout['timeout']:
                v_return['v_code'] = response.PasswordRequired
                v_return['v_context_code'] = v_context_code
                v_return['v_data'] = v_timeout['message']
                queue_response(client_object,v_return)
                return JsonResponse(
                    {}
                )

        if v_code == requestType.Terminal:
            #create tab object if it doesn't exist
            try:
                tab_object = client_object['tab_list'][v_data['v_tab_id']]
                if not tab_object['terminal_transport'].is_active():
                    raise
                try:
                    tab_object['last_update'] = datetime.now()
                    tab_object['terminal_object'].send(v_data['v_cmd'])
                except Exception:
                    None
            except Exception as exc:
                tab_object = create_tab_object(
                    request.session,
                    v_data['v_tab_id'],
                    {
                        'thread': None,
                        'terminal_object': None
                    }
                )

                start_thread = True

                try:
                    v_conn_object = v_session.v_databases[v_data['v_ssh_id']]

                    client = paramiko.SSHClient()
                    client.load_system_host_keys()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    #ssh key provided
                    if v_conn_object['tunnel']['key'].strip() != '':
                        v_file_name = '{0}'.format(str(time.time())).replace('.','_')
                        v_full_file_name = os.path.join(settings.TEMP_DIR, v_file_name)
                        with open(v_full_file_name,'w') as f:
                            f.write(v_conn_object['tunnel']['key'])
                        client.connect(hostname=v_conn_object['tunnel']['server'],username=v_conn_object['tunnel']['user'],key_filename=v_full_file_name,passphrase=v_conn_object['tunnel']['password'],port=int(v_conn_object['tunnel']['port']))
                    else:
                        client.connect(hostname=v_conn_object['tunnel']['server'],username=v_conn_object['tunnel']['user'],password=v_conn_object['tunnel']['password'],port=int(v_conn_object['tunnel']['port']))

                    transport = client.get_transport()
                    transport.set_keepalive(120)

                    tab_object['terminal_ssh_client'] = client
                    tab_object['terminal_transport'] = transport
                    tab_object['terminal_object'] = custom_paramiko_expect.SSHClientInteraction(client,timeout=60, display=False)
                    tab_object['terminal_object'].send(v_data['v_cmd'])

                    tab_object['terminal_type'] = 'remote'

                except Exception as exc:
                    start_thread = False
                    v_return['v_code'] = response.MessageException
                    v_return['v_context_code'] = v_context_code
                    v_return['v_data'] = str(exc)
                    queue_response(client_object,v_return)

                if start_thread:
                    v_data['v_context_code'] = v_context_code
                    v_data['v_tab_object'] = tab_object
                    v_data['v_client_object'] = client_object
                    v_data['v_session'] = v_session
                    t = StoppableThread(thread_terminal,v_data)
                    tab_object['thread'] = t
                    tab_object['type'] = 'terminal'
                    tab_object['tab_id'] = v_data['v_tab_id']
                    t.start()


        elif v_code == requestType.Query or v_code == requestType.QueryEditData or v_code == requestType.SaveEditData or v_code == requestType.AdvancedObjectSearch or v_code == requestType.Console:
            #create tab object if it doesn't exist
            try:
                tab_object = client_object['tab_list'][v_data['v_tab_id']]
            except Exception as exc:
                tab_object = create_tab_object(
                    request.session,
                    v_data['v_tab_id'],
                    {
                        'thread': None,
                        'omnidatabase': None,
                        'inserted_tab': False
                    }
                )

            try:
                get_database_tab_object(
                    v_session,
                    client_object,
                    tab_object,
                    v_data['v_conn_tab_id'],
                    v_data['v_db_index'],
                    True
                )

            except Exception as exc:
                v_return['v_code'] = response.PasswordRequired
                v_return['v_context_code'] = v_context_code
                v_return['v_data'] = str(exc)
                queue_response(client_object,v_return)
                return JsonResponse(
                    {}
                )

            v_data['v_context_code'] = v_context_code
            v_data['v_database'] = tab_object['omnidatabase']
            v_data['v_client_object'] = client_object
            v_data['v_session'] = v_session
            #Query request
            if v_code == requestType.Query:
                tab_object['tab_db_id'] = v_data['v_tab_db_id']
                v_data['v_tab_object'] = tab_object
                t = StoppableThread(thread_query,v_data)
                tab_object['thread'] = t
                tab_object['type'] = 'query'
                tab_object['sql_cmd'] = v_data['v_sql_cmd']
                tab_object['sql_save'] = v_data['v_sql_save']
                tab_object['tab_id'] = v_data['v_tab_id']
                #t.setDaemon(True)
                t.start()

            #Console request
            elif v_code == requestType.Console:
                v_data['v_tab_object'] = tab_object
                t = StoppableThread(thread_console,v_data)
                tab_object['thread'] = t
                tab_object['type'] = 'console'
                tab_object['sql_cmd'] = v_data['v_sql_cmd']
                tab_object['tab_id'] = v_data['v_tab_id']
                #t.setDaemon(True)
                t.start()

            #Query edit data
            elif v_code == requestType.QueryEditData:
                t = StoppableThread(thread_query_edit_data,v_data)
                tab_object['thread'] = t
                tab_object['type'] = 'edit'
                #t.setDaemon(True)
                t.start()

            #Save edit data
            elif v_code == requestType.SaveEditData:
                t = StoppableThread(thread_save_edit_data,v_data)
                tab_object['thread'] = t
                tab_object['type'] = 'edit'
                #t.setDaemon(True)
                t.start()

        #Debugger
        elif v_code == requestType.Debug:

            #create tab object if it doesn't exist
            try:
                tab_object = client_object['tab_list'][v_data['v_tab_id']]
            except Exception as exc:
                tab_object = create_tab_object(
                    request.session,
                    v_data['v_tab_id'],
                    {
                        'thread': None,
                        'omnidatabase_debug': None,
                        'omnidatabase_control': None,
                        'port': None,
                        'debug_pid': -1,
                        'cancelled': False,
                        'tab_id': v_data['v_tab_id'],
                        'type': 'debug'
                    }
                )

            #New debugger, create connections
            if v_data['v_state'] == debugState.Starting:
                try:
                    v_conn_tab_connection = v_session.v_databases[v_data['v_db_index']]['database']

                    v_database_debug = OmniDatabase.Generic.InstantiateDatabase(
                        v_conn_tab_connection.v_db_type,
                        v_conn_tab_connection.v_connection.v_host,
                        str(v_conn_tab_connection.v_connection.v_port),
                        v_conn_tab_connection.v_active_service,
                        v_conn_tab_connection.v_active_user,
                        v_conn_tab_connection.v_connection.v_password,
                        v_conn_tab_connection.v_conn_id,
                        v_conn_tab_connection.v_alias,
                        p_conn_string = v_conn_tab_connection.v_conn_string,
                        p_parse_conn_string = False
                    )
                    v_database_control = OmniDatabase.Generic.InstantiateDatabase(
                        v_conn_tab_connection.v_db_type,
                        v_conn_tab_connection.v_connection.v_host,
                        str(v_conn_tab_connection.v_connection.v_port),
                        v_conn_tab_connection.v_active_service,
                        v_conn_tab_connection.v_active_user,
                        v_conn_tab_connection.v_connection.v_password,
                        v_conn_tab_connection.v_conn_id,
                        v_conn_tab_connection.v_alias,
                        p_conn_string = v_conn_tab_connection.v_conn_string,
                        p_parse_conn_string = False
                    )
                    tab_object['omnidatabase_debug'] = v_database_debug
                    tab_object['cancelled'] = False
                    tab_object['omnidatabase_control'] = v_database_control
                    tab_object['port'] = v_database_debug.v_connection.ExecuteScalar('show port')
                except Exception as exc:
                    logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
                    v_response = {}
                    v_response['v_code'] = response.MessageException
                    v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
                    queue_response(client_object,v_response)

            v_data['v_context_code'] = v_context_code
            v_data['v_tab_object'] = tab_object
            v_data['v_client_object'] = client_object

            t = StoppableThread(thread_debug,v_data)
            tab_object['thread'] = t
            #t.setDaemon(True)
            t.start()

    return JsonResponse(
        {}
    )

def thread_debug(self,args):
    v_response = {
        'v_code': -1,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }
    v_state = args['v_state']
    v_tab_id = args['v_tab_id']
    v_tab_object = args['v_tab_object']
    v_client_object = args['v_client_object']
    v_database_debug = v_tab_object['omnidatabase_debug']
    v_database_control = v_tab_object['omnidatabase_control']

    try:

        if v_state == debugState.Starting:

            #Start debugger and return ready state
            v_database_debug.v_connection.Open()
            v_database_control.v_connection.Open()

            #Cleaning contexts table
            v_database_debug.v_connection.Execute('delete from omnidb.contexts t where t.pid not in (select pid from pg_stat_activity where pid = t.pid)')

            connections_details = v_database_debug.v_connection.Query('select pg_backend_pid()',True)
            pid = connections_details.Rows[0][0]

            v_database_debug.v_connection.Execute('insert into omnidb.contexts (pid, function, hook, lineno, stmttype, breakpoint, finished) values ({0}, null, null, null, null, 0, false)'.format(pid))

            #lock row for current pid
            v_database_control.v_connection.Execute('select pg_advisory_lock({0}) from omnidb.contexts where pid = {0}'.format(pid))

            #updating pid and port in tab object
            v_tab_object['debug_pid'] = pid

            #Run thread that will execute the function
            t = StoppableThread(thread_debug_run_func,{'v_tab_object': v_tab_object, 'v_context_code': args['v_context_code'], 'v_function': args['v_function'], 'v_type': args['v_type'], 'v_client_object': v_client_object})
            v_tab_object['thread'] = t
            #t.setDaemon(True)
            t.start()

            #ws_object.v_list_tab_objects[v_tab_id] = v_tab_object

            v_lineno = None
            #wait for context to be ready or thread ends
            while v_lineno is None and t.isAlive():
                time.sleep(0.5)
                v_lineno = v_database_control.v_connection.ExecuteScalar('select lineno from omnidb.contexts where pid = {0} and lineno is not null'.format(pid))

            # Function ended instantly
            if not t.isAlive():
                v_database_control.v_connection.Close()
            else:
                v_variables = v_database_control.v_connection.Query('select name,attribute,vartype,value from omnidb.variables where pid = {0}'.format(pid),True)

                v_response['v_code'] = response.DebugResponse
                v_response['v_data'] = {
                    'v_state': debugState.Ready,
                    'v_remove_context': False,
                    'v_variables': v_variables.Rows,
                    'v_lineno': v_lineno
                }
                queue_response(v_client_object,v_response)

        elif v_state == debugState.Step:

            v_database_control.v_connection.Execute('update omnidb.contexts set breakpoint = {0} where pid = {1}'.format(args['v_next_breakpoint'],v_tab_object['debug_pid']))

            try:
                v_database_control.v_connection.Execute('select pg_advisory_unlock({0}) from omnidb.contexts where pid = {0}; select pg_advisory_lock({0}) from omnidb.contexts where pid = {0};'.format(v_tab_object['debug_pid']))

                #acquired the lock, get variables and lineno
                v_variables = v_database_control.v_connection.Query('select name,attribute,vartype,value from omnidb.variables where pid = {0}'.format(v_tab_object['debug_pid']),True)
                v_context_data = v_database_control.v_connection.Query('select lineno,finished from omnidb.contexts where pid = {0}'.format(v_tab_object['debug_pid']),True)

                #not last statement
                if (v_context_data.Rows[0][1]!='True'):
                    v_response['v_code'] = response.DebugResponse
                    v_response['v_data'] = {
                        'v_state': debugState.Ready,
                        'v_remove_context': True,
                        'v_variables': v_variables.Rows,
                        'v_lineno': v_context_data.Rows[0][0]
                    }
                    queue_response(v_client_object,v_response)
                else:
                    v_database_control.v_connection.Execute('select pg_advisory_unlock({0}) from omnidb.contexts where pid = {0};'.format(v_tab_object['debug_pid']))
                    v_database_control.v_connection.Close()
                    v_response['v_code'] = response.RemoveContext
                    queue_response(v_client_object,v_response)

            except Exception:
                v_response['v_code'] = response.RemoveContext
                queue_response(v_client_object,v_response)

        #Cancelling debugger, the thread executing the function will return the cancel status
        elif v_state == debugState.Cancel:
            v_tab_object['cancelled'] = True
            v_database_control.v_connection.Cancel(False)
            v_database_control.v_connection.Terminate(v_tab_object['debug_pid'])
            v_database_control.v_connection.Close()

    except Exception as exc:
        v_response['v_code'] = response.DebugResponse
        v_response['v_data'] = {
            'v_state': debugState.Finished,
            'v_remove_context': True,
            'v_error': True,
            'v_error_msg': str(exc)
        }

        try:
            v_database_debug.v_connection.Close()
            v_database_control.v_connection.Close()
        except Exception:
            None

        queue_response(v_client_object,v_response)

def thread_debug_run_func(self,args):
    v_response = {
        'v_code': -1,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }
    v_tab_object = args['v_tab_object']
    v_client_object = args['v_client_object']
    v_database_debug = v_tab_object['omnidatabase_debug']
    v_database_control = v_tab_object['omnidatabase_control']

    try:
        #enable debugger for current connection
        v_conn_string = "host=''localhost'' port={0} dbname=''{1}'' user=''{2}''".format(v_tab_object['port'],v_database_debug.v_service,v_database_debug.v_user)

        v_database_debug.v_connection.Execute("select omnidb.omnidb_enable_debugger('{0}')".format(v_conn_string))

        #run function it will lock until the function ends
        if args['v_type'] == 'f':
            v_func_return = v_database_debug.v_connection.Query('select * from {0} limit 1000'.format(args['v_function']),True)
        else:
            v_func_return = v_database_debug.v_connection.Query('call {0}'.format(args['v_function']),True)

        #Not cancelled, return all data
        if not v_tab_object['cancelled']:

            #retrieve variables
            v_variables = v_database_debug.v_connection.Query('select name,attribute,vartype,value from omnidb.variables where pid = {0}'.format(v_tab_object['debug_pid']),True)

            #retrieve statistics
            v_statistics = v_database_debug.v_connection.Query('select lineno,coalesce(trunc((extract("epoch" from tend)  - extract("epoch" from tstart))::numeric,4),0) as msec from omnidb.statistics where pid = {0} order by step'.format(v_tab_object['debug_pid']),True)

            #retrieve statistics summary
            v_statistics_summary = v_database_debug.v_connection.Query('''
            select lineno, max(msec) as msec
            from (select lineno,coalesce(trunc((extract("epoch" from tend) - extract("epoch" from tstart))::numeric,4),0) as msec from omnidb.statistics where pid = {0}) t
            group by lineno
            order by lineno
            '''.format(v_tab_object['debug_pid']),True)

            #retrieve notices
            v_notices = v_database_debug.v_connection.GetNotices()
            v_notices_text = ''
            if len(v_notices) > 0:
                for v_notice in v_notices:
                    v_notices_text += v_notice.replace('\n','<br/>')

            v_response['v_data'] = {
                'v_state': debugState.Finished,
                'v_remove_context': True,
                'v_result_rows': v_func_return.Rows,
                'v_result_columns': v_func_return.Columns,
                'v_result_statistics': v_statistics.Rows,
                'v_result_statistics_summary': v_statistics_summary.Rows,
                'v_result_notices': v_notices_text,
                'v_result_notices_length': len(v_notices),
                'v_variables': v_variables.Rows,
                'v_error': False
            }

            v_database_debug.v_connection.Close()

            #send debugger finished message
            v_response['v_code'] = response.DebugResponse

            queue_response(v_client_object,v_response)
        #Cancelled, return cancelled status
        else:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            queue_response(v_client_object,v_response)

    except Exception as exc:
        #Not cancelled
        if not v_tab_object['cancelled']:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Finished,
                'v_remove_context': True,
                'v_error': True,
                'v_error_msg': str(exc)
            }
            try:
                v_database_debug.v_connection.Close()
            except Exception:
                None
            try:
                v_database_control.v_connection.Close()
            except Exception:
                None

            queue_response(v_client_object,v_response)
        else:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            queue_response(v_client_object,v_response)

def GetDuration(p_start, p_end):
    duration = ''
    time_diff = p_end - p_start
    if time_diff.days==0 and time_diff.seconds==0:
        duration = str(time_diff.microseconds/1000) + ' ms'
    else:
        days, seconds = time_diff.days, time_diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        duration = '{0}:{1}:{2}'.format("%02d" % (hours,),"%02d" % (minutes,),"%02d" % (seconds,))

    return duration

def LogHistory(p_user_id,
               p_user_name,
               p_sql,
               p_start,
               p_end,
               p_duration,
               p_status,
               p_conn_id):

    try:

        query_object = QueryHistory(
            user=User.objects.get(id=p_user_id),
            connection=Connection.objects.get(id=p_conn_id),
            start_time=make_aware(p_start),
            end_time=make_aware(p_end),
            duration=p_duration,
            status=p_status,
            snippet=p_sql
        )
        query_object.save()
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

def thread_terminal(self,args):

    try:
        v_cmd             = args['v_cmd']
        v_tab_id          = args['v_tab_id']
        v_tab_object      = args['v_tab_object']
        v_terminal_object = v_tab_object['terminal_object']
        v_terminal_ssh_client = v_tab_object['terminal_ssh_client']
        v_client_object  = args['v_client_object']

        while not self.cancel:
            try:
                if v_tab_object['terminal_type'] == 'local':
                    v_data_return = v_terminal_object.read_nonblocking(size=1024)
                else:
                    v_data_return = v_terminal_object.read_current()

                #send data in chunks to avoid blocking the websocket server
                chunks = [v_data_return[x:x+10000] for x in range(0, len(v_data_return), 10000)]

                if len(chunks)>0:
                    for count in range(0,len(chunks)):
                        if self.cancel:
                            break

                        v_response = {
                            'v_code': response.TerminalResult,
                            'v_context_code': args['v_context_code'],
                            'v_error': False,
                            'v_data': 1
                        }

                        if not count==len(chunks)-1:
                            v_response['v_data'] = {
                                'v_data' : chunks[count],
                                'v_last_block': False
                            }
                        else:
                            v_response['v_data'] = {
                                'v_data' : chunks[count],
                                'v_last_block': True
                            }
                        if not self.cancel:
                            queue_response(v_client_object,v_response)
                else:
                    if not self.cancel:
                        queue_response(v_client_object,v_response)

            except Exception as exc:
                transport = v_terminal_ssh_client.get_transport()
                if transport is None or transport.is_active() is False:
                    break
                if 'EOF' in str(exc):
                    break


    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_data'] = {
            'v_data': str(exc),
            'v_duration': ''
        }
        if not self.cancel:
            queue_response(v_client_object,v_response)

def thread_query(self,args):
    v_response = {
        'v_code': response.QueryResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    try:
        v_sql            = args['v_sql_cmd']
        v_cmd_type       = args['v_cmd_type']
        v_tab_id         = args['v_tab_id']
        v_tab_object     = args['v_tab_object']
        v_mode           = args['v_mode']
        v_all_data       = args['v_all_data']
        v_log_query      = args['v_log_query']
        v_tab_title      = args['v_tab_title']
        v_autocommit     = args['v_autocommit']
        v_client_object  = args['v_client_object']

        #Removing last character if it is a semi-colon
        if v_sql[-1:]==';':
            v_sql = v_sql[:-1]

        v_session = args['v_session']
        v_database = args['v_database']

        log_start_time = datetime.now()
        log_status = 'success'

        v_inserted_id = None
        try:
            #insert new tab record
            if not v_tab_object['tab_db_id'] and not v_tab_object['inserted_tab'] and v_log_query:
                try:
                    tab_object = Tab(
                        user=User.objects.get(id=v_session.v_user_id),
                        connection=Connection.objects.get(id=v_database.v_conn_id),
                        title=v_tab_title,
                        snippet=v_tab_object['sql_save']
                    )
                    tab_object.save()
                    v_inserted_id = tab_object.id
                    v_tab_object['inserted_tab'] = True
                    v_inserted_tab = True
                except Exception as exc:
                    None

            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)

            if v_cmd_type=='export_csv' or v_cmd_type=='export_xlsx':

                #cleaning temp folder
                clean_temp_folder()

                if v_cmd_type=='export_csv':
                    v_extension = 'csv'
                else:
                    v_extension = 'xlsx'

                v_export_dir = settings.TEMP_DIR
                if not os.path.exists(v_export_dir):
                    os.makedirs(v_export_dir)

                v_database.v_connection.Open()
                v_file_name = '{0}.{1}'.format(str(time.time()).replace('.','_'),v_extension)
                v_data1 = v_database.v_connection.QueryBlock(v_sql, 1000, False, True)
                #if platform.system() == 'Windows':
                #    f = Spartacus.Utils.DataFileWriter(os.path.join(v_export_dir, v_file_name), v_data1.Columns, 'windows-1252')
                #else:
                #    f = Spartacus.Utils.DataFileWriter(os.path.join(v_export_dir, v_file_name), v_data1.Columns)
                f = Spartacus.Utils.DataFileWriter(os.path.join(v_export_dir, v_file_name), v_data1.Columns,v_session.v_csv_encoding, v_session.v_csv_delimiter)
                f.Open()
                if v_database.v_connection.v_start:
                    f.Write(v_data1)
                    v_hasmorerecords = False
                elif len(v_data1.Rows) > 0:
                    f.Write(v_data1)
                    v_hasmorerecords = True
                else:
                    v_hasmorerecords = False
                while v_hasmorerecords:
                    v_data1 = v_database.v_connection.QueryBlock(v_sql, 1000, False, True)
                    if v_database.v_connection.v_start:
                        f.Write(v_data1)
                        v_hasmorerecords = False
                    elif len(v_data1.Rows) > 0:
                        f.Write(v_data1)
                        v_hasmorerecords = True
                    else:
                        v_hasmorerecords = False

                v_database.v_connection.Close()
                f.Flush()

                log_end_time = datetime.now()
                v_duration = GetDuration(log_start_time,log_end_time)

                v_response['v_data'] = {
                    'v_filename': settings.PATH + '/static/temp/{0}'.format(v_file_name),
                    'v_downloadname': 'omnidb_exported.{0}'.format(v_extension),
                    'v_duration': v_duration,
                    'v_inserted_id': v_inserted_id,
                    'v_con_status': v_database.v_connection.GetConStatus(),
                    'v_chunks': False
                }

                if not self.cancel:
                    queue_response(v_client_object,v_response)

            else:
                if v_mode==0:
                    v_database.v_connection.v_autocommit = v_autocommit
                    if not v_database.v_connection.v_con or v_database.v_connection.GetConStatus() == 0:
                        v_database.v_connection.Open()
                    else:
                        v_database.v_connection.v_start=True
                if (v_mode==0 or v_mode==1) and not v_all_data:
                    v_data1 = v_database.v_connection.QueryBlock(v_sql, 50, True, True)

                    v_notices = v_database.v_connection.GetNotices()
                    v_notices_text = ''
                    v_notices_length = len(v_notices)
                    if v_notices_length > 0:
                        for v_notice in v_notices:
                            v_notices_text += v_notice.replace('\n','<br/>')
                    v_database.v_connection.ClearNotices()

                    log_end_time = datetime.now()
                    v_duration = GetDuration(log_start_time,log_end_time)

                    v_response = {
                        'v_code': response.QueryResult,
                        'v_context_code': args['v_context_code'],
                        'v_error': False,
                        'v_data': 1
                    }

                    v_response['v_data'] = {
                        'v_col_names' : v_data1.Columns,
                        'v_data' : v_data1.Rows,
                        'v_last_block': True,
                        'v_duration': v_duration,
                        'v_notices': v_notices_text,
                        'v_notices_length': v_notices_length,
                        'v_inserted_id': v_inserted_id,
                        'v_status': v_database.v_connection.GetStatus(),
                        'v_con_status': v_database.v_connection.GetConStatus(),
                        'v_chunks': True
                    }

                    if not self.cancel:
                        queue_response(v_client_object,v_response)

                    #if len(v_data1.Rows) < 50 and v_autocommit:
                    #    try:
                    #        v_database.v_connection.Close()
                    #    except Exception:
                    #        pass

                elif v_mode==2 or v_all_data:

                    v_hasmorerecords = True
                    k = 0
                    while v_hasmorerecords:

                        k = k + 1

                        v_data1 = v_database.v_connection.QueryBlock(v_sql, 10000, True, True)
                        v_notices = v_database.v_connection.GetNotices()
                        v_notices_text = ''
                        v_notices_length = len(v_notices)
                        if v_notices_length > 0:
                            for v_notice in v_notices:
                                v_notices_text += v_notice.replace('\n','<br/>')
                        v_database.v_connection.ClearNotices()

                        log_end_time = datetime.now()
                        v_duration = GetDuration(log_start_time,log_end_time)

                        v_response = {
                            'v_code': response.QueryResult,
                            'v_context_code': args['v_context_code'],
                            'v_error': False,
                            'v_data': 1
                        }

                        v_response['v_data'] = {
                            'v_col_names' : v_data1.Columns,
                            'v_data' : v_data1.Rows,
                            'v_last_block': False,
                            #'v_query_info' : "Number of records: {0}".format(len(v_data1.Rows)),
                            'v_duration': v_duration,
                            'v_notices': v_notices_text,
                            'v_notices_length': v_notices_length,
                            'v_inserted_id': v_inserted_id,
                            'v_status': '',
                            'v_con_status': 0,
                            'v_chunks': True
                        }

                        if v_database.v_connection.v_start:
                            v_hasmorerecords = False
                        elif len(v_data1.Rows) > 0:
                            v_hasmorerecords = True
                        else:
                            v_hasmorerecords = False

                        if self.cancel:
                            break
                        elif v_hasmorerecords:
                            queue_response(v_client_object,v_response)

                    if not self.cancel:

                        v_notices = v_database.v_connection.GetNotices()
                        v_notices_text = ''
                        if len(v_notices) > 0:
                            for v_notice in v_notices:
                                v_notices_text += v_notice.replace('\n','<br/>')

                        log_end_time = datetime.now()
                        v_duration = GetDuration(log_start_time,log_end_time)

                        v_response = {
                            'v_code': response.QueryResult,
                            'v_context_code': args['v_context_code'],
                            'v_error': False,
                            'v_data': 1
                        }

                        v_response['v_data'] = {
                            'v_col_names' : v_data1.Columns,
                            'v_data' : v_data1.Rows,
                            'v_last_block': True,
                            #'v_query_info' : "Number of records: {0}".format(len(v_data1.Rows)),
                            'v_duration': v_duration,
                            'v_notices': v_notices_text,
                            'v_notices_length': len(v_notices),
                            'v_inserted_id': v_inserted_id,
                            'v_status': v_database.v_connection.GetStatus(),
                            'v_con_status': v_database.v_connection.GetConStatus(),
                            'v_chunks': True
                        }
                        queue_response(v_client_object,v_response)

                elif v_mode==3 or v_mode==4:
                    v_duration = GetDuration(log_start_time,log_end_time)
                    #commit
                    if v_mode==3:
                        v_database.v_connection.Query('COMMIT;',True)
                    else:
                        v_database.v_connection.Query('ROLLBACK;',True)

                    v_response = {
                        'v_code': response.QueryResult,
                        'v_context_code': args['v_context_code'],
                        'v_error': False,
                        'v_data': 1
                    }

                    v_response['v_data'] = {
                        'v_col_names' : None,
                        'v_data' : [],
                        'v_last_block': True,
                        #'v_query_info' : "",
                        'v_duration': v_duration,
                        'v_notices': "",
                        'v_notices_length': 0,
                        'v_inserted_id': v_inserted_id,
                        'v_status': v_database.v_connection.GetStatus(),
                        'v_con_status': v_database.v_connection.GetConStatus(),
                        'v_chunks': False
                    }
                    queue_response(v_client_object,v_response)
        except Exception as exc:
            if not self.cancel:
                try:
                    v_notices = v_database.v_connection.GetNotices()
                    v_notices_text = ''
                    if len(v_notices) > 0:
                        for v_notice in v_notices:
                            v_notices_text += v_notice.replace('\n','<br/>')
                except Exception:
                    v_notices = []
                    v_notices_text = ''

                log_end_time = datetime.now()
                v_duration = GetDuration(log_start_time,log_end_time)
                log_status = 'error'
                v_response = {
                    'v_code': response.QueryResult,
                    'v_context_code': args['v_context_code'],
                    'v_error': False,
                    'v_data': 1
                }
                v_response['v_data'] = {
                    'position': v_database.GetErrorPosition(str(exc)),
                    'message' : str(exc).replace('\n','<br>'),
                    'v_duration': v_duration,
                    'v_notices': v_notices_text,
                    'v_notices_length': len(v_notices),
                    'v_inserted_id': v_inserted_id,
                    'v_status': 0,
                    'v_con_status': v_database.v_connection.GetConStatus(),
                    'v_chunks': False
                }
                v_response['v_error'] = True

                queue_response(v_client_object,v_response)

        #Log to history
        if v_mode==0 and v_log_query:
            LogHistory(
                v_session.v_user_id,
                v_session.v_user_name,
                v_sql,
                log_start_time,
                log_end_time,
                v_duration,
                log_status,
                v_database.v_conn_id
            )

        #if mode=0 save tab
        if v_mode==0 and v_tab_object['tab_db_id'] and v_log_query:
            try:
                tab = Tab.objects.get(id=v_tab_object['tab_db_id'])
                tab.snippet=v_tab_object['sql_save']
                tab.title=v_tab_title
                tab.save()
            except Exception as exc:
                None
    except Exception as exc:
        raise
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            queue_response(v_client_object,v_response)

def thread_console(self,args):
    v_response = {
        'v_code': response.ConsoleResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    try:
        v_sql            = args['v_sql_cmd']
        v_tab_id         = args['v_tab_id']
        v_tab_object     = args['v_tab_object']
        v_autocommit     = args['v_autocommit']
        v_mode           = args['v_mode']
        v_client_object  = args['v_client_object']

        v_session = args['v_session']
        v_database = args['v_database']

        #Removing last character if it is a semi-colon
        if v_sql[-1:]==';':
            v_sql = v_sql[:-1]

        log_start_time = datetime.now()
        log_status = 'success'

        try:
            list_sql = sqlparse.split(v_sql)

            v_data_return = ''
            run_command_list = True

            if v_mode==0:
                v_database.v_connection.v_autocommit = v_autocommit
                if not v_database.v_connection.v_con or v_database.v_connection.GetConStatus() == 0:
                    v_database.v_connection.Open()
                else:
                    v_database.v_connection.v_start=True

            if v_mode == 1 or v_mode ==2:
                v_table = v_database.v_connection.QueryBlock('', 50, True, True)
                #need to stop again
                if not v_database.v_connection.v_start or len(v_table.Rows)>=50:
                    v_data_return += '\n' + v_table.Pretty(v_database.v_connection.v_expanded) + '\n' + v_database.v_connection.GetStatus()
                    run_command_list = False
                    v_show_fetch_button = True
                else:
                    v_data_return += '\n' + v_table.Pretty(v_database.v_connection.v_expanded) + '\n' + v_database.v_connection.GetStatus()
                    run_command_list = True
                    list_sql = v_tab_object['remaining_commands']

            if v_mode == 3:
                run_command_list = True
                list_sql = v_tab_object['remaining_commands']

            if run_command_list:
                counter = 0
                v_show_fetch_button = False
                for sql in list_sql:
                    counter = counter + 1
                    try:
                        formated_sql = sql.strip()
                        v_data_return += '\n' + v_database.v_active_service + '=# ' + formated_sql + '\n'

                        v_database.v_connection.ClearNotices()
                        v_database.v_connection.v_start=True
                        v_data1 = v_database.v_connection.Special(sql)

                        v_notices = v_database.v_connection.GetNotices()
                        v_notices_text = ''
                        if len(v_notices) > 0:
                            for v_notice in v_notices:
                                v_notices_text += v_notice
                            v_data_return += v_notices_text

                        v_data_return += v_data1

                        if v_database.v_use_server_cursor:
                            if v_database.v_connection.v_last_fetched_size == 50:
                                v_tab_object['remaining_commands'] = list_sql[counter:]
                                v_show_fetch_button = True
                                break
                    except Exception as exc:
                        try:
                            v_notices = v_database.v_connection.GetNotices()
                            v_notices_text = ''
                            if len(v_notices) > 0:
                                for v_notice in v_notices:
                                    v_notices_text += v_notice
                                v_data_return += v_notices_text
                        except Exception as exc:
                            None
                        v_data_return += str(exc)
                    v_tab_object['remaining_commands'] = []

            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)

            v_data_return = v_data_return.replace("\n","\r\n")

            v_response = {
                'v_code': response.ConsoleResult,
                'v_context_code': args['v_context_code'],
                'v_error': False,
                'v_data': 1
            }
            v_response['v_data'] = {
                'v_data' : v_data_return,
                'v_last_block': True,
                'v_duration': v_duration
            }

            #send data in chunks to avoid blocking the websocket server
            chunks = [v_data_return[x:x+10000] for x in range(0, len(v_data_return), 10000)]
            if len(chunks)>0:
                for count in range(0,len(chunks)):
                    if self.cancel:
                        break
                    if not count==len(chunks)-1:
                        v_response = {
                            'v_code': response.ConsoleResult,
                            'v_context_code': args['v_context_code'],
                            'v_error': False,
                            'v_data': 1
                        }
                        v_response['v_data'] = {
                            'v_data' : chunks[count],
                            'v_last_block': False,
                            'v_duration': v_duration,
                            'v_show_fetch_button': v_show_fetch_button,
                            'v_con_status': '',
                        }
                    else:
                        v_response = {
                            'v_code': response.ConsoleResult,
                            'v_context_code': args['v_context_code'],
                            'v_error': False,
                            'v_data': 1
                        }
                        v_response['v_data'] = {
                            'v_data' : chunks[count],
                            'v_last_block': True,
                            'v_duration': v_duration,
                            'v_show_fetch_button': v_show_fetch_button,
                            'v_con_status': v_database.v_connection.GetConStatus(),
                        }
                    if not self.cancel:
                        queue_response(v_client_object,v_response)
            else:
                if not self.cancel:
                    queue_response(v_client_object,v_response)

            try:
                v_database.v_connection.ClearNotices()
            except Exception:
                None
        except Exception as exc:
            #try:
            #    v_database.v_connection.Close()
            #except Exception:
            #    pass
            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)
            log_status = 'error'
            v_response['v_data'] = {
                'v_data': str(exc),
                'v_duration': v_duration
            }

            if not self.cancel:
                queue_response(v_client_object,v_response)

        if v_mode == 0:
            #logging to console history
            query_object = ConsoleHistory(
                user=User.objects.get(id=v_session.v_user_id),
                connection=Connection.objects.get(id=v_database.v_conn_id),
                start_time=make_aware(datetime.now()),
                snippet=v_sql.replace("'","''")
            )

            query_object.save()


    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_data'] = {
            'v_data': str(exc),
            'v_duration': ''
        }
        if not self.cancel:
            queue_response(v_client_object,v_response)

def thread_query_edit_data(self,args):
    v_response = {
        'v_code': response.QueryEditDataResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': {
            'v_data' : [],
            'v_row_pk' : [],
            'v_query_info' : ''
        }
    }

    try:
        v_session = args['v_session']
        v_database = args['v_database']

        v_table = args['v_table']

        if v_database.v_has_schema:
            v_schema = args['v_schema']

        v_filter         = args['v_filter']
        v_count          = args['v_count']
        v_pk_list        = args['v_pk_list']
        v_columns        = args['v_columns']
        v_tab_id         = args['v_tab_id']
        v_client_object  = args['v_client_object']

        try:
            if v_database.v_has_schema:
                v_table_name = v_schema + '.' + v_table
            else:
                v_table_name = v_table

            v_column_list = ''
            v_first = True
            for v_column in v_columns:
                if not v_first:
                    v_column_list = v_column_list + ','
                v_first = False
                v_column_list = v_column_list + v_column['v_column']

            v_data1 = v_database.QueryTableRecords(v_column_list, v_table_name, v_filter, v_count)

            v_response['v_data']['v_query_info'] = str(len(v_data1.Rows))

            for v_row in v_data1.Rows:
                v_row_data = []

                v_row_pk = []
                for j in range(0, len(v_pk_list)):
                    v_pk_col = {}
                    v_pk_col['v_column'] = v_pk_list[j]['v_column']
                    v_pk_col['v_type'] = v_pk_list[j]['v_type']
                    v_pk_col['v_value'] = v_row[v_pk_list[j]['v_column'].replace('"','')]
                    v_row_pk.append(v_pk_col)
                v_response['v_data']['v_row_pk'].append(v_row_pk)

                v_row_data.append('')
                for v_col in v_data1.Columns:
                    if v_row[v_col] is None:
                        v_row_data.append('[null]')
                    else:
                        v_row_data.append(str(v_row[v_col]))
                v_response['v_data']['v_data'].append(v_row_data)

        except Exception as exc:
            v_response['v_data'] = str(exc)
            v_response['v_error'] = True

        if not self.cancel:
            queue_response(v_client_object,v_response)
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            queue_response(v_client_object,v_response)

def thread_save_edit_data(self,args):
    v_response = {
        'v_code': response.SaveEditDataResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': []
    }

    try:
        v_session = args['v_session']
        v_database = args['v_database']

        v_table = args['v_table']

        if v_database.v_has_schema:
            v_schema = args['v_schema']

        v_data_rows      = args['v_data_rows']
        v_rows_info      = args['v_rows_info']
        v_pk_info        = args['v_pk_info']
        v_columns        = args['v_columns']
        v_client_object  = args['v_client_object']

        if v_database.v_has_schema:
            v_table_name = v_schema + '.' + v_table
        else:
            v_table_name = v_table

        i = 0
        for v_row_info in v_rows_info:

            if (self.cancel):
                return

            v_command = ''

            # Deleting row
            if v_row_info['mode'] == -1:

                v_command = 'delete from ' + v_table_name + ' where '
                v_first = True
                v_pk_index = 0

                for v_pk in v_row_info['pk']:
                    if not v_first:
                        v_command = v_command + ' and '
                    v_first = False

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_pk['v_type']]
                    # Type not found
                    except Exception:
                        v_type_details = {
                            'quoted': True
                        }

                    if v_type_details['quoted']:
                        v_command = "{0} {1} = '{2}'".format(v_command,v_pk['v_column'],v_pk['v_value'])
                    else:
                        v_command = "{0} {1} = {2}".format(v_command,v_pk['v_column'],v_pk['v_value'])

                v_row_info_return = {}
                v_row_info_return['mode'] = -1
                v_row_info_return['index'] = v_row_info['index']
                v_row_info_return['command'] = v_command

                try:
                    v_database.v_connection.Execute(v_command)
                    v_row_info_return['error'] = False
                    v_row_info_return['v_message'] = 'Success.'
                except Exception as exc:
                    v_row_info_return['error'] = True
                    v_row_info_return['v_message'] = str(exc)

                v_response['v_data'].append(v_row_info_return)

            # Inserting new row
            elif v_row_info['mode'] == 2:

                v_command = 'insert into ' + v_table_name + ' ( '
                v_first = True

                for v_col in v_columns:
                    if not v_first:
                        v_command = v_command + ', '
                    v_first = False
                    v_command = v_command + v_col['v_column']

                v_command = v_command + ' ) values ( '
                v_first = True

                for j in range(1, len(v_data_rows[i])):
                    if not v_first:
                        v_command = v_command + ', '
                    v_first = False

                    v_value = ''
                    if v_data_rows[i][j] is not None:
                        v_value = v_data_rows[i][j]

                    v_value = v_value.replace("'","''")

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_columns[j-1]['v_type']]
                    # Type not found
                    except Exception:
                        v_type_details = {
                            'quoted': True
                        }

                    if v_value == '[null]':
                        v_command = v_command + 'null'
                    elif v_type_details['quoted']:
                        v_command = "{0} '{1}'".format(v_command,v_value)
                    else:
                        v_command = "{0} {1}".format(v_command,v_value)

                v_command = v_command + ' )'

                v_row_info_return = {}
                v_row_info_return['mode'] = 2
                v_row_info_return['index'] = v_row_info['index']
                v_row_info_return['command'] = v_command

                try:
                    v_database.v_connection.Execute(v_command)
                    v_row_info_return['error'] = False
                    v_row_info_return['v_message'] = 'Success.'
                except Exception as exc:
                    v_row_info_return['error'] = True
                    v_row_info_return['v_message'] = str(exc)

                v_response['v_data'].append(v_row_info_return)

            # Updating existing row
            elif v_row_info['mode'] == 1:

                v_command = 'update ' + v_table_name + ' set '
                v_first = True

                for v_col_index in v_rows_info[i]['changed_cols']:
                    if not v_first:
                        v_command = v_command + ', '
                    v_first = False

                    v_value = ''
                    if v_data_rows[i][v_col_index+1] is not None:
                        v_value = v_data_rows[i][v_col_index+1]

                    v_value = v_value.replace("'","''")

                    v_command = v_command + v_columns[v_col_index]['v_column'] + ' = '

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_columns[v_col_index]['v_type']]
                    # Type not found
                    except Exception:
                        v_type_details = {
                            'quoted': True
                        }

                    if v_value == '[null]':
                        v_command = v_command + 'null'
                    elif v_type_details['quoted']:
                        v_command = "{0} '{1}'".format(v_command,v_value)
                    else:
                        v_command = "{0} {1}".format(v_command,v_value)

                v_command = v_command + ' where '
                v_first = True
                v_pk_index = 0

                for v_pk in v_row_info['pk']:
                    if not v_first:
                        v_command = v_command + ' and '
                    v_first = False

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_pk['v_type']]
                    # Type not found
                    except Exception:
                        v_type_details = {
                            'quoted': True
                        }

                    if v_type_details['quoted']:
                        v_command = "{0} {1} = '{2}'".format(v_command,v_pk['v_column'],v_pk['v_value'])
                    else:
                        v_command = "{0} {1} = {2}".format(v_command,v_pk['v_column'],v_pk['v_value'])

                v_row_info_return = {}
                v_row_info_return['mode'] = 1
                v_row_info_return['index'] = v_row_info['index']
                v_row_info_return['command'] = v_command

                try:
                    v_database.v_connection.Execute(v_command)
                    v_row_info_return['error'] = False
                    v_row_info_return['v_message'] = 'Success.'
                except Exception as exc:
                    v_row_info_return['error'] = True
                    v_row_info_return['v_message'] = str(exc)

                v_response['v_data'].append(v_row_info_return)

            i = i + 1

        if not self.cancel:
            queue_response(v_client_object,v_response)
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            queue_response(v_client_object,v_response)
