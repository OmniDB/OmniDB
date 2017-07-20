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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'database' == data['v_data']['v_mode']

    def test_template_create_tablespace(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE TABLESPACE name
LOCATION 'directory'
--OWNER new_owner | CURRENT_USER | SESSION_USER
--WITH ( tablespace_option = value [, ... ] )
''' == data['v_data']['v_database_return']['create_tablespace']

    def test_template_alter_tablespace(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP TABLESPACE #tablespace_name#' == data['v_data']['v_database_return']['drop_tablespace']

    def test_template_create_role(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP ROLE #role_name#' == data['v_data']['v_database_return']['drop_role']

    def test_template_create_database(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'DROP DATABASE #database_name#' == data['v_data']['v_database_return']['drop_database']

    def test_template_create_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE SCHEMA schema_name
--AUTHORIZATION [ GROUP ] user_name | CURRENT_USER | SESSION_USER
''' == data['v_data']['v_database_return']['create_schema']

    def test_template_alter_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''ALTER SCHEMA #schema_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
''' == data['v_data']['v_database_return']['alter_schema']

    def test_template_drop_schema(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SCHEMA #schema_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_schema']

    def test_template_drop_table(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP TABLE #table_name#
-- CASCADE
''' == data['v_data']['v_database_return']['drop_table']

    def test_template_create_sequence(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP SEQUENCE #sequence_name#
-- CASCADE
''' == data['v_data']['v_database_return']['drop_sequence']

    def test_template_create_function(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP FUNCTION #function_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_function']

    def test_template_create_view(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''CREATE OR REPLACE VIEW #schema_name#.name AS
SELECT ...
''' == data['v_data']['v_database_return']['create_view']

    def test_template_drop_view(self):
        response = self.cs.post('/get_tree_info_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert '''DROP VIEW #view_name#
--CASCADE
''' == data['v_data']['v_database_return']['drop_view']

    def test_get_tables_postgresql_nosession(self):
        response = self.cn.post('/get_tables_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_tables_postgresql_session(self):
        response = self.cs.post('/get_tables_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public"}'})
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
        response = self.cs.post('/get_schemas_postgresql/', {'data': '{"p_database_index": 0}'})
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
        response = self.cs.post('/get_columns_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "orders"}'})
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
        response = self.cs.post('/get_pk_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['orders_pkey'])

    def test_get_fks_postgresql_nosession(self):
        response = self.cn.post('/get_fks_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_fks_postgresql_session(self):
        response = self.cs.post('/get_fks_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['fk_customerid'])

    def test_get_uniques_postgresql_nosession(self):
        response = self.cn.post('/get_uniques_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_uniques_postgresql_session(self):
        response = self.cs.post('/get_uniques_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], [])

    def test_get_indexes_postgresql_nosession(self):
        response = self.cn.post('/get_indexes_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_indexes_postgresql_session(self):
        response = self.cs.post('/get_indexes_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "orders"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a[0] for a in data['v_data']], ['ix_order_custid', 'orders_pkey'])

    def test_get_functions_postgresql_nosession(self):
        response = self.cn.post('/get_functions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_functions_postgresql_session(self):
        response = self.cs.post('/get_functions_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], ['new_customer'])

    def test_get_function_fields_postgresql_nosession(self):
        response = self.cn.post('/get_function_fields_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_function_fields_postgresql_session(self):
        response = self.cs.post('/get_function_fields_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_function": "new_customer(character varying, character varying, character varying, character varying, character varying, character varying, integer, character varying, integer, character varying, character varying, integer, character varying, character varying, character varying, character varying, integer, integer, character varying)"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal([a['v_name'] for a in data['v_data']], [
            'address1_in character varying',
            'address2_in character varying',
            'age_in integer',
            'city_in character varying',
            'country_in character varying',
            'creditcardexpiration_in character varying',
            'creditcard_in character varying',
            'creditcardtype_in integer',
            'email_in character varying',
            'firstname_in character varying',
            'gender_in character varying',
            'income_in integer',
            'lastname_in character varying',
            'OUT customerid_out integer',
            'password_in character varying',
            'phone_in character varying',
            'region_in integer',
            'state_in character varying',
            'username_in character varying',
            'zip_in integer'
        ])

    def test_get_function_definition_postgresql_nosession(self):
        response = self.cn.post('/get_function_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_function_definition_postgresql_session(self):
        response = self.cs.post('/get_function_definition_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_function": "new_customer(character varying, character varying, character varying, character varying, character varying, character varying, integer, character varying, integer, character varying, character varying, integer, character varying, character varying, character varying, character varying, integer, integer, character varying)"}'})
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
        response = self.cs.post('/get_sequences_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.lists_equal(data['v_data'], [
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
        response = self.cs.post('/get_views_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public"}'})
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
        response = self.cs.post('/get_views_columns_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_table": "vw_omnidb_test"}'})
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
        response = self.cs.post('/get_view_definition_postgresql/', {'data': '{"p_database_index": 0, "p_schema": "public", "p_view": "vw_omnidb_test"}'})
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
        response = self.cs.post('/get_databases_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.service in [a['v_name'] for a in data['v_data']]

    def test_get_tablespaces_postgresql_nosession(self):
        response = self.cn.post('/get_tablespaces_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_tablespaces_postgresql_session(self):
        response = self.cs.post('/get_tablespaces_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 'pg_default' in [a['v_name'] for a in data['v_data']]

    def test_get_roles_postgresql_nosession(self):
        response = self.cn.post('/get_roles_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_roles_postgresql_session(self):
        response = self.cs.post('/get_roles_postgresql/', {'data': '{"p_database_index": 0}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert self.role in [a['v_name'] for a in data['v_data']]
