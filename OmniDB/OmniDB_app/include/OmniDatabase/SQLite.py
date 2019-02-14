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
SQLite
------------------------------------------------------------------------
'''
class SQLite:
    def __init__(self, p_service, p_conn_id=0, p_alias='', p_foreignkeys=True):
        self.v_alias = p_alias
        self.v_db_type = 'sqlite'
        self.v_conn_string = ''
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
        self.v_has_checks = False
        self.v_has_excludes = False
        self.v_has_rules = False
        self.v_has_triggers = False
        self.v_has_partitions = True

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
        self.v_reserved_words = []
        self.v_console_help = "Console tab."
        self.v_use_server_cursor = False

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
