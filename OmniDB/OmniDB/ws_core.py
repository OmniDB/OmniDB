import threading, time, datetime, json
from concurrent.futures.thread import ThreadPoolExecutor
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
from . import custom_settings

from django.contrib.sessions.backends.db import SessionStore

import logging
logger = logging.getLogger('OmniDB_app.QueryServer')

import os
import platform
import re

from tornado.options import options, define, parse_command_line
from . import ws_chat
from OmniDB.startup import clean_temp_folder

import sqlparse

class StoppableThread(threading.Thread):
    def __init__(self,p1,p2,p3):
        super(StoppableThread, self).__init__(target=p1, args=(self,p2,p3,))
        self.cancel = False
    def stop(self):
        self.cancel = True

class StoppableThreadPool(ThreadPoolExecutor):
    def __init__(self, p_max_workers=custom_settings.THREAD_POOL_MAX_WORKERS, p_tag={}):
        super(StoppableThreadPool, self).__init__(max_workers=p_max_workers)
        self.tag = p_tag
        self.cancel = False

    def stop(self, p_callback=None):
        self.cancel = True

        if p_callback is not None:
            p_callback(self)

    def start(self, p_function, p_argsList=[]):
        for p_args in p_argsList:
            self.submit(p_function, self, *p_args)

        super(StoppableThreadPool, self).shutdown(True)

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
  DataMining     = 9
  Console        = 10

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
  DataMiningResult    = 10
  ConsoleResult       = 11

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
                tab_object['omnidatabase'].v_connection.Cancel(False)
            except Exception:
                None
            try:
                tab_object['omnidatabase'].v_connection.Close()
            except Exception:
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
        del ws_object.v_list_tab_objects[p_tab_object_id]
    except Exception as exc:
        None

def thread_dispatcher(self,args,ws_object):
    message = args

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
            ws_object.v_user_key = v_data
            try:
                v_session = SessionStore(session_key=v_data)['omnidb_session']
                ws_object.v_session = v_session
                v_response['v_code'] = response.LoginResult
                ws_object.v_list_tab_objects = dict([])
                ws_object.write_message(json.dumps(v_response))
            except Exception:
                v_response['v_code'] = response.SessionMissing
                ws_object.write_message(json.dumps(v_response))
        else:
            #Cancel thread
            if v_code == request.CancelThread:
                try:
                    thread_data = ws_object.v_list_tab_objects[v_data]
                    if thread_data:
                        if thread_data['type'] == 'datamining':
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
                    None;

            #Close Tab
            elif v_code == request.CloseTab:
                for v_tab_close_data in v_data:
                    closeTabHandler(ws_object,v_tab_close_data['tab_id'])
                    #remove from tabs table if db_tab_id is not null
                    if v_tab_close_data['tab_db_id']:
                        try:
                            ws_object.v_session.v_omnidb_database.v_connection.Execute('''
                            delete from tabs
                            where tab_id = {0}
                            '''.format(v_tab_close_data['tab_db_id']))
                        except Exception as exc:
                            None

            else:
                try:
                    #Send Ack Message
                    v_response['v_code'] = response.QueryAck
                    #ws_object.write_message(json.dumps(v_response))
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

                    #Getting refreshed session
                    s = SessionStore(session_key=ws_object.v_user_key)
                    v_session = s['omnidb_session']
                    ws_object.v_session = v_session

                    #Check database prompt timeout
                    v_timeout = v_session.DatabaseReachPasswordTimeout(v_data['v_db_index'])
                    if v_timeout['timeout']:
                        v_response['v_code'] = response.PasswordRequired
                        v_response['v_data'] = v_timeout['message']
                        ws_object.write_message(json.dumps(v_response))
                        return

                    if v_code == request.Query or v_code == request.QueryEditData or v_code == request.SaveEditData or v_code == request.DataMining or v_code == request.Console:

                        #create tab object if it doesn't exist
                        try:
                            tab_object = ws_object.v_list_tab_objects[v_data['v_tab_id']]
                        except Exception as exc:
                            tab_object =  { 'thread': None,
                                         'omnidatabase': None,
                                         'database_index': -1,
                                         'inserted_tab': False }
                            ws_object.v_list_tab_objects[v_data['v_tab_id']] = tab_object
                            None;
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
                            logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
                            v_response['v_code'] = response.MessageException
                            v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
                            ws_object.write_message(json.dumps(v_response))

                        v_data['v_context_code'] = v_context_code
                        v_data['v_database'] = tab_object['omnidatabase']

                        #Query request
                        if v_code == request.Query:
                            tab_object['tab_db_id'] = v_data['v_tab_db_id']
                            v_data['v_tab_object'] = tab_object
                            t = StoppableThread(thread_query,v_data,ws_object)
                            tab_object['thread'] = t
                            tab_object['type'] = 'query'
                            tab_object['sql_cmd'] = v_data['v_sql_cmd']
                            tab_object['sql_save'] = v_data['v_sql_save']
                            tab_object['tab_id'] = v_data['v_tab_id']
                            #t.setDaemon(True)
                            t.start()

                        #Console request
                        if v_code == request.Console:
                            v_data['v_tab_object'] = tab_object
                            t = StoppableThread(thread_console,v_data,ws_object)
                            tab_object['thread'] = t
                            tab_object['type'] = 'console'
                            tab_object['sql_cmd'] = v_data['v_sql_cmd']
                            tab_object['tab_id'] = v_data['v_tab_id']
                            #t.setDaemon(True)
                            t.start()

                        #Query edit data
                        elif v_code == request.QueryEditData:
                            t = StoppableThread(thread_query_edit_data,v_data,ws_object)
                            tab_object['thread'] = t
                            tab_object['type'] = 'edit'
                            #t.setDaemon(True)
                            t.start()

                        #Save edit data
                        elif v_code == request.SaveEditData:
                            t = StoppableThread(thread_save_edit_data,v_data,ws_object)
                            tab_object['thread'] = t
                            tab_object['type'] = 'edit'
                            #t.setDaemon(True)
                            t.start()
                        #Query Data Mining
                        elif v_code == request.DataMining:
                            v_response = {
                                'v_code': response.DataMiningResult,
                                'v_context_code': v_data['v_context_code'],
                                'v_error': False,
                                'v_data': 1
                            }

                            tab_object['tab_db_id'] = v_data['v_tab_db_id']
                            v_data['v_tab_object'] = tab_object
                            v_data['v_sql_dict'] = tab_object['omnidatabase'].DataMining(v_data['text'], v_data['caseSensitive'], v_data['regex'], v_data['categoryList'], v_data['schemaList'], v_data['dataCategoryFilter'])

                            t = StoppableThreadPool(
                                p_tag = {
                                    'activeConnections': [],
                                    'lock': threading.RLock(),
                                    'result': {}
                                }
                            )

                            tab_object['thread_pool'] = t
                            tab_object['type'] = 'datamining'
                            tab_object['tab_id'] = v_data['v_tab_id']

                            v_argsList = []

                            for v_key1 in v_data['v_sql_dict']:
                                if v_key1 == 'Data':
                                    for v_key2 in v_data['v_sql_dict'][v_key1]:
                                        v_sql = v_data['v_sql_dict'][v_key1][v_key2]
                                        v_argsList.append([v_key1, v_key2, v_sql, v_data, ws_object])
                                else:
                                    v_sql = v_data['v_sql_dict'][v_key1]
                                    v_argsList.append([v_key1, None, v_sql, v_data, ws_object])

                            log_start_time = datetime.now()
                            log_status = 'success'

                            try:
                                #Will block here until thread pool ends
                                t.start(thread_datamining, v_argsList)

                                log_end_time = datetime.now()
                                v_duration = GetDuration(log_start_time,log_end_time)

                                v_response['v_data'] = {
                                    'v_duration': v_duration,
                                    'v_result': t.tag['result']
                                }
                            except Exception as exc:
                                log_end_time = datetime.now()
                                v_duration = GetDuration(log_start_time,log_end_time)
                                log_status = 'error'
                                v_response['v_data'] = {
                                    'message' : str(exc).replace('\n','<br>'),
                                    'v_duration': v_duration
                                }
                                v_response['v_error'] = True

                            #If the thread pool wasn't previously cancelled
                            if not t.cancel:
                                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

                    #Debugger
                    elif v_code == request.Debug:

                        #New debugger, create connections
                        if v_data['v_state'] == debugState.Starting:
                            try:
                                v_conn_tab_connection = v_session.v_tab_connections[v_data['v_conn_tab_id']]
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
                                tab_object =  { 'thread': None,
                                             'omnidatabase_debug': v_database_debug,
                                             'omnidatabase_control': v_database_control,
                                             'debug_pid': -1,
                                             'cancelled': False,
                                             'tab_id': v_data['v_tab_id'],
                                             'type': 'debug' }
                                ws_object.v_list_tab_objects[v_data['v_tab_id']] = tab_object
                            except Exception as exc:
                                logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
                                v_response['v_code'] = response.MessageException
                                v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
                                ws_object.write_message(json.dumps(v_response))

                        #Existing debugger, get existing tab_object
                        else:
                            tab_object = ws_object.v_list_tab_objects[v_data['v_tab_id']]

                        v_data['v_context_code'] = v_context_code
                        v_data['v_tab_object'] = tab_object

                        # Instead of getting the connection port which can be forwarded, we get the local PostgreSQL port
                        #v_data['v_port'] = v_session.v_databases[v_data['v_db_index']]['database'].v_port
                        v_data['v_port'] = v_session.v_databases[v_data['v_db_index']]['database'].v_connection.ExecuteScalar('show port')

                        t = StoppableThread(thread_debug,v_data,ws_object)
                        #tab_object['thread'] = t
                        #t.setDaemon(True)
                        t.start()

                except Exception as exc:
                    v_response['v_code'] = response.SessionMissing
                    #ws_object.write_message(json.dumps(v_response))
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_code'] = response.MessageException
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        #ws_object.write_message(json.dumps(v_response))
        ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    self.event_loop = tornado.ioloop.IOLoop.instance()
    None
  def on_message(self, message):
    t = StoppableThread(thread_dispatcher,message,self)
    t.start()

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

import asyncio
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

def start_wsserver():
    logger.info('''*** Starting OmniDB ***''')

    try:
        application = tornado.web.Application([
          (r'/ws', WSHandler),
          (r'/wss',WSHandler),
          (r'/chatws', ws_chat.WSHandler),
          (r'/chatwss',ws_chat.WSHandler)
        ])

        if settings.IS_SSL:
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(settings.SSL_CERTIFICATE,
                                   settings.SSL_KEY)
            server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)
        else:
            server = tornado.httpserver.HTTPServer(application)

        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        server.listen(settings.OMNIDB_WEBSOCKET_PORT,address=settings.OMNIDB_ADDRESS)
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
               p_status,
               p_conn_id):

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
            '{5}',
            {6})
        '''.format(p_user_id,
                   p_sql.replace("'","''"),
                   p_start.strftime('%Y-%m-%d %H:%M:%S'),
                   p_end.strftime('%Y-%m-%d %H:%M:%S'),
                   p_status,
                   p_duration,
                   p_conn_id))
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

def thread_datamining(self, p_key1, p_key2, p_sql, p_args, p_ws_object):
    try:
        v_session = p_ws_object.v_session

        #This thread pool was canceled by the user, so do nothing
        if self.cancel:
            return

        v_database = OmniDatabase.Generic.InstantiateDatabase(
            p_args['v_database'].v_db_type,
            p_args['v_database'].v_connection.v_host,
            p_args['v_database'].v_connection.v_port,
            p_args['v_database'].v_active_service,
            p_args['v_database'].v_active_user,
            p_args['v_database'].v_connection.v_password,
            p_args['v_database'].v_conn_id,
            p_args['v_database'].v_alias,
            p_conn_string = p_args['v_database'].v_conn_string,
            p_parse_conn_string = False
        )

        v_database.v_connection.Open()

        try:
            self.tag['lock'].acquire()
            self.tag['activeConnections'].append(v_database.v_connection)
        finally:
            self.tag['lock'].release()

        v_sql = re.sub(r'--#FILTER_PATTERN_CASE_SENSITIVE#.*\n', '', p_sql)
        v_sql = re.sub(r'--#FILTER_PATTERN_CASE_INSENSITIVE#.*\n', '', v_sql)
        v_sql = re.sub(r'--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#.*\n', '', v_sql)
        v_sql = re.sub(r'--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#.*\n', '', v_sql)
        v_sql = re.sub(r'--#FILTER_DATA_CATEGORY_FILTER#.*\n', '', v_sql)
        v_sql = re.sub(r'--#FILTER_BY_SCHEMA#.*\n', '', v_sql)

        v_result = {
            'count': v_database.v_connection.ExecuteScalar('''
                select count(x.*)
                from (
                    {0}
                ) x
                '''.format(p_sql)
            ),
            'sql': sqlparse.format(v_sql, reindent=True),
            'exception': None
        }

        v_database.v_connection.Close()

        try:
            self.tag['lock'].acquire()
            self.tag['activeConnections'].remove(v_database.v_connection)

            if p_key1 is not None:
                if p_key2 is not None: #Data category on
                    if p_key1 not in self.tag['result']: #If data not in result
                        self.tag['result'][p_key1] = {
                            'count': 0,
                            'result': {},
                            'exception': None
                        }

                    self.tag['result'][p_key1]['count'] += v_result['count']
                    self.tag['result'][p_key1]['result'][p_key2] = v_result
                else:
                    self.tag['result'][p_key1] = v_result
        finally:
            self.tag['lock'].release()
    except Exception as exc:
        #logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))

        v_result = {
            'count': 0,
            'sql': '',
            'exception': traceback.format_exc().replace('\n', '<br />')
        }

        try:
            self.tag['lock'].acquire()

            if v_database is not None and v_database.v_connection is not None and v_database.v_connection in self.tag['activeConnections']:
                v_database.v_connection.Close()
                self.tag['activeConnections'].remove(v_database.v_connection)

            if p_key1 is not None:
                if p_key2 is not None: #Data category on
                    if p_key1 not in self.tag['result']: #If data not in result
                        self.tag['result'][p_key1] = {
                            'count': 0,
                            'result': {},
                            'exception': ''
                        }

                    self.tag['result'][p_key1]['count'] += v_result['count']
                    self.tag['result'][p_key1]['exception'] += '<br />{0}'.format(v_result['exception'])
                    self.tag['result'][p_key1]['result'][p_key2] = v_result
                else:
                    self.tag['result'][p_key1] = v_result
        finally:
            self.tag['lock'].release()

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
        v_cmd_type       = args['v_cmd_type']
        v_tab_id         = args['v_tab_id']
        v_tab_object     = args['v_tab_object']
        v_mode           = args['v_mode']
        v_all_data       = args['v_all_data']
        v_log_query      = args['v_log_query']
        v_tab_title      = args['v_tab_title']
        v_autocommit     = args['v_autocommit']

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
                    insert into tabs (conn_id,user_id,tab_id,snippet,title)
                    values
                    ({0},{1},(select coalesce(max(tab_id), 0) + 1 from tabs),'{2}','{3}')
                    '''.format(ws_object.v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id, ws_object.v_session.v_user_id, v_tab_object['sql_save'].replace("'","''"),v_tab_title.replace("'","''")))
                    v_inserted_id = v_omnidb_database.v_connection.ExecuteScalar('''
                    select coalesce(max(tab_id), 0) from tabs
                    ''')
                    v_omnidb_database.v_connection.Close()
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
                    'v_filename': '/static/temp/{0}'.format(v_file_name),
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
                        ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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

                        ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
        except Exception as exc:
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

            if not self.cancel:
                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

        #Log to history
        if v_mode==0 and v_log_query:
            LogHistory(v_omnidb_database,
                    v_session.v_user_id,
                    v_session.v_user_name,
                    v_sql,
                    log_start_time,
                    log_end_time,
                    v_duration,
                    log_status,
                    ws_object.v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id)

        #if mode=0 save tab
        if v_mode==0 and v_tab_object['tab_db_id'] and v_log_query:
            try:
                v_omnidb_database.v_connection.Execute('''
                update tabs
                set conn_id = {0},
                    snippet = '{1}',
                    title = '{2}'
                where tab_id = {3}
                '''.format(ws_object.v_session.v_databases[v_tab_object['database_index']]['database'].v_conn_id, v_tab_object['sql_save'].replace("'","''"),v_tab_title.replace("'","''"), v_tab_object['tab_db_id']))
            except Exception as exc:
                None
    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_error'] = True
        v_response['v_data'] = traceback.format_exc().replace('\n','<br>')
        if not self.cancel:
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

def thread_console(self,args,ws_object):
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
                        ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
            else:
                if not self.cancel:
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

        if v_mode == 0:
            #logging to console history
            v_omnidb_database.v_connection.Open()
            v_omnidb_database.v_connection.Execute('BEGIN TRANSACTION')
            v_omnidb_database.v_connection.Execute('''
                insert into console_history values (
                {0},
                {1},
                '{2}',
                DATETIME('now'))
            '''.format(v_session.v_user_id,
                       v_database.v_conn_id,
                       v_sql.replace("'","''")))

            #keep 100 rows in console history table for current user/connection
            v_omnidb_database.v_connection.Execute('''
                delete
                from console_history
                where command_date not in (
                    select command_date
                    from console_history
                    where user_id = {0}
                      and conn_id = {1}
                    order by command_date desc
                    limit 100
                )
                and user_id = {0}
                and conn_id = {1}
            '''.format(v_session.v_user_id,
                       v_database.v_conn_id,
                       v_sql.replace("'","''")))

            #Log to history
            LogHistory(v_omnidb_database,
                    v_session.v_user_id,
                    v_session.v_user_name,
                    v_sql,
                    log_start_time,
                    log_end_time,
                    v_duration,
                    log_status,
                    v_database.v_conn_id)
            v_omnidb_database.v_connection.Close()

    except Exception as exc:
        logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
        v_response['v_data'] = {
            'v_data': str(exc),
            'v_duration': ''
        }
        if not self.cancel:
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                    v_pk_col['v_value'] = v_row[v_pk_list[j]['v_column'].replace('"','')]
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
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
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
                            v_command = v_command + v_columns[j-1]['v_writeformat'].replace('#', v_value.replace("'", "''"))
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
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
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
        v_conn_string = "port={0} dbname=''{1}'' user=''{2}''".format(args['v_port'],v_database_debug.v_service,v_database_debug.v_user);
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

            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
        #Cancelled, return cancelled status
        else:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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

            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
        else:
            v_response['v_code'] = response.DebugResponse
            v_response['v_data'] = {
                'v_state': debugState.Cancel,
                'v_remove_context': True,
                'v_error': False
            }
            ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))


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
            t = StoppableThread(thread_debug_run_func,{ 'v_tab_object': v_tab_object, 'v_context_code': args['v_context_code'], 'v_function': args['v_function'], 'v_type': args['v_type'], 'v_port': args['v_port']},ws_object)
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
                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
                else:
                    v_database_control.v_connection.Execute('select pg_advisory_unlock({0}) from omnidb.contexts where pid = {0};'.format(v_tab_object['debug_pid']))
                    v_database_control.v_connection.Close()
                    v_response['v_code'] = response.RemoveContext
                    ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

            except Exception:
                v_response['v_code'] = response.RemoveContext
                ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))

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

        ws_object.event_loop.add_callback(send_response_thread_safe,ws_object,json.dumps(v_response))
