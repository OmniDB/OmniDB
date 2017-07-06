import threading, time, datetime, json

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.httpserver
import ssl,os

import Spartacus.Database, Spartacus.Utils
import OmniDatabase

from enum import IntEnum
import sys

from . import settings

#global list of sessions
omnidb_sessions = dict([])
omnidb_ws_sessions = dict([])

class StoppableThread(threading.Thread):
    def __init__(self,p1,p2,p3):
        super(StoppableThread, self).__init__(target=p1, args=(self,p2,p3,))
        self.cancel = False
    def stop(self):
        self.cancel = True

class request(IntEnum):
  Login = 0
  Query = 1
  Execute = 2
  Script = 3
  QueryEditData = 4
  SaveEditData = 5
  CancelThread = 6

class response(IntEnum):
  LoginResult = 0
  QueryResult = 1
  QueryEditDataResult = 2
  SaveEditDataResult = 3
  SessionMissing = 4

def check_session_object(p_key):
    #Checking session
    try:
        v_session = omnidb_sessions[p_key]
        return True
    except Exception as exc:
        return False

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    None

  def on_message(self, message):
    json_object = json.loads(message)
    v_code = json_object['v_code']
    v_context_code = json_object['v_context_code']
    v_data = json_object['v_data']

    v_response = {
        'v_code': 0,
        'v_context_code': v_context_code,
        'v_error': False,
        'v_data': 1
    }

    #Login request
    if v_code == request.Login:
        self.v_user_key = v_data
        if check_session_object(self.v_user_key):
            v_response['v_code'] = response.LoginResult
            self.v_list_threads = dict([])
            omnidb_ws_sessions[self.v_user_key] = self
            self.write_message(json.dumps(v_response))
        else:
            v_response['v_code'] = response.SessionMissing
            self.write_message(json.dumps(v_response))
    #Query request
    elif v_code == request.Query:
        if check_session_object(self.v_user_key):
            v_data['v_context_code'] = v_context_code
            t = StoppableThread(thread_query,v_data,self)
            self.v_list_threads[v_context_code] =  { 'thread': t }
            #t.setDaemon(True)
            t.start()
        else:
            v_response['v_code'] = response.SessionMissing
            self.write_message(json.dumps(v_response))
    #Query edit data
    elif v_code == request.QueryEditData:
        if check_session_object(self.v_user_key):
            v_data['v_context_code'] = v_context_code
            t = StoppableThread(thread_query_edit_data,v_data,self)
            self.v_list_threads[v_context_code] =  { 'thread': t }
            #t.setDaemon(True)
            t.start()
        else:
            v_response['v_code'] = response.SessionMissing
            self.write_message(json.dumps(v_response))
    #Save edit data
    elif v_code == request.SaveEditData:
        if check_session_object(self.v_user_key):
            v_data['v_context_code'] = v_context_code
            t = StoppableThread(thread_save_edit_data,v_data,self)
            self.v_list_threads[v_context_code] =  { 'thread': t }
            #t.setDaemon(True)
            t.start()
        else:
            v_response['v_code'] = response.SessionMissing
            self.write_message(json.dumps(v_response))
    #Cancel thread
    elif v_code == request.CancelThread:
        thread_data = self.v_list_threads[v_data]
        if thread_data:
            thread_data['thread'].stop()

  def on_close(self):
    omnidb_ws_sessions.pop(self.v_user_key,None)

  def check_origin(self, origin):
    return True

def start_wsserver_thread():
    t = threading.Thread(target=start_wsserver)
    t.setDaemon(True)
    t.start()


def start_wsserver():
    application = tornado.web.Application([
      (r'/ws', WSHandler),
      (r'/wss',WSHandler),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
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

def thread_query(self,args,ws_object):
    v_database_index = args['v_db_index']
    v_sql            = args['v_sql_cmd']
    v_select_value   = args['v_cmd_type']

    v_response = {
        'v_code': response.QueryResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': 1
    }

    v_session = omnidb_sessions[ws_object.v_user_key]
    v_database2 = v_session.v_databases[v_database_index]
    v_database = OmniDatabase.Generic.InstantiateDatabase(
        v_database2.v_db_type,
        v_database2.v_server,
        v_database2.v_port,
        v_database2.v_service,
        v_database2.v_user,
        v_database2.v_connection.v_password,
        v_database2.v_conn_id,
        v_database2.v_alias
    )

    if v_select_value == '-2':
        try:
            v_session.Execute(v_database, v_sql, True)
            #v_database.v_connection.Execute(v_sql)
        except Exception as exc:
            v_response['v_data'] = str(exc)
            v_response['v_error'] = True

    elif v_select_value == '-3':
        v_commands = v_sql.split (';')

        v_return_html = ""

        v_num_success_commands = 0
        v_num_error_commands = 0

        v_database.v_connection.Open()

        for v_command in v_commands:

            if (self.cancel):
                ws_object.v_list_threads.pop(args['v_context_code'],None)
                return

            if v_command:
                try:
                    v_session.Execute(v_database, v_command, True)
                    #v_database.v_connection.Execute(v_command)
                    v_num_success_commands = v_num_success_commands + 1
                except Exception as exc:
                    v_num_error_commands = v_num_error_commands + 1
                    v_return_html += "<b>Command:</b> " + v_command + "<br/><br/><b>Message:</b> " + str(exc) + "<br/><br/>"

        v_response['v_data'] = "<b>Successful commands:</b> " + str(v_num_success_commands) + "<br/>"
        v_response['v_data'] += "<b>Errors: </b> " + str(v_num_error_commands) + "<br/><br/>"

        if v_num_error_commands > 0:
            v_response['v_data'] += "<b>Errors details:</b><br/><br/>" + v_return_html;

        v_database.v_connection.Close ()

    else:
        try:
            if v_select_value == '-1':
                v_data1 = v_session.Query(v_database, v_sql, True);
                #v_data1 = v_database.v_connection.Query(v_sql,True)
            else:
                v_data1 = v_session.QueryDataLimited(v_database, v_sql, v_select_value, True);
                #v_data1 = v_database.QueryDataLimited(v_sql, v_select_value)

            v_response['v_data'] = {
                'v_col_names' : v_data1.Columns,
                'v_data' : v_data1.Rows,
                'v_query_info' : "Number of records: {0}".format(len(v_data1.Rows))
            }
        except Exception as exc:
            v_response['v_data'] = str(exc)
            v_response['v_error'] = True

    if not self.cancel:
        ws_object.write_message(json.dumps(v_response))

def thread_query_edit_data(self,args,ws_object):
    v_database_index = args['v_db_index']
    v_table = args['v_table']
    v_schema = args['v_schema']
    v_filter = args['v_filter']
    v_count = args['v_count']
    v_pk_list = args['v_pk_list']
    v_columns = args['v_columns']

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

    v_session = omnidb_sessions[ws_object.v_user_key]
    v_database2 = v_session.v_databases[v_database_index]
    v_database = OmniDatabase.Generic.InstantiateDatabase(
        v_database2.v_db_type,
        v_database2.v_server,
        v_database2.v_port,
        v_database2.v_service,
        v_database2.v_user,
        v_database2.v_connection.v_password,
        v_database2.v_conn_id,
        v_database2.v_alias
    )

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
        ws_object.write_message(json.dumps(v_response))

def thread_save_edit_data(self,args,ws_object):
    v_database_index = args['v_db_index']
    v_table = args['v_table']
    v_schema = args['v_schema']
    v_data_rows = args['v_data_rows']
    v_rows_info = args['v_rows_info']
    v_pk_info = args['v_pk_info']
    v_columns = args['v_columns']

    v_response = {
        'v_code': response.SaveEditDataResult,
        'v_context_code': args['v_context_code'],
        'v_error': False,
        'v_data': []
    }

    v_session = omnidb_sessions[ws_object.v_user_key]
    v_database2 = v_session.v_databases[v_database_index]
    v_database = OmniDatabase.Generic.InstantiateDatabase(
        v_database2.v_db_type,
        v_database2.v_server,
        v_database2.v_port,
        v_database2.v_service,
        v_database2.v_user,
        v_database2.v_connection.v_password,
        v_database2.v_conn_id,
        v_database2.v_alias
    )

    if v_database.v_has_schema:
        v_table_name = v_schema + '.' + v_table
    else:
        v_table_name = v_table

    i = 0
    for v_row_info in v_rows_info:

        if (self.cancel):
            ws_object.v_list_threads.pop(args['v_context_code'],None)
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
        ws_object.write_message(json.dumps(v_response))
