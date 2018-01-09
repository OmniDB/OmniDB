import threading, time, datetime, json
import traceback

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.httpserver
from tornado import gen
import ssl,os

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

from enum import IntEnum
from datetime import datetime
import sys

from . import settings

from django.contrib.sessions.backends.db import SessionStore

import logging
logger = logging.getLogger('OmniDB_app.QueryServer')

class StoppableThread(threading.Thread):
    def __init__(self,p1,p2,p3):
        super(StoppableThread, self).__init__(target=p1, args=(self,p2,p3,))
        self.cancel = False
    def stop(self):
        self.cancel = True

class request(IntEnum):
  Login          = 0
  Query          = 1
  Execute        = 2
  Script         = 3
  QueryEditData  = 4
  SaveEditData   = 5
  CancelThread   = 6
  Debug          = 7
  CloseTab       = 8

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

class debugState(IntEnum):
  Initial  = 0
  Starting = 1
  Ready    = 2
  Step     = 3
  Finished = 4
  Cancel   = 5

def closeTabHandler(ws_object,p_tab_object_id):
    try:
        tab_object = ws_object.v_list_tab_objects[p_tab_object_id]
        if tab_object['type'] == 'query':
            try:
                tab_object['omnidatabase'].v_connection.Cancel()
            except Exception:
                None
            try:
                tab_object['omnidatabase'].v_connection.Close()
            except Exception:
                None
        elif tab_object['type'] == 'debug':
            tab_object['cancelled'] = True
            try:
                tab_object['omnidatabase_control'].v_connection.Cancel()
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
        del ws_object.v_list_tab_objects[p_tab_object_id]
    except Exception as exc:
        None



class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    None
  def on_message(self, message):
    v_response = {
        'v_code': 0,
        'v_context_code': 0,
        'v_error': False,
        'v_data': 1
    }

    try:
        json_object = json.loads(message)
        v_code = json_object['v_code']
        v_context_code = json_object['v_context_code']
        v_data = json_object['v_data']

        v_response['v_context_code'] = v_context_code
        #Login request
        if v_code == request.Login:
            self.v_user_key = v_data
            try:
                v_session = SessionStore(session_key=v_data)['omnidb_session']
                self.v_session = v_session
                v_response['v_code'] = response.LoginResult
                self.v_list_tab_objects = dict([])
                self.write_message(json.dumps(v_response))
            except Exception:
                v_response['v_code'] = response.SessionMissing
                self.write_message(json.dumps(v_response))
        else:
            #Cancel thread
            if v_code == request.CancelThread:
                try:
                    thread_data = self.v_list_tab_objects[v_data]
                    if thread_data:

                        thread_data['thread'].stop()
                        thread_data['omnidatabase'].v_connection.Cancel()
                except Exception as exc:
                    None;

            #Close Tab
            elif v_code == request.CloseTab:
                for v_tab_close_data in v_data:
                    closeTabHandler(self,v_tab_close_data['tab_id'])
                    #remove from tabs table if db_tab_id is not null
                    if v_tab_close_data['tab_db_id']:
                        try:
                            self.v_session.v_omnidb_database.v_connection.Execute('''
                            delete from tabs
                            where tab_id = {0}
                            '''.format(v_tab_close_data['tab_db_id']))
                        except Exception as exc:
                            None

            else:
                try:
                    #Getting refreshed session
                    s = SessionStore(session_key=self.v_user_key)
                    v_session = s['omnidb_session']
                    self.v_session = v_session

                    #Check database prompt timeout
                    v_timeout = v_session.DatabaseReachPasswordTimeout(v_data['v_db_index'])
                    if v_timeout['timeout']:
                        v_response['v_code'] = response.PasswordRequired
                        self.write_message(json.dumps(v_response))
                        return

                    if v_code == request.Query or v_code == request.QueryEditData or v_code == request.SaveEditData:

                        #create tab object if it doesn't exist
                        try:
                            tab_object = self.v_list_tab_objects[v_data['v_tab_id']]
                        except Exception as exc:
                            v_database = v_session.v_databases[v_data['v_db_index']]['database']
                            v_database_new = OmniDatabase.Generic.InstantiateDatabase(
                                v_database.v_db_type,
                                v_database.v_server,
                                v_database.v_port,
                                v_database.v_service,
                                v_database.v_user,
                                v_database.v_connection.v_password,
                                v_database.v_conn_id,
                                v_database.v_alias
                            )
                            tab_object =  { 'thread': None,
                                         'omnidatabase': v_database_new,
                                         'database_index': -1,
                                         'inserted_tab': False }
                            self.v_list_tab_objects[v_data['v_tab_id']] = tab_object
                            None;

                        #create database object
                        if tab_object['database_index']!=v_data['v_db_index']:
                            v_database = v_session.v_databases[v_data['v_db_index']]['database']
                            v_database_new = OmniDatabase.Generic.InstantiateDatabase(
                                v_database.v_db_type,
                                v_database.v_server,
                                v_database.v_port,
                                v_database.v_service,
                                v_database.v_user,
                                v_database.v_connection.v_password,
                                v_database.v_conn_id,
                                v_database.v_alias
                            )
                            tab_object['omnidatabase'] = v_database_new
                            tab_object['database_index'] = v_data['v_db_index']

                        v_data['v_context_code'] = v_context_code
                        v_data['v_database'] = tab_object['omnidatabase']

                        #Query request
                        if v_code == request.Query:
                            tab_object['tab_db_id'] = v_data['v_tab_db_id']
                            v_data['v_tab_object'] = tab_object
                            t = StoppableThread(thread_query,v_data,self)
                            tab_object['thread'] = t
                            tab_object['type'] = 'query'
                            tab_object['sql_cmd'] = v_data['v_sql_cmd']
                            tab_object['tab_id'] = v_data['v_tab_id']
                            #t.setDaemon(True)
                            t.start()

                            #Send Ack Message
                            v_response['v_code'] = response.QueryAck
                            self.write_message(json.dumps(v_response))

                        #Query edit data
                        elif v_code == request.QueryEditData:
                            t = StoppableThread(thread_query_edit_data,v_data,self)
                            tab_object['thread'] = t
                            tab_object['type'] = 'edit'
                            #t.setDaemon(True)
                            t.start()

                            #Send Ack Message
                            v_response['v_code'] = response.QueryAck
                            self.write_message(json.dumps(v_response))

                        #Save edit data
                        elif v_code == request.SaveEditData:
                            t = StoppableThread(thread_save_edit_data,v_data,self)
                            tab_object['thread'] = t
                            tab_object['type'] = 'edit'
                            #t.setDaemon(True)
                            t.start()
                    #Debugger
                    elif v_code == request.Debug:

                        #New debugger, create connections
                        if v_data['v_state'] == debugState.Starting:
                            v_database = v_session.v_databases[v_data['v_db_index']]['database']
                            v_database_debug = OmniDatabase.Generic.InstantiateDatabase(
                                v_database.v_db_type,
                                v_database.v_server,
                                v_database.v_port,
                                v_database.v_service,
                                v_database.v_user,
                                v_database.v_connection.v_password,
                                v_database.v_conn_id,
                                v_database.v_alias
                            )
                            v_database_control = OmniDatabase.Generic.InstantiateDatabase(
                                v_database.v_db_type,
                                v_database.v_server,
                                v_database.v_port,
                                v_database.v_service,
                                v_database.v_user,
                                v_database.v_connection.v_password,
                                v_database.v_conn_id,
                                v_database.v_alias
                            )
                            tab_object =  { 'thread': None,
                                         'omnidatabase_debug': v_database_debug,
                                         'omnidatabase_control': v_database_control,
                                         'debug_pid': -1,
                                         'cancelled': False,
                                         'tab_id': v_data['v_tab_id'],
                                         'type': 'debug' }
                            self.v_list_tab_objects[v_data['v_tab_id']] = tab_object
                        #Existing debugger, get existing tab_object
                        else:
                            tab_object = self.v_list_tab_objects[v_data['v_tab_id']]

                        v_data['v_context_code'] = v_context_code
                        v_data['v_tab_object'] = tab_object

                        t = StoppableThread(thread_debug,v_data,self)
                        #tab_object['thread'] = t
                        #t.setDaemon(True)
                        t.start()

                        #Send Ack Message
                        v_response['v_code'] = response.QueryAck
                        self.write_message(json.dumps(v_response))

                except Exception as exc:
                    v_response['v_code'] = response.SessionMissing
                    self.write_message(json.dumps(v_response))

    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_code'] = response.MessageException
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        self.write_message(json.dumps(v_response))

  def on_close(self):
    try:
        for k in list(self.v_list_tab_objects.keys()):
            closeTabHandler(self,k)
    except Exception:
        None


  def check_origin(self, origin):
    return True

def start_wsserver_thread():
    t = threading.Thread(target=start_wsserver)
    t.setDaemon(True)
    t.start()

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OmniDB.settings")
#from tornado.options import options, define, parse_command_line
#import django.conf
#import django.contrib.auth
#import django.core.handlers.wsgi
#import django.db
#import tornado.wsgi

def start_wsserver():
    #logger.info('''*** Starting OmniDB ***''')
    #logger.info('''*** Starting Query WS Server ***''')
    #wsgi_app = tornado.wsgi.WSGIContainer(
    # django.core.handlers.wsgi.WSGIHandler())
    try:
        application = tornado.web.Application([
          (r'/ws', WSHandler),
          (r'/wss',WSHandler),
          #('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])

        if settings.IS_SSL:
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(settings.SSL_CERTIFICATE,
                                   settings.SSL_KEY)
            server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)
        else:
            server = tornado.httpserver.HTTPServer(application)

        server.listen(settings.WS_QUERY_PORT)
        tornado.ioloop.IOLoop.instance().start()

    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

def send_response_thread_safe(ws_object,message):
    try:
        ws_object.write_message(message)
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

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

def LogHistory(p_omnidb_database,
               p_user_id,
               p_user_name,
               p_sql,
               p_start,
               p_end,
               p_duration,
               p_status):

    try:

        logger.info('''*** SQL Command ***
USER: {0},
START: {1},
END: {2},
DURATION: {3},
STATUS: {4},
COMMAND: {5}'''.format(p_user_name,
           p_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
           p_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
           p_duration,
           p_status,
           p_sql.replace("'","''")))

        p_omnidb_database.v_connection.Execute('''
            insert into command_list values (
            {0},
            (select coalesce(max(cl_in_codigo), 0) + 1 from command_list),
            '{1}',
            '{2}',
            '{3}',
            '{4}',
            '{5}')
        '''.format(p_user_id,
                   p_sql.replace("'","''"),
                   p_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                   p_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                   p_status,
                   p_duration))
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

def thread_query(self,args,ws_object):
    v_response = {
        'v_code': response.QueryResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    try:
        v_database_index = args['v_db_index']
        v_sql            = args['v_sql_cmd']
        v_select_value   = args['v_cmd_type']
        v_tab_id         = args['v_tab_id']
        v_tab_object     = args['v_tab_object']
        v_mode           = args['v_mode']
        v_all_data       = args['v_all_data']
        v_log_query      = args['v_log_query']

        #Removing last character if it is a semi-colon
        if v_sql[-1:]==';':
            v_sql = v_sql[:-1]

        v_session = ws_object.v_session
        v_database = args['v_database']
        v_omnidb_database = OmniDatabase.Generic.InstantiateDatabase(
            'sqlite',
            '',
            '',
            settings.OMNIDB_DATABASE,
            '',
            '',
            '0',
            ''
        )

        log_start_time = datetime.now()
        log_status = 'success'

        v_inserted_id = None
        try:
            #insert new tab record
            if not v_tab_object['tab_db_id'] and not v_tab_object['inserted_tab'] and v_log_query:
                try:
                    v_omnidb_database.v_connection.Open()
                    v_omnidb_database.v_connection.Execute('''
                    insert into tabs (conn_id,user_id,tab_id,snippet)
                    values
                    ({0},{1},(select coalesce(max(tab_id), 0) + 1 from tabs),'{2}')
                    '''.format(ws_object.v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id, ws_object.v_session.v_user_id, v_tab_object['sql_cmd'].replace("'","''")))
                    v_inserted_id = v_omnidb_database.v_connection.ExecuteScalar('''
                    select coalesce(max(tab_id), 0) from tabs
                    ''')
                    v_omnidb_database.v_connection.Close()
                    v_tab_object['inserted_tab'] = True
                    v_inserted_tab = True
                except Exception as exc:
                    None

            if v_mode==0:
                v_database.v_connection.Open()

            if (v_mode==0 or v_mode==1) and not v_all_data:
                v_data1 = v_database.v_connection.QueryBlock(v_sql,50, True)
            elif v_mode==2 or v_all_data:
                v_data1 = v_database.v_connection.QueryBlock(v_sql,-1, True)

            v_notices = v_database.v_connection.GetNotices()
            v_notices_text = ''
            if len(v_notices) > 0:
                for v_notice in v_notices:
                    v_notices_text += v_notice.replace('\n','<br/>')

            if v_mode==2 or v_all_data or len(v_data1.Rows)<50:
                try:
                    v_database.v_connection.Close()
                except:
                    pass

            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)

            v_response['v_data'] = {
                'v_col_names' : v_data1.Columns,
                'v_data' : v_data1.Rows,
                'v_query_info' : "Number of records: {0}".format(len(v_data1.Rows)),
                'v_duration': v_duration,
                'v_notices': v_notices_text,
                'v_notices_length': len(v_notices),
                'v_inserted_id': v_inserted_id
            }
        except Exception as exc:
            try:
                v_database.v_connection.Close()
            except:
                pass
            log_end_time = datetime.now()
            v_duration = GetDuration(log_start_time,log_end_time)
            log_status = 'error'
            v_response['v_data'] = {
                'position': v_database.GetErrorPosition(str(exc)),
                'message' : str(exc).replace('\n','<br>'),
                'v_duration': v_duration,
                'v_inserted_id': v_inserted_id
            }
            v_response['v_error'] = True

        if not self.cancel:
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

        #Log to history
        if v_mode==0 and v_log_query:
            LogHistory(v_omnidb_database,
                    v_session.v_user_id,
                    v_session.v_user_name,
                    v_sql,
                    log_start_time,
                    log_end_time,
                    v_duration,
                    log_status)

        #if mode=0 save tab
        if v_mode==0 and v_tab_object['tab_db_id'] and v_log_query:
            try:
                v_omnidb_database.v_connection.Execute('''
                update tabs
                set conn_id = {0},
                    snippet = '{1}'
                where tab_id = {2}
                '''.format(ws_object.v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id, v_tab_object['sql_cmd'].replace("'","''"), v_tab_object['tab_db_id']))
            except Exception as exc:
                None
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

def thread_query_edit_data(self,args,ws_object):
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

        v_session = ws_object.v_session
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
                v_column_list = v_column_list + v_column['v_readformat'].replace('#', v_column['v_column'])

            v_data1 = v_database.QueryTableRecords(v_column_list, v_table_name, v_filter, v_count)

            v_response['v_data']['v_query_info'] = 'Number of records: ' + str(len(v_data1.Rows))

            for v_row in v_data1.Rows:
                v_row_data = []

                v_row_pk = []
                for j in range(0, len(v_pk_list)):
                    v_pk_col = {}
                    v_pk_col['v_column'] = v_pk_list[j]['v_column']
                    v_pk_col['v_value'] = v_row[v_pk_list[j]['v_column']]
                    v_row_pk.append(v_pk_col)
                v_response['v_data']['v_row_pk'].append(v_row_pk)

                v_row_data.append('')
                for v_col in v_data1.Columns:
                    v_row_data.append(str(v_row[v_col]))
                v_response['v_data']['v_data'].append(v_row_data)

        except Exception as exc:
            v_response['v_data'] = str(exc)
            v_response['v_error'] = True

        if not self.cancel:
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            ws_object.write_message(json.dumps(v_response))

def thread_save_edit_data(self,args,ws_object):
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
        v_tab_id         = args['v_tab_id']

        v_session = ws_object.v_session
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

                    for j in range(0, len(v_pk_info)):
                        if v_pk['v_column'] == v_pk_info[j]['v_column']:
                            v_pk_index = j
                            break

                    if v_pk_info[v_pk_index]['v_class'] == 'numeric':
                        v_command = v_command + v_pk_info[v_pk_index]['v_compareformat'].replace('#', v_pk['v_column'] + ' = ' + str(v_pk['v_value']))
                    else:
                        v_command = v_command + v_pk_info[v_pk_index]['v_compareformat'].replace('#', v_pk['v_column'] + " = '" + str(v_pk['v_value']) + "'")

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

                    if v_columns[j-1]['v_class'] == 'numeric' or v_columns[j-1]['v_class'] == 'other':
                        if v_value == '':
                            v_command = v_command + 'null'
                        else:
                            v_command = v_command + v_columns[j-1]['v_writeformat'].replace('#', v_value)
                    else:
                        v_command = v_command + v_columns[j-1]['v_writeformat'].replace('#', v_value.replace("'", "''"))

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

                    if v_columns[v_col_index]['v_class'] == 'numeric' or v_columns[v_col_index]['v_class'] == 'other':
                        if v_value == '':
                            v_command = v_command + 'null'
                        else:
                            v_command = v_command + v_columns[v_col_index]['v_writeformat'].replace('#', v_value)
                    else:
                        v_command = v_command + v_columns[v_col_index]['v_writeformat'].replace('#', v_value.replace("'", "''"))

                v_command = v_command + ' where '
                v_first = True
                v_pk_index = 0

                for v_pk in v_row_info['pk']:
                    if not v_first:
                        v_command = v_command + ' and '
                    v_first = False

                    for j in range(0, len(v_pk_info)):
                        if v_pk['v_column'] == v_pk_info[j]['v_column']:
                            v_pk_index = j
                            break

                    if v_pk_info[v_pk_index]['v_class'] == 'numeric':
                        v_command = v_command + v_pk_info[v_pk_index]['v_compareformat'].replace('#', v_pk['v_column'] + ' = ' + str(v_pk['v_value']))
                    else:
                        v_command = v_command + v_pk_info[v_pk_index]['v_compareformat'].replace('#', v_pk['v_column'] + " = '" + str(v_pk['v_value']) + "'")

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
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            ws_object.write_message(json.dumps(v_response))


def thread_debug_run_func(self,args,ws_object):
    v_response = {
        'v_code': -1,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }
    v_tab_object = args['v_tab_object']
    v_database_debug = v_tab_object['omnidatabase_debug']
    v_database_control = v_tab_object['omnidatabase_control']

    try:
        #enable debugger for current connection
        v_database_debug.v_connection.Execute("select omnidb.omnidb_enable_debugger('{0}')".format(v_database_debug.v_connection.GetConnectionString().replace("'", "''")))

        #run function it will lock until the function ends
        v_func_return = v_database_debug.v_connection.Query('select * from {0} limit 1000'.format(args['v_function']),True)

        #Not cancelled, return all data
        if not v_tab_object['cancelled']:

            #retrieve variables
            v_variables = v_database_debug.v_connection.Query('select name,attribute,vartype,value from omnidb.variables where pid = {0}'.format(v_tab_object['debug_pid']),True)

            #retrieve statistics
            v_statistics = v_database_debug.v_connection.Query('select lineno,coalesce(trunc((extract("epoch" from tend)  - extract("epoch" from tstart))::numeric,4),0) as msec from omnidb.statistics where pid = {0} order by step'.format(v_tab_object['debug_pid']),True)

            #retrieve statistics summary
            v_statistics_summary = v_database_debug.v_connection.Query('''
            select lineno, max(msec) as msec
            from (select lineno,coalesce(trunc((extract("epoch" from tend)  - extract("epoch" from tstart))::numeric,4),0) as msec from omnidb.statistics where pid = {0}) t
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

            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
        #Cancelled, return cancelled status
        else:
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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

            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
        else:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))


def thread_debug(self,args,ws_object):
    v_response = {
        'v_code': -1,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }
    v_state = args['v_state']
    v_tab_id = args['v_tab_id']
    v_tab_object = args['v_tab_object']
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
            t = StoppableThread(thread_debug_run_func,{ 'v_tab_object': v_tab_object, 'v_context_code': args['v_context_code'], 'v_function': args['v_function']},ws_object)
            v_tab_object['thread'] = t
            #t.setDaemon(True)
            t.start()

            ws_object.v_list_tab_objects[v_tab_id] = v_tab_object

            v_lineno = None
            #wait for context to be ready or thread ends
            while v_lineno == None and t.isAlive():
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
                tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                    tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
                else:
                    v_database_control.v_connection.Execute('select pg_advisory_unlock({0}) from omnidb.contexts where pid = {0};'.format(v_tab_object['debug_pid']))
                    v_database_control.v_connection.Close()
                    v_response['v_code'] = response.RemoveContext
                    tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

            except Exception:
                v_response['v_code'] = response.RemoveContext
                tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

        #Cancelling debugger, the thread executing the function will return the cancel status
        elif v_state == debugState.Cancel:
            v_tab_object['cancelled'] = True
            v_database_control.v_connection.Cancel()
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

        tornado.ioloop.IOLoop.instance().add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
