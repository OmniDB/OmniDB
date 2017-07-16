from django.test import TestCase, Client
from django.http import JsonResponse

import json

import Spartacus.Database, Spartacus.Utils
import OmniDatabase

class PostgreSQL(TestCase):

    @classmethod
    def lists_equal(self, p_list_a, p_list_b):
        equal = True
        equal = len(p_list_a) == len(p_list_b)
        k = 0
        while k < len(p_list_a) and equal:
            if p_list_a[k] != p_list_b[k]:
                equal = False
            k = k + 1
        return equal

    @classmethod
    def setup_session(self):
        c = Client()
        response = c.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "admin"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert True == data['v_data']
        session = c.session
        assert 'admin' == session['omnidb_session'].v_user_name
        session['omnidb_session'].v_databases = [
            OmniDatabase.Generic.InstantiateDatabase(
                'postgresql',
                '127.0.0.1',
                '5432',
                'omnidb_tests',
                'omnidb',
                'omnidb',
                0,
                'OmniDB Tests'
            )
        ]
        session.save()
        return c

    def test_get_tree_info_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tree_info_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_tree_info_postgresql_session(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'database' == data['v_data']['v_mode']

    def test_template_create_tablespace(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TABLESPACE name
LOCATION 'directory'
--OWNER new_owner | CURRENT_USER | SESSION_USER
--WITH ( tablespace_option = value [, ... ] )
''' == data['v_data']['v_database_return']['create_tablespace']

    def test_template_alter_tablespace(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLESPACE #tablespace_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET seq_page_cost = value
--RESET seq_page_cost
--SET random_page_cost = value
--RESET random_page_cost
--SET effective_io_concurrency = value
--RESET effective_io_concurrency
''' == data['v_data']['v_database_return']['alter_tablespace']

    def test_template_drop_tablespace(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP TABLESPACE #tablespace_name#' == data['v_data']['v_database_return']['drop_tablespace']

    def test_template_create_role(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE ROLE name
--[ ENCRYPTED | UNENCRYPTED ] PASSWORD 'password'
--SUPERUSER | NOSUPERUSER
--CREATEDB | NOCREATEDB
--CREATEROLE | NOCREATEROLE
--INHERIT | NOINHERIT
--LOGIN | NOLOGIN
--REPLICATION | NOREPLICATION
--BYPASSRLS | NOBYPASSRLS
--CONNECTION LIMIT connlimit
--VALID UNTIL 'timestamp'
--IN ROLE role_name [, ...]
--IN GROUP role_name [, ...]
--ROLE role_name [, ...]
--ADMIN role_name [, ...]
--USER role_name [, ...]
--SYSID uid
''' == data['v_data']['v_database_return']['create_role']

    def test_template_alter_role(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER ROLE #role_name#
--SUPERUSER | NOSUPERUSER
--CREATEDB | NOCREATEDB
--CREATEROLE | NOCREATEROLE
--INHERIT | NOINHERIT
--LOGIN | NOLOGIN
--REPLICATION | NOREPLICATION
--BYPASSRLS | NOBYPASSRLS
--CONNECTION LIMIT connlimit
--[ ENCRYPTED | UNENCRYPTED ] PASSWORD 'password'
--VALID UNTIL 'timestamp'
--RENAME TO new_name
--[ IN DATABASE database_name ] SET configuration_parameter TO { value | DEFAULT }
--[ IN DATABASE database_name ] SET configuration_parameter FROM CURRENT
--[ IN DATABASE database_name ] RESET configuration_parameter
--[ IN DATABASE database_name ] RESET ALL
''' == data['v_data']['v_database_return']['alter_role']

    def test_template_drop_role(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP ROLE #role_name#' == data['v_data']['v_database_return']['drop_role']

    def test_template_create_database(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE DATABASE name
--OWNER user_name
--TEMPLATE template
--ENCODING encoding
--LC_COLLATE lc_collate
--LC_CTYPE lc_ctype
--TABLESPACE tablespace
--CONNECTION LIMIT connlimit
''' == data['v_data']['v_database_return']['create_database']

    def test_template_alter_database(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER DATABASE #database_name#
--ALLOW_CONNECTIONS allowconn
--CONNECTION LIMIT connlimit
--IS_TEMPLATE istemplate
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET TABLESPACE new_tablespace
--SET configuration_parameter TO { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
''' == data['v_data']['v_database_return']['alter_database']

    def test_template_drop_database(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP DATABASE #database_name#' == data['v_data']['v_database_return']['drop_database']

    def test_template_create_schema(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE SCHEMA schema_name
--AUTHORIZATION [ GROUP ] user_name | CURRENT_USER | SESSION_USER
''' == data['v_data']['v_database_return']['create_schema']

    def test_template_alter_schema(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER SCHEMA #schema_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
''' == data['v_data']['v_database_return']['alter_schema']

    def test_template_drop_schema(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SCHEMA #schema_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_schema']

    def test_template_drop_table(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP TABLE #table_name#
-- CASCADE
''' == data['v_data']['v_database_return']['drop_table']

    def test_template_create_sequence(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE SEQUENCE #schema_name#.name
--INCREMENT BY increment
--MINVALUE minvalue | NO MINVALUE
--MAXVALUE maxvalue | NO MAXVALUE
--START WITH start
--CACHE cache
--CYCLE
--OWNED BY { table_name.column_name | NONE }
''' == data['v_data']['v_database_return']['create_sequence']

    def test_template_alter_sequence(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER SEQUENCE #sequence_name#
--INCREMENT BY increment
--MINVALUE minvalue | NO MINVALUE
--MAXVALUE maxvalue | NO MAXVALUE
--START WITH start
--RESTART
--RESTART WITH restart
--CACHE cache
--CYCLE
--NO CYCLE
--OWNED BY { table_name.column_name | NONE }
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
--SET SCHEMA new_schema
''' == data['v_data']['v_database_return']['alter_sequence']

    def test_template_drop_sequence(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SEQUENCE #sequence_name#
-- CASCADE
''' == data['v_data']['v_database_return']['drop_sequence']

    def test_template_create_function(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE FUNCTION #schema_name#.name
--(
--    [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ]
--)
--RETURNS rettype
--RETURNS TABLE ( column_name column_type )
LANGUAGE plpgsql
--IMMUTABLE | STABLE | VOLATILE
--STRICT
--SECURITY DEFINER
--COST execution_cost
--ROWS result_rows
AS
$function$
--DECLARE
-- variables
BEGIN
-- definition
END;
$function$
''' == data['v_data']['v_database_return']['create_function']

    def test_template_drop_function(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP FUNCTION #function_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_function']

    def test_template_create_view(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE VIEW #schema_name#.name AS
SELECT ...
''' == data['v_data']['v_database_return']['create_view']

    def test_template_drop_view(self):
        c = self.setup_session()
        response = c.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP VIEW #view_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_view']

    def test_get_tables_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tables_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_tables_postgresql_session(self):
        c = self.setup_session()
        response = c.post('/get_tables_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], [
            'categories',
            'cust_hist',
            'customers',
            'inventory',
            'orderlines',
            'orders',
            'products',
            'reorder'
        ])

    def test_get_schemas_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_schemas_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_columns_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_pk_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_pk_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_fks_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_fks_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_uniques_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_uniques_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_indexes_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_indexes_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_functions_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_functions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_function_fields_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_function_fields_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_function_definition_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_function_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_sequences_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_sequences_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_views_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_views_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_views_columns_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_views_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_view_definition_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_view_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_databases_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_databases_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_tablespaces_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tablespaces_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_roles_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_roles_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']
