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
                p_omnidb_database,
                p_editor_theme,
                p_theme_type,
                p_theme_id,
                p_editor_font_size,
                p_interface_font_size,
                p_enable_omnichat,
                p_super_user,
                p_cryptor,
                p_user_key,
                p_csv_encoding,
                p_csv_delimiter):
        self.v_user_id = p_user_id
        self.v_user_name = p_user_name
        self.v_omnidb_database = p_omnidb_database
        self.v_editor_theme = p_editor_theme
        self.v_theme_type = p_theme_type
        self.v_theme_id = p_theme_id
        self.v_editor_font_size = p_editor_font_size
        self.v_interface_font_size = p_interface_font_size
        self.v_enable_omnichat = p_enable_omnichat
        self.v_super_user = p_super_user
        self.v_cryptor = p_cryptor
        self.v_database_index = -1
        self.v_databases = OrderedDict()
        self.v_user_key = p_user_key
        self.v_csv_encoding = p_csv_encoding
        self.v_csv_delimiter = p_csv_delimiter
        self.v_tab_connections = dict([])

        self.RefreshDatabaseList()

    def AddDatabase(self,
                    p_database,
                    p_prompt_password,
                    p_tunnel_information = None):
        if len(self.v_databases)==0:
            self.v_database_index = 0

        self.v_databases[p_database.v_conn_id] = {
                                'database': p_database,
                                'prompt_password': p_prompt_password,
                                'prompt_timeout': None,
                                'tunnel': p_tunnel_information,
                                'tunnel_object': None
                                }

    def DatabaseReachPasswordTimeout(self,p_database_index):
        if not self.v_databases[p_database_index]['prompt_password']:
            return { 'timeout': False, 'message': ''}
        else:
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
                                remote_bind_address=(self.v_databases[p_database_index]['database'].v_active_server, int(self.v_databases[p_database_index]['database'].v_active_port))
                            )
                        else:
                            server = SSHTunnelForwarder(
                                (self.v_databases[p_database_index]['tunnel']['server'], int(self.v_databases[p_database_index]['tunnel']['port'])),
                                ssh_username=self.v_databases[p_database_index]['tunnel']['user'],
                                ssh_password=self.v_databases[p_database_index]['tunnel']['password'],
                                remote_bind_address=(self.v_databases[p_database_index]['database'].v_active_server, int(self.v_databases[p_database_index]['database'].v_active_port))
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
        table = self.v_omnidb_database.v_connection.Query('''
            select *
            from connections
            where user_id = {0}
            order by dbt_st_name,
                     conn_id
        '''.format(self.v_user_id))

        for r in table.Rows:
            try:
                v_server = self.v_cryptor.Decrypt(r["server"])
            except Exception as exc:
                v_server = r["server"]
            try:
                v_port = self.v_cryptor.Decrypt(r["port"])
            except Exception as exc:
                v_port = r["port"]
            try:
                v_service = self.v_cryptor.Decrypt(r["service"])
            except Exception as exc:
                v_service = r["service"]
            try:
                v_user = self.v_cryptor.Decrypt(r["user"])
            except Exception as exc:
                v_user = r["user"]
            try:
                v_alias = self.v_cryptor.Decrypt(r["alias"])
            except Exception as exc:
                v_alias = r["alias"]
            try:
                v_conn_string = self.v_cryptor.Decrypt(r["conn_string"])
            except Exception as exc:
                v_conn_string = r["conn_string"]

            #SSH Tunnel information
            try:
                v_ssh_server = self.v_cryptor.Decrypt(r["ssh_server"])
            except Exception as exc:
                v_ssh_server = r["ssh_server"]
            try:
                v_ssh_port = self.v_cryptor.Decrypt(r["ssh_port"])
            except Exception as exc:
                v_ssh_port = r["ssh_port"]
            try:
                v_ssh_user = self.v_cryptor.Decrypt(r["ssh_user"])
            except Exception as exc:
                v_ssh_user = r["ssh_user"]
            try:
                v_ssh_password = self.v_cryptor.Decrypt(r["ssh_password"])
            except Exception as exc:
                v_ssh_password = r["ssh_password"]
            try:
                v_ssh_key = self.v_cryptor.Decrypt(r["ssh_key"])
            except Exception as exc:
                v_ssh_key = r["ssh_key"]
            try:
                v_use_tunnel = self.v_cryptor.Decrypt(r["use_tunnel"])
            except Exception as exc:
                v_use_tunnel = r["use_tunnel"]

            tunnel_information = {
                'enabled': False,
                'server': v_ssh_server,
                'port': v_ssh_port,
                'user': v_ssh_user,
                'password': v_ssh_password,
                'key': v_ssh_key
            }
            if v_use_tunnel == 1:
                tunnel_information['enabled'] = True

            database = OmniDatabase.Generic.InstantiateDatabase(
				r["dbt_st_name"],
				v_server,
				v_port,
				v_service,
				v_user,
                '',
                r["conn_id"],
                v_alias,
                p_conn_string = v_conn_string,
                p_parse_conn_string = True
            )

            if 1==0:
                self.AddDatabase(database,False,tunnel_information)
            else:
                self.AddDatabase(database,True,tunnel_information)

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
