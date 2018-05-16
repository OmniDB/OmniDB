from django.test import TestCase, Client
from django.http import JsonResponse

import json
from datetime import datetime, timedelta

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

class PostgreSQL(TestCase):

    @classmethod
    def setUpClass(self):
        super(PostgreSQL, self).setUpClass()
        self.host = '127.0.0.1'
        self.port = '5496'
        self.service = 'omnidb_tests'
        self.role = 'omnidb'
        self.password = 'omnidb'
        self.database = OmniDatabase.Generic.InstantiateDatabase(
            'postgresql',
            self.host,
            self.port,
            self.service,
            self.role,
            0,
            'OmniDB Tests'
        )
        self.database.v_connection.v_password = self.password

        self.cn = Client()

        self.cs = Client()
        response = self.cs.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "admin"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 0 <= data['v_data']
        session = self.cs.session
        assert 'admin' == session['omnidb_session'].v_user_name
        session['omnidb_session'].v_databases = [{
            'database': self.database,
            'prompt_password': False,
            'prompt_timeout': datetime.now() + timedelta(0,60000)
        }]
        session['omnidb_session'].v_tab_connections = {0: self.database}
        session.save()

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

    def test_get_tree_info_postgresql_nosession(self):
        response = self.cn.post('/get_tree_info_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_tree_info_postgresql_session(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'database' == data['v_data']['v_mode']

    def test_template_create_tablespace(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TABLESPACE name
LOCATION 'directory'
--OWNER new_owner | CURRENT_USER | SESSION_USER
--WITH ( tablespace_option = value [, ... ] )
''' == data['v_data']['v_database_return']['create_tablespace']

    def test_template_alter_tablespace(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP TABLESPACE #tablespace_name#' == data['v_data']['v_database_return']['drop_tablespace']

    def test_template_create_role(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP ROLE #role_name#' == data['v_data']['v_database_return']['drop_role']

    def test_template_create_database(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP DATABASE #database_name#' == data['v_data']['v_database_return']['drop_database']

    def test_template_create_extension(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE EXTENSION name
--SCHEMA schema_name
--VERSION VERSION
--FROM old_version
''' == data['v_data']['v_database_return']['create_extension']

    def test_template_alter_extension(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER EXTENSION #extension_name#
--UPDATE [ TO new_version ]
--SET SCHEMA new_schema
--ADD member_object
--DROP member_object
''' == data['v_data']['v_database_return']['alter_extension']

    def test_template_drop_extension(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP EXTENSION #extension_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_extension']

    def test_template_create_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE SCHEMA schema_name
--AUTHORIZATION [ GROUP ] user_name | CURRENT_USER | SESSION_USER
''' == data['v_data']['v_database_return']['create_schema']

    def test_template_alter_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER SCHEMA #schema_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
''' == data['v_data']['v_database_return']['alter_schema']

    def test_template_drop_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SCHEMA #schema_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_schema']

    def test_template_drop_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP TABLE #table_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_table']

    def test_template_create_sequence(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SEQUENCE #sequence_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_sequence']

    def test_template_create_function(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP FUNCTION #function_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_function']

    def test_template_create_triggerfunction(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE FUNCTION #schema_name#.name()
RETURNS trigger
LANGUAGE plpgsql
--IMMUTABLE | STABLE | VOLATILE
--COST execution_cost
AS
$function$
--DECLARE
-- variables
BEGIN
-- definition
END;
$function$
''' == data['v_data']['v_database_return']['create_triggerfunction']

    def test_template_drop_triggerfunction(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP FUNCTION #function_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_triggerfunction']

    def test_template_create_view(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE VIEW #schema_name#.name AS
SELECT ...
''' == data['v_data']['v_database_return']['create_view']

    def test_template_drop_view(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP VIEW #view_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_view']

    def test_template_create_mview(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE MATERIALIZED VIEW #schema_name#.name AS
SELECT ...
--WITH NO DATA
''' == data['v_data']['v_database_return']['create_mview']

    def test_template_refresh_mview(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''REFRESH MATERIALIZED VIEW #view_name#
--CONCURRENTLY
--WITH NO DATA
''' == data['v_data']['v_database_return']['refresh_mview']

    def test_template_drop_mview(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP MATERIALIZED VIEW #view_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_mview']

    def test_template_create_column(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD COLUMN name data_type
--COLLATE collation
--column_constraint [ ... ] ]
''' == data['v_data']['v_database_return']['create_column']

    def test_template_alter_column(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
--ALTER COLUMN #column_name#
--RENAME COLUMN #column_name# TO new_column
--TYPE data_type [ COLLATE collation ] [ USING expression ]
--SET DEFAULT expression
--DROP DEFAULT
--SET NOT NULL
--DROP NOT NULL
--SET STATISTICS integer
--SET ( attribute_option = value [, ... ] )
--RESET ( attribute_option [, ... ] )
--SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
''' == data['v_data']['v_database_return']['alter_column']

    def test_template_drop_column(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP COLUMN #column_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_column']

    def test_template_create_primarykey(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD CONSTRAINT name
PRIMARY KEY ( column_name [, ... ] )
--WITH ( storage_parameter [= value] [, ... ] )
--WITH OIDS
--WITHOUT OIDS
--USING INDEX TABLESPACE tablespace_name
''' == data['v_data']['v_database_return']['create_primarykey']

    def test_template_drop_primarykey(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_primarykey']

    def test_template_create_unique(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD CONSTRAINT name
UNIQUE ( column_name [, ... ] )
--WITH ( storage_parameter [= value] [, ... ] )
--WITH OIDS
--WITHOUT OIDS
--USING INDEX TABLESPACE tablespace_name
''' == data['v_data']['v_database_return']['create_unique']

    def test_template_drop_unique(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_unique']

    def test_template_create_foreignkey(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD CONSTRAINT name
FOREIGN KEY ( column_name [, ... ] )
REFERENCES reftable [ ( refcolumn [, ... ] ) ]
--MATCH { FULL | PARTIAL | SIMPLE }
--ON DELETE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT }
--ON UPDATE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT }
--NOT VALID
''' == data['v_data']['v_database_return']['create_foreignkey']

    def test_template_drop_foreignkey(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_foreignkey']

    def test_template_create_index(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] name
ON #table_name#
--USING method
( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
--WITH ( storage_parameter = value [, ... ] )
--WHERE predicate
''' == data['v_data']['v_database_return']['create_index']

    def test_template_alter_index(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''' == data['v_data']['v_database_return']['alter_index']

    def test_template_drop_index(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP INDEX [ CONCURRENTLY ] #index_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_index']

    def test_template_create_check(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD CONSTRAINT name
CHECK ( expression )
''' == data['v_data']['v_database_return']['create_check']

    def test_template_drop_check(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_check']

    def test_template_create_exclude(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
ADD CONSTRAINT name
--USING index_method
EXCLUDE ( exclude_element WITH operator [, ... ] )
--index_parameters
--WHERE ( predicate )
''' == data['v_data']['v_database_return']['create_exclude']

    def test_template_drop_exclude(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_exclude']

    def test_template_create_rule(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE RULE name
AS ON { SELECT | INSERT | UPDATE | DELETE }
TO #table_name#
--WHERE condition
--DO ALSO { NOTHING | command | ( command ; command ... ) }
--DO INSTEAD { NOTHING | command | ( command ; command ... ) }
''' == data['v_data']['v_database_return']['create_rule']

    def test_template_alter_rule(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER RULE #rule_name# ON #table_name# RENAME TO new_name' == data['v_data']['v_database_return']['alter_rule']

    def test_template_drop_rule(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP RULE #rule_name# ON #table_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_rule']

    def test_template_create_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TRIGGER name
--BEFORE { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE [ OR ] | TRUNCATE }
--AFTER { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE [ OR ] | TRUNCATE }
ON #table_name#
--FROM referenced_table_name
--NOT DEFERRABLE | [ DEFERRABLE ] { INITIALLY IMMEDIATE | INITIALLY DEFERRED }
--FOR EACH ROW
--FOR EACH STATEMENT
--WHEN ( condition )
--EXECUTE PROCEDURE function_name ( arguments )
''' == data['v_data']['v_database_return']['create_trigger']

    def test_template_create_view_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TRIGGER name
--BEFORE { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE }
--AFTER { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE }
--INSTEAD OF { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE }
ON #table_name#
--FROM referenced_table_name
--NOT DEFERRABLE | [ DEFERRABLE ] { INITIALLY IMMEDIATE | INITIALLY DEFERRED }
--FOR EACH ROW
--FOR EACH STATEMENT
--WHEN ( condition )
--EXECUTE PROCEDURE function_name ( arguments )
''' == data['v_data']['v_database_return']['create_view_trigger']

    def test_template_alter_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TRIGGER #trigger_name# ON #table_name# RENAME TO new_name' == data['v_data']['v_database_return']['alter_trigger']

    def test_template_enable_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TABLE #table_name# ENABLE TRIGGER #trigger_name#' == data['v_data']['v_database_return']['enable_trigger']

    def test_template_disable_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TABLE #table_name# DISABLE TRIGGER #trigger_name#' == data['v_data']['v_database_return']['disable_trigger']

    def test_template_drop_trigger(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP TRIGGER #trigger_name# ON #table_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_trigger']

    def test_template_create_inherited(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TABLE name (
    CHECK ( condition )
) INHERITS (#table_name#)
''' == data['v_data']['v_database_return']['create_inherited']

    def test_template_noinherit_partition(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TABLE #partition_name# NO INHERIT #table_name#' == data['v_data']['v_database_return']['noinherit_partition']

    def test_template_drop_partition(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP TABLE #partition_name#' == data['v_data']['v_database_return']['drop_partition']

    def test_template_vacuum(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''VACUUM
--FULL
--FREEZE
--ANALYZE
''' == data['v_data']['v_database_return']['vacuum']

    def test_template_vacuum_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''VACUUM
--FULL
--FREEZE
--ANALYZE
#table_name#
--(column_name, [, ...])
''' == data['v_data']['v_database_return']['vacuum_table']

    def test_template_analyze(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ANALYZE' == data['v_data']['v_database_return']['analyze']

    def test_template_analyze_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ANALYZE #table_name#
--(column_name, [, ...])
''' == data['v_data']['v_database_return']['analyze_table']

    def test_template_truncate(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''TRUNCATE
--ONLY
#table_name#
--RESTART IDENTITY
--CASCADE
''' == data['v_data']['v_database_return']['truncate']

    def test_template_create_physicalreplicationslot(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''SELECT * FROM pg_create_physical_replication_slot('slot_name')''' == data['v_data']['v_database_return']['create_physicalreplicationslot']

    def test_template_drop_physicalreplicationslot(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''SELECT pg_drop_replication_slot('#slot_name#')''' == data['v_data']['v_database_return']['drop_physicalreplicationslot']

    def test_template_create_logicalreplicationslot(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''SELECT * FROM pg_create_logical_replication_slot('slot_name', 'test_decoding')''' == data['v_data']['v_database_return']['create_logicalreplicationslot']

    def test_template_drop_logicalreplicationslot(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''SELECT pg_drop_replication_slot('#slot_name#')''' == data['v_data']['v_database_return']['drop_logicalreplicationslot']

    def test_template_create_publication(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE PUBLICATION name
--FOR TABLE [ ONLY ] table_name [ * ] [, ...]
--FOR ALL TABLES
--WITH ( publish = 'insert, update, delete' )
''' == data['v_data']['v_database_return']['create_publication']

    def test_template_alter_publication(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER PUBLICATION #pub_name#
--ADD TABLE [ ONLY ] table_name [ * ] [, ...]
--SET TABLE [ ONLY ] table_name [ * ] [, ...]
--DROP TABLE [ ONLY ] table_name [ * ] [, ...]
--SET ( publish = 'insert, update, delete' )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''' == data['v_data']['v_database_return']['alter_publication']

    def test_template_drop_publication(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP PUBLICATION #pub_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_publication']

    def test_template_add_pubtable(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER PUBLICATION #pub_name# ADD TABLE table_name' == data['v_data']['v_database_return']['add_pubtable']

    def test_template_drop_pubtable(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER PUBLICATION #pub_name# DROP TABLE #table_name#' == data['v_data']['v_database_return']['drop_pubtable']

    def test_template_create_subscription(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE SUBSCRIPTION name
CONNECTION 'conninfo'
PUBLICATION pub_name [, ...]
--WITH (
--copy_data = { true | false }
--, create_slot = { true | false }
--, enabled = { true | false }
--, slot_name = 'name'
--, synchronous_commit = { on | remote_apply | remote_write | local | off }
--, connect = { true | false }
--)
''' == data['v_data']['v_database_return']['create_subscription']

    def test_template_alter_subscription(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER SUBSCRIPTION #sub_name#
--CONNECTION 'conninfo'
--SET PUBLICATION pub_name [, ...] [ WITH ( refresh = { true | false } ) ]
--REFRESH PUBLICATION [ WITH ( copy_data = { true | false } ) ]
--ENABLE
--DISABLE
--SET (
--slot_name = 'name'
--, synchronous_commit = { on | remote_apply | remote_write | local | off }
--)
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''' == data['v_data']['v_database_return']['alter_subscription']

    def test_template_drop_subscription(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SUBSCRIPTION #sub_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_subscription']

    def test_template_pglogical_drop_node(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.drop_node(
node_name := '#node_name#',
ifexists := true
)''' == data['v_data']['v_database_return']['pglogical_drop_node']

    def test_template_pglogical_add_interface(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_node_add_interface(
node_name := '#node_name#',
interface_name := 'name',
dsn := 'host= port= dbname= user= password='
)''' == data['v_data']['v_database_return']['pglogical_add_interface']

    def test_template_pglogical_drop_interface(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_node_drop_interface(
node_name := '#node_name#',
interface_name := '#interface_name#'
)'''== data['v_data']['v_database_return']['pglogical_drop_interface']

    def test_template_pglogical_create_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.create_replication_set(
set_name := 'name',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true
)'''== data['v_data']['v_database_return']['pglogical_create_repset']

    def test_template_pglogical_alter_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_replication_set(
set_name := '#repset_name#',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true
)'''== data['v_data']['v_database_return']['pglogical_alter_repset']

    def test_template_pglogical_drop_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.drop_replication_set(
set_name := '#repset_name#',
ifexists := true
)'''== data['v_data']['v_database_return']['pglogical_drop_repset']

    def test_template_pglogical_repset_add_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_add_table(
set_name := '#repset_name#',
relation := 'schema.table'::regclass,
synchronize_data := true,
columns := null,
row_filter := null
)''' == data['v_data']['v_database_return']['pglogical_repset_add_table']

    def test_template_pglogical_repset_add_all_tables(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_add_all_tables(
set_name := '#repset_name#',
schema_names := ARRAY['public'],
synchronize_data := true
)''' == data['v_data']['v_database_return']['pglogical_repset_add_all_tables']

    def test_template_pglogical_repset_remove_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_remove_table(
set_name := '#repset_name#',
relation := '#table_name#'::regclass
)''' == data['v_data']['v_database_return']['pglogical_repset_remove_table']

    def test_template_pglogical_repset_add_seq(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_add_sequence(
set_name := '#repset_name#',
relation := 'schema.sequence'::regclass,
synchronize_data := true
)''' == data['v_data']['v_database_return']['pglogical_repset_add_seq']

    def test_template_pglogical_repset_add_all_seqs(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_add_all_sequences(
set_name := '#repset_name#',
schema_names := ARRAY['public'],
synchronize_data := true
)''' == data['v_data']['v_database_return']['pglogical_repset_add_all_seqs']

    def test_template_pglogical_repset_remove_seq(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.replication_set_remove_sequence(
set_name := '#repset_name#',
relation := '#sequence_name#'::regclass
)''' == data['v_data']['v_database_return']['pglogical_repset_remove_seq']

    def test_template_pglogical_create_sub(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.create_subscription(
subscription_name := 'sub_name',
provider_dsn := 'host= port= dbname= user= password=',
replication_sets := array['default','default_insert_only','ddl_sql'],
synchronize_structure := true,
synchronize_data := true,
forward_origins := array['all'],
apply_delay := '0 seconds'::interval
)''' == data['v_data']['v_database_return']['pglogical_create_sub']

    def test_template_pglogical_enable_sub(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_subscription_enable(
subscription_name := '#sub_name#',
immediate := true
)''' == data['v_data']['v_database_return']['pglogical_enable_sub']

    def test_template_pglogical_disable_sub(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_subscription_disable(
subscription_name := '#sub_name#',
immediate := true
)''' == data['v_data']['v_database_return']['pglogical_disable_sub']

    def test_template_pglogical_sync_sub(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_subscription_synchronize(
subscription_name := '#sub_name#',
truncate := true
)''' == data['v_data']['v_database_return']['pglogical_sync_sub']

    def test_template_pglogical_drop_sub(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.drop_subscription(
subscription_name := '#sub_name#',
ifexists := true
)''' == data['v_data']['v_database_return']['pglogical_drop_sub']

    def test_template_pglogical_sub_add_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_subscription_add_replication_set(
subscription_name := '#sub_name#',
replication_set := 'set_name'
)''' == data['v_data']['v_database_return']['pglogical_sub_add_repset']

    def test_template_pglogical_sub_remove_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select pglogical.alter_subscription_remove_replication_set(
subscription_name := '#sub_name#',
replication_set := '#set_name#'
)''' == data['v_data']['v_database_return']['pglogical_sub_remove_repset']

    def test_template_bdr_join_wait(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'select bdr.bdr_node_join_wait_for_ready()' == data['v_data']['v_database_return']['bdr_join_wait']

    def test_template_bdr_pause(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'select bdr.bdr_apply_pause()' == data['v_data']['v_database_return']['bdr_pause']

    def test_template_bdr_resume(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'select bdr.bdr_apply_resume()' == data['v_data']['v_database_return']['bdr_resume']

    def test_template_bdr_replicate_ddl_command(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.bdr_replicate_ddl_command('DDL command here...')" == data['v_data']['v_database_return']['bdr_replicate_ddl_command']

    def test_template_bdr_part_node(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.bdr_part_by_node_names('{#node_name#}')" == data['v_data']['v_database_return']['bdr_part_node']

    def test_template_bdr_insert_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''INSERT INTO bdr.bdr_replication_set_config (set_name, replicate_inserts, replicate_updates, replicate_deletes)
VALUES ('set_name', 't', 't', 't')
''' == data['v_data']['v_database_return']['bdr_insert_repset']

    def test_template_bdr_update_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''UPDATE bdr.bdr_replication_set_config SET
--replicate_inserts = { 't' | 'f' }
--, replicate_updates = { 't' | 'f' }
--, replicate_deletes = { 't' | 'f' }
WHERE set_name = '#set_name#'
''' == data['v_data']['v_database_return']['bdr_update_repset']

    def test_template_bdr_delete_repset(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DELETE
FROM bdr.bdr_replication_set_config
WHERE set_name = '#set_name#'
''' == data['v_data']['v_database_return']['bdr_delete_repset']

    def test_template_bdr_set_repsets(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.table_set_replication_sets('#table_name#', '{repset1,repset2,...}')" == data['v_data']['v_database_return']['bdr_set_repsets']

    def test_template_bdr_create_confhand(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE FUNCTION #table_name#_fnc_conflict_handler (
  row1 #table_name#,
  row2 #table_name#,
  table_name text,
  table_regclass regclass,
  conflict_type bdr.bdr_conflict_type, /* [insert_insert | insert_update | update_update | update_delete | delete_delete | unhandled_tx_abort] */
  OUT row_out #table_name#,
  OUT handler_action bdr.bdr_conflict_handler_action) /* [IGNORE | ROW | SKIP] */
  RETURNS record AS
$BODY$
BEGIN
  raise warning 'conflict detected for #table_name#, old_row: %, incoming_row: %', row1, row2;
  -- sample code to choose the output row or to merge values
  row_out := row1;
  handler_action := 'ROW';
END;
$BODY$
LANGUAGE plpgsql;

-- after writing the handler procedure we also need to register it as an handler
select *
from bdr.bdr_create_conflict_handler(
  ch_rel := '#table_name#',
  ch_name := '#table_name#_conflict_handler',
  ch_proc := '#table_name#_fnc_conflict_handler(#table_name#, #table_name#, text, regclass, bdr.bdr_conflict_type)',
  ch_type := 'insert_insert' /* [insert_insert | insert_update | update_update | update_delete | delete_delete | unhandled_tx_abort] */
)
''' == data['v_data']['v_database_return']['bdr_create_confhand']

    def test_template_bdr_drop_confhand(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.bdr_drop_conflict_handler('#table_name#', '#ch_name#')" == data['v_data']['v_database_return']['bdr_drop_confhand']

# only in BDR >= 1

    def test_template_bdr_terminate_apply(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.terminate_apply_workers('{#node_name#}')" == data['v_data']['v_database_return']['bdr_terminate_apply']

    def test_template_bdr_terminate_walsender(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert "select bdr.terminate_walsender_workers('{#node_name#}')" == data['v_data']['v_database_return']['bdr_terminate_walsender']

    def test_template_bdr_remove(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''select bdr.remove_bdr_from_local_node(
force := False
, convert_global_sequences := True
)
''' == data['v_data']['v_database_return']['bdr_remove']

    def test_template_xl_pause_cluster(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'PAUSE CLUSTER' == data['v_data']['v_database_return']['xl_pause_cluster']

    def test_template_xl_unpause_cluster(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'UNPAUSE CLUSTER' == data['v_data']['v_database_return']['xl_unpause_cluster']

    def test_template_xl_clean_connection(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CLEAN CONNECTION TO
--COORDINATOR ( nodename [, ... ] )
--NODE ( nodename [, ... ] )
--ALL
--ALL FORCE
--FOR DATABASE database_name
--TO USER role_name
''' == data['v_data']['v_database_return']['xl_clean_connection']

    def test_template_xl_execute_direct(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''EXECUTE DIRECT ON (#node_name#)
'SELECT ...'
''' == data['v_data']['v_database_return']['xl_execute_direct']

    def test_template_xl_pool_reload(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'EXECUTE DIRECT ON (#node_name#) \'SELECT pgxc_pool_reload()\'' == data['v_data']['v_database_return']['xl_pool_reload']

    def test_template_xl_altertable_distribution(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name# DISTRIBUTE BY
--REPLICATION
--ROUNDROBIN
--HASH ( column_name )
--MODULO ( column_name )
''' == data['v_data']['v_database_return']['xl_altertable_distribution']

    def test_template_xl_altertable_location(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER TABLE #table_name#
TO NODE ( nodename [, ... ] )
--TO GROUP ( groupname [, ... ] )
''' == data['v_data']['v_database_return']['xl_altertable_location']

    def test_template_xl_altertable_addnode(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TABLE #table_name# ADD NODE (node_name)' == data['v_data']['v_database_return']['xl_altertable_addnode']

    def test_template_xl_altertable_deletenode(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'ALTER TABLE #table_name# DELETE NODE (#node_name#)' == data['v_data']['v_database_return']['xl_altertable_deletenode']

    def test_get_tables_postgresql_nosession(self):
        response = self.cn.post('/get_tables_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_tables_postgresql_session(self):
        response = self.cs.post('/get_tables_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
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
        response = self.cn.post('/get_schemas_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_schemas_postgresql_session(self):
        response = self.cs.post('/get_schemas_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], [
            'public',
            'pg_catalog',
            'information_schema'
        ])

    def test_get_columns_postgresql_nosession(self):
        response = self.cn.post('/get_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_columns_postgresql_session(self):
        response = self.cs.post('/get_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_column_name'] for a in data['v_data']], [
            'orderid',
            'orderdate',
            'customerid',
            'netamount',
            'tax',
            'totalamount'
        ])

    def test_get_pk_postgresql_nosession(self):
        response = self.cn.post('/get_pk_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_pk_postgresql_session(self):
        response = self.cs.post('/get_pk_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['orders_pkey'])

    def test_get_pk_columns_postgresql_nosession(self):
        response = self.cn.post('/get_pk_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_pk_columns_postgresql_session(self):
        response = self.cs.post('/get_pk_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_key": "orders_pkey", "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['orderid'])

    def test_get_fks_postgresql_nosession(self):
        response = self.cn.post('/get_fks_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_fks_postgresql_session(self):
        response = self.cs.post('/get_fks_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['fk_customerid'])

    def test_get_fks_columns_postgresql_nosession(self):
        response = self.cn.post('/get_fks_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_fks_columns_postgresql_session(self):
        response = self.cs.post('/get_fks_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_fkey": "fk_customerid", "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[3] for a in data['v_data']], ['customerid'])

    def test_get_uniques_postgresql_nosession(self):
        response = self.cn.post('/get_uniques_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_uniques_postgresql_session(self):
        self.database.v_connection.Execute('alter table public.categories add constraint un_test unique (categoryname)')
        response = self.cs.post('/get_uniques_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['un_test'])
        self.database.v_connection.Execute('alter table public.categories drop constraint un_test')

    def test_get_uniques_columns_postgresql_nosession(self):
        response = self.cn.post('/get_uniques_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_uniques_columns_postgresql_session(self):
        self.database.v_connection.Execute('alter table public.categories add constraint un_test unique (categoryname)')
        response = self.cs.post('/get_uniques_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_unique": "un_test", "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['categoryname'])
        self.database.v_connection.Execute('alter table public.categories drop constraint un_test')

    def test_get_indexes_postgresql_nosession(self):
        response = self.cn.post('/get_indexes_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_indexes_postgresql_session(self):
        response = self.cs.post('/get_indexes_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['ix_order_custid', 'orders_pkey'])

    def test_get_indexes_columns_postgresql_nosession(self):
        response = self.cn.post('/get_indexes_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_indexes_columns_postgresql_session(self):
        response = self.cs.post('/get_indexes_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_index": "ix_order_custid", "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['customerid'])

    def test_get_functions_postgresql_nosession(self):
        response = self.cn.post('/get_functions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_functions_postgresql_session(self):
        response = self.cs.post('/get_functions_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['new_customer'])

    def test_get_function_fields_postgresql_nosession(self):
        response = self.cn.post('/get_function_fields_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_function_fields_postgresql_session(self):
        response = self.cs.post('/get_function_fields_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_function": "new_customer(character varying, character varying, character varying, character varying, character varying, character varying, integer, character varying, integer, character varying, character varying, integer, character varying, character varying, character varying, character varying, integer, integer, character varying)"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], [
            'firstname_in character varying',
            'lastname_in character varying',
            'address1_in character varying',
            'address2_in character varying',
            'city_in character varying',
            'state_in character varying',
            'zip_in integer',
            'country_in character varying',
            'region_in integer',
            'email_in character varying',
            'phone_in character varying',
            'creditcardtype_in integer',
            'creditcard_in character varying',
            'creditcardexpiration_in character varying',
            'username_in character varying',
            'password_in character varying',
            'age_in integer',
            'income_in integer',
            'gender_in character varying',
            'OUT customerid_out integer'
        ])

    def test_get_function_definition_postgresql_nosession(self):
        response = self.cn.post('/get_function_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_function_definition_postgresql_session(self):
        response = self.cs.post('/get_function_definition_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_function": "new_customer(character varying, character varying, character varying, character varying, character varying, character varying, integer, character varying, integer, character varying, character varying, integer, character varying, character varying, character varying, character varying, integer, integer, character varying)"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE FUNCTION public.new_customer(firstname_in character varying, lastname_in character varying, address1_in character varying, address2_in character varying, city_in character varying, state_in character varying, zip_in integer, country_in character varying, region_in integer, email_in character varying, phone_in character varying, creditcardtype_in integer, creditcard_in character varying, creditcardexpiration_in character varying, username_in character varying, password_in character varying, age_in integer, income_in integer, gender_in character varying, OUT customerid_out integer)
 RETURNS integer
 LANGUAGE plpgsql''' in data['v_data']

    def test_get_sequences_postgresql_nosession(self):
        response = self.cn.post('/get_sequences_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_sequences_postgresql_session(self):
        response = self.cs.post('/get_sequences_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_sequence_name'] for a in data['v_data']], [
            'categories_category_seq',
            'customers_customerid_seq',
            'orders_orderid_seq',
            'products_prod_id_seq'
        ])

    def test_get_views_postgresql_nosession(self):
        response = self.cn.post('/get_views_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_views_postgresql_session(self):
        self.database.v_connection.Execute('create or replace view vw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_views_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['vw_omnidb_test'])
        self.database.v_connection.Execute('drop view vw_omnidb_test')

    def test_get_views_columns_postgresql_nosession(self):
        response = self.cn.post('/get_views_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_views_columns_postgresql_session(self):
        self.database.v_connection.Execute('create or replace view vw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_views_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "vw_omnidb_test"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_column_name'] for a in data['v_data']], [
            'customerid',
            'firstname',
            'lastname',
            'totalamount'
        ])
        self.database.v_connection.Execute('drop view vw_omnidb_test')

    def test_get_view_definition_postgresql_nosession(self):
        response = self.cn.post('/get_view_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_view_definition_postgresql_session(self):
        self.database.v_connection.Execute('create or replace view vw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_view_definition_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_view": "vw_omnidb_test"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE VIEW public.vw_omnidb_test AS
 SELECT c.customerid,
    c.firstname,
    c.lastname,
    sum(o.totalamount) AS totalamount
   FROM (customers c
     JOIN orders o ON ((o.customerid = c.customerid)))
  GROUP BY c.customerid, c.firstname, c.lastname''' in data['v_data']
        self.database.v_connection.Execute('drop view vw_omnidb_test')

    def test_get_databases_postgresql_nosession(self):
        response = self.cn.post('/get_databases_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_databases_postgresql_session(self):
        response = self.cs.post('/get_databases_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.service in [a['v_name'] for a in data['v_data']]

    def test_get_tablespaces_postgresql_nosession(self):
        response = self.cn.post('/get_tablespaces_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_tablespaces_postgresql_session(self):
        response = self.cs.post('/get_tablespaces_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'pg_default' in [a['v_name'] for a in data['v_data']]

    def test_get_roles_postgresql_nosession(self):
        response = self.cn.post('/get_roles_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_roles_postgresql_session(self):
        response = self.cs.post('/get_roles_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.role in [a['v_name'] for a in data['v_data']]

    def test_get_checks_postgresql_nosession(self):
        response = self.cn.post('/get_checks_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_checks_postgresql_session(self):
        self.database.v_connection.Execute("alter table public.categories add constraint ch_test check ( position(' ' in categoryname) = 0 )")
        response = self.cs.post('/get_checks_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['ch_test'])
        self.database.v_connection.Execute('alter table public.categories drop constraint ch_test')

    def test_get_excludes_postgresql_nosession(self):
        response = self.cn.post('/get_excludes_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_excludes_postgresql_session(self):
        self.database.v_connection.Execute('alter table public.categories add constraint ex_test exclude (categoryname with = )')
        response = self.cs.post('/get_excludes_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['ex_test'])
        self.database.v_connection.Execute('alter table public.categories drop constraint ex_test')

    def test_get_rules_postgresql_nosession(self):
        response = self.cn.post('/get_rules_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_rules_postgresql_session(self):
        self.database.v_connection.Execute('create rule ru_test as on delete to public.categories do instead nothing')
        response = self.cs.post('/get_rules_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['ru_test'])
        self.database.v_connection.Execute('drop rule ru_test on public.categories')

    def test_get_rule_definition_postgresql_nosession(self):
        response = self.cn.post('/get_rule_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_rule_definition_postgresql_session(self):
        self.database.v_connection.Execute('create rule ru_test as on delete to public.categories do instead nothing')
        response = self.cs.post('/get_rule_definition_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories", "p_rule": "ru_test"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE RULE ru_test AS
    ON DELETE TO public.categories DO INSTEAD NOTHING;''' in data['v_data']
        self.database.v_connection.Execute('drop rule ru_test on public.categories')

    def test_get_triggerfunctions_postgresql_nosession(self):
        response = self.cn.post('/get_triggerfunctions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_triggerfunctions_postgresql_session(self):
        self.database.v_connection.Execute("create or replace function public.tg_ins_category() returns trigger language plpgsql as $function$begin new.categoryname := old.categoryname || ' modified'; end;$function$")
        response = self.cs.post('/get_triggerfunctions_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['tg_ins_category'])
        self.database.v_connection.Execute('drop function tg_ins_category()')

    def test_get_triggerfunction_definition_postgresql_nosession(self):
        response = self.cn.post('/get_triggerfunction_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_triggerfunction_definition_postgresql_session(self):
        self.database.v_connection.Execute("create or replace function public.tg_ins_category() returns trigger language plpgsql as $function$begin new.categoryname := old.categoryname || ' modified'; end;$function$")
        response = self.cs.post('/get_triggerfunction_definition_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_function": "public.tg_ins_category()"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE FUNCTION public.tg_ins_category()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$begin new.categoryname := old.categoryname || ' modified'; end;$function$''' in data['v_data']
        self.database.v_connection.Execute('drop function tg_ins_category()')

    def test_get_triggers_postgresql_nosession(self):
        response = self.cn.post('/get_triggers_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_triggers_postgresql_session(self):
        self.database.v_connection.Execute("create or replace function public.tg_ins_category() returns trigger language plpgsql as $function$begin new.categoryname := old.categoryname || ' modified'; end;$function$")
        self.database.v_connection.Execute('create trigger tg_ins before insert on public.categories for each statement execute procedure public.tg_ins_category()')
        response = self.cs.post('/get_triggers_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['tg_ins'])
        self.database.v_connection.Execute('drop trigger tg_ins on public.categories')
        self.database.v_connection.Execute('drop function public.tg_ins_category()')

    def test_get_inheriteds_postgresql_nosession(self):
        response = self.cn.post('/get_inheriteds_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_inheriteds_postgresql_session(self):
        self.database.v_connection.Execute('create table public.categories_p1 (check ( category < 100 )) inherits (public.categories)')
        response = self.cs.post('/get_inheriteds_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "categories"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['public.categories_p1'])
        self.database.v_connection.Execute('alter table public.categories_p1 no inherit public.categories')
        self.database.v_connection.Execute('drop table public.categories_p1')

    def test_get_mviews_postgresql_nosession(self):
        response = self.cn.post('/get_mviews_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_mviews_postgresql_session(self):
        self.database.v_connection.Execute('create materialized view public.mvw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_mviews_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['mvw_omnidb_test'])
        self.database.v_connection.Execute('drop materialized view public.mvw_omnidb_test')

    def test_get_mviews_columns_postgresql_nosession(self):
        response = self.cn.post('/get_mviews_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_mviews_columns_postgresql_session(self):
        self.database.v_connection.Execute('create materialized view public.mvw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_mviews_columns_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_table": "mvw_omnidb_test"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_column_name'] for a in data['v_data']], [
            'customerid',
            'firstname',
            'lastname',
            'totalamount'
        ])
        self.database.v_connection.Execute('drop materialized view public.mvw_omnidb_test')

    def test_get_mview_definition_postgresql_nosession(self):
        response = self.cn.post('/get_mview_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_mview_definition_postgresql_session(self):
        self.database.v_connection.Execute('create materialized view public.mvw_omnidb_test as select c.customerid, c.firstname, c.lastname, sum(o.totalamount) as totalamount from customers c inner join orders o on o.customerid = c.customerid group by c.customerid, c.firstname, c.lastname')
        response = self.cs.post('/get_mview_definition_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0, "p_schema": "public", "p_view": "mvw_omnidb_test"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP MATERIALIZED VIEW public.mvw_omnidb_test;

CREATE MATERIALIZED VIEW public.mvw_omnidb_test AS
 SELECT c.customerid,
    c.firstname,
    c.lastname,
    sum(o.totalamount) AS totalamount
   FROM (customers c
     JOIN orders o ON ((o.customerid = c.customerid)))
  GROUP BY c.customerid, c.firstname, c.lastname;
''' in data['v_data']
        self.database.v_connection.Execute('drop materialized view public.mvw_omnidb_test')

    def test_get_extensions_postgresql_nosession(self):
        response = self.cn.post('/get_extensions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_extensions_postgresql_session(self):
        response = self.cs.post('/get_extensions_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['plpgsql'])

    def test_get_physicalreplicationslots_postgresql_nosession(self):
        response = self.cn.post('/get_physicalreplicationslots_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_physicalreplicationslots_postgresql_session(self):
        self.database.v_connection.Execute("select * from pg_create_physical_replication_slot('test_slot')")
        response = self.cs.post('/get_physicalreplicationslots_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['test_slot'])
        self.database.v_connection.Execute("select pg_drop_replication_slot('test_slot')")

    def test_get_logicalreplicationslots_postgresql_nosession(self):
        response = self.cn.post('/get_logicalreplicationslots_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_logicalreplicationslots_postgresql_session(self):
        self.database.v_connection.Execute("select * from pg_create_logical_replication_slot('test_slot', 'test_decoding')")
        response = self.cs.post('/get_logicalreplicationslots_postgresql/', {'data': '{"p_database_index": 0, "p_tab_id": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['test_slot'])
        self.database.v_connection.Execute("select pg_drop_replication_slot('test_slot')")
