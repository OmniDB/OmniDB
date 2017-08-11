'''
The MIT License (MIT)

Copyright (c) 2014-2017 The OmniDB Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os.path
import re
from collections import OrderedDict
from enum import Enum
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils

'''
------------------------------------------------------------------------
Template
------------------------------------------------------------------------
'''
class TemplateType(Enum):
    EXECUTE = 1
    SCRIPT = 2

class Template:
    def __init__(self, p_text, p_type=TemplateType.EXECUTE):
        self.v_text = p_text
        self.v_type = p_type

'''
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
'''
class Generic(object):
    @staticmethod
    def InstantiateDatabase(p_db_type,
                            p_server,
                            p_port,
                            p_service,
                            p_user,
                            p_password,
                            p_conn_id=0,
                            p_alias='',
                            p_foreignkeys=True):

        if p_db_type == 'postgresql':
            return PostgreSQL(p_server, p_port, p_service, p_user, p_password, p_conn_id, p_alias)
        if p_db_type == 'sqlite':
            return SQLite(p_service, p_conn_id, p_alias, p_foreignkeys)

'''
------------------------------------------------------------------------
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_conn_id=0, p_alias=''):
        self.v_alias = p_alias
        self.v_db_type = 'postgresql'
        self.v_conn_id = p_conn_id
        self.v_server = p_server
        self.v_port = p_port
        self.v_service = p_service
        self.v_user = p_user
        self.v_schema = 'public'
        self.v_connection = Spartacus.Database.PostgreSQL(p_server, p_port, p_service, p_user, p_password)

        self.v_has_schema = True
        self.v_has_functions = True
        self.v_has_procedures = False
        self.v_has_sequences = True
        self.v_has_primary_keys = True
        self.v_has_foreign_keys = True
        self.v_has_uniques = True
        self.v_has_indexes = True
        self.v_has_checks = True
        self.v_has_rules = True
        self.v_has_triggers = True
        self.v_has_triggers = True

        self.v_has_update_rule = True
        self.v_can_rename_table = True
        self.v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#"
        self.v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)"
        self.v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#"
        self.v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)"
        self.v_can_alter_type = True
        self.v_alter_type_command = "alter table #p_table_name# alter #p_column_name# type #p_new_data_type#"
        self.v_can_alter_nullable = True
        self.v_set_nullable_command = "alter table #p_table_name# alter #p_column_name# drop not null"
        self.v_drop_nullable_command = "alter table #p_table_name# alter #p_column_name# set not null"
        self.v_can_rename_column = True
        self.v_rename_column_command = "alter table #p_table_name# rename #p_column_name# to #p_new_column_name#"
        self.v_can_add_column = True
        self.v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#"
        self.v_can_drop_column = True
        self.v_drop_column_command = "alter table #p_table_name# drop #p_column_name#"
        self.v_can_add_constraint = True
        self.v_add_pk_command = "alter table #p_table_name# add constraint #p_constraint_name# primary key (#p_columns#)"
        self.v_add_fk_command = "alter table #p_table_name# add constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#"
        self.v_add_unique_command = "alter table #p_table_name# add constraint #p_constraint_name# unique (#p_columns#)"
        self.v_can_drop_constraint = True
        self.v_drop_pk_command = "alter table #p_table_name# drop constraint #p_constraint_name#"
        self.v_drop_fk_command = "alter table #p_table_name# drop constraint #p_constraint_name#"
        self.v_drop_unique_command = "alter table #p_table_name# drop constraint #p_constraint_name#"
        self.v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
        self.v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)"
        self.v_drop_index_command = "drop index #p_schema_name#.#p_index_name#"
        self.v_update_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]
        self.v_delete_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]

    def GetName(self):
        return self.v_service

    def GetVersion(self):
        return 'PostgreSQL ' + self.v_connection.ExecuteScalar('show server_version')

    def PrintDatabaseInfo(self):
        return self.v_user + "@" + self.v_service

    def PrintDatabaseDetails(self):
        return self.v_server + ":" + self.v_port

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):
        v_rules = ''
        if p_update_rule.strip() != "":
            v_rules += " on update " + p_update_rule + " "
        if p_delete_rule.strip() != "":
            v_rules += " on delete " + p_delete_rule + " "
        return v_rules

    def TestConnection(self):
        v_return = ''
        try:
            self.v_connection.Open()
            v_schema = self.QuerySchemas()
            if len(v_schema.Rows) > 0:
                v_return = 'Connection successful.'
            self.v_connection.Close()
        except Exception as exc:
            v_return = str(exc)
        return v_return

    def QueryRoles(self):
        return self.v_connection.Query('''
            select rolname as role_name
            from pg_roles
            order by rolname
        ''', True)

    def QueryTablespaces(self):
        return self.v_connection.Query('''
            select spcname as tablespace_name
            from pg_tablespace
            order by spcname
        ''', True)

    def QueryDatabases(self):
        return self.v_connection.Query('''
            select database_name
            from (
            select datname as database_name,
                   1 as sort
            from pg_database
            where datname = 'postgres'
            union all
            select database_name,
                   1 + row_number() over() as sort
            from (
            select datname as database_name
            from pg_database
            where not datistemplate
              and datname <> 'postgres'
            order by datname asc
            ) x
            ) y
            order by sort
        ''', True)

    def QueryExtensions(self):
        return self.v_connection.Query('''
            select extname as extension_name
            from pg_extension
            order by extname
        ''', True)

    def QuerySchemas(self):
        return self.v_connection.Query('''
            select schema_name
            from (
            select schema_name,
                   row_number() over() as sort
            from (
            select nspname as schema_name
            from pg_catalog.pg_namespace
            where nspname in ('public', 'pg_catalog', 'information_schema')
            order by nspname desc
            ) x
            union all
            select schema_name,
                   3 + row_number() over() as sort
            from (
            select nspname as schema_name
            from pg_catalog.pg_namespace
            where nspname not in ('public', 'pg_catalog', 'information_schema', 'pg_toast')
              and nspname not like 'pg%%temp%%'
            order by nspname desc
            ) x
            ) y
            order by sort
        ''', True)

    def QueryTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and lower(table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = "and lower(table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select table_name as table_name,
                   table_schema as table_schema
            from information_schema.tables
            where table_type = 'BASE TABLE'
            {0}
            order by table_schema,
                     table_name
        '''.format(v_filter), True)

    def QueryTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(t.table_schema) = '{0}' and lower(c.table_name) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(t.table_schema) = '{0}' and lower(c.table_name) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(t.table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(t.table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(t.table_schema) not in ('information_schema','pg_catalog') and lower(c.table_name) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(t.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select c.table_name as table_name,
                   c.column_name as column_name,
                   c.data_type as data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale
            from information_schema.columns c
            join information_schema.tables t on (c.table_name = t.table_name and c.table_schema = t.table_schema)
            where t.table_type = 'BASE TABLE'
            {0}
            order by c.table_name, c.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesForeignKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(rc.constraint_schema) = '{0}' and lower(kcu1.table_name) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(rc.constraint_schema) = '{0}' and lower(kcu1.table_name) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(rc.constraint_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(rc.constraint_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(rc.constraint_schema) not in ('information_schema','pg_catalog') and lower(kcu1.table_name) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(rc.constraint_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select *
            from (select distinct
                         kcu1.constraint_name as constraint_name,
                         kcu1.table_name as table_name,
                         kcu1.column_name as column_name,
                         kcu2.constraint_name as r_constraint_name,
                         kcu2.table_name as r_table_name,
                         kcu2.column_name as r_column_name,
                         kcu1.constraint_schema as table_schema,
                         kcu2.constraint_schema as r_table_schema,
                         kcu1.ordinal_position,
                         rc.update_rule as update_rule,
                         rc.delete_rule as delete_rule
            from information_schema.referential_constraints rc
            join information_schema.key_column_usage kcu1
            on kcu1.constraint_catalog = rc.constraint_catalog
            and kcu1.constraint_schema = rc.constraint_schema
            and kcu1.constraint_name = rc.constraint_name
            join information_schema.key_column_usage kcu2
            on kcu2.constraint_catalog = rc.unique_constraint_catalog
            and kcu2.constraint_schema = rc.unique_constraint_schema
            and kcu2.constraint_name = rc.unique_constraint_name
            and kcu2.ordinal_position = kcu1.ordinal_position
            where 1 = 1
            {0}
            ) t
            order by constraint_name,
                     table_name,
                     ordinal_position
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(tc.table_schema) = '{0}' and lower(tc.table_name) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(tc.table_schema) = '{0}' and lower(tc.table_name) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(tc.table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(tc.table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(tc.table_schema) not in ('information_schema','pg_catalog') and lower(tc.table_name) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(tc.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select tc.constraint_name as constraint_name,
                   kc.column_name as column_name,
                   tc.table_name as table_name,
                   tc.table_schema as table_schema
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'PRIMARY KEY'
            {0}
            order by tc.constraint_name,
                     tc.table_name,
                     kc.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesUniques(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(tc.table_schema) = '{0}' and lower(tc.table_name) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(tc.table_schema) = '{0}' and lower(tc.table_name) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(tc.table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(tc.table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(tc.table_schema) not in ('information_schema','pg_catalog') and lower(tc.table_name) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(tc.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select tc.constraint_name as constraint_name,
                   kc.column_name as column_name,
                   tc.table_name as table_name,
                   tc.table_schema as table_schema
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'UNIQUE'
            {0}
            order by tc.constraint_name,
                     tc.table_name,
                     kc.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesIndexes(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(t.schemaname) = '{0}' and lower(t.tablename) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(t.schemaname) = '{0}' and lower(t.tablename) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(t.schemaname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(t.schemaname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(t.schemaname) not in ('information_schema','pg_catalog') and lower(t.tablename) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(t.schemaname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select t.tablename as table_name,
                   t.indexname as index_name,
                   unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as column_name,
                   (case when strpos(t.indexdef, 'UNIQUE') > 0 then 'Unique' else 'Non Unique' end) as uniqueness,
                   t.schemaname as schema_name
            from pg_indexes t
            where 1 = 1
            {0}
            order by t.tablename,
                     t.indexname
        '''.format(v_filter), True)

    def QueryTablesChecks(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(n.nspname) = '{0}' and ltrim(lower(c.conrelid::regclass), lower(n.nspname) || '.') = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(n.nspname) = '{0}' and ltrim(lower(c.conrelid::regclass), lower(n.nspname) || '.') = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') and ltrim(lower(c.conrelid::regclass), lower(n.nspname) || '.') = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select n.nspname as schema_name,
                   ltrim(c.conrelid::regclass, n.nspname || '.') as table_name,
                   conname as constraint_name,
                   consrc as constraint_source
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where 1 = 1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def QueryTablesPartitions(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(np.nspname) = '{0}' and lower(cp.relname) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(np.nspname) = '{0}' and lower(cp.relname) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(np.nspname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(np.nspname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(np.nspname) not in ('information_schema','pg_catalog') and lower(cp.relname) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(np.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select np.nspname as parent_schema,
                   cp.relname as parent_table,
                   nc.nspname as child_schema,
                   cc.relname as child_table
            from pg_inherits i
            inner join pg_class cp on cp.oid = i.inhparent
            inner join pg_namespace np on np.oid = cp.relnamespace
            inner join pg_class cc on cc.oid = i.inhrelid
            inner join pg_namespace nc on nc.oid = cc.relnamespace
            where 1 = 1
            {0}
            order by 1, 2, 3, 4
        '''.format(v_filter))

    def QueryDataLimited(self, p_query, p_count=-1):
        if p_count != -1:
            self.v_connection.Open()
            v_data = self.v_connection.QueryBlock(p_query, p_count, True)
            self.v_connection.Close()
            return v_data
        else:
            return self.v_connection.Query(p_query, True)

    def QueryTableRecords(self, p_column_list, p_table, p_filter, p_count=-1):
        v_limit = ''
        if p_count != -1:
            v_limit = ' limit ' + p_count
        return self.v_connection.Query('''
            select {0}
            from {1} t
            {2}
            {3}
        '''.format(
                p_column_list,
                p_table,
                p_filter,
                v_limit
            ), True
        )

    def QueryFunctions(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   p.proname as name,
                   n.nspname as schema_name
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where format_type(p.prorettype, null) <> 'trigger'
            {0}
            order by 1
        '''.format(v_filter), True)

    def QueryFunctionFields(self, p_function, p_schema):
        if p_schema:
            return self.v_connection.Query('''
                select y.type::character varying as type,
                       y.name
                from (
                    select 'O' as type,
                           'return ' || format_type(p.prorettype, null) as name
                    from pg_proc p,
                         pg_namespace n
                    where p.pronamespace = n.oid
                      and n.nspname = '{0}'
                      and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
                ) y
                union all
                select x.type::character varying as type,
                       trim(x.name) as name
                from (
                    select 'I' as type,
                    unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 1 desc, 2 asc
            '''.format(p_schema, p_function), True)
        else:
            return self.v_connection.Query('''
                select y.type::character varying as type,
                       y.name
                from (
                    select 'O' as type,
                           'return ' || format_type(p.prorettype, null) as name
                    from pg_proc p,
                         pg_namespace n
                    where p.pronamespace = n.oid
                      and n.nspname = '{0}'
                      and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
                ) y
                union all
                select x.type::character varying as type,
                       trim(x.name) as name
                from (
                    select 'I' as type,
                    unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 1 desc, 2 asc
            '''.format(self.v_schema.lower(), p_function), True)

    def GetFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    def QueryTriggerFunctions(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   p.proname as name,
                   n.nspname as schema_name
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where format_type(p.prorettype, null) = 'trigger'
            {0}
            order by 1
        '''.format(v_filter), True)

    def GetTriggerFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    def QuerySequences(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and lower(sequence_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(sequence_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = "and lower(sequence_schema) not in ('information_schema','pg_catalog') "
        v_table = self.v_connection.Query('''
            select sequence_name as sequence_name,
                   minimum_value,
                   maximum_value,
                   0 as current_value,
                   increment,
                   sequence_schema as sequence_schema
            from information_schema.sequences
            where 1 = 1
            {0}
            order by 1
        '''.format(v_filter), True)
        for i in range(0, len(v_table.Rows)):
            v_table.Rows[i]['current_value'] = self.v_connection.ExecuteScalar(
                "select last_value from {0}.{1}".format(v_table.Rows[i]['sequence_schema'], v_table.Rows[i]['sequence_name'])
            )
        return v_table

    def QueryViews(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and lower(table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = "and lower(table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select table_name as table_name,
                   table_schema as table_schema
            from information_schema.views
            where 1 = 1
            {0}
            order by table_schema, table_name
        '''.format(v_filter), True)

    def QueryViewFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(t.table_schema) = '{0}' and lower(c.table_name) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(t.table_schema) = '{0}' and lower(c.table_name) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(t.table_schema) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(t.table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(t.table_schema) not in ('information_schema','pg_catalog') and lower(c.table_name) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(t.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select c.table_name as table_name,
                   c.column_name as column_name,
                   c.data_type as data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale
            from information_schema.columns c
            join information_schema.views t on (c.table_name = t.table_name and c.table_schema = t.table_schema)
            where 1 = 1
            {0}
            order by c.table_name, c.ordinal_position
        '''.format(v_filter), True)

    def GetViewDefinition(self, p_view, p_schema):
        return '''CREATE OR REPLACE VIEW {0}.{1} AS
{2}
'''.format(p_schema, p_view,
        self.v_connection.ExecuteScalar('''
                select view_definition
                from information_schema.views
                where table_schema = '{0}'
                  and table_name = '{1}'
            '''.format(p_schema, p_view)
    ))

    def QueryRules(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(schema_name) = '{0}' and lower(tablename) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(schema_name) = '{0}' and lower(tablename) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(schema_name) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(schema_name) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(schema_name) not in ('information_schema','pg_catalog') and lower(tablename) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(schema_name) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select schema_name as table_schema,
                   tablename as table_name,
                   rulename as rule_name
            from pg_rules
            where 1 = 1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def GetRuleDefinition(self, p_rule, p_table, p_schema):
        return self.v_connection.ExecuteScalar('''
            select definition
            from pg_rules
            where table_schema = '{0}'
              and table_name = '{1}'
              and rulename = '{2}'
        '''.format(p_schema, p_table, p_rule))

    def QueryTriggers(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and lower(n.nspname) = '{0}' and lower(c.relname) = '{1}' ".format(str.lower(p_schema), str.lower(p_table))
            elif p_table:
                v_filter = "and lower(n.nspname) = '{0}' and lower(c.relname) = '{1}' ".format(str.lower(self.v_schema), str.lower(p_table))
            elif p_schema:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(p_schema))
            else:
                v_filter = "and lower(n.nspname) = '{0}' ".format(str.lower(self.v_schema))
        else:
            if p_table:
                v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') and lower(c.relname) = {0}".format(str.lower(p_table))
            else:
                v_filter = "and lower(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select n.nspname as schema_name,
                   c.relname as table_name,
                   t.tgname as trigger_name,
                   t.tgenabled as trigger_enabled,
                   np.nspname || '.' || p.proname as trigger_funtion_name,
                   np.nspname || '.' || p.proname || '()' as trigger_function_id
            from pg_trigger t
            inner join pg_class c
            on c.oid = t.tgrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_proc p
            on p.oid = t.tgfoid
            inner join pg_namespace np
            on np.oid = p.pronamespace
            where not t.tgisinternal
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def GetTriggerDefinition(self, p_trigger, p_table, p_schema):
        return self.v_connection.ExecuteScalar('''
            select 'CREATE TRIGGER ' || x.trigger_name || chr(10) ||
                   '  ' || x.action_timing || ' ' || x.event_manipulation || chr(10) ||
                   '  ON {0}.{1}' || chr(10) ||
                   '  FOR EACH ' || x.action_orientation || chr(10) ||
                   (case when length(coalesce(x.action_condition, '')) > 0 then '  WHEN ( ' || x.action_condition || ') ' || chr(10) else '' end) ||
                   '  ' || x.action_statement as definition
            from (
            select distinct t.trigger_name,
                   t.action_timing,
                   e.event as event_manipulation,
                   t.action_orientation,
                   t.action_condition,
                   t.action_statement
            from information_schema.triggers t
            inner join (
            select array_to_string(array(
            select event_manipulation::text
            from information_schema.triggers
            where event_object_schema = '{0}'
              and event_object_table = '{1}'
              and trigger_name = '{2}'
            ), ' OR ') as event
            ) e
            on 1 = 1
            where t.event_object_schema = '{0}'
              and t.event_object_table = '{1}'
              and t.trigger_name = '{2}'
            ) x
        ''''.format(p_schema, p_table, p_trigger))

    def TemplateCreateRole(self):
        return Template('''CREATE ROLE name
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
''')

    def TemplateAlterRole(self):
        return Template('''ALTER ROLE #role_name#
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
''')

    def TemplateDropRole(self):
        return Template('DROP ROLE #role_name#')

    def TemplateCreateTablespace(self):
        return Template('''CREATE TABLESPACE name
LOCATION 'directory'
--OWNER new_owner | CURRENT_USER | SESSION_USER
--WITH ( tablespace_option = value [, ... ] )
''')

    def TemplateAlterTablespace(self):
        return Template('''ALTER TABLESPACE #tablespace_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET seq_page_cost = value
--RESET seq_page_cost
--SET random_page_cost = value
--RESET random_page_cost
--SET effective_io_concurrency = value
--RESET effective_io_concurrency
''')

    def TemplateDropTablespace(self):
        return Template('DROP TABLESPACE #tablespace_name#')

    def TemplateCreateDatabase(self):
        return Template('''CREATE DATABASE name
--OWNER user_name
--TEMPLATE template
--ENCODING encoding
--LC_COLLATE lc_collate
--LC_CTYPE lc_ctype
--TABLESPACE tablespace
--CONNECTION LIMIT connlimit
''')

    def TemplateAlterDatabase(self):
        return Template('''ALTER DATABASE #database_name#
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
''')

    def TemplateDropDatabase(self):
        return Template('DROP DATABASE #database_name#')

    def TemplateCreateExtension(self):
        return Template('''CREATE EXTENSION name
--SCHEMA schema_name
--VERSION VERSION
--FROM old_version
''')

    def TemplateAlterExtension(self):
        return Template('''ALTER EXTENSION extension_name
--UPDATE [ TO new_version ]
--SET SCHEMA new_schema
--ADD member_object
--DROP member_object
''')

    def TemplateDropExtension(self):
        return Template('''DROP EXTENSION #extension_name#
--CASCADE
''')

    def TemplateCreateSchema(self):
        return Template('''CREATE SCHEMA schema_name
--AUTHORIZATION [ GROUP ] user_name | CURRENT_USER | SESSION_USER
''')

    def TemplateAlterSchema(self):
        return Template('''ALTER SCHEMA #schema_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
''')

    def TemplateDropSchema(self):
        return Template('''DROP SCHEMA #schema_name#
--CASCADE
''')

    def TemplateCreateSequence(self):
        return Template('''CREATE SEQUENCE #schema_name#.name
--INCREMENT BY increment
--MINVALUE minvalue | NO MINVALUE
--MAXVALUE maxvalue | NO MAXVALUE
--START WITH start
--CACHE cache
--CYCLE
--OWNED BY { table_name.column_name | NONE }
''')

    def TemplateAlterSequence(self):
        return Template('''ALTER SEQUENCE #sequence_name#
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
''')

    def TemplateDropSequence(self):
        return Template('''DROP SEQUENCE #sequence_name#
-- CASCADE
''')

    def TemplateCreateFunction(self):
        return Template('''CREATE OR REPLACE FUNCTION #schema_name#.name
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
''')

    def TemplateDropFunction(self):
        return Template('''DROP FUNCTION #function_name#
--CASCADE
''')

    def TemplateCreateTriggerFunction(self):
        return Template('''CREATE OR REPLACE FUNCTION #schema_name#.name()
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
''')

    def TemplateDropTriggerFunction(self):
        return Template('''DROP FUNCTION #function_name#
--CASCADE
''')

    def TemplateCreateView(self):
        return Template('''CREATE OR REPLACE VIEW #schema_name#.name AS
SELECT ...
''')

    def TemplateDropView(self):
        return Template('''DROP VIEW #view_name#
--CASCADE
''')

    def TemplateCreateTable(self):
        pass

    def TemplateAlterTable(self):
        pass

    def TemplateDropTable(self):
        return Template('''DROP TABLE #table_name#
--CASCADE
''')

    def TemplateCreatePrimaryKey(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
PRIMARY KEY ( column_name [, ... ] )
--WITH ( storage_parameter [= value] [, ... ] )
--WITH OIDS
--WITHOUT OIDS
--USING INDEX TABLESPACE tablespace_name
''')

    def TemplateDropPrimaryKey(self):
        return Template('''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''')

    def TemplateCreateForeignKey(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
FOREIGN KEY ( column_name [, ... ] )
REFERENCES reftable [ ( refcolumn [, ... ] ) ]
--MATCH { FULL | PARTIAL | SIMPLE }
--ON DELETE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT }
--ON UPDATE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT }
--NOT VALID
''')

    def TemplateDropForeignKey(self):
        return Template('''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''')

    def TemplateCreateIndex(self):
        return Template('''CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] name
ON #table_name#
--USING method
( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
--WITH ( storage_parameter = value [, ... ] )
--WHERE predicate
''')

    def TemplateAlterIndex(self):
        return Template('''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''')

    def TemplateDropIndex(self):
        return Template('''DROP INDEX [ CONCURRENTLY ] #index_name#
--CASCADE
''')

    def TemplateCreateCheck(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
CHECK ( expression )
''')

    def TemplateDropCheck(self):
        return Template('''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''')

    def TemplateCreateRule(self):
        return Template('''CREATE OR REPLACE name
AS ON { SELECT | INSERT | UPDATE | DELETE }
TO #table_name#
--WHERE condition
--DO ALSO { NOTHING | command | ( command ; command ... ) }
--DO INSTEAD { NOTHING | command | ( command ; command ... ) }
''')

    def TemplateAlterRule(self):
        return Template('ALTER RULE #rule_name# ON #table_name# RENAME TO new_name')

    def TemplateDropRule(self):
        return Template('''DROP RULE #rule_name# ON #table_name#
--CASCADE
''')

    def TemplateCreateTrigger(self):
        return Template('''CREATE TRIGGER name
--BEFORE { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE [ OR ] | TRUNCATE }
--AFTER { INSERT [ OR ] | UPDATE [ OF column_name [, ... ] ] [ OR ] | DELETE [ OR ] | TRUNCATE }
ON #table_name#
--FROM referenced_table_name
--NOT DEFERRABLE | [ DEFERRABLE ] { INITIALLY IMMEDIATE | INITIALLY DEFERRED }
--FOR EACH ROW
--FOR EACH STATEMENT
--WHEN ( condition )
--EXECUTE PROCEDURE function_name ( arguments )
''')

    def TemplateAlterTrigger(self):
        return Template('ALTER TRIGGER #trigger_name# ON #table_name# RENAME TO new_name')

    def TemplateEnableTrigger(self):
        return Template('ALTER TABLE #table_name# ENABLE TRIGGER #trigger_name#')

    def TemplateDisableTrigger(self):
        return Template('ALTER TABLE #table_name# DISABLE TRIGGER #trigger_name#')

    def TemplateDropTrigger(self):
        return Template('''DROP RULE #trigger_name# ON #table_name#
--CASCADE
''')

    def TemplateCreatePartition(self):
        return Template('''CREATE TABLE name (
    CHECK ( condition )
) INHERITS #table_name#
''')

    def TemplateNoInheritPartition(self):
        return Template('ALTER TABLE #partition_name# NO INHERIT #table_name#')

    def TemplateDropPartition(self):
        return Template('DROP TABLE #partition_name#')

'''
------------------------------------------------------------------------
SQLite
------------------------------------------------------------------------
'''
class SQLite:
    def __init__(self, p_service, p_conn_id=0, p_alias='', p_foreignkeys=True):
        self.v_alias = p_alias
        self.v_db_type = 'sqlite'
        self.v_conn_id = p_conn_id
        self.v_server = ''
        self.v_port = ''
        self.v_service = p_service
        self.v_user = ''
        self.v_schema = ''
        self.v_connection = Spartacus.Database.SQLite(p_service, p_foreignkeys)

        self.v_has_schema = False
        self.v_has_functions = False
        self.v_has_procedures = False
        self.v_has_sequences = False
        self.v_has_primary_keys = True
        self.v_has_foreign_keys = True
        self.v_has_uniques = True
        self.v_has_indexes = True
        self.v_has_checks = True
        self.v_has_rules = True
        self.v_has_triggers = True
        self.v_has_triggers = True

        self.v_has_update_rule = True
        self.v_can_rename_table = True
        self.v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#"
        self.v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)"
        self.v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#"
        self.v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)"
        self.v_can_alter_type = False
        self.v_can_alter_nullable = False
        self.v_can_rename_column = False
        self.v_can_add_column = True
        self.v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#"
        self.v_can_drop_column = False
        self.v_can_add_constraint = False
        self.v_can_drop_constraint = False
        self.v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
        self.v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)"
        self.v_drop_index_command = "drop index #p_index_name#"
        self.v_update_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]
        self.v_delete_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]

    def GetName(self):
        return self.v_service

    def PrintDatabaseInfo(self):
        if '/' in self.v_service:
            v_strings = self.v_service.split('/')
            return v_strings[len(v_strings)-1]
        else:
            return self.v_service

    def PrintDatabaseDetails(self):
        return 'Local File'

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):
        v_rules = ''
        if p_update_rule.strip() != "":
            v_rules += " on update " + p_update_rule + " "
        if p_delete_rule.strip() != "":
            v_rules += " on delete " + p_delete_rule + " "
        return v_rules

    def TestConnection(self):
        v_return = ''
        try:
            if os.path.isfile(self.v_service):
                v_return = 'Connection successful.'
            else:
                v_return = 'File does not exist, if you try to manage this connection a database file will be created.'
        except Exception as exc:
            v_return = str(exc)
        return v_return

    def QueryTables(self):
        return self.v_connection.Query('''
            select name as table_name
		    from sqlite_master
			where type = 'table'
        ''', True)

    def QueryTablesFields(self, p_table=None):
        v_table_columns_all = Spartacus.Database.DataTable()
        v_table_columns_all.Columns = [
            'column_name',
            'data_type',
            'nullable',
            'data_length',
            'data_precision',
            'data_scale',
            'table_name'
        ]
        if p_table:
            v_tables = Spartacus.Database.DataTable()
            v_tables.Columns.append('table_name')
            v_tables.Rows.append(OrderedDict(zip(v_tables.Columns, [p_table])))
        else:
            v_tables = self.QueryTables()
        for v_table in v_tables.Rows:
            v_table_columns_tmp = self.v_connection.Query("pragma table_info('{0}')".format(v_table['table_name']), True)
            v_table_columns = Spartacus.Database.DataTable()
            v_table_columns.Columns = [
                'column_name',
                'data_type',
                'nullable',
                'data_length',
                'data_precision',
                'data_scale',
                'table_name'
            ]
            for r in v_table_columns_tmp.Rows:
                v_row = []
                v_row.append(r['name'])
                if '(' in r['type']:
                    v_index = r['type'].find('(')
                    v_data_type = r['type'].lower()[0 : v_index]
                    if ',' in r['type']:
                        v_sizes = r['type'][v_index + 1 : r['type'].find(')')].split(',')
                        v_data_length = ''
                        v_data_precision = v_sizes[0]
                        v_data_scale = v_sizes[1]
                    else:
                        v_data_length = r['type'][v_index + 1 : r['type'].find(')')]
                        v_data_precision = ''
                        v_data_scale = ''
                else:
                    v_data_type = r['type'].lower()
                    v_data_length = ''
                    v_data_precision = ''
                    v_data_scale = ''
                v_row.append(v_data_type)
                if r['notnull'] == '1':
                    v_row.append('NO')
                else:
                    v_row.append('YES')
                v_row.append(v_data_length)
                v_row.append(v_data_precision)
                v_row.append(v_data_scale)
                v_row.append(v_table['table_name'])
                v_table_columns.Rows.append(OrderedDict(zip(v_table_columns.Columns, v_row)))
            v_table_columns_all.Merge(v_table_columns)
        return v_table_columns_all

    def QueryTablesForeignKeys(self, p_table=None):
        v_fks_all = Spartacus.Database.DataTable()
        v_fks_all.Columns = [
            'r_table_name',
            'table_name',
            'r_column_name',
            'column_name',
            'constraint_name',
            'update_rule',
            'delete_rule',
            'table_schema',
            'r_table_schema'
        ]
        if p_table:
            v_tables = Spartacus.Database.DataTable()
            v_tables.Columns.append('table_name')
            v_tables.Rows.append(OrderedDict(zip(v_tables.Columns, [p_table])))
        else:
            v_tables = self.QueryTables()
        for v_table in v_tables.Rows:
            v_fks_tmp = self.v_connection.Query("pragma foreign_key_list('{0}')".format(v_table['table_name']), True)
            v_fks = Spartacus.Database.DataTable()
            v_fks.Columns = [
                'r_table_name',
                'table_name',
                'r_column_name',
                'column_name',
                'constraint_name',
                'update_rule',
                'delete_rule',
                'table_schema',
                'r_table_schema'
            ]
            for r in v_fks_tmp.Rows:
                v_row = []
                v_row.append(r['table'])
                v_row.append(v_table['table_name'])
                v_row.append(r['to'])
                v_row.append(r['from'])
                v_row.append(v_table['table_name'] + '_fk_' + str(r['id']))
                v_row.append(r['on_update'])
                v_row.append(r['on_delete'])
                v_row.append('')
                v_row.append('')
                v_fks.Rows.append(OrderedDict(zip(v_fks.Columns, v_row)))
            v_fks_all.Merge(v_fks)
        return v_fks_all

    def QueryTablesPrimaryKeys(self, p_table=None):
        v_pks_all = Spartacus.Database.DataTable()
        v_pks_all.Columns = [
            'constraint_name',
            'column_name',
            'table_name'
        ]
        if p_table:
            v_tables = Spartacus.Database.DataTable()
            v_tables.Columns.append('table_name')
            v_tables.Rows.append(OrderedDict(zip(v_tables.Columns, [p_table])))
        else:
            v_tables = self.QueryTables()
        for v_table in v_tables.Rows:
            v_pks_tmp = self.v_connection.Query("pragma table_info('{0}')".format(v_table['table_name']), True)
            v_pks = Spartacus.Database.DataTable()
            v_pks.Columns = [
                'constraint_name',
                'column_name',
                'table_name'
            ]
            for r in v_pks_tmp.Rows:
                if r['pk'] != 0:
                    v_row = []
                    v_row.append('pk_' + v_table['table_name'])
                    v_row.append(r['name'])
                    v_row.append(v_table['table_name'])
                    v_pks.Rows.append(OrderedDict(zip(v_pks.Columns, v_row)))
            v_pks_all.Merge(v_pks)
        return v_pks_all

    # DOING
    def QueryTablesUniques(self, p_table=None):
        v_uniques_all = Spartacus.Database.DataTable()
        v_uniques_all.Columns = [
            'constraint_name',
            'column_name',
            'table_name'
        ]
        if p_table:
            v_tables = self.v_connection.Query('''
                select name,
                       sql
                from sqlite_master
                where type = 'table'
                  and name = '{0}'
            '''.format(p_table), True)
        else:
            v_tables = self.v_connection.Query('''
                select name,
                       sql
                from sqlite_master
                where type = 'table'
            ''', True)
        v_regex = re.compile(r"\s+")
        for v_table in v_tables.Rows:
            v_sql = v_table['sql'].lower().strip()
            if 'unique' in v_sql:
                v_index = v_sql.find('(') + 1
                v_filtered_sql = v_sql[v_index : ]
                v_formatted = v_regex.sub(' ', v_filtered_sql)

    def QueryTablesIndexes(self, p_table=None):
        pass

    def QueryDataLimited(self, p_query, p_count=-1):
        if p_count != -1:
            self.v_connection.Open()
            v_data = self.v_connection.QueryBlock(p_query, p_count, True)
            self.v_connection.Close()
            return v_data
        else:
            return self.v_connection.Query(p_query, True)

    def QueryTableRecords(self, p_column_list, p_table, p_filter, p_count=-1):
        v_limit = ''
        if p_count != -1:
            v_limit = ' limit ' + p_count
        return self.v_connection.Query('''
            select {0}
            from {1} t
            {2}
            {3}
        '''.format(
                p_column_list,
                p_table,
                p_filter,
                v_limit
            ), True
        )

    def TemplateCreateTable(self):
        pass

    def TemplateAlterTable(self):
        pass

    def TemplateDropTable(self):
        return Template('DROP TABLE #table_name#')

    def TemplateCreateIndex(self):
        pass

    def TemplateDropIndex(self):
        pass
