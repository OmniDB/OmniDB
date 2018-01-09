import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
import uuid
from datetime import datetime,timedelta
from django.contrib.sessions.backends.db import SessionStore
from OmniDB import settings

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
                p_enable_omnichat,
                p_super_user,
                p_cryptor,
                p_user_key):
        self.v_user_id = p_user_id
        self.v_user_name = p_user_name
        self.v_omnidb_database = p_omnidb_database
        self.v_editor_theme = p_editor_theme
        self.v_theme_type = p_theme_type
        self.v_theme_id = p_theme_id
        self.v_editor_font_size = p_editor_font_size
        self.v_enable_omnichat = p_enable_omnichat
        self.v_super_user = p_super_user
        self.v_cryptor = p_cryptor
        self.v_database_index = -1
        self.v_databases = {}
        self.v_user_key = p_user_key

        self.RefreshDatabaseList()

    def AddDatabase(self,
                    p_database,
                    p_prompt_password):
        if len(self.v_databases)==0:
            self.v_database_index = 0

        self.v_databases[p_database.v_conn_id] = {
                                'database': p_database,
                                'prompt_password': p_prompt_password,
                                'prompt_timeout': None
                                }

    def DatabaseReachPasswordTimeout(self,p_database_index):
        if not self.v_databases[p_database_index]['prompt_password']:
            return { 'timeout': False, 'message': ''}
        else:
            #Reached timeout, must request password
            if not self.v_databases[p_database_index]['prompt_timeout'] or datetime.now() > self.v_databases[p_database_index]['prompt_timeout'] + timedelta(0,settings.PWD_TIMEOUT_TOTAL):
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

            database = OmniDatabase.Generic.InstantiateDatabase(
				r["dbt_st_name"],
				v_server,
				v_port,
				v_service,
				v_user,
                '',
                r["conn_id"],
                v_alias
            )

            if 1==0:
                self.AddDatabase(database,False)
            else:
                self.AddDatabase(database,True)

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
