import Spartacus.Database, Spartacus.Utils
import OmniDatabase
import uuid
from datetime import datetime

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
        self.v_databases = []
        self.v_user_key = p_user_key

        self.RefreshDatabaseList()

    def AddDatabase(self,
                    p_database):
        if len(self.v_databases)==0:
            self.v_database_index = 0

        self.v_databases.append(p_database)

    def GetSelectedDatabase(self):
        return self.v_databases(self.v_database_index)

    def RefreshDatabaseList(self):
        self.v_databases = []
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
                v_password = self.v_cryptor.Decrypt(r["password"])
            except Exception as exc:
                v_password = r["password"]
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
                v_password,
                r["conn_id"],
                v_alias
            )
            self.AddDatabase(database)

    def LogHistory(self,
                   p_sql):

        self.v_omnidb_database.v_connection.Execute('''
            insert into command_list values (
            {0},
            (select coalesce(max(cl_in_codigo), 0) + 1 from command_list),
            '{1}',
            '{2}')
        '''.format(self.v_user_id,p_sql.replace("'","''"),datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def Execute(self,
                p_database,
                p_sql,
                p_loghistory):
        v_table = p_database.v_connection.Execute(p_sql)

        if p_loghistory:
            self.LogHistory(p_sql)

        return v_table

    def Query(self,
                p_database,
                p_sql,
                p_loghistory):
        v_table = p_database.v_connection.Query(p_sql,True)

        if p_loghistory:
            self.LogHistory(p_sql)

        return v_table

    def QueryDataLimited(self,
                p_database,
                p_sql,
                p_count,
                p_loghistory):
        v_table = p_database.QueryDataLimited(p_sql, p_count)

        if p_loghistory:
            self.LogHistory(p_sql)

        return v_table
