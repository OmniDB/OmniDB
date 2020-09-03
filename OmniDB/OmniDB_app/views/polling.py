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

from enum import IntEnum
from datetime import datetime
from django.utils.timezone import make_aware
import sys

import sqlparse

import pexpect
sys.path.append('OmniDB_app/include')
from OmniDB_app.include import paramiko
from OmniDB_app.include import custom_paramiko_expect

from django.contrib.auth.models import User
from OmniDB_app.models.main import *

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

def closeTabHandler(p_client_object,p_tab_object_id):
    try:
        tab_object = p_client_object['tab_list'][p_tab_object_id]
        del p_client_object['tab_list'][p_tab_object_id]
        if tab_object['type'] == 'query':
            try:
                tab_object['omnidatabase'].v_connection.Cancel(False)
            except Exception:
                None
            try:
                tab_object['omnidatabase'].v_connection.Close()
            except Exception as exc:
                None
        elif tab_object['type'] == 'debug':
            tab_object['cancelled'] = True
            try:
                tab_object['omnidatabase_control'].v_connection.Cancel(False)
            except Exception:
                None
            try:
                tab_object['omnidatabase_control'].v_connection.Terminate(tab_object['debug_pid'])
            except Exception:
                None
            try:
                tab_object['omnidatabase_control'].v_connection.Close()
            except Exception:
                None
            try:
                tab_object['omnidatabase_debug'].v_connection.Close()
            except Exception:
                None
        elif tab_object['type'] == 'terminal':
            if tab_object['thread']!=None:
                tab_object['thread'].stop()
            if tab_object['terminal_type'] == 'local':
                tab_object['terminal_object'].terminate()
            else:
                tab_object['terminal_object'].close()
                tab_object['terminal_ssh_client'].close()

    except Exception as exc:
        None

global_object = {}
global_lock = threading.Lock()

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
    v_client_id = json_object['p_client_id']

    #get client attribute in global object or create if it doesn't exist
    try:
        global_lock.acquire()
        client_object = global_object[v_client_id]
    except Exception as exc:
        client_object = {
            'id': v_client_id,
            'polling_lock': threading.Lock(),
            'returning_data': [],
            'tab_list': {}
        }
        global_object[v_client_id] = client_object
    global_lock.release()

    # Acquire client polling lock to read returning data
    client_object['polling_lock'].acquire()

    v_returning_data = []
    global_lock.acquire()
    while len(client_object['returning_data'])>0:
        v_returning_data.append(client_object['returning_data'].pop(0))

    global_lock.release()

    return JsonResponse(
    {
        'returning_rows': v_returning_data
    }
    )

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
    v_client_id = json_object['v_client_id']
    v_code = json_object['v_code']
    v_context_code = json_object['v_context_code']
    v_data = json_object['v_data']

    #get client attribute in global object or create if it doesn't exist
    try:
        global_lock.acquire()
        client_object = global_object[v_client_id]
    except Exception as exc:
        None
    global_lock.release()

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
            None;

    #Close Tab
    elif v_code == requestType.CloseTab:
        for v_tab_close_data in v_data:
            closeTabHandler(client_object,v_tab_close_data['tab_id'])
            #remove from tabs table if db_tab_id is not null
            if v_tab_close_data['tab_db_id']:
                try:
                    tab = Tab.objects.get(id=v_tab_close_data['tab_db_id'])
                    tab.delete()
                except Exception as exc:
                    None

    elif v_code == requestType.Terminal:
        #create tab object if it doesn't exist
        try:
            tab_object = client_object['tab_list'][v_data['v_tab_id']]
            try:
                tab_object['terminal_object'].send(v_data['v_cmd'])
            except:
                None
        except Exception as exc:
            tab_object =  {
                            'thread': None,
                            'terminal_object': None
                          }
            client_object['tab_list'][v_data['v_tab_id']] = tab_object

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
                tab_object['terminal_ssh_client'] = client
                tab_object['terminal_object'] = custom_paramiko_expect.SSHClientInteraction(client,timeout=60, display=False)
                tab_object['terminal_object'].send(v_data['v_cmd'])

                tab_object['terminal_type'] = 'remote'

            except Exception as exc:
                start_thread = False
                print(str(exc))
                logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
                v_response['v_code'] = response.MessageException
                v_response['v_data'] = str(exc)
                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
            tab_object =  { 'thread': None,
                         'omnidatabase': None,
                         'database_index': -1,
                         'inserted_tab': False }
            client_object['tab_list'][v_data['v_tab_id']] = tab_object
        try:
            v_conn_tab_connection = v_session.v_tab_connections[v_data['v_conn_tab_id']]
            #create database object
            if (tab_object['database_index']!=v_data['v_db_index'] or
            v_conn_tab_connection.v_db_type!=tab_object['omnidatabase'].v_db_type or
            v_conn_tab_connection.v_connection.v_host!=tab_object['omnidatabase'].v_connection.v_host or
            str(v_conn_tab_connection.v_connection.v_port)!=str(tab_object['omnidatabase'].v_connection.v_port) or
            v_conn_tab_connection.v_active_service!=tab_object['omnidatabase'].v_active_service or
            v_conn_tab_connection.v_user!=tab_object['omnidatabase'].v_user or
            v_conn_tab_connection.v_connection.v_password!=tab_object['omnidatabase'].v_connection.v_password):
                v_database_new = OmniDatabase.Generic.InstantiateDatabase(
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

                tab_object['omnidatabase'] = v_database_new
                tab_object['database_index'] = v_data['v_db_index']

        except Exception as exc:
            raise

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


    #global_lock.acquire()
    #client_object['returning_data'].append('test1')
    #client_object['returning_data'].append('test2')
    #try:
        # Attempt to release client polling lock so that the polling thread can read data
    #    client_object['polling_lock'].release()
    #except Exception:
    #    None
    #global_lock.release()
    return JsonResponse(
    {}
    )

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
                            global_lock.acquire()
                            v_client_object['returning_data'].append(v_response)
                            try:
                                # Attempt to release client polling lock so that the polling thread can read data
                                v_client_object['polling_lock'].release()
                            except Exception:
                                None
                            global_lock.release()
                else:
                    if not self.cancel:
                        global_lock.acquire()
                        v_client_object['returning_data'].append(v_response)
                        try:
                            # Attempt to release client polling lock so that the polling thread can read data
                            v_client_object['polling_lock'].release()
                        except Exception:
                            None
                        global_lock.release()

            except Exception as exc:
                transport = v_terminal_ssh_client.get_transport()
                if transport == None or transport.is_active() == False:
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
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()

def thread_query(self,args):
    v_response = {
        'v_code': response.QueryResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    try:
        v_database_index = args['v_db_index']
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
                        connection=Connection.objects.get(id=v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id),
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
                    global_lock.acquire()
                    v_client_object['returning_data'].append(v_response)
                    try:
                        # Attempt to release client polling lock so that the polling thread can read data
                        v_client_object['polling_lock'].release()
                    except Exception:
                        None
                    global_lock.release()

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
                        global_lock.acquire()
                        v_client_object['returning_data'].append(v_response)
                        try:
                            # Attempt to release client polling lock so that the polling thread can read data
                            v_client_object['polling_lock'].release()
                        except Exception:
                            None
                        global_lock.release()

                    #if len(v_data1.Rows) < 50 and v_autocommit:
                    #    try:
                    #        v_database.v_connection.Close()
                    #    except:
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
                            global_lock.acquire()
                            v_client_object['returning_data'].append(v_response)
                            try:
                                # Attempt to release client polling lock so that the polling thread can read data
                                v_client_object['polling_lock'].release()
                            except Exception:
                                None
                            global_lock.release()

                    if not self.cancel:

                        v_notices = v_database.v_connection.GetNotices()
                        v_notices_text = ''
                        if len(v_notices) > 0:
                            for v_notice in v_notices:
                                v_notices_text += v_notice.replace('\n','<br/>')

                        log_end_time = datetime.now()
                        v_duration = GetDuration(log_start_time,log_end_time)

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

                        global_lock.acquire()
                        v_client_object['returning_data'].append(v_response)
                        try:
                            # Attempt to release client polling lock so that the polling thread can read data
                            v_client_object['polling_lock'].release()
                        except Exception:
                            None
                        global_lock.release()

                elif v_mode==3 or v_mode==4:
                    v_duration = GetDuration(log_start_time,log_end_time)
                    #commit
                    if v_mode==3:
                        v_database.v_connection.Query('COMMIT;',True)
                    else:
                        v_database.v_connection.Query('ROLLBACK;',True)
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
                    global_lock.acquire()
                    v_client_object['returning_data'].append(v_response)
                    try:
                        # Attempt to release client polling lock so that the polling thread can read data
                        v_client_object['polling_lock'].release()
                    except Exception:
                        None
                    global_lock.release()
        except Exception as exc:
            if not self.cancel:
                try:
                    v_notices = v_database.v_connection.GetNotices()
                    v_notices_text = ''
                    if len(v_notices) > 0:
                        for v_notice in v_notices:
                            v_notices_text += v_notice.replace('\n','<br/>')
                except:
                    v_notices = []
                    v_notices_text = ''
                #try:
                #    v_database.v_connection.Close()
                #except:
                #    pass
                log_end_time = datetime.now()
                v_duration = GetDuration(log_start_time,log_end_time)
                log_status = 'error'
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

                global_lock.acquire()
                v_client_object['returning_data'].append(v_response)
                try:
                    # Attempt to release client polling lock so that the polling thread can read data
                    v_client_object['polling_lock'].release()
                except Exception:
                    None
                global_lock.release()

        #Log to history
        if v_mode==0 and v_log_query:
            LogHistory(v_session.v_user_id,
                    v_session.v_user_name,
                    v_sql,
                    log_start_time,
                    log_end_time,
                    v_duration,
                    log_status,
                    v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id)

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
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()

def thread_console(self,args):
    v_response = {
        'v_code': response.ConsoleResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    try:
        v_database_index = args['v_db_index']
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
                        v_data_return += '\n>> ' + formated_sql + '\n'

                        v_database.v_connection.ClearNotices()
                        v_database.v_connection.v_start=True
                        v_data1 = v_database.v_connection.Special(sql);

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
                        v_response['v_data'] = {
                            'v_data' : chunks[count],
                            'v_last_block': False,
                            'v_duration': v_duration,
                            'v_show_fetch_button': v_show_fetch_button,
                            'v_con_status': '',
                        }
                    else:
                        v_response['v_data'] = {
                            'v_data' : chunks[count],
                            'v_last_block': True,
                            'v_duration': v_duration,
                            'v_show_fetch_button': v_show_fetch_button,
                            'v_con_status': v_database.v_connection.GetConStatus(),
                        }
                    if not self.cancel:
                        global_lock.acquire()
                        v_client_object['returning_data'].append(v_response)
                        try:
                            # Attempt to release client polling lock so that the polling thread can read data
                            v_client_object['polling_lock'].release()
                        except Exception:
                            None
                        global_lock.release()
            else:
                if not self.cancel:
                    global_lock.acquire()
                    v_client_object['returning_data'].append(v_response)
                    try:
                        # Attempt to release client polling lock so that the polling thread can read data
                        v_client_object['polling_lock'].release()
                    except Exception:
                        None
                    global_lock.release()

            try:
                v_database.v_connection.ClearNotices()
            except Exception:
                None
        except Exception as exc:
            #try:
            #    v_database.v_connection.Close()
            #except:
            #    pass
            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)
            log_status = 'error'
            v_response['v_data'] = {
                'v_data': str(exc),
                'v_duration': v_duration
            }

            if not self.cancel:
                global_lock.acquire()
                v_client_object['returning_data'].append(v_response)
                try:
                    # Attempt to release client polling lock so that the polling thread can read data
                    v_client_object['polling_lock'].release()
                except Exception:
                    None
                global_lock.release()

        if v_mode == 0:
            #logging to console history
            query_object = ConsoleHistory(
                user=User.objects.get(id=v_session.v_user_id),
                connection=Connection.objects.get(id=v_database.v_conn_id),
                snippet=v_sql.replace("'","''")
            )
            query_object.save()

            #keep 100 rows in console history table for current user/connection
            #v_omnidb_database.v_connection.Execute('''
            #    delete
            #    from console_history
            #    where command_date not in (
            #        select command_date
            #        from console_history
            #        where user_id = {0}
            #          and conn_id = {1}
            #        order by command_date desc
            #        limit 100
            #    )
            #    and user_id = {0}
            #    and conn_id = {1}
            #'''.format(v_session.v_user_id,
            #           v_database.v_conn_id,
            #           v_sql.replace("'","''")))

    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_data'] = {
            'v_data': str(exc),
            'v_duration': ''
        }
        if not self.cancel:
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()

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
        v_database_index = args['v_db_index']
        v_table          = args['v_table']
        v_schema         = args['v_schema']
        v_filter         = args['v_filter']
        v_count          = args['v_count']
        v_pk_list        = args['v_pk_list']
        v_columns        = args['v_columns']
        v_tab_id         = args['v_tab_id']
        v_client_object  = args['v_client_object']

        v_session = args['v_session']
        v_database = args['v_database']

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
                    if v_row[v_col] == None:
                        v_row_data.append('[null]')
                    else:
                        v_row_data.append(str(v_row[v_col]))
                v_response['v_data']['v_data'].append(v_row_data)

        except Exception as exc:
            v_response['v_data'] = str(exc)
            v_response['v_error'] = True

        if not self.cancel:
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()

def thread_save_edit_data(self,args):
    v_response = {
        'v_code': response.SaveEditDataResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': []
    }

    try:
        v_database_index = args['v_db_index']
        v_table          = args['v_table']
        v_schema         = args['v_schema']
        v_data_rows      = args['v_data_rows']
        v_rows_info      = args['v_rows_info']
        v_pk_info        = args['v_pk_info']
        v_columns        = args['v_columns']
        v_client_object  = args['v_client_object']

        v_session = args['v_session']
        v_database = args['v_database']

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
                    except:
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
                    if v_data_rows[i][j] != None:
                        v_value = v_data_rows[i][j]

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_columns[j-1]['v_type']]
                    # Type not found
                    except:
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
                    if v_data_rows[i][v_col_index+1] != None:
                        v_value = v_data_rows[i][v_col_index+1]

                    v_command = v_command + v_columns[v_col_index]['v_column'] + ' = '

                    # Getting details about the data type
                    try:
                        v_type_details = v_database.v_data_types[v_columns[v_col_index]['v_type']]
                    # Type not found
                    except:
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
                    except:
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
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            global_lock.acquire()
            v_client_object['returning_data'].append(v_response)
            try:
                # Attempt to release client polling lock so that the polling thread can read data
                v_client_object['polling_lock'].release()
            except Exception:
                None
            global_lock.release()
