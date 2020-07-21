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
        print(client_object)
    except Exception as exc:
        print("doesn't exist, creating")
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

    print('ACQUIRED')

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


    if v_code == requestType.Query or v_code == requestType.QueryEditData or v_code == requestType.SaveEditData or v_code == requestType.AdvancedObjectSearch or v_code == requestType.Console:

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
        #Query request
        if v_code == requestType.Query:
            tab_object['tab_db_id'] = v_data['v_tab_db_id']
            v_data['v_tab_object'] = tab_object
            v_data['v_session'] = v_session
            t = StoppableThread(thread_query,v_data)
            tab_object['thread'] = t
            tab_object['type'] = 'query'
            tab_object['sql_cmd'] = v_data['v_sql_cmd']
            tab_object['sql_save'] = v_data['v_sql_save']
            tab_object['tab_id'] = v_data['v_tab_id']
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
            snippet=p_sql.replace("'","''")
        )
        query_object.save()
    except Exception as exc:
        print(str(exc))
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

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
                        title=v_tab_title.replace("'","''"),
                        snippet=v_tab_object['sql_save'].replace("'","''")
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
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                tab.snippet=v_tab_object['sql_save'].replace("'","''")
                tab.title=v_tab_title.replace("'","''")
                tab.save()
            except Exception as exc:
                None
    except Exception as exc:
        raise
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
