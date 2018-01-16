'''
The MIT License (MIT)

Portions Copyright (c) 2015-2018, The OmniDB Team
Portions Copyright (c) 2017-2018, 2ndQuadrant Limited

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
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_conn_id=0, p_alias=''):
        self.v_alias = p_alias
        self.v_db_type = 'postgresql'
        self.v_conn_id = p_conn_id

        if p_port is None or p_port == '':
            self.v_port = '5432'
        else:
            self.v_port = p_port
        if p_service is None or p_service == '':
            self.v_service = 'postgres'
        else:
            self.v_service = p_service

        self.v_server = p_server
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
        self.v_has_excludes = True
        self.v_has_rules = True
        self.v_has_triggers = True
        self.v_has_partitions = True

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

    def GetUserSuper(self):
        return self.v_connection.ExecuteScalar("select rolsuper from pg_roles where rolname = '{0}'".format(self.v_user))

    def PrintDatabaseInfo(self):
        return self.v_user + '@' + self.v_service

    def PrintDatabaseDetails(self):
        return self.v_server + ':' + self.v_port

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):
        v_rules = ''
        if p_update_rule.strip() != '':
            v_rules += ' on update ' + p_update_rule + ' '
        if p_delete_rule.strip() != '':
            v_rules += ' on delete ' + p_delete_rule + ' '
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

    def GetErrorPosition(self, p_error_message):
        vector = str(p_error_message).split('\n')
        v_return = None
        if len(vector) > 1 and vector[1][0:4]=='LINE':
            v_return = {
                'row': vector[1].split(':')[0].split(' ')[1],
                'col': vector[2].index('^') - len(vector[1].split(':')[0])-2
            }
        return v_return

    def QueryRoles(self):
        return self.v_connection.Query('''
            select quote_ident(rolname) as role_name
            from pg_roles
            order by rolname
        ''', True)

    def QueryTablespaces(self):
        return self.v_connection.Query('''
            select quote_ident(spcname) as tablespace_name
            from pg_tablespace
            order by spcname
        ''', True)

    def QueryDatabases(self):
        return self.v_connection.Query('''
            select database_name
            from (
            select quote_ident(datname) as database_name,
                   1 as sort
            from pg_database
            where datname = 'postgres'
            union all
            select database_name,
                   1 + row_number() over() as sort
            from (
            select quote_ident(datname) as database_name
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
            select quote_ident(extname) as extension_name
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
            select quote_ident(nspname) as schema_name
            from pg_catalog.pg_namespace
            where nspname in ('public', 'pg_catalog', 'information_schema')
            order by nspname desc
            ) x
            union all
            select schema_name,
                   3 + row_number() over() as sort
            from (
            select quote_ident(nspname) as schema_name
            from pg_catalog.pg_namespace
            where nspname not in ('public', 'pg_catalog', 'information_schema', 'pg_toast')
              and nspname not like 'pg%%temp%%'
            order by nspname
            ) x
            ) y
            order by sort
        ''', True)

    def QueryTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(table_schema) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(table_name) as table_name,
                   quote_ident(table_schema) as table_schema
            from information_schema.tables
            where table_type = 'BASE TABLE'
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(t.table_schema) = '{0}' and quote_ident(c.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(t.table_schema) = '{0}' and quote_ident(c.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(t.table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(t.table_schema) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(t.table_schema) not in ('information_schema','pg_catalog') and quote_ident(c.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(t.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(c.table_name) as table_name,
                   quote_ident(c.column_name) as column_name,
                   c.data_type as data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale
            from information_schema.columns c
            join information_schema.tables t on (c.table_name = t.table_name and c.table_schema = t.table_schema)
            where t.table_type = 'BASE TABLE'
            {0}
            order by quote_ident(c.table_name), c.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesForeignKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(rc.constraint_schema) = '{0}' and quote_ident(kcu1.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(rc.constraint_schema) = '{0}' and quote_ident(kcu1.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(rc.constraint_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(rc.constraint_schema) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(rc.constraint_schema) not in ('information_schema','pg_catalog') and quote_ident(kcu1.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(rc.constraint_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select *
            from (select distinct
                         quote_ident(kcu1.constraint_name) as constraint_name,
                         quote_ident(kcu1.table_name) as table_name,
                         quote_ident(kcu1.column_name) as column_name,
                         quote_ident(kcu2.constraint_name) as r_constraint_name,
                         quote_ident(kcu2.table_name) as r_table_name,
                         quote_ident(kcu2.column_name) as r_column_name,
                         quote_ident(kcu1.constraint_schema) as table_schema,
                         quote_ident(kcu2.constraint_schema) as r_table_schema,
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
            order by quote_ident(constraint_name),
                     quote_ident(table_name),
                     ordinal_position
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' and quote_ident(tc.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' and quote_ident(tc.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(tc.table_schema) not in ('information_schema','pg_catalog') and quote_ident(tc.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(tc.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(tc.constraint_name) as constraint_name,
                   quote_ident(kc.column_name) as column_name,
                   quote_ident(tc.table_name) as table_name,
                   quote_ident(tc.table_schema) as table_schema
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'PRIMARY KEY'
            {0}
            order by quote_ident(tc.constraint_name),
                     quote_ident(tc.table_name),
                     kc.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesUniques(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' and quote_ident(tc.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' and quote_ident(tc.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(tc.table_schema) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(tc.table_schema) not in ('information_schema','pg_catalog') and quote_ident(tc.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(tc.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(tc.constraint_name) as constraint_name,
                   quote_ident(kc.column_name) as column_name,
                   quote_ident(tc.table_name) as table_name,
                   quote_ident(tc.table_schema) as table_schema
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'UNIQUE'
            {0}
            order by quote_ident(tc.constraint_name),
                     quote_ident(tc.table_name),
                     kc.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesIndexes(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(t.schemaname) = '{0}' and quote_ident(t.tablename) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(t.schemaname) = '{0}' and quote_ident(t.tablename) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(t.schemaname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(t.schemaname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(t.schemaname) not in ('information_schema','pg_catalog') and quote_ident(t.tablename) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(t.schemaname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(t.tablename) as table_name,
                   quote_ident(t.indexname) as index_name,
                   unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as column_name,
                   (case when strpos(t.indexdef, 'UNIQUE') > 0 then 'Unique' else 'Non Unique' end) as uniqueness,
                   quote_ident(t.schemaname) as schema_name
            from pg_indexes t
            where 1 = 1
            {0}
            order by quote_ident(t.tablename),
                     quote_ident(t.indexname)
        '''.format(v_filter), True)

    def QueryTablesChecks(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) as schema_name,
                   ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') as table_name,
                   quote_ident(c.conname) as constraint_name,
                   c.consrc as constraint_source
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'c'
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def QueryTablesExcludes(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_exclude_ops(text, text, text)
            returns text as $$
            select array_to_string(array(
            select oprname
            from (
            select o.oprname
            from (
            select unnest(c.conexclop) as conexclop
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = $1
              and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_operator o
            on o.oid = x.conexclop
            ) t
            ), ',')
            $$ language sql;
            create or replace function pg_temp.fnc_omnidb_exclude_attrs(text, text, text)
            returns text as $$
            select array_to_string(array(
            select a.attname
            from (
            select unnest(c.conkey) as conkey
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = $1
              and ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_attribute a
            on a.attnum = x.conkey
            inner join pg_class r
            on r.oid = a.attrelid
            inner join pg_namespace n
            on n.oid = r.relnamespace
            where quote_ident(n.nspname) = $1
              and quote_ident(r.relname) = $2
            ), ',')
            $$ language sql;
            select quote_ident(n.nspname) as schema_name,
                   ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.') as table_name,
                   quote_ident(c.conname) as constraint_name,
                   pg_temp.fnc_omnidb_exclude_ops(
                       quote_ident(n.nspname),
                       ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.'),
                       quote_ident(c.conname)
                   ) as operations,
                   pg_temp.fnc_omnidb_exclude_attrs(
                       quote_ident(n.nspname),
                       ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.'),
                       quote_ident(c.conname)
                   ) as attributes
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def QueryTablesRules(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(schemaname) = '{0}' and quote_ident(tablename) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(schemaname) = '{0}' and quote_ident(tablename) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(schemaname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(schemaname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(schemaname) not in ('information_schema','pg_catalog') and quote_ident(tablename) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(schemaname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(schemaname) as table_schema,
                   quote_ident(tablename) as table_name,
                   quote_ident(rulename) as rule_name
            from pg_rules
            where 1 = 1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def GetRuleDefinition(self, p_rule, p_table, p_schema):
        return self.v_connection.ExecuteScalar('''
            select definition
            from pg_rules
            where quote_ident(table_schema) = '{0}'
              and quote_ident(table_name) = '{1}'
              and quote_ident(rulename) = '{2}'
        '''.format(p_schema, p_table, p_rule))

    def QueryTablesTriggers(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and quote_ident(c.relname) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) as schema_name,
                   quote_ident(c.relname) as table_name,
                   quote_ident(t.tgname) as trigger_name,
                   t.tgenabled as trigger_enabled,
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) as trigger_function_name,
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) || '()' as trigger_function_id
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
            select distinct quote_ident(t.trigger_name),
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
            where quote_ident(t.event_object_schema) = '{0}'
              and quote_ident(t.event_object_table) = '{1}'
              and quote_ident(t.trigger_name) = '{2}'
            ) x
        '''.format(p_schema, p_table, p_trigger))

    def QueryTablesPartitions(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(np.nspname) = '{0}' and quote_ident(cp.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(np.nspname) = '{0}' and quote_ident(cp.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(np.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(np.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(np.nspname) not in ('information_schema','pg_catalog') and quote_ident(cp.relname) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(np.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(np.nspname) as parent_schema,
                   quote_ident(cp.relname) as parent_table,
                   quote_ident(nc.nspname) as child_schema,
                   quote_ident(cc.relname) as child_table
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
            try:
                self.v_connection.Open()
                v_data = self.v_connection.QueryBlock(p_query + ' limit {0}'.format(p_count), p_count, True)
                self.v_connection.Close()
                return v_data
            except Spartacus.Database.Exception as exc:
                try:
                    self.v_connection.Cancel()
                except:
                    pass
                raise exc
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
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   quote_ident(p.proname) as name,
                   quote_ident(n.nspname) as schema_name
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
                       quote_ident(y.name) as name,
                       1 as seq
                from (
                    select 'O' as type,
                           'returns ' || format_type(p.prorettype, null) as name
                    from pg_proc p,
                         pg_namespace n
                    where p.pronamespace = n.oid
                      and n.nspname = '{0}'
                      and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
                ) y
                union all
                select (case trim(substring((trim(x.name) || ' ') from 1 for position(' ' in (trim(x.name) || ' '))))
                          when 'OUT' then 'O'
                          when 'INOUT' then 'X'
                          else 'I'
                        end) as type,
                       trim(x.name) as name,
                       row_number() over() + 1 as seq
                from (
                    select unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 3
            '''.format(p_schema, p_function), True)
        else:
            return self.v_connection.Query('''
                select y.type::character varying as type,
                       quote_ident(y.name) as name,
                       1 as seq
                from (
                    select 'O' as type,
                           'returns ' || format_type(p.prorettype, null) as name
                    from pg_proc p,
                         pg_namespace n
                    where p.pronamespace = n.oid
                      and n.nspname = '{0}'
                      and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
                ) y
                union all
                select (case trim(substring((trim(x.name) || ' ') from 1 for position(' ' in (trim(x.name) || ' '))))
                          when 'OUT' then 'O'
                          when 'INOUT' then 'X'
                          else 'I'
                        end) as type,
                       trim(x.name) as name,
                       row_number() over() + 1 as seq
                from (
                    select unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 3
            '''.format(self.v_schema, p_function), True)

    def GetFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    def GetFunctionDebug(self, p_function):
        return self.v_connection.ExecuteScalar('''
            select p.prosrc
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
        '''.format(p_function))

    def QueryTriggerFunctions(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   quote_ident(p.proname) as name,
                   quote_ident(n.nspname) as schema_name
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
                v_filter = "and quote_ident(sequence_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(sequence_schema) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(sequence_schema) not in ('information_schema','pg_catalog') "
        v_table = self.v_connection.Query('''
            select quote_ident(sequence_schema) as sequence_schema,
                   quote_ident(sequence_name) as sequence_name
            from information_schema.sequences
            where 1 = 1
            {0}
            order by 1
        '''.format(v_filter), True)
        return v_table

    def QuerySequenceValues(self, p_sequence, p_schema):
        v_table = self.v_connection.Query('''
            select quote_ident(sequence_schema) as sequence_schema,
                   quote_ident(sequence_name) as sequence_name,
                   minimum_value,
                   maximum_value,
                   0 as current_value,
                   increment
            from information_schema.sequences
            where quote_ident(sequence_schema) = '{0}'
              and quote_ident(sequence_name) = '{1}'
            order by 1
        '''.format(p_schema, p_sequence), True)
        for i in range(0, len(v_table.Rows)):
            v_table.Rows[i]['current_value'] = self.v_connection.ExecuteScalar(
                "select last_value from {0}.{1}".format(v_table.Rows[i]['sequence_schema'], v_table.Rows[i]['sequence_name'])
            )
        return v_table

    def QueryViews(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(table_schema) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(table_name) as table_name,
                   quote_ident(table_schema) as table_schema
            from information_schema.views
            where 1 = 1
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryViewFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(t.table_schema) = '{0}' and quote_ident(c.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(t.table_schema) = '{0}' and quote_ident(c.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(t.table_schema) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(t.table_schema) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(t.table_schema) not in ('information_schema','pg_catalog') and quote_ident(c.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(t.table_schema) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(c.table_name) as table_name,
                   quote_ident(c.column_name) as column_name,
                   c.data_type as data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale
            from information_schema.columns c
            join information_schema.views t on (c.table_name = t.table_name and c.table_schema = t.table_schema)
            where 1 = 1
            {0}
            order by quote_ident(c.table_name), c.ordinal_position
        '''.format(v_filter), True)

    def GetViewDefinition(self, p_view, p_schema):
        return '''CREATE OR REPLACE VIEW {0}.{1} AS
{2}
'''.format(p_schema, p_view,
        self.v_connection.ExecuteScalar('''
                select view_definition
                from information_schema.views
                where quote_ident(table_schema) = '{0}'
                  and quote_ident(table_name) = '{1}'
            '''.format(p_schema, p_view)
    ))

    def QueryMaterializedViews(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(t.relname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(t.relname) as table_name,
                   quote_ident(n.nspname) as schema_name
            from pg_class t
            inner join pg_namespace n
            on n.oid = t.relnamespace
            where t.relkind = 'm'
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryMaterializedViewFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and quote_ident(c.relname) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(c.relname) as table_name,
                   quote_ident(a.attname) as column_name,
                   t.typname as data_type,
                   not t.typnotnull as nullable,
                   t.typlen as data_length,
                   null as data_precision,
                   null as data_scale
            from pg_attribute a
            inner join pg_class c
            on c.oid = a.attrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_type t
            on t.oid = a.atttypid
            where a.attnum > 0
              and not a.attisdropped
              and c.relkind = 'm'
              {0}
            order by quote_ident(c.relname),
                     a.attnum
        '''.format(v_filter), True)

    def GetMaterializedViewDefinition(self, p_view, p_schema):
        return '''DROP MATERIALIZED VIEW {0}.{1};

CREATE MATERIALIZED VIEW {0}.{1} AS
{2}
'''.format(p_schema, p_view,
        self.v_connection.ExecuteScalar('''
                select pg_get_viewdef('{0}.{1}'::regclass)
            '''.format(p_schema, p_view)
    ))

    def QueryPhysicalReplicationSlots(self):
        return self.v_connection.Query('''
            select quote_ident(slot_name) as slot_name
            from pg_replication_slots
            where slot_type = 'physical'
            order by 1
        ''', True)

    def QueryLogicalReplicationSlots(self):
        return self.v_connection.Query('''
            select quote_ident(slot_name) as slot_name
            from pg_replication_slots
            where slot_type = 'logical'
            order by 1
        ''', True)

    def QueryPublications(self):
        return self.v_connection.Query('''
            select quote_ident(pubname) as pubname,
                   puballtables,
                   pubinsert,
                   pubupdate,
                   pubdelete
            from pg_publication
            order by 1
        ''', True)

    def QueryPublicationTables(self, p_pub):
        return self.v_connection.Query('''
            select quote_ident(schemaname) || '.' || quote_ident(tablename) as table_name
            from pg_publication_tables
            where quote_ident(pubname) = '{0}'
            order by 1
        '''.format(p_pub), True)

    def QuerySubscriptions(self):
        return self.v_connection.Query('''
            select quote_ident(s.subname) as subname,
                   s.subenabled,
                   s.subconninfo,
                   array_to_string(s.subpublications, ',') as subpublications
            from pg_subscription s
            inner join pg_database d
            on d.oid = s.subdbid
            where d.datname = '{0}'
            order by 1
        '''.format(self.v_service), True)

    def QuerySubscriptionTables(self, p_sub):
        return self.v_connection.Query('''
            select quote_ident(n.nspname) || '.' || quote_ident(c.relname) as table_name
            from pg_subscription s
            inner join pg_database d
            on d.oid = s.subdbid
            inner join pg_subscription_rel r
            on r.srsubid = s.oid
            inner join pg_class c
            on c.oid = r.srrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where d.datname = '{0}'
              and quote_ident(s.subname) = '{1}'
            order by 1
        '''.format(self.v_service, p_sub), True)

    def DataMining(self, p_textPattern, p_caseSentive, p_regex, p_categoryList, p_schemaList, p_summarizeResults):
        v_sql = '''
            select x.*
            from (
                select null::text as category,
                       null::text as schema_name,
                       null::text as table_name,
                       null::text as column_name,
                       null::text as match_value

                /*#START_FUNCTION NAME#
                union

                select 'Function Name'::text as category,
                       n.nspname::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       p.proname::text as match_value
                from pg_proc p
                inner join pg_namespace n
                           on p.pronamespace = n.oid
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and format_type(p.prorettype, null) <> 'trigger'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and p.proname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.proname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and p.proname ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                #END_FUNCTION NAME#*/

                /*#START_TABLE NAME#
                union

                select 'Table Name'::text as category,
                       t.table_schema::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       t.table_name::text as match_value
                from information_schema.tables t
                where t.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and t.table_schema not like 'pg%%temp%%'
                  and t.table_type = 'BASE TABLE'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and t.table_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.table_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and t.table_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(t.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_TABLE NAME#*/

                /*#START_VIEW NAME#
                union

                select 'View Name'::text as category,
                       v.table_schema::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       v.table_name::text as match_value
                from information_schema.views v
                where v.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and v.table_schema not like 'pg%%temp%%'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and v.table_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(v.table_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and v.table_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(v.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_VIEW NAME#*/

                /*#START_MATERIALIZED VIEW NAME#
                union

                select 'Materialized View Name'::text as category,
                       n.nspname::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       c.relname::text as match_value
                from pg_class c
                inner join pg_namespace n
                           on n.oid = c.relnamespace
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and c.relkind = 'm'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and c.relname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.relname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and c.relname ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                #END_MATERIALIZED VIEW NAME#*/

                /*#START_SEQUENCE NAME#
                union

                select 'Sequence Name'::text as category,
                       s.sequence_schema::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       s.sequence_name::text as match_value
                from information_schema.sequences s
                where s.sequence_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and s.sequence_schema not like 'pg%%temp%%'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and s.sequence_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(s.sequence_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and s.sequence_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(s.sequence_schema) in (#VALUE_BY_SCHEMA#)
                #END_SEQUENCE NAME#*/

                /*#START_SCHEMA NAME#
                union

                select 'Schema Name'::text as category,
                       ''::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       n.nspname::text as match_value
                from pg_namespace n
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and n.nspname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(n.nspname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and n.nspname ~ '#VALUE_PATTERN_REGEX#'
                #END_SCHEMA NAME#*/

                /*#START_FUNCTION DEFINITION#
                union

                select 'Function Definition'::text as category,
                       y.schema_name::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       y.function_definition::text as match_value
                from (
                    select pg_get_functiondef(z.function_oid::regprocedure) as function_definition,
                           *
                    from (
                        select n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' as function_oid,
                               p.proname as function_name,
                               n.nspname as schema_name
                        from pg_proc p
                        inner join pg_namespace n
                                   on p.pronamespace = n.oid
                        where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                          and n.nspname not like 'pg%%temp%%'
                          and format_type(p.prorettype, null) <> 'trigger'
                        --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                    ) z
                ) y
                where 1 = 1
                --#FILTER_PATTERN_CASE_SENSITIVE#  and y.function_definition like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(y.function_definition) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and y.function_definition ~ '#VALUE_PATTERN_REGEX#'
                #END_FUNCTION DEFINITION#*/

                /*#START_TRIGGER NAME#
                union

                select 'Trigger Name'::text as category,
                       n.nspname::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       p.proname::text as match_value
                from pg_proc p
                inner join pg_namespace n
                           on p.pronamespace = n.oid
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and format_type(p.prorettype, null) = 'trigger'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and p.proname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.proname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and p.proname ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                #END_TRIGGER NAME#*/

                /*#START_TRIGGER SOURCE#
                union

                select 'Trigger Source'::text as category,
                       n.nspname::text as schema_name,
                       ''::text as table_name,
                       ''::text as column_name,
                       p.prosrc::text as match_value
                from pg_proc p
                inner join pg_namespace n
                           on p.pronamespace = n.oid
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and format_type(p.prorettype, null) = 'trigger'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and p.prosrc like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.prosrc) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and p.prosrc ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                #END_TRIGGER SOURCE#*/

                /*#START_TABLE COLUMN NAME#
                union

                select 'Table Column Name'::text as category,
                       c.table_schema::text as schema_name,
                       c.table_name::text as table_name,
                       ''::text as column_name,
                       c.column_name::text as match_value
                from information_schema.tables t
                inner join information_schema.columns c
                           on t.table_name = c.table_name and t.table_schema = c.table_schema
                where c.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and c.table_schema not like 'pg%%temp%%'
                  and t.table_type = 'BASE TABLE'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and c.column_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.column_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and c.column_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(c.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_TABLE COLUMN NAME#*/

                /*#START_VIEW COLUMN NAME#
                union

                select 'View Column Name'::text as category,
                       c.table_schema::text as schema_name,
                       c.table_name::text as table_name,
                       ''::text as column_name,
                       c.column_name::text as match_value
                from information_schema.views v
                inner join information_schema.columns c
                           on v.table_name = c.table_name and v.table_schema = c.table_schema
                where v.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and v.table_schema not like 'pg%%temp%%'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and c.column_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.column_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and c.column_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(c.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_VIEW COLUMN NAME#*/

                /*#START_MATERIALIZED VIEW COLUMN NAME#
                union

                select 'Materialized View Column Name'::text as category,
                       n.nspname::text as schema_name,
                       c.relname::text as table_name,
                       ''::text as column_name,
                       a.attname::text as match_value
                from pg_attribute a
                inner join pg_class c
                           on c.oid = a.attrelid
                inner join pg_namespace n
                           on n.oid = c.relnamespace
                inner join pg_type t
                           on t.oid = a.atttypid
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and a.attnum > 0
                  and not a.attisdropped
                  and c.relkind = 'm'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and a.attname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(a.attname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and a.attname ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                #END_MATERIALIZED VIEW COLUMN NAME#*/

                /*#START_PK NAME#
                union

                select 'PK Name'::text as category,
                       tc.table_schema::text as schema_name,
                       tc.table_name::text as table_name,
                       ''::text as column_name,
                       tc.constraint_name::text as match_value
                from information_schema.table_constraints tc
                where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and tc.table_schema not like 'pg%%temp%%'
                  and tc.constraint_type = 'PRIMARY KEY'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_PK NAME#*/

                /*#START_FK NAME#
                union

                select 'FK Name'::text as category,
                       tc.table_schema::text as schema_name,
                       tc.table_name::text as table_name,
                       ''::text as column_name,
                       tc.constraint_name::text as match_value
                from information_schema.table_constraints tc
                where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and tc.table_schema not like 'pg%%temp%%'
                  and tc.constraint_type = 'FOREIGN KEY'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_FK NAME#*/

                /*#START_UNIQUE NAME#
                union

                select 'Unique Name'::text as category,
                       tc.table_schema::text as schema_name,
                       tc.table_name::text as table_name,
                       ''::text as column_name,
                       tc.constraint_name::text as match_value
                from information_schema.table_constraints tc
                where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and tc.table_schema not like 'pg%%temp%%'
                  and tc.constraint_type = 'UNIQUE'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
                #END_UNIQUE NAME#*/

                /*#START_INDEX NAME#
                union

                select 'Index Name'::text as category,
                       i.schemaname::text as schema_name,
                       i.tablename::text as table_name,
                       ''::text as column_name,
                       i.indexname::text as match_value
                from pg_indexes i
                where i.schemaname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and i.schemaname not like 'pg%%temp%%'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and i.indexname like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(i.indexname) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and i.indexname ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(i.schemaname) in (#VALUE_BY_SCHEMA#)
                #END_INDEX NAME#*/

                /*#START_CHECK NAME#
                union

                select 'Check Name'::text as category,
                       quote_ident(n.nspname)::text as schema_name,
                       ltrim(quote_ident(t.relname), quote_ident(n.nspname) || '.')::text as table_name,
                       ''::text as column_name,
                       quote_ident(c.conname)::text as match_value
                from pg_constraint c
                inner join pg_class t
                           on t.oid = c.conrelid
                inner join pg_namespace n
                           on t.relnamespace = n.oid
                where contype = 'c'
                --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(c.conname) like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(c.conname)) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and quote_ident(c.conname) ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(n.nspname)) in (#VALUE_BY_SCHEMA#)
                #END_INDEX NAME#*/

                /*#START_RULE NAME#
                union

                select 'Rule Name'::text as category,
                       quote_ident(schemaname)::text as schema_name,
                       quote_ident(tablename)::text as table_name,
                       ''::text as column_name,
                       quote_ident(rulename)::text as match_value
                from pg_rules
                where 1 = 1
                --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(rulename) like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(rulename)) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and quote_ident(rulename) ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(schemaname)) in (#VALUE_BY_SCHEMA#)
                #END_RULE NAME#*/

                /*#START_RULE DEFINITION#
                union

                select 'Rule Definition'::text as category,
                       quote_ident(schemaname)::text as schema_name,
                       quote_ident(tablename)::text as table_name,
                       ''::text as column_name,
                       definition::text as match_value
                from pg_rules
                where 1 = 1
                --#FILTER_PATTERN_CASE_SENSITIVE#  and definition like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(definition) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and definition ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(schemaname)) in (#VALUE_BY_SCHEMA#)
                #END_RULE DEFINITION#*/

                /*#START_PARTITION NAME#
                union

                select 'Partition Name'::text as category,
                       quote_ident(np.nspname)::text as schema_name,
                       quote_ident(cp.relname)::text as table_name,
                       ''::text as column_name,
                       quote_ident(cc.relname)::text as match_value
                from pg_inherits i
                inner join pg_class cp
                           on cp.oid = i.inhparent
                inner join pg_namespace np
                           on np.oid = cp.relnamespace
                inner join pg_class cc
                           on cc.oid = i.inhrelid
                inner join pg_namespace nc
                           on nc.oid = cc.relnamespace
                where 1 = 1
                --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(cc.relname) like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(cc.relname)) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                --#FILTER_PATTERN_REGEX# and quote_ident(cc.relname) ~ '#VALUE_PATTERN_REGEX#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(np.nspname)) in (#VALUE_BY_SCHEMA#)
                #END_PARTITION NAME#*/

                --#START_DATA##END_DATA#
            ) x
            where x.category is not null
            order by x.category, x.schema_name, x.table_name, x.column_name, x.match_value
        '''

        v_inSchemas = ''

        if len(p_schemaList) > 0:
            for v_schema in p_schemaList:
                v_inSchemas += "'{0}', ".format(v_schema)

            v_inSchemas = v_inSchemas[:-2]

        if 'Data' in p_categoryList and v_inSchemas != '':
            v_columnsSql = '''
                select n.nspname as schema_name,
                       c.relname as table_name,
                       a.attname as column_name
                from pg_namespace n
                inner join pg_class c
                           on n.oid = c.relnamespace
                inner join pg_attribute a
                           on c.oid = a.attrelid
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and c.relkind = 'r'
                  and attnum > 0
                  and not a.attisdropped
                  and n.nspname in ({0})
            '''.format(v_inSchemas)

            v_columnsTable = self.v_connection.Query(v_columnsSql)

            if len(v_columnsTable.Rows) > 0:
                v_dataSql = ''

                for v_columnRow in v_columnsTable.Rows:
                    v_dataSql += '''

                        union

                        select 'Data' as category,
                               '{0}' as schema_name,
                               '{1}' as table_name,
                               '{2}' as column_name,
                               t.{2}::text as match_value
                        from (
                            select t.{2}
                            from {0}.{1} t
                            where 1 = 1
                            --#FILTER_PATTERN_CASE_SENSITIVE#  and t.{2}::text like '%#VALUE_PATTERN_CASE_SENSITIVE#%'
                            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.{2}::text) like lower('%#VALUE_PATTERN_CASE_INSENSITIVE#%')
                            --#FILTER_PATTERN_REGEX# and t.{2}::text ~ '#VALUE_PATTERN_REGEX#'
                        ) t
                    '''.format(
                        v_columnRow['schema_name'],
                        v_columnRow['table_name'],
                        v_columnRow['column_name']
                    )

                v_sql = v_sql.replace('--#START_DATA##END_DATA#', v_dataSql)

        if v_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', v_inSchemas)

        if p_regex:
            v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX#', '').replace('#VALUE_PATTERN_REGEX#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        for v_category in p_categoryList:
            if v_category != 'Data':
                v_sql = v_sql.replace('/*#START_{0}#'.format(v_category.upper()), '').replace('#END_{0}#*/'.format(v_category.upper()), '')

        if p_summarizeResults:
            v_sql = '''
                select s.category,
                       s.schema_name,
                       s.table_name,
                       s.column_name,
                       count(*) as match_count
                from (
                    {0}
                ) s
                group by s.category, s.schema_name, s.table_name, s.column_name
            '''.format(v_sql)

        return v_sql

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
        return Template('''ALTER EXTENSION #extension_name#
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
--CASCADE
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

    def TemplateCreateMaterializedView(self):
        return Template('''CREATE MATERIALIZED VIEW #schema_name#.name AS
SELECT ...
--WITH NO DATA
''')

    def TemplateRefreshMaterializedView(self):
        return Template('''REFRESH MATERIALIZED VIEW #view_name#
--CONCURRENTLY
--WITH NO DATA
''')

    def TemplateDropMaterializedView(self):
        return Template('''DROP MATERIALIZED VIEW #view_name#
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

    def TemplateCreateColumn(self):
        return Template('''ALTER TABLE #table_name#
ADD COLUMN name data_type
--COLLATE collation
--column_constraint [ ... ] ]
''')

    def TemplateAlterColumn(self):
        return Template('''ALTER TABLE #table_name#
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
'''
)

    def TemplateDropColumn(self):
        return Template('''ALTER TABLE #table_name#
DROP COLUMN #column_name#
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

    def TemplateCreateUnique(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
UNIQUE ( column_name [, ... ] )
--WITH ( storage_parameter [= value] [, ... ] )
--WITH OIDS
--WITHOUT OIDS
--USING INDEX TABLESPACE tablespace_name
''')

    def TemplateDropUnique(self):
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

    def TemplateCreateExclude(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
--USING index_method
EXCLUDE ( exclude_element WITH operator [, ... ] )
--index_parameters
--WHERE ( predicate )
''')

    def TemplateDropExclude(self):
        return Template('''ALTER TABLE #table_name#
DROP CONSTRAINT #constraint_name#
--CASCADE
''')

    def TemplateCreateRule(self):
        return Template('''CREATE RULE name
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

    def TemplateCreateViewTrigger(self):
        return Template('''CREATE TRIGGER name
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
''')

    def TemplateAlterTrigger(self):
        return Template('ALTER TRIGGER #trigger_name# ON #table_name# RENAME TO new_name')

    def TemplateEnableTrigger(self):
        return Template('ALTER TABLE #table_name# ENABLE TRIGGER #trigger_name#')

    def TemplateDisableTrigger(self):
        return Template('ALTER TABLE #table_name# DISABLE TRIGGER #trigger_name#')

    def TemplateDropTrigger(self):
        return Template('''DROP TRIGGER #trigger_name# ON #table_name#
--CASCADE
''')

    def TemplateCreatePartition(self):
        return Template('''CREATE TABLE name (
    CHECK ( condition )
) INHERITS (#table_name#)
''')

    def TemplateNoInheritPartition(self):
        return Template('ALTER TABLE #partition_name# NO INHERIT #table_name#')

    def TemplateDropPartition(self):
        return Template('DROP TABLE #partition_name#')

    def TemplateVacuum(self):
        return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
''')

    def TemplateVacuumTable(self):
        return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
#table_name#
--(column_name, [, ...])
''')

    def TemplateCreatePhysicalReplicationSlot(self):
        return Template('''SELECT * FROM pg_create_physical_replication_slot('slot_name')''')

    def TemplateDropPhysicalReplicationSlot(self):
        return Template('''SELECT pg_drop_replication_slot('#slot_name#')''')

    def TemplateCreateLogicalReplicationSlot(self):
        return Template('''SELECT * FROM pg_create_logical_replication_slot('slot_name', 'pgoutput')''')

    def TemplateDropLogicalReplicationSlot(self):
        return Template('''SELECT pg_drop_replication_slot('#slot_name#')''')

    def TemplateCreatePublication(self):
        return Template('''CREATE PUBLICATION name
--FOR TABLE [ ONLY ] table_name [ * ] [, ...]
--FOR ALL TABLES
--WITH ( publish = 'insert, update, delete' )
''')

    def TemplateAlterPublication(self):
        return Template('''ALTER PUBLICATION #pub_name#
--ADD TABLE [ ONLY ] table_name [ * ] [, ...]
--SET TABLE [ ONLY ] table_name [ * ] [, ...]
--DROP TABLE [ ONLY ] table_name [ * ] [, ...]
--SET ( publish = 'insert, update, delete' )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''')

    def TemplateDropPublication(self):
        return Template('''DROP PUBLICATION #pub_name#
--CASCADE
''')

    def TemplateAddPublicationTable(self):
        return Template('ALTER PUBLICATION #pub_name# ADD TABLE table_name')

    def TemplateDropPublicationTable(self):
        return Template('ALTER PUBLICATION #pub_name# DROP TABLE #table_name#')

    def TemplateCreateSubscription(self):
        return Template('''CREATE SUBSCRIPTION name
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
''')

    def TemplateAlterSubscription(self):
        return Template('''ALTER SUBSCRIPTION #sub_name#
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
''')

    def TemplateDropSubscription(self):
        return Template('''DROP SUBSCRIPTION #sub_name#
--CASCADE
''')

    def GetPglogicalVersion(self):
        return self.v_connection.ExecuteScalar('''
            select extversion
            from pg_extension
            where extname = 'pglogical'
        ''')

    def QueryPglogicalNodes(self):
        return self.v_connection.Query('''
            select quote_ident(n.node_name) || (case when l.node_id is not null then ' (local)' else '' end) as node_name
            from pglogical.node n
            left join pglogical.local_node l
            on l.node_id = n.node_id
            order by 1
        ''')

    def QueryPglogicalNodeInterfaces(self, p_node):
        return self.v_connection.Query('''
            select i.if_name,
                   i.if_dsn
            from pglogical.node_interface i
            inner join pglogical.node n
            on n.node_id = i.if_nodeid
            where n.node_name = '{0}'
        '''.format(p_node))

    def QueryPglogicalReplicationSets(self):
        return self.v_connection.Query('''
            select quote_ident(set_name) as set_name,
                   replicate_insert,
                   replicate_update,
                   replicate_delete,
                   replicate_truncate
            from pglogical.replication_set
            order by 1
        ''')

    def QueryPglogicalReplicationSetTables(self, p_repset):
        return self.v_connection.Query('''
            select quote_ident(n.nspname) || '.' || quote_ident(c.relname) as table_name
            from pglogical.replication_set_table t
            inner join pglogical.replication_set r
            on r.set_id = t.set_id
            inner join pg_class c
            on c.oid = t.set_reloid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where quote_ident(r.set_name) = '{0}'
            order by 1
        '''.format(p_repset))

    def QueryPglogicalReplicationSetSequences(self, p_repset):
        return self.v_connection.Query('''
            select quote_ident(n.nspname) || '.' || quote_ident(c.relname) as sequence_name
            from pglogical.replication_set_seq t
            inner join pglogical.replication_set r
            on r.set_id = t.set_id
            inner join pg_class c
            on c.oid = t.set_seqoid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where quote_ident(r.set_name) = '{0}'
            order by 1
        '''.format(p_repset))

    def QueryPglogicalSubscriptions(self):
        return self.v_connection.Query('''
            select quote_ident(s.sub_name) as sub_name,
                   (select status from pglogical.show_subscription_status(s.sub_name)) as sub_status,
                   quote_ident(n.node_name) as sub_origin,
                   s.sub_enabled,
                   s.sub_apply_delay::text as sub_apply_delay
            from pglogical.subscription s
            inner join pglogical.node n
            on n.node_id = s.sub_origin
            order by 1
        ''')

    def QueryPglogicalSubscriptionReplicationSets(self, p_subscription):
        return self.v_connection.Query('''
            select quote_ident(unnest(s.sub_replication_sets)) as set_name
            from pglogical.subscription s
            inner join pglogical.node n
            on n.node_id = s.sub_origin
            where quote_ident(s.sub_name) = '{0}'
        '''.format(p_subscription))

    def TemplatePglogicalCreateNode(self):
        return Template('''select pglogical.create_node(
node_name := 'node_name',
dsn := 'host={0} port={1} dbname={2} user={3} password=password'
)
'''.format(self.v_server, self.v_port, self.v_service, self.v_user))

    def TemplatePglogicalDropNode(self):
        return Template('''select pglogical.drop_node(
node_name := '#node_name#',
ifexists := true
)''')

    def TemplatePglogicalNodeAddInterface(self):
        return Template('''select pglogical.alter_node_add_interface(
node_name := '#node_name#',
interface_name := 'name',
dsn := 'host= port= dbname= user= password='
)''')

    def TemplatePglogicalNodeDropInterface(self):
        return Template('''select pglogical.alter_node_drop_interface(
node_name := '#node_name#',
interface_name := '#interface_name#'
)''')

    def TemplatePglogicalCreateReplicationSet(self):
        return Template('''select pglogical.create_replication_set(
set_name := 'name',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true
)''')

    def TemplatePglogicalAlterReplicationSet(self):
        return Template('''select pglogical.alter_replication_set(
set_name := '#repset_name#',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true
)''')

    def TemplatePglogicalDropReplicationSet(self):
        return Template('''select pglogical.drop_replication_set(
set_name := '#repset_name#',
ifexists := true
)''')

    def TemplatePglogicalReplicationSetAddTable(self):
        return Template('''select pglogical.replication_set_add_table(
set_name := '#repset_name#',
relation := 'schema.table'::regclass,
synchronize_data := true,
columns := null,
row_filter := null
)''')

    def TemplatePglogicalReplicationSetAddAllTables(self):
        return Template('''select pglogical.replication_set_add_all_tables(
set_name := '#repset_name#',
schema_names := ARRAY['public'],
synchronize_data := true
)''')

    def TemplatePglogicalReplicationSetRemoveTable(self):
        return Template('''select pglogical.replication_set_remove_table(
set_name := '#repset_name#',
relation := '#table_name#'::regclass
)''')

    def TemplatePglogicalReplicationSetAddSequence(self):
        return Template('''select pglogical.replication_set_add_sequence(
set_name := '#repset_name#',
relation := 'schema.sequence'::regclass,
synchronize_data := true
)''')

    def TemplatePglogicalReplicationSetAddAllSequences(self):
        return Template('''select pglogical.replication_set_add_all_sequences(
set_name := '#repset_name#',
schema_names := ARRAY['public'],
synchronize_data := true
)''')

    def TemplatePglogicalReplicationSetRemoveSequence(self):
        return Template('''select pglogical.replication_set_remove_sequence(
set_name := '#repset_name#',
relation := '#sequence_name#'::regclass
)''')

    def TemplatePglogicalCreateSubscription(self):
        return Template('''select pglogical.create_subscription(
subscription_name := 'sub_name',
provider_dsn := 'host= port= dbname= user= password=',
replication_sets := array['default','default_insert_only','ddl_sql'],
synchronize_structure := true,
synchronize_data := true,
forward_origins := array['all'],
apply_delay := '0 seconds'::interval
)''')

    def TemplatePglogicalEnableSubscription(self):
        return Template('''select pglogical.alter_subscription_enable(
subscription_name := '#sub_name#',
immediate := true
)''')

    def TemplatePglogicalDisableSubscription(self):
        return Template('''select pglogical.alter_subscription_disable(
subscription_name := '#sub_name#',
immediate := true
)''')

    def TemplatePglogicalSynchronizeSubscription(self):
        return Template('''select pglogical.alter_subscription_synchronize(
subscription_name := '#sub_name#',
truncate := true
)''')

    def TemplatePglogicalDropSubscription(self):
        return Template('''select pglogical.drop_subscription(
subscription_name := '#sub_name#',
ifexists := true
)''')

    def TemplatePglogicalSubscriptionAddReplicationSet(self):
        return Template('''select pglogical.alter_subscription_add_replication_set(
subscription_name := '#sub_name#',
replication_set := 'set_name'
)''')

    def TemplatePglogicalSubscriptionRemoveReplicationSet(self):
        return Template('''select pglogical.alter_subscription_remove_replication_set(
subscription_name := '#sub_name#',
replication_set := '#set_name#'
)''')

    def GetBDRVersion(self):
        return self.v_connection.ExecuteScalar('''
            select extversion
            from pg_extension
            where extname = 'bdr'
        ''')

    def GetBDRNodeName(self):
        return self.v_connection.ExecuteScalar('select bdr.bdr_get_local_node_name()')

    def QueryBDRProperties(self):
        try:
            v_tmp = self.v_connection.ExecuteScalar('select bdr.bdr_is_active_in_db()')
            v_test = True
        except Spartacus.Database.Exception as exc:
            v_test = False
        if v_test:
            return self.v_connection.Query('''
                select bdr.bdr_version() as version,
                       bdr.bdr_is_active_in_db() as active,
                       coalesce(bdr.bdr_get_local_node_name(), 'Not set') as node_name,
                       bdr.bdr_apply_is_paused() as paused
            ''')
        else:
            return self.v_connection.Query('''
                select bdr.bdr_version() as version,
                       (coalesce(bdr.bdr_get_local_node_name(), 'Not set') != 'Not set') as active,
                       coalesce(bdr.bdr_get_local_node_name(), 'Not set') as node_name,
                       bdr.bdr_apply_is_paused() as paused
            ''')

    def QueryBDRNodes(self):
        return self.v_connection.Query('''
            select quote_ident(node_name) as node_name
            from bdr.bdr_nodes
            where node_status <> 'k'
            order by 1
        ''')

    def QueryBDRReplicationSets(self):
        return self.v_connection.Query('''
            select quote_ident(set_name) as set_name,
                   replicate_inserts,
                   replicate_updates,
                   replicate_deletes
            from bdr.bdr_replication_set_config
            order by 1
        ''')

    def QueryBDRTableReplicationSets(self, p_table):
        return self.v_connection.Query("select unnest(bdr.table_get_replication_sets('{0}')) as set_name".format(p_table))

    def QueryBDRTableConflictHandlers(self, p_table, p_schema):
        return self.v_connection.Query('''
            select quote_ident(t.ch_name) as ch_name,
                   t.ch_type::text as ch_type,
                   t.ch_fun::text as ch_fun
            from bdr.bdr_conflict_handlers t
            inner join pg_class c
            on c.oid = t.ch_reloid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where n.nspname = '{0}'
              and c.relname = '{1}'
        '''.format(p_schema, p_table))

    def TemplateBDRCreateGroup(self):
        return Template('''select bdr.bdr_group_create(
local_node_name := 'node_name'
, node_external_dsn := 'host={0} port={1} dbname={2}'
, node_local_dsn := 'dbname={2}'
--, apply_delay := NULL
--, replication_sets := ARRAY['default']
)
'''.format(self.v_server, self.v_port, self.v_service))

    def TemplateBDRJoinGroup(self):
        return Template('''select bdr.bdr_group_join(
local_node_name := 'node_name'
, node_external_dsn := 'host={0} port={1} dbname={2}'
, join_using_dsn := 'host= port= dbname='
, node_local_dsn := 'dbname={2}'
--, apply_delay := NULL
--, replication_sets := ARRAY['default']
)
'''.format(self.v_server, self.v_port, self.v_service))

    def TemplateBDRJoinWait(self):
        return Template('select bdr.bdr_node_join_wait_for_ready()')

    def TemplateBDRPause(self):
        return Template('select bdr.bdr_apply_pause()')

    def TemplateBDRResume(self):
        return Template('select bdr.bdr_apply_resume()')

    def TemplateBDRReplicateDDLCommand(self):
        return Template("select bdr.bdr_replicate_ddl_command('DDL command here...')")

    def TemplateBDRPartNode(self):
        return Template("select bdr.bdr_part_by_node_names('{#node_name#}')")

    def TemplateBDRInsertReplicationSet(self):
        return Template('''INSERT INTO bdr.bdr_replication_set_config (set_name, replicate_inserts, replicate_updates, replicate_deletes)
VALUES ('set_name', 't', 't', 't')
''')

    def TemplateBDRUpdateReplicationSet(self):
        return Template('''UPDATE bdr.bdr_replication_set_config SET
--replicate_inserts = { 't' | 'f' }
--, replicate_updates = { 't' | 'f' }
--, replicate_deletes = { 't' | 'f' }
WHERE set_name = '#set_name#'
''')

    def TemplateBDRDeleteReplicationSet(self):
        return Template('''DELETE
FROM bdr.bdr_replication_set_config
WHERE set_name = '#set_name#'
''')

    def TemplateBDRSetTableReplicationSets(self):
        return Template("select bdr.table_set_replication_sets('#table_name#', '{repset1,repset2,...}')")

    def TemplateBDRCreateConflictHandler(self):
        return Template('''CREATE OR REPLACE FUNCTION #table_name#_fnc_conflict_handler (
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
''')

    def TemplateBDRDropConflictHandler(self):
        return Template("select bdr.bdr_drop_conflict_handler('#table_name#', '#ch_name#')")

    # only in BDR >= 1

    def TemplateBDRTerminateApplyWorkers(self):
        return Template("select bdr.terminate_apply_workers('{#node_name#}')")

    def TemplateBDRTerminateWalsenderWorkers(self):
        return Template("select bdr.terminate_walsender_workers('{#node_name#}')")

    def TemplateBDRRemove(self):
        return Template('''select bdr.remove_bdr_from_local_node(
force := False
, convert_global_sequences := True
)
''')

    def QueryXLNodes(self):
        return self.v_connection.Query('''
            select quote_ident(node_name) as node_name,
                   (case node_type
                      when 'C' then 'coordinator'
                      when 'D' then 'datanode'
                    end) as node_type,
                   node_host,
                   node_port,
                   nodeis_primary,
                   nodeis_preferred
            from pgxc_node
            order by 1
        ''')

    def QueryXLGroups(self):
        return self.v_connection.Query('''
            select quote_ident(group_name) as group_name
            from pgxc_group
            order by 1
        ''')

    def QueryXLGroupNodes(self, p_group):
        return self.v_connection.Query('''
            select quote_ident(n.node_name) as node_name
            from (
            select unnest(group_members) as group_member
            from pgxc_group
            where group_name = '{0}'
            ) g
            inner join pgxc_node n
            on n.oid = g.group_member
            order by 1
        '''.format(p_group))

    def QueryTablesXLProperties(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(c.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and quote_ident(c.relname) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) as schema_name,
                   quote_ident(c.relname) as table_name,
                   (case x.pclocatortype
                      when 'R' then 'replication'
                      when 'N' then 'roundrobin'
                      when 'H' then 'hash (' || a.attname || ')'
                      when 'M' then 'modulo (' || a.attname || ')'
                    end) as distributed_by,
                   (t.num_nodes = d.num_nodes) as all_nodes
            from pgxc_class x
            inner join pg_class c
            on c.oid = x.pcrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            left join pg_attribute a
            on a.attrelid = c.oid
            and a.attnum = x.pcattnum
            inner join (
            select t.pcrelid,
                   count(*) as num_nodes
            from (
            select pcrelid,
                   unnest(nodeoids) as nodeoid
            from pgxc_class
            ) t
            group by t.pcrelid
            ) t
            on t.pcrelid = c.oid
            inner join (
            select count(*) as num_nodes
            from pgxc_node
            where node_type = 'D'
            ) d
            on 1=1
            where 1=1
            {0}
        '''.format(v_filter), True)

    def QueryTablesXLNodes(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(t.schema_name) = '{0}' and quote_ident(t.table_name) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(t.schema_name) = '{0}' and quote_ident(t.table_name) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(t.schema_name) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(t.schema_name) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(t.schema_name) not in ('information_schema','pg_catalog') and quote_ident(t.table_name) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(t.schema_name) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(t.schema_name) as schema_name,
                   quote_ident(t.table_name) as table_name,
                   quote_ident(n.node_name) as node_name
            from (
            select n.nspname as schema_name,
                   c.relname as table_name,
                   unnest(nodeoids) as nodeoid
            from pgxc_class x
            inner join pg_class c
            on c.oid = x.pcrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            ) t
            inner join pgxc_node n
            on n.oid = t.nodeoid
            where 1=1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def TemplateXLPauseCluster(self):
        return Template('PAUSE CLUSTER')

    def TemplateXLUnpauseCluster(self):
        return Template('UNPAUSE CLUSTER')

    def TemplateXLCleanConnection(self):
        return Template('''CLEAN CONNECTION TO
--COORDINATOR ( nodename [, ... ] )
--NODE ( nodename [, ... ] )
--ALL
--ALL FORCE
--FOR DATABASE database_name
--TO USER role_name
''')

    def TemplateXLCreateGroup(self):
        if 'XL' in self.GetVersion():
            v_text = '''-- This command needs to be executed in all nodes.
-- Please adjust the parameters in all commands below.

'''
            v_table = self.QueryXLNodes()
            for r in v_table.Rows:
                v_text = v_text + '''EXECUTE DIRECT ON ({0}) 'CREATE NODE GROUP name WITH ( nodename [, ... ] )'

'''.format(r['node_name'])
        else:
            v_text = ''
        return Template(v_text)

    def TemplateXLDropGroup(self):
        if 'XL' in self.GetVersion():
            v_text = '''-- This command needs to be executed in all nodes.

'''
            v_table = self.QueryXLNodes()
            for r in v_table.Rows:
                v_text = v_text + '''EXECUTE DIRECT ON ({0}) 'DROP NODE GROUP #group_name#'

'''.format(r['node_name'])
        else:
            v_text = ''
        return Template(v_text)

    def TemplateXLCreateNode(self):
        if 'XL' in self.GetVersion():
            v_text = '''-- This command needs to be executed in all nodes.
-- Please adjust the parameters in all commands below.

'''
            v_table = self.QueryXLNodes()
            for r in v_table.Rows:
                v_text = v_text + '''EXECUTE DIRECT ON ({0}) 'CREATE NODE name WITH (
TYPE = {{ coordinator | datanode }},
HOST = hostname,
PORT = portnum
--, PRIMARY
--, PREFERRED
)'

'''.format(r['node_name'])
        else:
            v_text = ''
        return Template(v_text)

    def TemplateXLAlterNode(self):
        if 'XL' in self.GetVersion():
            v_text = '''-- This command needs to be executed in all nodes.
-- Please adjust the parameters in all commands below.

'''
            v_table = self.QueryXLNodes()
            for r in v_table.Rows:
                v_text = v_text + '''EXECUTE DIRECT ON ({0}) 'ALTER NODE #node_name# WITH (
TYPE = {{ coordinator | datanode }},
HOST = hostname,
PORT = portnum
--, PRIMARY
--, PREFERRED
)'

'''.format(r['node_name'])
        else:
            v_text = ''
        return Template(v_text)

    def TemplateXLExecuteDirect(self):
        return Template('''EXECUTE DIRECT ON (#node_name#)
'SELECT ...'
''')

    def TemplateXLPoolReload(self):
        return Template('EXECUTE DIRECT ON (#node_name#) \'SELECT pgxc_pool_reload()\'')

    def TemplateXLDropNode(self):
        if 'XL' in self.GetVersion():
            v_text = '''-- This command needs to be executed in all nodes.

'''
            v_table = self.QueryXLNodes()
            for r in v_table.Rows:
                v_text = v_text + '''EXECUTE DIRECT ON ({0}) 'DROP NODE #node_name#'

'''.format(r['node_name'])
        else:
            v_text = ''
        return Template(v_text)

    def TemplateXLAlterTableDistribution(self):
        return Template('''ALTER TABLE #table_name# DISTRIBUTE BY
--REPLICATION
--ROUNDROBIN
--HASH ( column_name )
--MODULO ( column_name )
''')

    def TemplateXLAlterTableLocation(self):
        return Template('''ALTER TABLE #table_name#
TO NODE ( nodename [, ... ] )
--TO GROUP ( groupname [, ... ] )
''')

    def TemplateXLALterTableAddNode(self):
        return Template('ALTER TABLE #table_name# ADD NODE (node_name)')

    def TemplateXLAlterTableDeleteNode(self):
        return Template('ALTER TABLE #table_name# DELETE NODE (#node_name#)')
