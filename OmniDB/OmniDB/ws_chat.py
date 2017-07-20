import threading, time, datetime, json

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

from enum import IntEnum

omnidb_sessions = dict([])
omnidb_ws_sessions = dict([])

class ChatUser:
    def __init__(self, p_user_id = None, p_user_name = None, p_user_online = None):
        self.v_user_id = p_user_id
        self.v_user_name = p_user_name
        self.v_user_online = p_user_online

class ChatMessage:
    def __init__(self, p_message_id = None, p_user_name = None, p_text = None, p_timestamp = None, p_image = None):
        self.v_message_id = p_message_id
        self.v_user_name = p_user_name
        self.v_text = p_text
        self.v_timestamp = p_timestamp
        self.v_image = p_image

class request(IntEnum):
    Login = 0
    GetOldMessages = 1
    SendText = 2
    Writing = 3
    NotWriting = 4
    SendImage = 5

class response(IntEnum):
    OldMessages = 0
    NewMessage = 1
    UserList = 2
    UserWriting = 3
    UserNotWriting = 4

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('connection opened...')

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
            omnidb_ws_sessions[self.v_user_key] = self
            v_session = omnidb_sessions[self.v_user_key]
            self.v_user_id = v_session.v_user_id

            v_userList = []

            try:
                v_onlineUsers = '';

                for v_key in omnidb_ws_sessions:
                    if omnidb_ws_sessions[v_key].v_user_id is not None:
                        v_onlineUsers += str(omnidb_ws_sessions[v_key].v_user_id) + ', ';

                v_onlineUsers = v_onlineUsers[:-2]

                v_sql = '''
                	select x.*
                	from (
                	    select user_id,
                	           user_name,
                	           1 as online
                	    from users
                	    where user_id in ({0})

                	    union

                	    select user_id,
                	           user_name,
                	           0 as online
                	    from users
                	    where user_id not in ({1})
                	) x
                    where x.user_id not in (select user_id
                                            from users
                                            where chat_enabled = 0)
                	order by x.online desc, x.user_name'''.format(v_onlineUsers, v_onlineUsers)

                v_table = v_session.v_omnidb_database.v_connection.Query(v_sql, False)

                if v_table is not None:
                	for v_row in v_table.Rows:
                		v_userList.append(ChatUser(int(v_row['user_id']), v_row['user_name'], int(v_row['online'])).__dict__)
            except Exception as exc:
                v_response['v_data'] = str(exc)
                v_response['v_error'] = True
                self.write_message(json.dumps(v_response))
                return

            v_response['v_code'] = response.UserList
            v_response['v_data'] = v_userList

            for v_key in omnidb_ws_sessions:
                omnidb_ws_sessions[v_key].write_message(json.dumps(v_response))
        #GetOldMessages Request
        elif v_code == request.GetOldMessages:
            v_session = omnidb_sessions[self.v_user_key]

            v_messageList = []

            try:
                v_sql = '''
                    select mes.mes_in_code,
                           use.user_name,
                           mes.mes_st_text,
                           mes.mes_dt_timestamp,
                           mes.mes_bo_image
                    from messages mes
                    inner join messages_users meu
                               on mes.mes_in_code = meu.mes_in_code
                    inner join users use
                               on mes.user_id = use.user_id
                    where meu.user_id = {0}
                    order by mes.mes_dt_timestamp desc
                    limit 20 offset {1}'''.format(v_session.v_user_id, v_data)

                v_table = v_session.v_omnidb_database.v_connection.Query(v_sql, False);

                if v_table is not None:
                    for v_row in v_table.Rows:
                        v_messageList.append(ChatMessage(int(v_row['mes_in_code']), v_row['user_name'], v_row['mes_st_text'], v_row['mes_dt_timestamp'], int(v_row['mes_bo_image'])).__dict__)
            except Exception as exc:
                v_response['v_data'] = str(exc)
                v_response['v_error'] = True
                self.write_message(json.dumps(v_response))
                return

            v_response['v_code'] = response.OldMessages
            v_response['v_data'] = v_messageList
            self.write_message(json.dumps(v_response))
        #SendText Request
        elif v_code == request.SendText:
            v_session = omnidb_sessions[self.v_user_key]

            v_message = ChatMessage()

            try:
                v_database = Database.SQLite(v_session.v_omnidb_database.v_connection.v_service)
                v_database.Open()

                v_sql = '''
                    insert into messages (
                        mes_st_text,
                        mes_dt_timestamp,
                        user_id,
                        mes_bo_image
                    ) values (
                        '{0}',
                        datetime('now', 'localtime'),
                        {1},
                        0
                    )
                '''.format(v_data.replace("'", "&apos;"), v_session.v_user_id)

                v_database.Execute(v_sql)

                v_sql = '''
                    select max(mes_in_code)
                    from messages;
                '''

                v_messageCode = int(v_database.ExecuteScalar(v_sql))

                v_database.Close()

                v_sql = '''
                    insert into messages_users (
                        mes_in_code,
                        user_id
                    )
                    select {0},
                           use.user_id
                    from users use;'''.format(v_messageCode)

                v_session.v_omnidb_database.v_connection.Execute(v_sql)

                v_sql = '''
                    select mes_dt_timestamp
                    from messages
                    where mes_in_code = {0}'''.format(v_messageCode)

                v_message.v_message_id = v_messageCode
                v_message.v_user_name = v_session.v_user_name
                v_message.v_text = v_data
                v_message.v_timestamp = v_session.v_omnidb_database.v_connection.ExecuteScalar(v_sql)
                v_message.v_image = 0
            except Exception as exc:
                v_response['v_data'] = str(exc)
                v_response['v_error'] = True
                self.write_message(json.dumps(v_response))
                return

            v_response['v_code'] = response.NewMessage
            v_response['v_data'] = v_message.__dict__

            for v_key in omnidb_ws_sessions:
                omnidb_ws_sessions[v_key].write_message(json.dumps(v_response))
        #Writing Request
        elif v_code == request.Writing:
            v_session = omnidb_sessions[self.v_user_key]

            v_response['v_code'] = response.UserWriting
            v_response['v_data'] = v_session.v_user_id

            for v_key in omnidb_ws_sessions:
                omnidb_ws_sessions[v_key].write_message(json.dumps(v_response))
        #NotWriting Request
        elif v_code == request.NotWriting:
            v_session = omnidb_sessions[self.v_user_key]

            v_response['v_code'] = response.UserNotWriting
            v_response['v_data'] = v_session.v_user_id

            for v_key in omnidb_ws_sessions:
                omnidb_ws_sessions[v_key].write_message(json.dumps(v_response))
        #SendImage Request
        elif v_code == request.SendImage:
            v_session = omnidb_sessions[self.v_user_key]

            v_message = ChatMessage()

            try:
                v_database = Database.SQLite(v_session.v_omnidb_database.v_connection.v_service)
                v_database.Open()

                v_sql = '''
                    insert into messages (
                        mes_st_text,
                        mes_dt_timestamp,
                        user_id,
                        mes_bo_image
                    ) values (
                        '{0}',
                        datetime('now', 'localtime'),
                        {1},
                        1
                    )
                '''.format(v_data, v_session.v_user_id)

                v_database.Execute(v_sql)

                v_sql = '''
                    select max(mes_in_code)
                    from messages;
                '''

                v_messageCode = int(v_database.ExecuteScalar(v_sql))

                v_database.Close()

                v_sql = '''
                    insert into messages_users (
                        mes_in_code,
                        user_id
                    )
                    select {0},
                           use.user_id
                    from users use;'''.format(v_messageCode)

                v_session.v_omnidb_database.v_connection.Execute(v_sql)

                v_sql = '''
                    select mes_dt_timestamp
                    from messages
                    where mes_in_code = {0}'''.format(v_messageCode)

                v_message.v_message_id = v_messageCode
                v_message.v_user_name = v_session.v_user_name
                v_message.v_text = v_data
                v_message.v_timestamp = v_session.v_omnidb_database.v_connection.ExecuteScalar(v_sql)
                v_message.v_image = 1
            except Exception as exc:
                v_response['v_data'] = str(exc)
                v_response['v_error'] = True
                self.write_message(json.dumps(v_response))
                return

            v_response['v_code'] = response.NewMessage
            v_response['v_data'] = v_message.__dict__

            for v_key in omnidb_ws_sessions:
                omnidb_ws_sessions[v_key].write_message(json.dumps(v_response))

    def on_close(self):
        omnidb_ws_sessions.pop(self.v_user_key, None)
        print ('connection closed...')

    def check_origin(self, origin):
        return True

def start_wsserver_thread():
    t = threading.Thread(target=start_wsserver)
    t.setDaemon(True)
    t.start()

def start_wsserver():
    application = tornado.web.Application([
        (r'/ws', WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])
    application.listen(2011)
    #tornado.ioloop.IOLoop.instance().start()
