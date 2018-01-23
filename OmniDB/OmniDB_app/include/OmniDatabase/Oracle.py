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
Oracle
------------------------------------------------------------------------
'''
class Oracle:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_conn_id=0, p_alias=''):
        self.v_alias = p_alias
        self.v_db_type = 'oracle'
        self.v_conn_id = p_conn_id

        if p_port is None or p_port == '':
            self.v_port = '1521'
        else:
            self.v_port = p_port
        if p_service is None or p_service == '':
            self.v_service = 'XE'
        else:
            self.v_service = p_service.upper()

        self.v_server = p_server
        self.v_user = p_user.upper()
        self.v_schema = p_user.upper()
        self.v_connection = Spartacus.Database.Oracle(p_server, p_port, p_service, p_user, p_password)

        self.v_has_schema = True
        self.v_has_functions = True
        self.v_has_procedures = True
        self.v_has_sequences = True
        self.v_has_primary_keys = True
        self.v_has_foreign_keys = True
        self.v_has_uniques = True
        self.v_has_indexes = True
        self.v_has_checks = False
        self.v_has_excludes = False
        self.v_has_rules = False
        self.v_has_triggers = False
        self.v_has_partitions = False

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
            "NO ACTION"
        ]
        self.v_delete_rules = [
            "NO ACTION",
			"SET NULL",
			"CASCADE"
        ]

    def GetName(self):
        return self.v_service

    def GetVersion(self):
        return self.v_connection.ExecuteScalar('''
            select (case when product like '%Express%'
                         then 'Oracle XE '
                         else 'Oracle '
                    end) || version
            from product_component_version
            where product like 'Oracle%'
        ''')

    def GetUserName(self):
        return self.v_user

    def GetUserSuper(self):
        return True

    def PrintDatabaseInfo(self):
        return self.v_user + '@' + self.v_service

    def PrintDatabaseDetails(self):
        return self.v_server + ':' + self.v_port

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):
        v_rules = ''
        if p_delete_rule.strip() != '':
            v_rules += ' on delete ' + p_delete_rule + ' '
        return v_rules

    def TestConnection(self):
        v_return = ''
        try:
            self.v_connection.Open()
            self.v_connection.Close()
            v_return = 'Connection successful.'
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
            select username as role_name
            from all_users
            order by 1
        ''', True)

    def QueryTablespaces(self):
        return self.v_connection.Query('''
            select tablespace_name
            from dba_tablespaces
            order by 1
        ''', True)

    def QueryDatabases(self):
        return self.v_connection.Query('''
            select name as database_name
            from v$database
            order by 1
        ''', True)

    def QueryTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and owner = '{0}' ".format(p_schema)
            else:
                v_filter = "and owner = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select table_name,
                   owner as table_schema
            from all_tables
            where 1 = 1
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and owner = '{0}' and table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and owner = '{0}' and table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and owner = '{0}' ".format(p_schema)
            else:
                v_filter = "and owner = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and table_name = '{0}'".format(p_table)
        return self.v_connection.Query('''
            select table_name,
                   column_name,
                   case when data_type = 'NUMBER' and data_scale = '0' then 'INTEGER' else data_type end as data_type,
                   case nullable when 'Y' then 'YES' else 'NO' end as nullable,
                   data_length,
                   data_precision,
                   data_scale
            from all_tab_columns
            where 1 = 1
            {0}
            order by table_name, column_id
        '''.format(v_filter), True)

    def QueryTablesForeignKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and constraint_info.owner = '{0}' and detail_table.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and constraint_info.owner = '{0}' and detail_table.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and constraint_info.owner = '{0}' ".format(p_schema)
            else:
                v_filter = "and constraint_info.owner = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and detail_table.table_name = {0}".format(p_table)
        return self.v_connection.Query('''
            select master_table.table_name as r_table_name,
                   master_table.owner as r_table_schema,
                   master_table.column_name as r_column_name,
                   detail_table.table_name,
                   detail_table.column_name,
                   detail_table.owner as table_schema,
                   constraint_info.constraint_name,
                   constraint_info.delete_rule,
                   'NO ACTION' as update_rule,
                   constraint_info.r_constraint_name,
                   detail_table.position as ordinal_position
            from user_constraints constraint_info,
                 user_cons_columns detail_table,
                 user_cons_columns master_table
            where constraint_info.constraint_name = detail_table.constraint_name
              and constraint_info.r_constraint_name = master_table.constraint_name
              and detail_table.position = master_table.position
              and constraint_info.constraint_type = 'R'
            {0}
            order by constraint_info.constraint_name,
                     detail_table.table_name,
                     detail_table.position
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and table_schema = '{0}' and table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and table_schema = '{0}' and table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and table_name = {0}".format(p_table)
        return self.v_connection.Query('''
            select distinct *
            from (
                select cons.constraint_name,
                       cols.column_name,
                       cols.table_name,
                       cons.owner as table_schema
                from all_constraints cons,
                     all_cons_columns cols,
                     all_tables t
                where cons.constraint_type = 'P'
                  and t.table_name = cols.table_name
                  and cons.constraint_name = cols.constraint_name
                  and cons.owner = cols.owner
                order by cons.owner,
                         cols.table_name,
                         cons.constraint_name,
                         cols.position
            )
            where 1 = 1
            {0}
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

    def QueryDataLimited(self, p_query, p_count=-1):
        if p_count != -1:
            try:
                self.v_connection.Open()
                v_data = self.v_connection.QueryBlock('select * from ( {0} ) t where rownum <= {1}'.format(p_query, p_count), p_count, True, True)
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
            v_limit = ' where rownum <= ' + p_count
        return self.v_connection.Query('''
            select *
            from (
            select {0}
            from {1} t
            {2}
            )
            {3}
        '''.format(
                p_column_list,
                p_table,
                p_filter,
                v_limit
            ), True, True
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
                v_filter = "and owner = '{0}' ".format(p_schema.upper())
            else:
                v_filter = "and owner = '{0}' ".format(self.v_schema.upper())
        return self.v_connection.Query('''
            select view_name as table_name,
                   owner as table_schema
            from all_views
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
