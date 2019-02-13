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
from urllib.parse import urlparse

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
MariaDB
------------------------------------------------------------------------
'''
class MariaDB:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_conn_id=0, p_alias='', p_conn_string='', p_parse_conn_string = False):
        self.v_alias = p_alias
        self.v_db_type = 'mariadb'
        self.v_conn_string = p_conn_string
        self.v_conn_string_error = ''
        self.v_conn_id = p_conn_id

        self.v_server = p_server
        self.v_active_server = p_server
        self.v_user = p_user
        self.v_active_user = p_user
        self.v_schema = p_service
        self.v_service = p_service
        self.v_active_service = p_service

        self.v_port = p_port
        if p_port is None or p_port == '':
            self.v_active_port = '3306'
        else:
            self.v_active_port = p_port

        #try to get info from connection string
        if p_conn_string!='' and p_parse_conn_string:
            try:
                parsed = urlparse(p_conn_string)
                if parsed.port!=None:
                    self.v_active_port = str(parsed.port)
                if parsed.hostname!=None:
                    self.v_active_server = parsed.hostname
                if parsed.username!=None:
                    self.v_active_user = parsed.username
                if parsed.query!=None:
                    self.v_conn_string_query = parsed.query
                parsed_database = parsed.path
                if len(parsed_database)>1:
                    self.v_active_service = parsed_database[1:]
            except Exception as exc:
                self.v_conn_string_error = 'Syntax error in the connection string.'
                None

        self.v_connection = Spartacus.Database.MariaDB(self.v_active_server, self.v_active_port, self.v_active_service, self.v_active_user, p_password, p_conn_string)

        self.v_has_schema = True
        self.v_has_functions = True
        self.v_has_procedures = True
        self.v_has_sequences = False
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
        self.v_alter_type_command = "alter table #p_table_name# modify #p_column_name# #p_new_data_type#"
        self.v_can_alter_nullable = True
        self.v_set_nullable_command = "alter table #p_table_name# modify #p_column_name# null"
        self.v_drop_nullable_command = "alter table #p_table_name# modify #p_column_name# not null"
        self.v_can_rename_column = True
        self.v_rename_column_command = "alter table #p_table_name# rename column #p_column_name# to #p_new_column_name#"
        self.v_can_add_column = True
        self.v_add_column_command = "alter table #p_table_name# add #p_column_name# #p_data_type# #p_nullable#"
        self.v_can_drop_column = True
        self.v_drop_column_command = "alter table #p_table_name# drop column #p_column_name#"
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
			"CASCADE"
        ]
        self.v_delete_rules = [
            "NO ACTION",
            "RESTRICT",
			"SET NULL",
			"CASCADE"
        ]
        self.v_reserved_words = []
        self.v_console_help = "Console tab. Type the commands in the editor below this box. \? to view command list."
        self.v_use_server_cursor = False

    def GetName(self):
        return self.v_service

    def GetVersion(self):
        return 'MariaDB ' + self.v_connection.ExecuteScalar('select version()')

    def GetUserName(self):
        return self.v_user

    def GetUserSuper(self):
        try:
            v_super = self.v_connection.ExecuteScalar('''
                select super_priv
                from mysql.user
                where user = '{0}'
            '''.format(self.v_user))
            if v_super == 'Y':
                return True
            else:
                return False
        except Exception as exc:
            return False

    def PrintDatabaseInfo(self):
        if self.v_conn_string=='':
            return self.v_active_user + '@' + self.v_active_service
        else:
            return self.v_active_user + '@' + self.v_active_service

    def PrintDatabaseDetails(self):
        if self.v_conn_string=='':
            return self.v_active_server + ':' + self.v_active_port
        else:
            return "<i title='{0}' class='fas fa-asterisk icon-conn-string'></i> ".format(self.v_conn_string) + self.v_active_server + ':' + self.v_active_port

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):
        v_rules = ''
        if p_update_rule.strip() != '':
            v_rules += ' on update ' + p_delete_rule + ' '
        if p_delete_rule.strip() != '':
            v_rules += ' on delete ' + p_delete_rule + ' '
        return v_rules

    def TestConnection(self):
        v_return = ''
        if self.v_conn_string and self.v_conn_string_error!='':
            return self.v_conn_string_error

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
        return self.v_connection.Query("""
            select concat('''',user,'''','@','''',host,'''') as role_name
            from mysql.user
            order by 1
        """, True)

    def QueryDatabases(self):
        return self.v_connection.Query('show databases', True, True)

    def QueryTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and table_schema = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select table_name,
                   table_schema
            from information_schema.tables
            where table_type in ('BASE TABLE', 'SYSTEM VIEW')
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct c.table_name as table_name,
                   c.column_name,
                   c.data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale,
                   c.ordinal_position
            from information_schema.columns c,
                 information_schema.tables t
            where t.table_name = c.table_name
              and t.table_type in ('BASE TABLE', 'SYSTEM VIEW')
            {0}
            order by c.table_name,
                     c.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesForeignKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and i.table_schema = '{0}' and i.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and i.table_schema = '{0}' and i.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and i.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and i.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and i.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct i.constraint_name,
                   i.table_name,
                   k.referenced_table_name as r_table_name,
                   k.table_schema,
                   k.referenced_table_schema as r_table_schema,
                   r.update_rule,
                   r.delete_rule
            from information_schema.table_constraints i
            left join information_schema.key_column_usage k on i.constraint_name = k.constraint_name
            left join information_schema.referential_constraints r on i.constraint_name = r.constraint_name
            where i.constraint_type = 'FOREIGN KEY'
            {0}
            order by i.constraint_name,
                     i.table_name
        '''.format(v_filter), True)

    def QueryTablesForeignKeysColumns(self, p_fkey, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and i.table_schema = '{0}' and i.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and i.table_schema = '{0}' and i.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and i.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and i.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and i.table_name = '{0}' ".format(p_table)
        v_filter = v_filter + "and i.constraint_name = '{0}' ".format(p_fkey)
        return self.v_connection.Query('''
            select distinct i.constraint_name,
                   i.table_name,
                   k.referenced_table_name as r_table_name,
                   k.column_name,
                   k.referenced_column_name as r_column_name,
                   k.table_schema,
                   k.referenced_table_schema as r_table_schema,
                   r.update_rule,
                   r.delete_rule,
                   k.ordinal_position
            from information_schema.table_constraints i
            left join information_schema.key_column_usage k on i.constraint_name = k.constraint_name
            left join information_schema.referential_constraints r on i.constraint_name = r.constraint_name
            where i.constraint_type = 'FOREIGN KEY'
            {0}
            order by i.constraint_name,
                     i.table_name,
                     k.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct concat('pk_', t.table_name) as constraint_name,
                   t.table_name,
                   t.table_schema
            from information_schema.table_constraints t
            where t.constraint_type = 'PRIMARY KEY'
            {0}
            order by t.table_schema,
                     t.table_name
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeysColumns(self, p_pkey, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        v_filter = "and concat('pk_', t.table_name) = '{0}' ".format(p_pkey)
        return self.v_connection.Query('''
            select distinct k.column_name,
                   k.ordinal_position
            from information_schema.table_constraints t
            join information_schema.key_column_usage k
            using (constraint_name, table_schema, table_name)
            where t.constraint_type = 'PRIMARY KEY'
            {0}
            order by k.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesUniques(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct t.constraint_name,
                   t.table_name,
                   t.table_schema
            from information_schema.table_constraints t
            where t.constraint_type = 'UNIQUE'
            {0}
            order by t.table_schema,
                     t.table_name
        '''.format(v_filter), True)

    def QueryTablesUniquesColumns(self, p_unique, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        v_filter = "and t.constraint_name = '{0}' ".format(p_unique)
        return self.v_connection.Query('''
            select distinct k.column_name,
                   k.ordinal_position
            from information_schema.table_constraints t
            join information_schema.key_column_usage k
            using (constraint_name, table_schema, table_name)
            where t.constraint_type = 'UNIQUE'
            {0}
            order by k.ordinal_position
        '''.format(v_filter), True)

    def QueryTablesIndexes(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct t.table_schema as schema_name,
                   t.table_name,
                   (case when t.index_name = 'PRIMARY' then concat('pk_', t.table_name) else t.index_name end) as index_name,
                   case when t.non_unique = 1 then 'Non Unique' else 'Unique' end as uniqueness
            from information_schema.statistics t
            where 1 = 1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    def QueryTablesIndexesColumns(self, p_index, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and t.table_schema = '{0}' and t.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and t.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and t.table_name = '{0}' ".format(p_table)
        v_filter = "and (case when t.index_name = 'PRIMARY' then concat('pk_', t.table_name) else t.index_name end) = '{0}' ".format(p_index)
        return self.v_connection.Query('''
            select distinct t.column_name,
                   t.seq_in_index
            from information_schema.statistics t
            where 1 = 1
            {0}
            order by t.seq_in_index
        '''.format(v_filter), True)

    def QueryDataLimited(self, p_query, p_count=-1):
        if p_count != -1:
            try:
                self.v_connection.Open()
                v_data = self.v_connection.QueryBlock('select * from ( {0} ) t limit {1}'.format(p_query, p_count), p_count, True, True)
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
            select *
            from (
            select {0}
            from {1} t
            {2}
            ) t
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
                v_filter = "and t.routine_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.routine_schema = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select t.routine_schema as schema_name,
                   t.routine_name as id,
                   t.routine_name as name
            from information_schema.routines t
            where t.routine_type = 'FUNCTION'
            {0}
            order by 2
        '''.format(v_filter), True)

    def QueryFunctionFields(self, p_function, p_schema):
        if p_schema:
            v_schema = p_schema
        else:
            v_schema = self.v_schema
        return self.v_connection.Query('''
            select 'O' as type,
                   concat('returns ', t.data_type) as name,
                   0 as seq
            from information_schema.routines t
            where t.routine_type = 'FUNCTION'
              and t.routine_schema = '{0}'
              and t.specific_name = '{1}'
            union
            select (case t.parameter_mode
                      when 'IN' then 'I'
                      when 'OUT' then 'O'
                      else 'R'
                    end) as type,
                   concat(t.parameter_name, ' ', t.data_type) as name,
                   t.ordinal_position+1 as seq
            from information_schema.parameters t
            where t.ordinal_position > 0
              and t.specific_schema = '{0}'
              and t.specific_name = '{1}'
            order by 3 desc
        '''.format(v_schema, p_function), True)

    def GetFunctionDefinition(self, p_function):
        v_body = '--DROP FUNCTION {0};\n'.format(p_function)
        v_body = v_body + self.v_connection.Query('show create function {0}.{1}'.format(self.v_schema, p_function), True, True).Rows[0][2]
        return v_body

    def QueryProcedures(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and t.routine_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and t.routine_schema = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select t.routine_schema as schema_name,
                   t.routine_name as id,
                   t.routine_name as name
            from information_schema.routines t
            where t.routine_type = 'PROCEDURE'
            {0}
            order by 2
        '''.format(v_filter), True)

    def QueryProcedureFields(self, p_procedure, p_schema):
        if p_schema:
            v_schema = p_schema
        else:
            v_schema = self.v_schema
        return self.v_connection.Query('''
            select (case t.parameter_mode
                      when 'IN' then 'I'
                      when 'OUT' then 'O'
                      else 'R'
                    end) as type,
                   concat(t.parameter_name, ' ', t.data_type) as name,
                   t.ordinal_position+1 as seq
            from information_schema.parameters t
            where t.specific_schema = '{0}'
              and t.specific_name = '{1}'
            order by 3 desc
        '''.format(v_schema, p_procedure), True)

    def GetProcedureDefinition(self, p_procedure):
        v_body = '--DROP PROCEDURE {0};\n'.format(p_procedure)
        v_body = v_body + self.v_connection.Query('show create procedure {0}.{1}'.format(self.v_schema, p_procedure), True, True).Rows[0][2]
        return v_body

    def QuerySequences(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and table_schema = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select table_name as sequence_name,
                   table_schema as sequence_schema
            from information_schema.tables
            where table_type = 'SEQUENCE'
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryViews(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and table_schema = '{0}' ".format(self.v_schema)
        return self.v_connection.Query('''
            select table_name,
                   table_schema
            from information_schema.views
            where 1=1
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    def QueryViewFields(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and c.table_schema = '{0}' and c.table_name = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and c.table_schema = '{0}' and c.table_name = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and c.table_schema = '{0}' ".format(p_schema)
            else:
                v_filter = "and c.table_schema = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and c.table_name = '{0}' ".format(p_table)
        return self.v_connection.Query('''
            select distinct c.table_name as table_name,
                   c.column_name,
                   c.data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale,
                   c.ordinal_position
            from information_schema.columns c,
                 information_schema.tables t
            where t.table_name = c.table_name
              and t.table_type = 'VIEW'
            {0}
            order by c.table_name,
                     c.ordinal_position
        '''.format(v_filter), True)

    def GetViewDefinition(self, p_view, p_schema):
        if p_schema:
            v_schema = p_schema
        else:
            v_schema = self.v_schema
        return self.v_connection.Query('show create view {0}.{1}'.format(v_schema, p_view), True, True).Rows[0][1]

    def TemplateCreateRole(self):
        return Template('''CREATE USER name
-- IDENTIFIED BY password
-- REQUIRE NONE
-- REQUIRE SSL
-- REQUIRE X509
-- REQUIRE CIPHER 'cipher'
-- REQUIRE ISSUER 'issuer'
-- REQUIRE SUBJECT 'subject'
-- WITH MAX_QUERIES_PER_HOUR count
-- WITH MAX_UPDATES_PER_HOUR count
-- WITH MAX_CONNECTIONS_PER_HOUR count
-- WITH MAX_USER_CONNECTIONS count
-- PASSWORD EXPIRE
-- ACCOUNT { LOCK | UNLOCK }
''')

    def TemplateAlterRole(self):
        return Template('''ALTER USER #role_name#
-- IDENTIFIED BY password
-- REQUIRE NONE
-- REQUIRE SSL
-- REQUIRE X509
-- REQUIRE CIPHER 'cipher'
-- REQUIRE ISSUER 'issuer'
-- REQUIRE SUBJECT 'subject'
-- WITH MAX_QUERIES_PER_HOUR count
-- WITH MAX_UPDATES_PER_HOUR count
-- WITH MAX_CONNECTIONS_PER_HOUR count
-- WITH MAX_USER_CONNECTIONS count
-- PASSWORD EXPIRE
-- ACCOUNT { LOCK | UNLOCK }
-- RENAME USER #role_name# TO new_name
-- SET PASSWORD FOR #role_name# = password
''')

    def TemplateDropRole(self):
        return Template('DROP USER #role_name#')

    def TemplateCreateDatabase(self):
        return Template('''CREATE DATABASE name
-- CHARACTER SET charset
-- COLLATE collate
''')

    def TemplateAlterDatabase(self):
        return Template('''ALTER DATABASE #database_name#
-- CHARACTER SET charset
-- COLLATE collate
''')

    def TemplateDropDatabase(self):
        return Template('DROP DATABASE #database_name#')

    def TemplateCreateFunction(self):
        return Template('''CREATE FUNCTION #schema_name#.name
(
-- argname argtype
)
RETURNS rettype
BEGIN
-- DECLARE variables
-- definition
-- RETURN variable | value
END;
''')

    def TemplateDropFunction(self):
        return Template('DROP FUNCTION #function_name#')

    def TemplateCreateProcedure(self):
        return Template('''CREATE PROCEDURE #schema_name#.name
(
-- [argmode] argname argtype
)
BEGIN
-- DECLARE variables
-- definition
END;
''')

    def TemplateDropProcedure(self):
        return Template('DROP PROCEDURE #function_name#')

    def TemplateCreateTable(self):
        return Template('''CREATE
-- TEMPORARY
TABLE #schema_name#.table_name
-- AS query
(
    column_name data_type
    -- NOT NULL
    -- NULL
    -- DEFAULT default_value
    -- AUTO_INCREMENT
    -- UNIQUE
    -- PRIMARY KEY
    -- COMMENT 'string'
    -- COLUMN_FORMAT { FIXED | DYNAMIC | DEFAULT }
    -- STORAGE { DISK | MEMORY | DEFAULT }
    -- [ GENERATED ALWAYS ] AS (expression) [ VIRTUAL | STORED ]
    -- [ CONSTRAINT [ symbol ] ] PRIMARY KEY [ USING { BTREE | HASH } ] ( column_name, ... )
    -- { INDEX | KEY } [ index_name ] [ USING { BTREE | HASH } ] ( column_name, ... )
    -- [ CONSTRAINT [ symbol ] ] UNIQUE [ INDEX | KEY ] [ index_name ] [ USING { BTREE | HASH } ] ( column_name, ... )
    -- { FULLTEXT | SPATIAL } [ INDEX | KEY ] [ index_name ] [ USING { BTREE | HASH } ] ( column_name, ... )
    -- [ CONSTRAINT [ symbol ] ] FOREIGN KEY [ index_name ]  ( column_name, ... ) REFERENCES reftable ( refcolumn, ... ) [MATCH FULL | MATCH PARTIAL | MATCH SIMPLE] [ON DELETE { RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT }] [ON UPDATE { RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT }]
    -- CHECK ( expr )
)
-- AUTO_INCREMENT value
-- AVG_ROW_LENGTH value
-- [ DEFAULT ] CHARACTER SET charset_name
-- CHECKSUM { 0 | 1 }
-- [ DEFAULT ] COLLATE collation_name
-- COMMENT 'string'
-- COMPRESSION { 'ZLIB' | 'LZ4' | 'NONE' }
-- CONNECTION 'connect_string'
-- { DATA | INDEX } DIRECTORY 'absolute path to directory'
-- DELAY_KEY_WRITE { 0 | 1 }
-- ENCRYPTION { 'Y' | 'N' }
-- ENGINE engine_name
-- INSERT_METHOD { NO | FIRST | LAST }
-- KEY_BLOCK_SIZE value
-- MAX_ROWS value
-- MIN_ROWS value
-- PACK_KEYS { 0 | 1 | DEFAULT }
-- PASSWORD 'string'
-- ROW_FORMAT { DEFAULT | DYNAMIC | FIXED | COMPRESSED | REDUNDANT | COMPACT }
-- STATS_AUTO_RECALC { DEFAULT | 0 | 1 }
-- STATS_PERSISTENT { DEFAULT | 0 | 1 }
-- STATS_SAMPLE_PAGES value
-- TABLESPACE tablespace_name [STORAGE { DISK | MEMORY | DEFAULT } ]
''')

    def TemplateAlterTable(self):
        return Template('''ALTER TABLE #table_name#
-- ADD [ COLUMN ] col_name column_definition  [ FIRST | AFTER col_name ]
-- ADD [ COLUMN ] ( col_name column_definition , ... )
-- ADD { INDEX | KEY } [ index_name ] USING { BTREE | HASH } (index_col_name , ... )
-- ADD [ CONSTRAINT [ symbol ] ] PRIMARY KEY USING { BTREE | HASH } ( index_col_name , ... )
-- ADD [ CONSTRAINT [ symbol ] ] UNIQUE [ INDEX | KEY ] [ index_name ] USING { BTREE | HASH } ( index_col_name , ... )
-- ADD FULLTEXT [ INDEX | KEY ] ( index_col_name , ... )
-- ADD SPATIAL [ INDEX | KEY ] [ index_name ] (index_col_name , ... )
-- ADD [ CONSTRAINT [ symbol ] ] FOREIGN KEY [ index_name ] ( index_col_name , ... ) reference_definition
-- ALGORITHM { DEFAULT | INPLACE | COPY }
-- ALTER [ COLUMN ] col_name { SET DEFAULT literal | DROP DEFAULT }
-- CHANGE [ COLUMN ] old_col_name new_col_name column_definition [ FIRST | AFTER col_name ]
-- [DEFAULT] CHARACTER SET charset_name [ COLLATE collation_name ]
-- CONVERT TO CHARACTER SET charset_name [ COLLATE collation_name ]
-- { DISABLE | ENABLE } KEYS
-- { DISCARD | IMPORT } TABLESPACE
-- DROP [ COLUMN ] col_name
-- DROP { INDEX | KEY } index_name
-- DROP PRIMARY KEY
-- DROP FOREIGN KEY fk_symbol
-- FORCE
-- LOCK { DEFAULT | NONE | SHARED | EXCLUSIVE }
-- MODIFY [ COLUMN ] col_name column_definition [ FIRST | AFTER col_name ]
-- ORDER BY col_name [, col_name] ...
-- RENAME { INDEX | KEY } old_index_name TO new_index_name
-- RENAME [ TO | AS ] new_tbl_name
-- { WITHOUT | WITH } VALIDATION
-- ADD PARTITION ( partition_definition )
-- DROP PARTITION partition_names
-- DISCARD PARTITION { partition_names | ALL } TABLESPACE
-- IMPORT PARTITION { partition_names | ALL } TABLESPACE
-- TRUNCATE PARTITION { partition_names | ALL }
-- COALESCE PARTITION number
-- REORGANIZE PARTITION partition_names INTO ( partition_definitions )
-- EXCHANGE PARTITION partition_name WITH TABLE tbl_name [ { WITH | WITHOUT } VALIDATION ]
-- ANALYZE PARTITION { partition_names | ALL }
-- CHECK PARTITION { partition_names | ALL }
-- OPTIMIZE PARTITION { partition_names | ALL }
-- REBUILD PARTITION { partition_names | ALL }
-- REPAIR PARTITION { partition_names | ALL }
-- REMOVE PARTITIONING
-- UPGRADE PARTITIONING
-- AUTO_INCREMENT value
-- AVG_ROW_LENGTH value
-- [ DEFAULT ] CHARACTER SET charset_name
-- CHECKSUM { 0 | 1 }
-- [ DEFAULT ] COLLATE collation_name
-- COMMENT 'string'
-- COMPRESSION { 'ZLIB' | 'LZ4' | 'NONE' }
-- CONNECTION 'connect_string'
-- { DATA | INDEX } DIRECTORY 'absolute path to directory'
-- DELAY_KEY_WRITE { 0 | 1 }
-- ENCRYPTION { 'Y' | 'N' }
-- ENGINE engine_name
-- INSERT_METHOD { NO | FIRST | LAST }
-- KEY_BLOCK_SIZE value
-- MAX_ROWS value
-- MIN_ROWS value
-- PACK_KEYS { 0 | 1 | DEFAULT }
-- PASSWORD 'string'
-- ROW_FORMAT { DEFAULT | DYNAMIC | FIXED | COMPRESSED | REDUNDANT | COMPACT }
-- STATS_AUTO_RECALC { DEFAULT | 0 | 1 }
-- STATS_PERSISTENT { DEFAULT | 0 | 1 }
-- STATS_SAMPLE_PAGES value
-- TABLESPACE tablespace_name [STORAGE { DISK | MEMORY | DEFAULT } ]
''')

    def TemplateDropTable(self):
        return Template('''DROP TABLE #table_name#
-- RESTRICT
-- CASCADE
''')

    def TemplateCreateColumn(self):
        return Template('''ALTER TABLE #table_name#
ADD name data_type
--DEFAULT expr
--NOT NULL
''')

    def TemplateAlterColumn(self):
        return Template('''ALTER TABLE #table_name#
-- ALTER #column_name# { datatype | DEFAULT expr | [ NULL | NOT NULL ]}
-- CHANGE COLUMN #column_name# TO new_name
'''
)

    def TemplateDropColumn(self):
        return Template('''ALTER TABLE #table_name#
DROP COLUMN #column_name#
''')

    def TemplateCreatePrimaryKey(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
PRIMARY KEY ( column_name [, ... ] )
''')

    def TemplateDropPrimaryKey(self):
        return Template('''ALTER TABLE #table_name#
DROP PRIMARY KEY #constraint_name#
--CASCADE
''')

    def TemplateCreateUnique(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
UNIQUE ( column_name [, ... ] )
''')

    def TemplateDropUnique(self):
        return Template('''ALTER TABLE #table_name#
DROP #constraint_name#
''')

    def TemplateCreateForeignKey(self):
        return Template('''ALTER TABLE #table_name#
ADD CONSTRAINT name
FOREIGN KEY ( column_name [, ... ] )
REFERENCES reftable [ ( refcolumn [, ... ] ) ]
''')

    def TemplateDropForeignKey(self):
        return Template('''ALTER TABLE #table_name#
DROP FOREIGN KEY #constraint_name#
''')

    def TemplateCreateIndex(self):
        return Template('''CREATE [ UNIQUE ] INDEX name
ON #table_name#
( { column_name | ( expression ) } [ ASC | DESC ] )
''')

    def TemplateDropIndex(self):
        return Template('DROP INDEX #index_name#')

    def TemplateCreateSequence(self):
        return Template('''CREATE SEQUENCE #schema_name#.name
--INCREMENT BY increment
--MINVALUE minvalue | NOMINVALUE
--MAXVALUE maxvalue | NOMAXVALUE
--START WITH start
--CACHE cache | NOCACHE
--CYCLE | NOCYCLE
''')

    def TemplateAlterSequence(self):
        return Template('''ALTER SEQUENCE #sequence_name#
--INCREMENT BY increment
--MINVALUE minvalue | NOMINVALUE
--MAXVALUE maxvalue | NOMAXVALUE
--START WITH start
--CACHE cache | NOCACHE
--CYCLE | NOCYCLE
--RESTART WITH restart
''')

    def TemplateDropSequence(self):
        return Template('DROP SEQUENCE #sequence_name#')

    def TemplateCreateView(self):
        return Template('''CREATE OR REPLACE VIEW #schema_name#.name AS
SELECT ...
''')

    def TemplateDropView(self):
        return Template('''DROP VIEW #view_name#
-- RESTRICT
-- CASCADE
''')

    def TemplateSelect(self, p_schema, p_table):
        v_sql = 'SELECT t.'
        v_fields = self.QueryTablesFields(p_table, False, p_schema)
        if len(v_fields.Rows) > 0:
            v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])
        v_sql += '\nFROM {0}.{1} t'.format(p_schema, p_table)
        v_pk = self.QueryTablesPrimaryKeys(p_table, False, p_schema)
        if len(v_pk.Rows) > 0:
            v_fields = self.QueryTablesPrimaryKeysColumns(v_pk.Rows[0]['constraint_name'], p_table, False, p_schema)
            if len(v_fields.Rows) > 0:
                v_sql += '\nORDER BY t.'
                v_sql += '\n       , t.'.join([r['column_name'] for r in v_fields.Rows])
        return Template(v_sql)

    def TemplateInsert(self, p_schema, p_table):
        v_fields = self.QueryTablesFields(p_table, False, p_schema)
        if len(v_fields.Rows) > 0:
            v_sql = 'INSERT INTO {0}.{1} (\n'.format(p_schema, p_table)
            v_pk = self.QueryTablesPrimaryKeys(p_table, False, p_schema)
            if len(v_pk.Rows) > 0:
                v_table_pk_fields = self.QueryTablesPrimaryKeysColumns(v_pk.Rows[0]['constraint_name'], p_table, False, p_schema)
                v_pk_fields = [r['column_name'] for r in v_table_pk_fields.Rows]
                v_values = []
                v_first = True
                for r in v_fields.Rows:
                    if v_first:
                        v_sql += '      {0}'.format(r['column_name'])
                        if r['column_name'] in v_pk_fields:
                            v_values.append('      ? -- {0} {1} PRIMARY KEY'.format(r['column_name'], r['data_type']))
                        elif r['nullable'] == 'YES':
                            v_values.append('      ? -- {0} {1} NULLABLE'.format(r['column_name'], r['data_type']))
                        else:
                            v_values.append('      ? -- {0} {1}'.format(r['column_name'], r['data_type']))
                        v_first = False
                    else:
                        v_sql += '\n    , {0}'.format(r['column_name'])
                        if r['column_name'] in v_pk_fields:
                            v_values.append('\n    , ? -- {0} {1} PRIMARY KEY'.format(r['column_name'], r['data_type']))
                        elif r['nullable'] == 'YES':
                            v_values.append('\n    , ? -- {0} {1} NULLABLE'.format(r['column_name'], r['data_type']))
                        else:
                            v_values.append('\n    , ? -- {0} {1}'.format(r['column_name'], r['data_type']))
            else:
                v_values = []
                v_first = True
                for r in v_fields.Rows:
                    if v_first:
                        v_sql += '      {0}'.format(r['column_name'])
                        if r['nullable'] == 'YES':
                            v_values.append('      ? -- {0} {1} NULLABLE'.format(r['column_name'], r['data_type']))
                        else:
                            v_values.append('      ? -- {0} {1}'.format(r['column_name'], r['data_type']))
                        v_first = False
                    else:
                        v_sql += '\n    , {0}'.format(r['column_name'])
                        if r['nullable'] == 'YES':
                            v_values.append('\n    , ? -- {0} {1} NULLABLE'.format(r['column_name'], r['data_type']))
                        else:
                            v_values.append('\n    , ? -- {0} {1}'.format(r['column_name'], r['data_type']))
            v_sql += '\n) VALUES (\n'
            for v in v_values:
                v_sql += v
            v_sql += '\n)'
        else:
            v_sql = ''
        return Template(v_sql)

    def TemplateUpdate(self, p_schema, p_table):
        v_fields = self.QueryTablesFields(p_table, False, p_schema)
        if len(v_fields.Rows) > 0:
            v_sql = 'UPDATE {0}.{1}\nSET '.format(p_schema, p_table)
            v_pk = self.QueryTablesPrimaryKeys(p_table, False, p_schema)
            if len(v_pk.Rows) > 0:
                v_table_pk_fields = self.QueryTablesPrimaryKeysColumns(v_pk.Rows[0]['constraint_name'], p_table, False, p_schema)
                v_pk_fields = [r['column_name'] for r in v_table_pk_fields.Rows]
                v_values = []
                v_first = True
                for r in v_fields.Rows:
                    if v_first:
                        if r['column_name'] in v_pk_fields:
                            v_sql += '{0} = ? -- {1} PRIMARY KEY'.format(r['column_name'], r['data_type'])
                        elif r['nullable'] == 'YES':
                            v_sql += '{0} = ? -- {1} NULLABLE'.format(r['column_name'], r['data_type'])
                        else:
                            v_sql += '{0} = ? -- {1}'.format(r['column_name'], r['data_type'])
                        v_first = False
                    else:
                        if r['column_name'] in v_pk_fields:
                            v_sql += '\n    , {0} = ? -- {1} PRIMARY KEY'.format(r['column_name'], r['data_type'])
                        elif r['nullable'] == 'YES':
                            v_sql += '\n    , {0} = ? -- {1} NULLABLE'.format(r['column_name'], r['data_type'])
                        else:
                            v_sql += '\n    , {0} = ? -- {1}'.format(r['column_name'], r['data_type'])
            else:
                v_values = []
                v_first = True
                for r in v_fields.Rows:
                    if v_first:
                        if r['nullable'] == 'YES':
                            v_sql += '{0} = ? -- {1} NULLABLE'.format(r['column_name'], r['data_type'])
                        else:
                            v_sql += '{0} = ? -- {1}'.format(r['column_name'], r['data_type'])
                        v_first = False
                    else:
                        if r['nullable'] == 'YES':
                            v_sql += '\n    , {0} = ? -- {1} NULLABLE'.format(r['column_name'], r['data_type'])
                        else:
                            v_sql += '\n    , {0} = ? -- {1}'.format(r['column_name'], r['data_type'])
            v_sql += '\nWHERE condition'
        else:
            v_sql = ''
        return Template(v_sql)

    def TemplateDelete(self):
        return Template('''DELETE FROM #table_name#
WHERE condition
''')

    def GetProperties(self, p_schema, p_table, p_object, p_type):
        if p_type == 'table':
            return self.v_connection.Query('''
                select table_schema as "Table Schema",
                       table_name as "Table Name",
                       table_type as "Table Type",
                       engine as "Engine",
                       version as "Version",
                       row_format as "Row Format",
                       table_rows as "Table Rows",
                       avg_row_length as "Average Row Length",
                       data_length as "Data Length",
                       max_data_length as "Max Data Length",
                       index_length as "Index Length",
                       data_free as "Data Free",
                       auto_increment as "Auto Increment",
                       create_time as "Create Time",
                       update_time as "Update Time",
                       check_time as "Check Time",
                       table_collation as "Table Collaction",
                       checksum as "Checksum"
                from information_schema.tables
                where table_schema = '{0}'
                  and table_name = '{1}'
            '''.format(p_schema, p_object), True).Transpose('Property', 'Value')
        elif p_type == 'view':
            return self.v_connection.Query('''
                select table_schema as "View Schema",
                       table_name as "View Name",
                       check_option as "Check Option",
                       is_updatable as "Is Updatable",
                       security_type as "Security Type",
                       character_set_client as "Character Set Client",
                       collation_connection as "Collation Connection",
                       algorithm as "Algorithm"
                from information_schema.views
                where table_schema = '{0}'
                  and table_name = '{1}'
            '''.format(p_schema, p_object), True).Transpose('Property', 'Value')
        elif p_type == 'function':
            return self.v_connection.Query('''
                select routine_schema as "Routine Schema",
                       routine_name as "Routine Name",
                       routine_type as "Routine Type",
                       data_type as "Data Type",
                       character_maximum_length as "Character Maximum Length",
                       character_octet_length as "Character Octet Length",
                       numeric_precision as "Numeric Precision",
                       numeric_scale as "Numeric Scale",
                       datetime_precision as "Datetime Precision",
                       character_set_name as "Character Set Name",
                       collation_name as "Collation Name",
                       routine_body as "Routine Body",
                       external_name as "External Name",
                       external_language as "External Language",
                       parameter_style as "Parameter Style",
                       is_deterministic as "Is Deterministic",
                       sql_data_access as "SQL Data Access",
                       sql_path as "SQL Path",
                       security_type as "Security Type",
                       created as "Created",
                       last_altered as "Last Altered",
                       character_set_client as "Character Set Client",
                       collation_connection as "Collation Connection",
                       database_collation as "Database Collation"
                from information_schema.routines
                where routine_type = 'FUNCTION'
                  and routine_schema = '{0}'
                  and routine_name = '{1}'
            '''.format(p_schema, p_object), True).Transpose('Property', 'Value')
        elif p_type == 'procedure':
            return self.v_connection.Query('''
                select routine_schema as "Routine Schema",
                       routine_name as "Routine Name",
                       routine_type as "Routine Type",
                       data_type as "Data Type",
                       character_maximum_length as "Character Maximum Length",
                       character_octet_length as "Character Octet Length",
                       numeric_precision as "Numeric Precision",
                       numeric_scale as "Numeric Scale",
                       datetime_precision as "Datetime Precision",
                       character_set_name as "Character Set Name",
                       collation_name as "Collation Name",
                       routine_body as "Routine Body",
                       external_name as "External Name",
                       external_language as "External Language",
                       parameter_style as "Parameter Style",
                       is_deterministic as "Is Deterministic",
                       sql_data_access as "SQL Data Access",
                       sql_path as "SQL Path",
                       security_type as "Security Type",
                       created as "Created",
                       last_altered as "Last Altered",
                       character_set_client as "Character Set Client",
                       collation_connection as "Collation Connection",
                       database_collation as "Database Collation"
                from information_schema.routines
                where routine_type = 'PROCEDURE'
                  and routine_schema = '{0}'
                  and routine_name = '{1}'
            '''.format(p_schema, p_object), True).Transpose('Property', 'Value')
        elif p_type == 'sequence':
            return self.v_connection.Query('''
                select next_not_cached_value as "Next Not Cached Value",
                       minimum_value as "Min Value",
                       maximum_value as "Max Value",
                       start_value as "Start Value",
                       increment as "Increment By",
                       cache_size as "Cache Size",
                       (case when 0 then 'No Cycle' else 'Cycle' end) as "Cycle Option",
                       cycle_count as "Cycle Count"
                from {0}.{1}
            '''.format(p_schema, p_object), True).Transpose('Property', 'Value')
        else:
            return None

    def GetDDL(self, p_schema, p_table, p_object, p_type):
        if p_type == 'function' or p_type == 'procedure':
            return self.v_connection.Query('show create {0} {1}.{2}'.format(p_type, p_schema, p_object), True, True).Rows[0][2]
        else:
            return self.v_connection.Query('show create {0} {1}.{2}'.format(p_type, p_schema, p_object), True, True).Rows[0][1]

    def GetAutocompleteValues(self, p_columns, p_filter):
        return None
