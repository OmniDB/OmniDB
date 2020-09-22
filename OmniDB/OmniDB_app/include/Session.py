import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
import uuid
from datetime import datetime,timedelta
from django.contrib.sessions.backends.db import SessionStore
from OmniDB import settings
from OmniDB import custom_settings
import sys
sys.path.append('OmniDB_app/include')
import paramiko
from sshtunnel import SSHTunnelForwarder
import socket
import time
import os
from collections import OrderedDict

from django.contrib.auth.models import User
from OmniDB_app.models.main import *

import logging
logger = logging.getLogger('OmniDB_app.Session')

tunnels = dict([])

'''
------------------------------------------------------------------------
Session
------------------------------------------------------------------------
'''
class Session(object):
    def __init__(self,
                p_user_id,
                p_user_name,
                p_theme,
                p_font_size,
                p_super_user,
                p_user_key,
                p_csv_encoding,
                p_csv_delimiter):
        self.v_user_id = p_user_id
        self.v_user_name = p_user_name
        self.v_theme = p_theme
        self.v_font_size = p_font_size
        self.v_super_user = p_super_user
        self.v_database_index = -1
        self.v_databases = OrderedDict()
        self.v_user_key = p_user_key
        self.v_csv_encoding = p_csv_encoding
        self.v_csv_delimiter = p_csv_delimiter
        self.v_tab_connections = dict([])

        self.RefreshDatabaseList()

    def AddDatabase(self,
                    p_conn_id = None,
                    p_technology = None,
                    p_database = None,
                    p_prompt_password = True,
                    p_tunnel_information = None,
                    p_alias = None):
        if len(self.v_databases)==0:
            self.v_database_index = 0

        self.v_databases[p_conn_id] = {
                                'database': p_database,
                                'prompt_password': p_prompt_password,
                                'prompt_timeout': None,
                                'tunnel': p_tunnel_information,
                                'tunnel_object': None,
                                'alias': p_alias,
                                'technology': p_technology
                                }

    def DatabaseReachPasswordTimeout(self,p_database_index):
        #Create tunnel if enabled
        if self.v_databases[p_database_index]['tunnel']['enabled']:
            v_create_tunnel = False
            if self.v_databases[p_database_index]['tunnel_object'] != None:
                try:
                    result = 0
                    v_tunnel_object = tunnels[self.v_databases[p_database_index]['database'].v_conn_id]
                    if not v_tunnel_object.is_active:
                        v_tunnel_object.stop()
                        v_create_tunnel = True
                except Exception as exc:
                    v_create_tunnel = True
                    None

            if self.v_databases[p_database_index]['tunnel_object'] == None or v_create_tunnel:
                try:
                    if self.v_databases[p_database_index]['tunnel']['key'].strip() != '':
                        v_file_name = '{0}'.format(str(time.time())).replace('.','_')
                        v_full_file_name = os.path.join(settings.TEMP_DIR, v_file_name)
                        with open(v_full_file_name,'w') as f:
                            f.write(self.v_databases[p_database_index]['tunnel']['key'])
                        server = SSHTunnelForwarder(
                            (self.v_databases[p_database_index]['tunnel']['server'], int(self.v_databases[p_database_index]['tunnel']['port'])),
                            ssh_username=self.v_databases[p_database_index]['tunnel']['user'],
                            ssh_private_key_password=self.v_databases[p_database_index]['tunnel']['password'],
                            ssh_pkey = v_full_file_name,
                            remote_bind_address=(self.v_databases[p_database_index]['database'].v_active_server, int(self.v_databases[p_database_index]['database'].v_active_port)),
                            logger=logger
                        )
                    else:
                        server = SSHTunnelForwarder(
                            (self.v_databases[p_database_index]['tunnel']['server'], int(self.v_databases[p_database_index]['tunnel']['port'])),
                            ssh_username=self.v_databases[p_database_index]['tunnel']['user'],
                            ssh_password=self.v_databases[p_database_index]['tunnel']['password'],
                            remote_bind_address=(self.v_databases[p_database_index]['database'].v_active_server, int(self.v_databases[p_database_index]['database'].v_active_port)),
                            logger=logger
                        )
                    server.set_keepalive = 120
                    server.start()

                    s = SessionStore(session_key=self.v_user_key)
                    tunnels[self.v_databases[p_database_index]['database'].v_conn_id] = server

                    self.v_databases[p_database_index]['tunnel_object'] = str(server.local_bind_port)
                    self.v_databases[p_database_index]['database'].v_connection.v_host = '127.0.0.1'
                    self.v_databases[p_database_index]['database'].v_connection.v_port = server.local_bind_port

                    #GO OVER ALL TABS CONNECTION OBJECTS AND UPDATE HOST AND PORT FOR THIS CONN_ID
                    try:
                        for k in list(self.v_tab_connections.keys()):
                            if self.v_tab_connections[k].v_conn_id == p_database_index:
                                self.v_tab_connections[k].v_connection.v_host = '127.0.0.1'
                                self.v_tab_connections[k].v_connection.v_port = server.local_bind_port
                    except Exception:
                        None
                    s['omnidb_session'] = self
                    s.save()

                except Exception as exc:
                    return { 'timeout': True, 'message': str(exc)}
        if self.v_databases[p_database_index]['prompt_password']:
            #Reached timeout, must request password
            if not self.v_databases[p_database_index]['prompt_timeout'] or datetime.now() > self.v_databases[p_database_index]['prompt_timeout'] + timedelta(0,custom_settings.PWD_TIMEOUT_TOTAL):
                #Try passwordless connection
                self.v_databases[p_database_index]['database'].v_connection.v_password = ''
                v_test = self.v_databases[p_database_index]['database'].TestConnection()

                if v_test=='Connection successful.':
                    s = SessionStore(session_key=self.v_user_key)
                    s['omnidb_session'].v_databases[p_database_index]['prompt_timeout'] = datetime.now()
                    s['omnidb_session'].v_databases[p_database_index]['database'].v_connection.v_password = ''
                    s.save()
                    return { 'timeout': False, 'message': ''}
                else:
                    return { 'timeout': True, 'message': v_test}
            #Reached half way to timeout, update prompt_timeout
            if datetime.now() > self.v_databases[p_database_index]['prompt_timeout'] + timedelta(0,settings.PWD_TIMEOUT_REFRESH):
                s = SessionStore(session_key=self.v_user_key)
                s['omnidb_session'].v_databases[p_database_index]['prompt_timeout'] = datetime.now()
                s.save()
        return { 'timeout': False, 'message': ''}

    def GetSelectedDatabase(self):
        return self.v_databases(self.v_database_index)

    def RefreshDatabaseList(self):
        self.v_databases = {}

        try:
            for conn in Connection.objects.filter(user=User.objects.get(id=self.v_user_id)):
                tunnel_information = {
                    'enabled': conn.use_tunnel,
                    'server': conn.ssh_server,
                    'port': conn.ssh_port,
                    'user': conn.ssh_user,
                    'password': conn.ssh_password,
                    'key': conn.ssh_key
                }

                database = OmniDatabase.Generic.InstantiateDatabase(
    				conn.technology.name,
    				conn.server,
    				conn.port,
    				conn.database,
    				conn.username,
                    conn.password,
                    conn.id,
                    conn.alias,
                    p_conn_string = conn.conn_string,
                    p_parse_conn_string = True
                )

                prompt_password = conn.password == ''

                self.AddDatabase(conn.id,conn.technology.name,database,prompt_password,tunnel_information,conn.alias)
        # No connections
        except Exception as exc:
            None

    def Execute(self,
                p_database,
                p_sql,
                p_loghistory):
        v_table = p_database.v_connection.Execute(p_sql)

        return v_table

    def Query(self,
                p_database,
                p_sql,
                p_loghistory):
        v_table = p_database.v_connection.Query(p_sql,True)

        return v_table

    def QueryDataLimited(self,
                p_database,
                p_sql,
                p_count,
                p_loghistory):
        v_table = p_database.QueryDataLimited(p_sql, p_count)

        return v_table
