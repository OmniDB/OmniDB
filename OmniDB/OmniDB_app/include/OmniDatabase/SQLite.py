'''
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

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
        self.v_active_service = p_service
        self.v_user = ''
        self.v_active_user = ''
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
        self.v_has_triggers = True
        self.v_has_partitions = True
        self.v_has_statistics = False

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
        self.v_version = ''
        self.v_version_num = ''

    # Decorator to acquire lock before performing action
    def lock_required(function):
        def wrap(self, *args, **kwargs):
            try:
                if self.v_lock != None:
                    self.v_lock.acquire()
            except:
                None
            try:
                r = function(self, *args, **kwargs)
            except:
                try:
                    if self.v_lock != None:
                        self.v_lock.release()
                except:
                    None
                raise
            try:
                if self.v_lock != None:
                    self.v_lock.release()
            except:
                None
            return r
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap

    @lock_required
    def GetVersion(self):
        self.v_version = self.v_connection.ExecuteScalar('SELECT sqlite_version()')
        v_splitted_version = self.v_version.split('.')
        self.v_version_num = '{0}{1}{2}'.format(
            v_splitted_version[0].zfill(2),
            v_splitted_version[1].zfill(2),
            v_splitted_version[2].zfill(2)
        )
        return 'SQLite ' + self.v_version

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

    @lock_required
    def QueryTables(self):
        return self.v_connection.Query('''
            select name as table_name
		    from sqlite_master
			where type = 'table'
        ''', True)

    @lock_required
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

    @lock_required
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

    @lock_required
    def QueryTablesForeignKeysColumns(self, p_fkey, p_table=None):
        v_fk = Spartacus.Database.DataTable()

        v_fk.Columns = [
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

        v_fks_tmp = self.v_connection.Query("pragma foreign_key_list('{0}')".format(p_table), True)

        for v_row_tmp in v_fks_tmp.Rows:
            if (p_table + '_fk_' + str(v_row_tmp['id'])) == p_fkey:
                v_row = []
                v_row.append(v_row_tmp['table'])
                v_row.append(p_table)
                v_row.append(v_row_tmp['to'])
                v_row.append(v_row_tmp['from'])
                v_row.append(p_table + '_fk_' + str(v_row_tmp['id']))
                v_row.append(v_row_tmp['on_update'])
                v_row.append(v_row_tmp['on_delete'])
                v_row.append('')
                v_row.append('')
                v_fk.Rows.append(OrderedDict(zip(v_fk.Columns, v_row)))

        return v_fk

    @lock_required
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
                if r['pk'] != '0':
                    v_row = []
                    v_row.append('pk_' + v_table['table_name'])
                    v_row.append(r['name'])
                    v_row.append(v_table['table_name'])
                    v_pks.Rows.append(OrderedDict(zip(v_pks.Columns, v_row)))
            v_pks_all.Merge(v_pks)
        return v_pks_all

    @lock_required
    def QueryTablesPrimaryKeysColumns(self, p_table=None):
        v_pk_tmp = self.v_connection.Query("pragma table_info('{0}')".format(p_table), True)

        v_pk = Spartacus.Database.DataTable()
        v_pk.Columns = ['column_name']

        for v_row in v_pk_tmp.Rows:
            if v_row['pk'] != '0':
                v_row = [v_row['name']]
                v_pk.Rows.append(OrderedDict(zip(v_pk.Columns, v_row)))

        return v_pk

    @lock_required
    def QueryTablesUniques(self, p_table=None):
        v_uniques_all = Spartacus.Database.DataTable()

        v_uniques_all.Columns = [
            'constraint_name',
            'table_name'
        ]

        if p_table:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
                  and name = '{0}'
            '''.format(p_table), True)
        else:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
            ''', True)

        for v_table in v_tables.Rows:
            v_unique_count = -1

            v_uniques = self.v_connection.Query('''
                PRAGMA index_list('{0}')
            '''.format(
                v_table['name']
            ), True)

            for v_unique in v_uniques.Rows:
                if v_unique['origin'] == 'u':
                    v_unique_count += 1

                    v_uniques_all.AddRow([
                        'unique_{0}'.format(v_unique_count),
                        v_table['name']
                    ])

        return v_uniques_all

    @lock_required
    def QueryTablesUniquesColumns(self, p_unique, p_table=None):
        v_uniques_all = Spartacus.Database.DataTable()

        v_uniques_all.Columns = [
            'constraint_name',
            'column_name',
            'table_name'
        ]

        if p_table:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
                  and name = '{0}'
            '''.format(p_table), True)
        else:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
            ''', True)

        for v_table in v_tables.Rows:
            v_unique_count = -1

            v_uniques = self.v_connection.Query('''
                PRAGMA index_list('{0}')
            '''.format(
                v_table['name']
            ), True)

            for v_unique in v_uniques.Rows:
                if v_unique['origin'] == 'u':
                    v_unique_count += 1

                    if ('unique_{0}'.format(v_unique_count)) == p_unique:
                        v_unique_columns = self.v_connection.Query('''
                            PRAGMA index_info('{0}')
                        '''.format(
                            v_unique['name']
                        ), True)

                        for v_unique_column in v_unique_columns.Rows:
                            v_uniques_all.AddRow([
                                'unique_{0}'.format(v_unique_count),
                                v_unique_column['name'],
                                v_table['name']
                            ])

        return v_uniques_all

    @lock_required
    def QueryTablesIndexes(self, p_table=None):
        v_indexes_all = Spartacus.Database.DataTable()

        v_indexes_all.Columns = [
            'index_name',
            'table_name',
            'uniqueness'
        ]

        if p_table:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
                  and name = '{0}'
            '''.format(p_table), True)
        else:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
            ''', True)

        for v_table in v_tables.Rows:
            v_indexes = self.v_connection.Query('''
                PRAGMA index_list('{0}')
            '''.format(
                v_table['name']
            ), True)

            for v_index in v_indexes.Rows:
                if v_index['origin'] == 'c':
                    v_indexes_all.AddRow([
                        v_index['name'],
                        v_table['name'],
                        'Unique' if v_index['unique'] == '1' else 'Non Unique'
                    ])

        return v_indexes_all

    @lock_required
    def QueryTablesIndexesColumns(self, p_index, p_table=None):
        v_indexes_all = Spartacus.Database.DataTable()

        v_indexes_all.Columns = [
            'index_name',
            'column_name',
            'table_name'
        ]

        if p_table:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
                  and name = '{0}'
            '''.format(p_table), True)
        else:
            v_tables = self.v_connection.Query('''
                select name
                from sqlite_master
                where type = 'table'
            ''', True)

        for v_table in v_tables.Rows:
            v_indexes = self.v_connection.Query('''
                PRAGMA index_list('{0}')
            '''.format(
                v_table['name']
            ), True)

            for v_index in v_indexes.Rows:
                if v_index['origin'] == 'c':
                    if v_index['name'] == p_index:
                        v_index_columns = self.v_connection.Query('''
                            PRAGMA index_info('{0}')
                        '''.format(
                            v_index['name']
                        ), True)

                        for v_index_column in v_index_columns.Rows:
                            v_indexes_all.AddRow([
                                v_index['name'],
                                v_index_column['name'],
                                v_table['name']
                            ])

        return v_indexes_all

    @lock_required
    def QueryViews(self):
        return self.v_connection.Query('''
            select name as table_name
		    from sqlite_master
			where type = 'view'
        ''', True)

    @lock_required
    def QueryViewFields(self, p_table=None):
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

    @lock_required
    def QueryTablesTriggers(self, p_table=None):
        return self.v_connection.Query('''
            SELECT name AS trigger_name,
                   tbl_name AS table_name
            FROM sqlite_master
            WHERE type = 'trigger'
              AND tbl_name = '{0}'
        '''.format(
            p_table
        ), True)

    def TemplateSelect(self, p_table, p_kind):
        # table
        if p_kind == 't':
            v_sql = 'SELECT t.'
            v_fields = self.QueryTablesFields(p_table)

            if len(v_fields.Rows) > 0:
                v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])

            v_sql += '\nFROM {0} t'.format(p_table)

            v_pk = self.QueryTablesPrimaryKeys(p_table)

            if len(v_pk.Rows) > 0:
                v_fields = self.QueryTablesPrimaryKeysColumns(p_table)

                if len(v_fields.Rows) > 0:
                    v_sql += '\nORDER BY t.'
                    v_sql += '\n       , t.'.join([r['column_name'] for r in v_fields.Rows])
        # view
        elif p_kind == 'v':
            v_sql = 'SELECT t.'
            v_fields = self.QueryViewFields(p_table)

            if len(v_fields.Rows) > 0:
                v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])

            v_sql += '\nFROM {0} t'.format(p_table)

        return Template(v_sql)

    def TemplateInsert(self, p_table):
        v_fields = self.QueryTablesFields(p_table)

        if len(v_fields.Rows) > 0:
            v_sql = 'INSERT INTO {0} (\n'.format(p_table)
            v_pk = self.QueryTablesPrimaryKeys(p_table)

            if len(v_pk.Rows) > 0:
                v_table_pk_fields = self.QueryTablesPrimaryKeysColumns(p_table)
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

    def TemplateUpdate(self, p_table):
        v_fields = self.QueryTablesFields(p_table)

        if len(v_fields.Rows) > 0:
            v_sql = 'UPDATE {0}\nSET '.format(p_table)
            v_pk = self.QueryTablesPrimaryKeys(p_table)

            if len(v_pk.Rows) > 0:
                v_table_pk_fields = self.QueryTablesPrimaryKeysColumns(p_table)
                v_pk_fields = [r['column_name'] for r in v_table_pk_fields.Rows]
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

    @lock_required
    def QueryDataLimited(self, p_query, p_count=-1):
        if p_count != -1:
            self.v_connection.Open()
            v_data = self.v_connection.QueryBlock(p_query, p_count, True)
            self.v_connection.Close()
            return v_data
        else:
            return self.v_connection.Query(p_query, True)

    @lock_required
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

    def TemplateCreateView(self):
        return Template('''CREATE
--TEMPORARY
VIEW view_name
--( column_definition, ... )
AS
--SELECT...
''')

    def TemplateDropView(self):
        return Template('DROP VIEW #view_name#')

    def TemplateCreateTable(self):
        return Template('''CREATE
--TEMPORARY
TABLE table_name
(
    column_name data_type
    --CONSTRAINT constraint_name
    --NOT NULL
    --CHECK
    --UNIQUE
    --PRIMARY KEY
    --FOREIGN KEY
)
--WITHOUT ROWID
''')

    def TemplateAlterTable(self):
        return Template('''ALTER TABLE #table_name#
--RENAME TO new_table_name
--RENAME COLUMN column_name TO new_column_name
--ADD COLUMN columnd_definition
''')

    def TemplateDropTable(self):
        return Template('DROP TABLE #table_name#')

    def TemplateCreateColumn(self):
        return Template('''ALTER TABLE #table_name#
ADD COLUMN columnd_definition
''')

    def TemplateCreateIndex(self):
        return Template('''CREATE
--UNIQUE
INDEX index_name ON #table_name# ( column_name, ... )
--WHERE expression
''')

    def TemplateReindex(self):
        return Template('REINDEX #index_name#')

    def TemplateDropIndex(self):
        return Template('DROP INDEX #index_name#')

    def TemplateDelete(self):
        return Template('''DELETE FROM
#table_name#
WHERE condition
''')

    def TemplateCreateTrigger(self):
        return Template('''CREATE
--TEMPORARY
TRIGGER trigger_name
--BEFORE
--AFTER
--INSTEAD OF
--DELETE
--INSERT
--UPDATE
--OF column_name
ON #table_name#
--FOR EACH ROW
WHEN expression
BEGIN
    statement
;
END
''')

    def TemplateDropTrigger(self):
        return Template('DROP TRIGGER #trigger_name#')

    def GetAutocompleteValues(self, p_columns, p_filter):
        return None

    def GetErrorPosition(self, p_error_message):
        vector = str(p_error_message).split('\n')
        v_return = None

        if len(vector) > 1 and vector[1][0:4]=='LINE':
            v_return = {
                'row': vector[1].split(':')[0].split(' ')[1],
                'col': vector[2].index('^') - len(vector[1].split(':')[0])-2
            }

        return v_return
