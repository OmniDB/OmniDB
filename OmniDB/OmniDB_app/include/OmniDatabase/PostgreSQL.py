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
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_conn_id=0, p_alias='', p_application_name='OmniDB', p_conn_string='', p_parse_conn_string = False):
        self.v_alias = p_alias
        self.v_db_type = 'postgresql'
        self.v_conn_id = p_conn_id
        self.v_conn_string = p_conn_string
        self.v_conn_string_error = ''

        self.v_port = p_port
        if p_port is None or p_port == '':
            self.v_active_port = '5432'
        else:
            self.v_active_port = p_port
        self.v_service = p_service
        if p_service is None or p_service == '':
            self.v_active_service = 'postgres'
        else:
            self.v_active_service = p_service
        self.v_server = p_server
        self.v_active_server = p_server
        self.v_user = p_user
        self.v_active_user = p_user
        self.v_conn_string_query = ''
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


        self.v_schema = 'public'
        self.v_connection = Spartacus.Database.PostgreSQL(self.v_active_server, self.v_active_port, self.v_active_service, self.v_active_user, p_password, p_application_name, p_conn_string)

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
        self.v_reserved_words = [
            'ABORT',
            'ABS',
            'ABSOLUTE',
            'ACCESS',
            'ACTION',
            'ADA',
            'ADD',
            'ADMIN',
            'AFTER',
            'AGGREGATE',
            'ALIAS',
            'ALL',
            'ALLOCATE',
            'ALTER',
            'ANALYSE',
            'ANALYZE',
            'AND',
            'ANY',
            'ARE',
            'ARRAY',
            'AS',
            'ASC',
            'ASENSITIVE',
            'ASSERTION',
            'ASSIGNMENT',
            'ASYMMETRIC',
            'AT',
            'ATOMIC',
            'AUTHORIZATION',
            'AVG',
            'BACKWARD',
            'BEFORE',
            'BEGIN',
            'BETWEEN',
            'BIGINT',
            'BINARY',
            'BIT',
            'BITVAR',
            'BIT_LENGTH',
            'BLOB',
            'BOOLEAN',
            'BOTH',
            'BREADTH',
            'BY',
            'C',
            'CACHE',
            'CALL',
            'CALLED',
            'CARDINALITY',
            'CASCADE',
            'CASCADED',
            'CASE',
            'CAST',
            'CATALOG',
            'CATALOG_NAME',
            'CHAIN',
            'CHAR',
            'CHARACTER',
            'CHARACTERISTICS',
            'CHARACTER_LENGTH',
            'CHARACTER_SET_CATALOG',
            'CHARACTER_SET_NAME',
            'CHARACTER_SET_SCHEMA',
            'CHAR_LENGTH',
            'CHECK',
            'CHECKED',
            'CHECKPOINT',
            'CLASS',
            'CLASS_ORIGIN',
            'CLOB',
            'CLOSE',
            'CLUSTER',
            'COALESCE',
            'COBOL',
            'COLLATE',
            'COLLATION',
            'COLLATION_CATALOG',
            'COLLATION_NAME',
            'COLLATION_SCHEMA',
            'COLUMN',
            'COLUMN_NAME',
            'COMMAND_FUNCTION',
            'COMMAND_FUNCTION_CODE',
            'COMMENT',
            'COMMIT',
            'COMMITTED',
            'COMPLETION',
            'CONDITION_NUMBER',
            'CONNECT',
            'CONNECTION',
            'CONNECTION_NAME',
            'CONSTRAINT',
            'CONSTRAINTS',
            'CONSTRAINT_CATALOG',
            'CONSTRAINT_NAME',
            'CONSTRAINT_SCHEMA',
            'CONSTRUCTOR',
            'CONTAINS',
            'CONTINUE',
            'CONVERSION',
            'CONVERT',
            'COPY',
            'CORRESPONDING',
            'COUNT',
            'CREATE',
            'CREATEDB',
            'CREATEUSER',
            'CROSS',
            'CUBE',
            'CURRENT',
            'CURRENT_DATE',
            'CURRENT_PATH',
            'CURRENT_ROLE',
            'CURRENT_TIME',
            'CURRENT_TIMESTAMP',
            'CURRENT_USER',
            'CURSOR',
            'CURSOR_NAME',
            'CYCLE',
            'DATA',
            'DATABASE',
            'DATE',
            'DATETIME_INTERVAL_CODE',
            'DATETIME_INTERVAL_PRECISION',
            'DAY',
            'DEALLOCATE',
            'DEC',
            'DECIMAL',
            'DECLARE',
            'DEFAULT',
            'DEFERRABLE',
            'DEFERRED',
            'DEFINED',
            'DEFINER',
            'DELETE',
            'DELIMITER',
            'DELIMITERS',
            'DEPTH',
            'DEREF',
            'DESC',
            'DESCRIBE',
            'DESCRIPTOR',
            'DESTROY',
            'DESTRUCTOR',
            'DETERMINISTIC',
            'DIAGNOSTICS',
            'DICTIONARY',
            'DISCONNECT',
            'DISPATCH',
            'DISTINCT',
            'DO',
            'DOMAIN',
            'DOUBLE',
            'DROP',
            'DYNAMIC',
            'DYNAMIC_FUNCTION',
            'DYNAMIC_FUNCTION_CODE',
            'EACH',
            'ELSE',
            'ENCODING',
            'ENCRYPTED',
            'END',
            'END-EXEC',
            'EQUALS',
            'ESCAPE',
            'EVERY',
            'EXCEPT',
            'EXCEPTION',
            'EXCLUSIVE',
            'EXEC',
            'EXECUTE',
            'EXISTING',
            'EXISTS',
            'EXPLAIN',
            'EXTERNAL',
            'EXTRACT',
            'FALSE',
            'FETCH',
            'FINAL',
            'FIRST',
            'FLOAT',
            'FOR',
            'FORCE',
            'FOREIGN',
            'FORTRAN',
            'FORWARD',
            'FOUND',
            'FREE',
            'FREEZE',
            'FROM',
            'FULL',
            'FUNCTION',
            'G',
            'GENERAL',
            'GENERATED',
            'GET',
            'GLOBAL',
            'GO',
            'GOTO',
            'GRANT',
            'GRANTED',
            'GROUP',
            'GROUPING',
            'HANDLER',
            'HAVING',
            'HIERARCHY',
            'HOLD',
            'HOST',
            'HOUR',
            'IDENTITY',
            'IGNORE',
            'ILIKE',
            'IMMEDIATE',
            'IMMUTABLE',
            'IMPLEMENTATION',
            'IMPLICIT',
            'IN',
            'INCREMENT',
            'INDEX',
            'INDICATOR',
            'INFIX',
            'INHERITS',
            'INITIALIZE',
            'INITIALLY',
            'INNER',
            'INOUT',
            'INPUT',
            'INSENSITIVE',
            'INSERT',
            'INSTANCE',
            'INSTANTIABLE',
            'INSTEAD',
            'INT',
            'INTEGER',
            'INTERSECT',
            'INTERVAL',
            'INTO',
            'INVOKER',
            'IS',
            'ISNULL',
            'ISOLATION',
            'ITERATE',
            'JOIN',
            'K',
            'KEY',
            'KEY_MEMBER',
            'KEY_TYPE',
            'LANCOMPILER',
            'LANGUAGE',
            'LARGE',
            'LAST',
            'LATERAL',
            'LEADING',
            'LEFT',
            'LENGTH',
            'LESS',
            'LEVEL',
            'LIKE',
            'LIMIT',
            'LISTEN',
            'LOAD',
            'LOCAL',
            'LOCALTIME',
            'LOCALTIMESTAMP',
            'LOCATION',
            'LOCATOR',
            'LOCK',
            'LOWER',
            'M',
            'MAP',
            'MATCH',
            'MAX',
            'MAXVALUE',
            'MESSAGE_LENGTH',
            'MESSAGE_OCTET_LENGTH',
            'MESSAGE_TEXT',
            'METHOD',
            'MIN',
            'MINUTE',
            'MINVALUE',
            'MOD',
            'MODE',
            'MODIFIES',
            'MODIFY',
            'MODULE',
            'MONTH',
            'MORE',
            'MOVE',
            'MUMPS',
            'NAME',
            'NAMES',
            'NATIONAL',
            'NATURAL',
            'NCHAR',
            'NCLOB',
            'NEW',
            'NEXT',
            'NO',
            'NOCREATEDB',
            'NOCREATEUSER',
            'NONE',
            'NOT',
            'NOTHING',
            'NOTIFY',
            'NOTNULL',
            'NULL',
            'NULLABLE',
            'NULLIF',
            'NUMBER',
            'NUMERIC',
            'OBJECT',
            'OCTET_LENGTH',
            'OF',
            'OFF',
            'OFFSET',
            'OIDS',
            'OLD',
            'ON',
            'ONLY',
            'OPEN',
            'OPERATION',
            'OPERATOR',
            'OPTION',
            'OPTIONS',
            'OR',
            'ORDER',
            'ORDINALITY',
            'OUT',
            'OUTER',
            'OUTPUT',
            'OVERLAPS',
            'OVERLAY',
            'OVERRIDING',
            'OWNER',
            'PAD',
            'PARAMETER',
            'PARAMETERS',
            'PARAMETER_MODE',
            'PARAMETER_NAME',
            'PARAMETER_ORDINAL_POSITION',
            'PARAMETER_SPECIFIC_CATALOG',
            'PARAMETER_SPECIFIC_NAME',
            'PARAMETER_SPECIFIC_SCHEMA',
            'PARTIAL',
            'PASCAL',
            'PASSWORD',
            'PATH',
            'PENDANT',
            'PLACING',
            'PLI',
            'POSITION',
            'POSTFIX',
            'PRECISION',
            'PREFIX',
            'PREORDER',
            'PREPARE',
            'PRESERVE',
            'PRIMARY',
            'PRIOR',
            'PRIVILEGES',
            'PROCEDURAL',
            'PROCEDURE',
            'PUBLIC',
            'READ',
            'READS',
            'REAL',
            'RECHECK',
            'RECURSIVE',
            'REF',
            'REFERENCES',
            'REFERENCING',
            'REINDEX',
            'RELATIVE',
            'RENAME',
            'REPEATABLE',
            'REPLACE',
            'RESET',
            'RESTRICT',
            'RESULT',
            'RETURN',
            'RETURNED_LENGTH',
            'RETURNED_OCTET_LENGTH',
            'RETURNED_SQLSTATE',
            'RETURNS',
            'REVOKE',
            'RIGHT',
            'ROLE',
            'ROLLBACK',
            'ROLLUP',
            'ROUTINE',
            'ROUTINE_CATALOG',
            'ROUTINE_NAME',
            'ROUTINE_SCHEMA',
            'ROW',
            'ROWS',
            'ROW_COUNT',
            'RULE',
            'SAVEPOINT',
            'SCALE',
            'SCHEMA',
            'SCHEMA_NAME',
            'SCOPE',
            'SCROLL',
            'SEARCH',
            'SECOND',
            'SECTION',
            'SECURITY',
            'SELECT',
            'SELF',
            'SENSITIVE',
            'SEQUENCE',
            'SERIALIZABLE',
            'SERVER_NAME',
            'SESSION',
            'SESSION_USER',
            'SET',
            'SETOF',
            'SETS',
            'SHARE',
            'SHOW',
            'SIMILAR',
            'SIMPLE',
            'SIZE',
            'SMALLINT',
            'SOME',
            'SOURCE',
            'SPACE',
            'SPECIFIC',
            'SPECIFICTYPE',
            'SPECIFIC_NAME',
            'SQL',
            'SQLCODE',
            'SQLERROR',
            'SQLEXCEPTION',
            'SQLSTATE',
            'SQLWARNING',
            'STABLE',
            'START',
            'STATE',
            'STATEMENT',
            'STATIC',
            'STATISTICS',
            'STDIN',
            'STDOUT',
            'STORAGE',
            'STRICT',
            'STRUCTURE',
            'STYLE',
            'SUBCLASS_ORIGIN',
            'SUBLIST',
            'SUBSTRING',
            'SUM',
            'SYMMETRIC',
            'SYSID',
            'SYSTEM',
            'SYSTEM_USER',
            'TABLE',
            'TABLE_NAME',
            'TEMP',
            'TEMPLATE',
            'TEMPORARY',
            'TERMINATE',
            'THAN',
            'THEN',
            'TIME',
            'TIMESTAMP',
            'TIMEZONE_HOUR',
            'TIMEZONE_MINUTE',
            'TO',
            'TOAST',
            'TRAILING',
            'TRANSACTION',
            'TRANSACTIONS_COMMITTED',
            'TRANSACTIONS_ROLLED_BACK',
            'TRANSACTION_ACTIVE',
            'TRANSFORM',
            'TRANSFORMS',
            'TRANSLATE',
            'TRANSLATION',
            'TREAT',
            'TRIGGER',
            'TRIGGER_CATALOG',
            'TRIGGER_NAME',
            'TRIGGER_SCHEMA',
            'TRIM',
            'TRUE',
            'TRUNCATE',
            'TRUSTED',
            'TYPE',
            'UNCOMMITTED',
            'UNDER',
            'UNENCRYPTED',
            'UNION',
            'UNIQUE',
            'UNKNOWN',
            'UNLISTEN',
            'UNNAMED',
            'UNNEST',
            'UNTIL',
            'UPDATE',
            'UPPER',
            'USAGE',
            'USER',
            'USER_DEFINED_TYPE_CATALOG',
            'USER_DEFINED_TYPE_NAME',
            'USER_DEFINED_TYPE_SCHEMA',
            'USING',
            'VACUUM',
            'VALID',
            'VALIDATOR',
            'VALUE',
            'VALUES',
            'VARCHAR',
            'VARIABLE',
            'VARYING',
            'VERBOSE',
            'VERSION',
            'VIEW',
            'VOLATILE',
            'WHEN',
            'WHENEVER',
            'WHERE',
            'WITH',
            'WITHOUT',
            'WORK',
            'WRITE',
            'YEAR',
            'ZONE',
        ]
        self.v_console_help = "Console tab. Type the commands in the editor below this box. \? to view command list."
        self.v_version = ''
        self.v_version_num = ''
        self.v_use_server_cursor = True

    def GetName(self):
        return self.v_service

    def GetVersion(self):
        self.v_version = self.v_connection.ExecuteScalar('show server_version')
        self.v_version_num = self.v_connection.ExecuteScalar('show server_version_num')
        return 'PostgreSQL ' + self.v_version

    def GetUserSuper(self):
        return self.v_connection.ExecuteScalar("select rolsuper from pg_roles where rolname = '{0}'".format(self.v_user))

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
            v_rules += ' on update ' + p_update_rule + ' '
        if p_delete_rule.strip() != '':
            v_rules += ' on delete ' + p_delete_rule + ' '
        return v_rules

    def TestConnection(self):
        v_return = ''
        if self.v_conn_string and self.v_conn_string_error!='':
            return self.v_conn_string_error

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
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.Query('''
                select quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema,
                       false as is_partition,
                       false as is_partitioned
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                where c.relkind in ('r', 'p')
                {0}
                order by 2, 1
            '''.format(v_filter), True)
        else:
            return self.v_connection.Query('''
                select quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema,
                       c.relispartition as is_partition,
                       c.relkind = 'p' as is_partitioned
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                where c.relkind in ('r', 'p')
                {0}
                order by 2, 1
            '''.format(v_filter), True)

    def QueryTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
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
                   (case when t.typtype = 'd'::"char"
                         then case when bt.typelem <> 0::oid and bt.typlen = '-1'::integer
                                   then 'ARRAY'::text
                                   when nbt.nspname = 'pg_catalog'::name
                                   then format_type(t.typbasetype, NULL::integer)
                                   else 'USER-DEFINED'::text
                              end
                         else case when t.typelem <> 0::oid and t.typlen = '-1'::integer
                                   then 'ARRAY'::text
                                   when nt.nspname = 'pg_catalog'::name
                                   then format_type(a.atttypid, NULL::integer)
                                   else 'USER-DEFINED'::text
                              end
                    end) as data_type,
                   (case when a.attnotnull or t.typtype = 'd'::char and t.typnotnull
                         then 'NO'
                         else 'YES'
                    end
                   ) as nullable,
                   (select case when x.truetypmod = -1 /* default typmod */
                                then null
                                when x.truetypid in (1042, 1043) /* char, varchar */
                                then x.truetypmod - 4
                                when x.truetypid in (1560, 1562) /* bit, varbit */
                                then x.truetypmod
                                else null
                           end
                    from (
                        select (case when t.typtype = 'd'
                                     then t.typbasetype
                                     else a.atttypid
                                end
                               ) as truetypid,
                               (case when t.typtype = 'd'
                                     then t.typtypmod
                                     else a.atttypmod
                                end
                               ) as truetypmod
                    ) x
                   ) as data_length,
                   null as data_precision,
                   null as data_scale
            from pg_attribute a
            inner join pg_class c
            on c.oid = a.attrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join (
                pg_type t
                inner join pg_namespace nt
                on t.typnamespace = nt.oid
            ) on a.atttypid = t.oid
            left join (
                pg_type bt
                inner join pg_namespace nbt
                on bt.typnamespace = nbt.oid
            ) on t.typtype = 'd'::"char" and t.typbasetype = bt.oid
            where a.attnum > 0
              and not a.attisdropped
              and c.relkind in ('r', 'f', 'p')
              {0}
            order by quote_ident(c.relname),
                     a.attnum
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
                         quote_ident(kcu2.constraint_name) as r_constraint_name,
                         quote_ident(kcu2.table_name) as r_table_name,
                         quote_ident(kcu1.constraint_schema) as table_schema,
                         quote_ident(kcu2.constraint_schema) as r_table_schema,
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
                     quote_ident(table_name)
        '''.format(v_filter), True)

    def QueryTablesForeignKeysColumns(self, p_fkey, p_table=None, p_all_schemas=False, p_schema=None):
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
        v_filter = v_filter + "and quote_ident(kcu1.constraint_name) = '{0}' ".format(p_fkey)
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
                         rc.update_rule as update_rule,
                         rc.delete_rule as delete_rule,
                         kcu1.ordinal_position
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
            order by ordinal_position
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
                   quote_ident(tc.table_name) as table_name,
                   quote_ident(tc.table_schema) as table_schema
            from information_schema.table_constraints tc
            where tc.constraint_type = 'PRIMARY KEY'
            {0}
            order by quote_ident(tc.constraint_name),
                     quote_ident(tc.table_name)
        '''.format(v_filter), True)

    def QueryTablesPrimaryKeysColumns(self, p_pkey, p_table=None, p_all_schemas=False, p_schema=None):
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
        v_filter = v_filter + "and quote_ident(tc.constraint_name) = '{0}' ".format(p_pkey)
        return self.v_connection.Query('''
            select quote_ident(kc.column_name) as column_name
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'PRIMARY KEY'
            {0}
            order by kc.ordinal_position
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
                   quote_ident(tc.table_name) as table_name,
                   quote_ident(tc.table_schema) as table_schema
            from information_schema.table_constraints tc
            where tc.constraint_type = 'UNIQUE'
            {0}
            order by quote_ident(tc.constraint_name),
                     quote_ident(tc.table_name)
        '''.format(v_filter), True)

    def QueryTablesUniquesColumns(self, p_unique, p_table=None, p_all_schemas=False, p_schema=None):
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
        v_filter = v_filter + "and quote_ident(tc.constraint_name) = '{0}' ".format(p_unique)
        return self.v_connection.Query('''
            select quote_ident(kc.column_name) as column_name
            from information_schema.table_constraints tc
            join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'UNIQUE'
            {0}
            order by kc.ordinal_position
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
                   (case when strpos(t.indexdef, 'UNIQUE') > 0 then 'Unique' else 'Non Unique' end) as uniqueness,
                   quote_ident(t.schemaname) as schema_name
            from pg_indexes t
            where 1 = 1
            {0}
            order by quote_ident(t.tablename),
                     quote_ident(t.indexname)
        '''.format(v_filter), True)

    def QueryTablesIndexesColumns(self, p_index, p_table=None, p_all_schemas=False, p_schema=None):
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
        v_filter = v_filter + "and quote_ident(t.indexname) = '{0}' ".format(p_index)
        return self.v_connection.Query('''
            select unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as column_name
            from pg_indexes t
            where 1 = 1
            {0}
        '''.format(v_filter), True)

    def QueryTablesChecks(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(t.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(t.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and quote_ident(t.relname) = {0}".format(p_table)
            else:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select quote_ident(n.nspname) as schema_name,
                   quote_ident(t.relname) as table_name,
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
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(t.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "and quote_ident(n.nspname) = '{0}' and quote_ident(t.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') and quote_ident(t.relname) = {0}".format(p_table)
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
              and quote_ident(t.relname) = $2
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
              and quote_ident(t.relname) = $2
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
                   quote_ident(t.relname) as table_name,
                   quote_ident(c.conname) as constraint_name,
                   pg_temp.fnc_omnidb_exclude_ops(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as operations,
                   pg_temp.fnc_omnidb_exclude_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
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
            where quote_ident(schemaname) = '{0}'
              and quote_ident(tablename) = '{1}'
              and quote_ident(rulename) = '{2}'
        '''.format(p_schema, p_table, p_rule)).replace('CREATE RULE', 'CREATE OR REPLACE RULE')

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
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) as trigger_function,
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id
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
            select distinct quote_ident(t.trigger_name) as trigger_name,
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
            where quote_ident(event_object_schema) = '{0}'
              and quote_ident(event_object_table) = '{1}'
              and quote_ident(trigger_name) = '{2}'
            ), ' OR ') as event
            ) e
            on 1 = 1
            where quote_ident(t.event_object_schema) = '{0}'
              and quote_ident(t.event_object_table) = '{1}'
              and quote_ident(t.trigger_name) = '{2}'
            ) x
        '''.format(p_schema, p_table, p_trigger))

    def QueryTablesInheriteds(self, p_table=None, p_all_schemas=False, p_schema=None):
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000:
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
                where not cc.relispartition
                {0}
                order by 1, 2, 3, 4
            '''.format(v_filter))
        else:
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
            where cc.relispartition
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query('''
                select quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                       quote_ident(p.proname) as name,
                       quote_ident(n.nspname) as schema_name
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                where not p.proisagg
                  and format_type(p.prorettype, null) <> 'trigger'
                {0}
                order by 1
            '''.format(v_filter), True)
        else:
            return self.v_connection.Query('''
                select quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                       quote_ident(p.proname) as name,
                       quote_ident(n.nspname) as schema_name
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                where p.prokind = 'f'
                  and format_type(p.prorettype, null) <> 'trigger'
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

    def QueryProcedures(self, p_all_schemas=False, p_schema=None):
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
            where p.prokind = 'p'
              and format_type(p.prorettype, null) <> 'trigger'
            {0}
            order by 1
        '''.format(v_filter), True)

    def QueryProcedureFields(self, p_procedure, p_schema):
        if p_schema:
            return self.v_connection.Query('''
                select (case trim(substring((trim(x.name) || ' ') from 1 for position(' ' in (trim(x.name) || ' '))))
                          when 'OUT' then 'O'
                          when 'INOUT' then 'X'
                          else 'I'
                        end) as type,
                       trim(x.name) as name,
                       row_number() over() as seq
                from (
                    select unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 3
            '''.format(p_schema, p_procedure), True)
        else:
            return self.v_connection.Query('''
                select (case trim(substring((trim(x.name) || ' ') from 1 for position(' ' in (trim(x.name) || ' '))))
                          when 'OUT' then 'O'
                          when 'INOUT' then 'X'
                          else 'I'
                        end) as type,
                       trim(x.name) as name,
                       row_number() over() as seq
                from (
                    select unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
                ) x
                where length(trim(x.name)) > 0
                order by 3
            '''.format(self.v_schema, p_procedure), True)

    def GetProcedureDefinition(self, p_procedure):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_procedure))

    def GetProcedureDebug(self, p_procedure):
        return self.v_connection.ExecuteScalar('''
            select p.prosrc
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
        '''.format(p_procedure))

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
            order by 1, 2
        '''.format(v_filter), True)
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
                   (case when a.attnotnull or t.typtype = 'd'::char and t.typnotnull
                         then 'NO'
                         else 'YES'
                    end
                   ) as nullable,
                   (select case when x.truetypmod = -1 /* default typmod */
                                then null
                                when x.truetypid in (1042, 1043) /* char, varchar */
                                then x.truetypmod - 4
                                when x.truetypid in (1560, 1562) /* bit, varbit */
                                then x.truetypmod
                                else null
                           end
                    from (
                        select (case when t.typtype = 'd'
                                     then t.typbasetype
                                     else a.atttypid
                                end
                               ) as truetypid,
                               (case when t.typtype = 'd'
                                     then t.typtypmod
                                     else a.atttypmod
                                end
                               ) as truetypmod
                    ) x
                   ) as data_length,
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
              and c.relkind = 'v'
              {0}
            order by quote_ident(c.relname),
                     a.attnum
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
                   (case when a.attnotnull or t.typtype = 'd'::char and t.typnotnull
                         then 'NO'
                         else 'YES'
                    end
                   ) as nullable,
                   (select case when x.truetypmod = -1 /* default typmod */
                                then null
                                when x.truetypid in (1042, 1043) /* char, varchar */
                                then x.truetypmod - 4
                                when x.truetypid in (1560, 1562) /* bit, varbit */
                                then x.truetypmod
                                else null
                           end
                    from (
                        select (case when t.typtype = 'd'
                                     then t.typbasetype
                                     else a.atttypid
                                end
                               ) as truetypid,
                               (case when t.typtype = 'd'
                                     then t.typtypmod
                                     else a.atttypmod
                                end
                               ) as truetypmod
                    ) x
                   ) as data_length,
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) >= 110000:
            return self.v_connection.Query('''
                select quote_ident(pubname) as pubname,
                       puballtables,
                       pubinsert,
                       pubupdate,
                       pubdelete,
                       pubtruncate
                from pg_publication
                order by 1
            ''', True)
        else:
            return self.v_connection.Query('''
                select quote_ident(pubname) as pubname,
                       puballtables,
                       pubinsert,
                       pubupdate,
                       pubdelete,
                       false as pubtruncate
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

    def QueryForeignDataWrappers(self):
        return self.v_connection.Query('''
            select fdwname
            from pg_foreign_data_wrapper
            order by 1
        ''')

    def QueryForeignServers(self, v_fdw):
        return self.v_connection.Query('''
            select s.srvname,
                   s.srvtype,
                   s.srvversion,
                   array_to_string(srvoptions, ',') as srvoptions
            from pg_foreign_server s
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            where w.fdwname = '{0}'
            order by 1
        '''.format(v_fdw))

    def QueryUserMappings(self, v_foreign_server):
        return self.v_connection.Query('''
            select rolname,
                   umoptions
            from (
            select seq,
                   rolname,
                   string_agg(umoption, ','::text) as umoptions
            from (
            select seq,
                   rolname,
                   (case when lower(umoption[1]) in ('password', 'passwd', 'passw', 'pass', 'pwd')
                         then umoption[1] || '=' || '*****'
                         else umoption[1] || '=' || umoption[2]
                    end) as umoption
            from (
            select seq,
                   rolname,
                   string_to_array(umoption, '=') as umoption
            from (
            select 1 as seq,
                   'PUBLIC' as rolname,
                   unnest(coalesce(u.umoptions, '{{null}}')) as umoption
            from pg_user_mapping u
            inner join pg_foreign_server s
            on s.oid = u.umserver
            where u.umuser = 0
              and s.srvname = '{0}'
            union
            select 1 + row_number() over(order by r.rolname) as seq,
                   r.rolname,
                   unnest(coalesce(u.umoptions, '{{null}}')) as umoption
            from pg_user_mapping u
            inner join pg_foreign_server s
            on s.oid = u.umserver
            inner join pg_roles r
            on r.oid = u.umuser
            where s.srvname = '{0}'
            ) x
            ) x
            ) x
            group by seq,
                     rolname
            ) x
            order by seq
'''.format(v_foreign_server))

    def QueryForeignTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.Query('''
                select quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema,
                       false as is_partition,
                       false as is_partitioned
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                where c.relkind = 'f'
                {0}
                order by 2, 1
            '''.format(v_filter), True)
        else:
            return self.v_connection.Query('''
                select quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema,
                       c.relispartition as is_partition,
                       false as is_partitioned
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                where c.relkind = 'f'
                {0}
                order by 2, 1
            '''.format(v_filter), True)

    def QueryForeignTablesFields(self, p_table=None, p_all_schemas=False, p_schema=None):
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
                   (case when a.attnotnull or t.typtype = 'd'::char and t.typnotnull
                         then 'NO'
                         else 'YES'
                    end
                   ) as nullable,
                   (select case when x.truetypmod = -1 /* default typmod */
                                then null
                                when x.truetypid in (1042, 1043) /* char, varchar */
                                then x.truetypmod - 4
                                when x.truetypid in (1560, 1562) /* bit, varbit */
                                then x.truetypmod
                                else null
                           end
                    from (
                        select (case when t.typtype = 'd'
                                     then t.typbasetype
                                     else a.atttypid
                                end
                               ) as truetypid,
                               (case when t.typtype = 'd'
                                     then t.typtypmod
                                     else a.atttypmod
                                end
                               ) as truetypmod
                    ) x
                   ) as data_length,
                   null as data_precision,
                   null as data_scale,
                   array_to_string(a.attfdwoptions, ',') as attfdwoptions,
                   array_to_string(f.ftoptions, ',') as ftoptions,
                   s.srvname,
                   w.fdwname
            from pg_attribute a
            inner join pg_class c
            on c.oid = a.attrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_type t
            on t.oid = a.atttypid
            inner join pg_foreign_table f
            on f.ftrelid = c.oid
            inner join pg_foreign_server s
            on s.oid = f.ftserver
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            where a.attnum > 0
              and not a.attisdropped
              and c.relkind = 'f'
              {0}
            order by quote_ident(c.relname),
                     a.attnum
        '''.format(v_filter), True)

    def QueryTypes(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        v_table = self.v_connection.Query('''
            select quote_ident(n.nspname) as type_schema,
                   quote_ident(t.typname) as type_name
            from pg_type t
            inner join pg_namespace n
            on n.oid = t.typnamespace
            where (t.typrelid = 0 or (select c.relkind = 'c' from pg_class c where c.oid = t.typrelid))
              and not exists(select 1 from pg_type el where el.oid = t.typelem and el.typarray = t.oid)
              and t.typtype <> 'd'
            {0}
            order by 1, 2
        '''.format(v_filter), True)
        return v_table

    def QueryDomains(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        v_table = self.v_connection.Query('''
            select quote_ident(n.nspname) as domain_schema,
                   quote_ident(t.typname) as domain_name
            from pg_type t
            inner join pg_namespace n
            on n.oid = t.typnamespace
            where (t.typrelid = 0 or (select c.relkind = 'c' from pg_class c where c.oid = t.typrelid))
              and not exists(select 1 from pg_type el where el.oid = t.typelem and el.typarray = t.oid)
              and t.typtype = 'd'
            {0}
            order by 1, 2
        '''.format(v_filter), True)
        return v_table

    def DataMiningData(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas, p_dataCategoryFilter):
        v_sqlDict = {}

        if p_inSchemas != '': #At least one schema must be selected
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
                  --#FILTER_DATA_CATEGORY_FILTER# and n.nspname || '.' || c.relname like any (string_to_array('#VALUE_DATA_CATEGORY_FILTER#', '|'))
            '''.format(p_inSchemas)

            if p_dataCategoryFilter.strip() != '':
                v_columnsSql = v_columnsSql.replace('--#FILTER_DATA_CATEGORY_FILTER#', '').replace('#VALUE_DATA_CATEGORY_FILTER#', p_dataCategoryFilter)

            v_columnsTable = self.v_connection.Query(v_columnsSql)

            for v_columnRow in v_columnsTable.Rows:
                v_sql = '''
                    select 'Data' as category,
                           '{0}' as schema_name,
                           '{1}' as table_name,
                           '{2}' as column_name,
                           t.{2}::text as match_value
                    from (
                        select t.{2}
                        from {0}.{1} t
                        where 1 = 1
                        --#FILTER_PATTERN_CASE_SENSITIVE#  and t.{2}::text like '#VALUE_PATTERN_CASE_SENSITIVE#'
                        --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.{2}::text) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
                        --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and t.{2}::text ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
                        --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and t.{2}::text ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
                    ) t
                '''.format(
                    v_columnRow['schema_name'],
                    v_columnRow['table_name'],
                    v_columnRow['column_name']
                )

                if p_inSchemas != '':
                    v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

                if p_regex:
                    if p_caseSentive:
                        v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
                    else:
                        v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
                else:
                    if p_caseSentive:
                        v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
                    else:
                        v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

                v_key = '{0}.{1}'.format(v_columnRow['schema_name'], v_columnRow['table_name'])

                if v_key not in v_sqlDict:
                    v_sqlDict[v_key] = v_sql
                else:
                    v_sqlDict[v_key] += '''

                        union

                        {0}
                    '''.format(v_sql)

        return v_sqlDict

    def DataMiningFKName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'FK Name'::text as category,
                   tc.table_schema::text as schema_name,
                   tc.table_name::text as table_name,
                   ''::text as column_name,
                   tc.constraint_name::text as match_value
            from information_schema.table_constraints tc
            where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and tc.table_schema not like 'pg%%temp%%'
              and tc.constraint_type = 'FOREIGN KEY'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and tc.constraint_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningFunctionDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and y.function_definition like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(y.function_definition) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and y.function_definition ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and y.function_definition ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningFunctioName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and p.proname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.proname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and p.proname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and p.proname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningIndexName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Index Name'::text as category,
                   i.schemaname::text as schema_name,
                   i.tablename::text as table_name,
                   ''::text as column_name,
                   i.indexname::text as match_value
            from pg_indexes i
            where i.schemaname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and i.schemaname not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and i.indexname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(i.indexname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and i.indexname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and i.indexname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(i.schemaname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningMaterializedViewColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and a.attname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(a.attname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and a.attname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and a.attname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningMaterializedViewName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and c.relname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.relname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and c.relname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and c.relname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningPKName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'PK Name'::text as category,
                   tc.table_schema::text as schema_name,
                   tc.table_name::text as table_name,
                   ''::text as column_name,
                   tc.constraint_name::text as match_value
            from information_schema.table_constraints tc
            where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and tc.table_schema not like 'pg%%temp%%'
              and tc.constraint_type = 'PRIMARY KEY'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and tc.constraint_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningSchemaName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Schema Name'::text as category,
                   ''::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   n.nspname::text as match_value
            from pg_namespace n
            where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and n.nspname not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and n.nspname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(n.nspname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and n.nspname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and n.nspname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningSequenceName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Sequence Name'::text as category,
                   s.sequence_schema::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   s.sequence_name::text as match_value
            from information_schema.sequences s
            where s.sequence_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and s.sequence_schema not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and s.sequence_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(s.sequence_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and s.sequence_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and s.sequence_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(s.sequence_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTableColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and c.column_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.column_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and c.column_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and c.column_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(c.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTableName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Table Name'::text as category,
                   t.table_schema::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   t.table_name::text as match_value
            from information_schema.tables t
            where t.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and t.table_schema not like 'pg%%temp%%'
              and t.table_type = 'BASE TABLE'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and t.table_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.table_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and t.table_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and t.table_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(t.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTriggerName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and p.proname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.proname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and p.proname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and p.proname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTriggerSource(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and p.prosrc like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(p.prosrc) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and p.prosrc ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and p.prosrc ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningUniqueName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Unique Name'::text as category,
                   tc.table_schema::text as schema_name,
                   tc.table_name::text as table_name,
                   ''::text as column_name,
                   tc.constraint_name::text as match_value
            from information_schema.table_constraints tc
            where tc.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and tc.table_schema not like 'pg%%temp%%'
              and tc.constraint_type = 'UNIQUE'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and tc.constraint_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(tc.constraint_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and tc.constraint_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and tc.constraint_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(tc.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningViewColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            --#FILTER_PATTERN_CASE_SENSITIVE#  and c.column_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.column_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and c.column_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and c.column_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(c.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningViewName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'View Name'::text as category,
                   v.table_schema::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   v.table_name::text as match_value
            from information_schema.views v
            where v.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and v.table_schema not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and v.table_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(v.table_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and v.table_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and v.table_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(v.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningCheckName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Check Name'::text as category,
                   quote_ident(n.nspname)::text as schema_name,
                   quote_ident(t.relname)::text as table_name,
                   ''::text as column_name,
                   quote_ident(c.conname)::text as match_value
            from pg_constraint c
            inner join pg_class t
                       on t.oid = c.conrelid
            inner join pg_namespace n
                       on t.relnamespace = n.oid
            where contype = 'c'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(c.conname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(c.conname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(c.conname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(c.conname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(n.nspname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningRuleName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Rule Name'::text as category,
                   quote_ident(schemaname)::text as schema_name,
                   quote_ident(tablename)::text as table_name,
                   ''::text as column_name,
                   quote_ident(rulename)::text as match_value
            from pg_rules
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(rulename) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(rulename)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(rulename) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(rulename) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(schemaname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningRuleDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Rule Definition'::text as category,
                   quote_ident(schemaname)::text as schema_name,
                   quote_ident(tablename)::text as table_name,
                   ''::text as column_name,
                   definition::text as match_value
            from pg_rules
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and definition like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(definition) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and definition ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and definition ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(schemaname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningInheritedTableName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000:
            v_sql = '''
                select 'Inherited Table Name'::text as category,
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
                where not cc.relispartition
                --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(cc.relname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(cc.relname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
                --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(cc.relname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
                --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(cc.relname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(np.nspname)) in (#VALUE_BY_SCHEMA#)
            '''
        else:
            v_sql = '''
                select 'Inherited Table Name'::text as category,
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
                --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(cc.relname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
                --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(cc.relname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
                --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(cc.relname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
                --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(cc.relname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
                --#FILTER_BY_SCHEMA#  and lower(quote_ident(np.nspname)) in (#VALUE_BY_SCHEMA#)
            '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningPartitionName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
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
            where cc.relispartition
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(cc.relname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(cc.relname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(cc.relname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(cc.relname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(np.nspname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningRoleName(self, p_textPattern, p_caseSentive, p_regex):
        v_sql = '''
            select 'Role Name'::text as category,
                   ''::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   quote_ident(rolname)::text as match_value
            from pg_roles
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(rolname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(rolname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(rolname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(rolname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTablespaceName(self, p_textPattern, p_caseSentive, p_regex):
        v_sql = '''
            select 'Tablespace Name'::text as category,
                   ''::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   quote_ident(spcname)::text as match_value
            from pg_tablespace
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(spcname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(spcname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(spcname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(spcname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningExtensionName(self, p_textPattern, p_caseSentive, p_regex):
        v_sql = '''
            select 'Extension Name'::text as category,
                   ''::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   quote_ident(extname)::text as match_value
            from pg_extension
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(extname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(extname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(extname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(extname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningFKColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            with select_fks as (
                select distinct
                       quote_ident(kcu1.constraint_schema) as table_schema,
                       quote_ident(kcu1.table_name) as table_name,
                       quote_ident(kcu1.column_name) as column_name,
                       quote_ident(kcu2.constraint_schema) as r_table_schema,
                       quote_ident(kcu2.table_name) as r_table_name,
                       quote_ident(kcu2.column_name) as r_column_name
                from information_schema.referential_constraints rc
                inner join information_schema.key_column_usage kcu1
                           on  kcu1.constraint_catalog = rc.constraint_catalog
                           and kcu1.constraint_schema = rc.constraint_schema
                           and kcu1.constraint_name = rc.constraint_name
                inner join information_schema.key_column_usage kcu2
                           on  kcu2.constraint_catalog = rc.unique_constraint_catalog
                           and kcu2.constraint_schema = rc.unique_constraint_schema
                           and kcu2.constraint_name = rc.unique_constraint_name
                           and kcu2.ordinal_position = kcu1.ordinal_position
                where 1 = 1
                  --#FILTER_BY_SCHEMA#  and lower(quote_ident(kcu1.constraint_schema)) in (#VALUE_BY_SCHEMA#) or lower(quote_ident(kcu2.constraint_schema)) in (#VALUE_BY_SCHEMA#)
            )
            select 'FK Column Name'::text as category,
                   sf.table_schema::text as schema_name,
                   sf.table_name::text as table_name,
                   ''::text as column_name,
                   sf.column_name::text as match_value
            from select_fks sf
            where sf.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and sf.table_schema not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and sf.column_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(sf.column_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and sf.column_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and sf.column_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(sf.table_schema) in (#VALUE_BY_SCHEMA#)

            union

            select 'FK Column Name'::text as category,
                   (sf.r_table_schema || ' (referenced)')::text as schema_name,
                   (sf.r_table_name || ' (referenced)')::text as table_name,
                   ''::text as column_name,
                   (sf.r_column_name || ' (referenced)')::text as match_value
            from select_fks sf
            where sf.r_table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and sf.r_table_schema not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and sf.r_column_name like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(sf.r_column_name) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and sf.r_column_name ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and sf.r_column_name ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(sf.r_table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningPKColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'PK Column Name'::text as category,
                   quote_ident(tc.table_schema)::text as schema_name,
                   quote_ident(tc.table_name)::text as table_name,
                   ''::text as column_name,
                   quote_ident(kc.column_name) as match_value
            from information_schema.table_constraints tc
            inner join information_schema.key_column_usage kc
                       on  kc.table_name = tc.table_name
                       and kc.table_schema = tc.table_schema
                       and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'PRIMARY KEY'
              and quote_ident(tc.table_schema) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(tc.table_schema) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(kc.column_name) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(kc.column_name)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(kc.column_name) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(kc.column_name) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(tc.table_schema)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningUniqueColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Unique Column Name'::text as category,
                   quote_ident(tc.table_schema)::text as schema_name,
                   quote_ident(tc.table_name)::text as table_name,
                   ''::text as column_name,
                   quote_ident(kc.column_name) as match_value
            from information_schema.table_constraints tc
            inner join information_schema.key_column_usage kc
                       on  kc.table_name = tc.table_name
                       and kc.table_schema = tc.table_schema
                       and kc.constraint_name = tc.constraint_name
            where tc.constraint_type = 'UNIQUE'
              and quote_ident(tc.table_schema) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(tc.table_schema) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(kc.column_name) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(kc.column_name)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(kc.column_name) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(kc.column_name) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(tc.table_schema)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningIndexColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select *
            from (
                select 'Index Column Name'::text as category,
                       quote_ident(t.schemaname)::text as schema_name,
                       quote_ident(t.tablename)::text as table_name,
                       ''::text as column_name,
                       unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as match_value
                from pg_indexes t
            ) t
            where quote_ident(t.schemaname) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(t.schemaname) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(t.match_value) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(t.match_value)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(t.match_value) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(t.match_value) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(t.schema_name)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningCheckDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Check Definition'::text as category,
                   quote_ident(n.nspname)::text as schema_name,
                   quote_ident(t.relname)::text as table_name,
                   ''::text as column_name,
                   c.consrc as match_value
            from pg_constraint c
            inner join pg_class t
                  on t.oid = c.conrelid
            inner join pg_namespace n
                  on t.relnamespace = n.oid
            where contype = 'c'
              and quote_ident(n.nspname) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(n.nspname) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and c.consrc like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(c.consrc) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and c.consrc ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and c.consrc ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(n.nspname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningTableTriggerName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Table Trigger Name'::text as category,
                   quote_ident(n.nspname)::text as schema_name,
                   quote_ident(c.relname)::text as table_name,
                   ''::text as column_name,
                   quote_ident(t.tgname) as match_value
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
              and quote_ident(n.nspname) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(n.nspname) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and quote_ident(t.tgname) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(quote_ident(t.tgname)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and quote_ident(t.tgname) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and quote_ident(t.tgname) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(quote_ident(n.nspname)) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningMaterializedViewDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Materialized View Definition'::text as category,
                   y.schema_name::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   y.mview_definition::text as match_value
            from (
                select n.nspname::text as schema_name,
                       pg_get_viewdef((n.nspname || '.' || c.relname)::regclass) as mview_definition
                from pg_class c
                inner join pg_namespace n
                           on n.oid = c.relnamespace
                where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                  and n.nspname not like 'pg%%temp%%'
                  and c.relkind = 'm'
                  --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
            ) y
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and y.mview_definition like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(y.mview_definition) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and y.mview_definition ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and y.mview_definition ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMiningViewDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'View Definition'::text as category,
                   v.table_schema::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   v.view_definition::text as match_value
            from information_schema.views v
            where v.table_schema not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and v.table_schema not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and v.view_definition like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(v.view_definition) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and v.view_definition ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and v.view_definition ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(v.table_schema) in (#VALUE_BY_SCHEMA#)
        '''

        if p_inSchemas != '':
            v_sql = v_sql.replace('--#FILTER_BY_SCHEMA#', '').replace('#VALUE_BY_SCHEMA#', p_inSchemas)

        if p_regex:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))
        else:
            if p_caseSentive:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_SENSITIVE#', '').replace('#VALUE_PATTERN_CASE_SENSITIVE#', p_textPattern.replace("'", "''"))
            else:
                v_sql = v_sql.replace('--#FILTER_PATTERN_CASE_INSENSITIVE#', '').replace('#VALUE_PATTERN_CASE_INSENSITIVE#', p_textPattern.replace("'", "''"))

        return v_sql

    def DataMining(self, p_textPattern, p_caseSentive, p_regex, p_categoryList, p_schemaList, p_dataCategoryFilter):
        v_sqlDict = {}

        v_inSchemas = ''

        if len(p_schemaList) > 0:
            for v_schema in p_schemaList:
                v_inSchemas += "'{0}', ".format(v_schema)

            v_inSchemas = v_inSchemas[:-2]

        if not p_regex:
            if '%' not in p_textPattern.replace('\%', ''):
                p_textPattern = '%{0}%'.format(p_textPattern)

        for v_category in p_categoryList:
            if v_category == 'Data':
                v_sqlDict[v_category] = self.DataMiningData(p_textPattern, p_caseSentive, p_regex, v_inSchemas, p_dataCategoryFilter)
            elif v_category == 'FK Name':
                v_sqlDict[v_category] = self.DataMiningFKName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Function Definition':
                v_sqlDict[v_category] = self.DataMiningFunctionDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Function Name':
                v_sqlDict[v_category] = self.DataMiningFunctioName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Index Name':
                v_sqlDict[v_category] = self.DataMiningIndexName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Column Name':
                v_sqlDict[v_category] = self.DataMiningMaterializedViewColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Name':
                v_sqlDict[v_category] = self.DataMiningMaterializedViewName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'PK Name':
                v_sqlDict[v_category] = self.DataMiningPKName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Schema Name':
                v_sqlDict[v_category] = self.DataMiningSchemaName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Sequence Name':
                v_sqlDict[v_category] = self.DataMiningSequenceName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Column Name':
                v_sqlDict[v_category] = self.DataMiningTableColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Name':
                v_sqlDict[v_category] = self.DataMiningTableName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Trigger Name':
                v_sqlDict[v_category] = self.DataMiningTriggerName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Trigger Source':
                v_sqlDict[v_category] = self.DataMiningTriggerSource(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Unique Name':
                v_sqlDict[v_category] = self.DataMiningUniqueName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Column Name':
                v_sqlDict[v_category] = self.DataMiningViewColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Name':
                v_sqlDict[v_category] = self.DataMiningViewName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Check Name':
                v_sqlDict[v_category] = self.DataMiningCheckName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Rule Name':
                v_sqlDict[v_category] = self.DataMiningRuleName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Rule Definition':
                v_sqlDict[v_category] = self.DataMiningRuleDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Inherited Table Name':
                v_sqlDict[v_category] = self.DataMiningInheritedTableName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Partition Name':
                v_sqlDict[v_category] = self.DataMiningPartitionName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Role Name':
                v_sqlDict[v_category] = self.DataMiningRoleName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'Tablespace Name':
                v_sqlDict[v_category] = self.DataMiningTablespaceName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'Extension Name':
                v_sqlDict[v_category] = self.DataMiningExtensionName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'FK Column Name':
                v_sqlDict[v_category] = self.DataMiningFKColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'PK Column Name':
                v_sqlDict[v_category] = self.DataMiningPKColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Unique Column Name':
                v_sqlDict[v_category] = self.DataMiningUniqueColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Index Column Name':
                v_sqlDict[v_category] = self.DataMiningIndexColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Check Definition':
                v_sqlDict[v_category] = self.DataMiningCheckDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Trigger Name':
                v_sqlDict[v_category] = self.DataMiningTableTriggerName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Definition':
                v_sqlDict[v_category] = self.DataMiningMaterializedViewDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Definition':
                v_sqlDict[v_category] = self.DataMiningViewDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)

        return v_sqlDict

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

    def TemplateCreateProcedure(self):
        return Template('''CREATE OR REPLACE PROCEDURE #schema_name#.name
--(
--    [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ]
--)
LANGUAGE plpgsql
--SECURITY DEFINER
AS
$procedure$
--DECLARE
-- variables
BEGIN
-- definition
END;
$procedure$
''')

    def TemplateDropProcedure(self):
        return Template('''DROP PROCEDURE #procedure_name#
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
        return Template('''REFRESH MATERIALIZED VIEW
--CONCURRENTLY
#view_name#
--WITH NO DATA
''')

    def TemplateDropMaterializedView(self):
        return Template('''DROP MATERIALIZED VIEW #view_name#
--CASCADE
''')

    def TemplateCreateTable(self):
        return Template('''CREATE
--TEMPORARY
--UNLOGGED
TABLE #schema_name#.table_name
--OF type_name
--AS query [ WITH [ NO ] DATA ]
--PARTITION OF parent_table
(
    column_name data_type
    --COLLATE collation
    --CONSTRAINT constraint_name
    --NOT NULL
    --NULL
    --CHECK ( expression ) [ NO INHERIT ]
    --DEFAULT default_expr
    --GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]
    --UNIQUE [ WITH ( storage_parameter [= value] [, ... ] ) ] [ USING INDEX TABLESPACE tablespace_name ]
    --PRIMARY KEY [ WITH ( storage_parameter [= value] [, ... ] ) ] [ USING INDEX TABLESPACE tablespace_name ]
    --REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT } ] [ ON UPDATE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT } ]
    --CHECK ( expression ) [ NO INHERIT ]
    --UNIQUE ( column_name [, ... ] ) [ WITH ( storage_parameter [= value] [, ... ] ) ] [ USING INDEX TABLESPACE tablespace_name ]
    --PRIMARY KEY ( column_name [, ... ] ) [ WITH ( storage_parameter [= value] [, ... ] ) ] [ USING INDEX TABLESPACE tablespace_name ]
    --EXCLUDE [ USING index_method ] ( { column_name | ( expression ) } [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] WITH operator [, ... ] ) [ WITH ( storage_parameter [= value] [, ... ] ) ] [ USING INDEX TABLESPACE tablespace_name ] [ WHERE ( predicate ) ]
    --FOREIGN KEY ( column_name [, ... ] ) REFERENCES reftable [ ( refcolumn [, ... ] ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT } ] [ ON UPDATE { NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT } ]
    --DEFERRABLE
    --NOT DEFERRABLE
    --INITIALLY DEFERRED
    --INITIALLY IMMEDIATE
    --LIKE source_table [ { INCLUDING | EXCLUDING } { COMMENTS | CONSTRAINTS | DEFAULTS | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL } ... ]
)
--FOR VALUES IN ( { numeric_literal | string_literal | TRUE | FALSE | NULL } [, ...] )
--FOR VALUES FROM ( { numeric_literal | string_literal | TRUE | FALSE | MINVALUE | MAXVALUE } [, ...] ) TO ( { numeric_literal | string_literal | TRUE | FALSE | MINVALUE | MAXVALUE } [, ...] )
--FOR VALUES WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )
--DEFAULT
--INHERITS ( parent_table [, ... ] )
--PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] )
--WITH ( storage_parameter [= value] [, ... ] )
--WITH OIDS
--WITHOUT OIDS
--ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP }
--TABLESPACE tablespace_name
''')

    def TemplateAlterTable(self):
        return Template('''ALTER TABLE
--ONLY
#table_name#
--ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
--DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
--ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ USING expression ]
--ALTER [ COLUMN ] column_name SET DEFAULT expression
--ALTER [ COLUMN ] column_name DROP DEFAULT
--ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
--ALTER [ COLUMN ] column_name ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]
--ALTER [ COLUMN ] column_name { SET GENERATED { ALWAYS | BY DEFAULT } | SET sequence_option | RESTART [ [ WITH ] restart ] } [...]
--ALTER [ COLUMN ] column_name DROP IDENTITY [ IF EXISTS ]
--ALTER [ COLUMN ] column_name SET STATISTICS integer
--ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
--ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
--ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
--ADD table_constraint [ NOT VALID ]
--ADD CONSTRAINT constraint_name { UNIQUE | PRIMARY KEY } USING INDEX index_name [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
--ALTER CONSTRAINT constraint_name [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
--VALIDATE CONSTRAINT constraint_name
--DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
--DISABLE TRIGGER [ trigger_name | ALL | USER ]
--ENABLE TRIGGER [ trigger_name | ALL | USER ]
--ENABLE REPLICA TRIGGER trigger_name
--ENABLE ALWAYS TRIGGER trigger_name
--DISABLE RULE rewrite_rule_name
--ENABLE RULE rewrite_rule_name
--ENABLE REPLICA RULE rewrite_rule_name
--ENABLE ALWAYS RULE rewrite_rule_name
--DISABLE ROW LEVEL SECURITY
--ENABLE ROW LEVEL SECURITY
--FORCE ROW LEVEL SECURITY
--NO FORCE ROW LEVEL SECURITY
--CLUSTER ON index_name
--SET WITHOUT CLUSTER
--SET WITH OIDS
--SET WITHOUT OIDS
--SET TABLESPACE new_tablespace
--SET { LOGGED | UNLOGGED }
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
--INHERIT parent_table
--NO INHERIT parent_table
--OF type_name
--NOT OF
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }
--RENAME [ COLUMN ] column_name TO new_column_name
--RENAME CONSTRAINT constraint_name TO new_constraint_name
--RENAME TO new_name
--SET SCHEMA new_schema
--ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ] SET TABLESPACE new_tablespace [ NOWAIT ]
--ATTACH PARTITION partition_name FOR VALUES partition_bound_spec
--DETACH PARTITION partition_name
''')

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

    def TemplateCreateInherited(self):
        return Template('''CREATE TABLE name (
    CHECK ( condition )
) INHERITS (#table_name#)
''')

    def TemplateNoInheritPartition(self):
        return Template('ALTER TABLE #partition_name# NO INHERIT #table_name#')

    def TemplateCreatePartition(self):
        return Template('''CREATE TABLE name PARTITION OF #table_name#
--FOR VALUES
--IN ( { numeric_literal | string_literal | NULL } [, ...] )
--FROM ( { numeric_literal | string_literal | MINVALUE | MAXVALUE } [, ...] ) TO ( { numeric_literal | string_literal | MINVALUE | MAXVALUE } [, ...] )
--WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )
--DEFAULT
--PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
''')

    def TemplateDetachPartition(self):
        return Template('ALTER TABLE #table_name# DETACH PARTITION #partition_name#')

    def TemplateDropPartition(self):
        return Template('DROP TABLE #partition_name#')

    def TemplateCreateType(self):
        return Template('''CREATE TYPE #schema_name#.name

-- AS (
--    attribute_name data_type [ COLLATE collation ] [, ... ]

-- AS ENUM (
--    'label' [, ... ]

-- AS RANGE (
--    SUBTYPE = subtype
--    , SUBTYPE_OPCLASS = subtype_operator_class
--    , COLLATION = collation
--    , CANONICAL = canonical_function
--    , SUBTYPE_DIFF = subtype_diff_function

-- (
--    INPUT = input_function,
--    OUTPUT = output_function
--    , RECEIVE = receive_function
--    , SEND = send_function
--    , TYPMOD_IN = type_modifier_input_function
--    , TYPMOD_OUT = type_modifier_output_function
--    , ANALYZE = analyze_function
--    , INTERNALLENGTH = { internallength | VARIABLE }
--    , PASSEDBYVALUE
--    , ALIGNMENT = alignment
--    , STORAGE = storage
--    , LIKE = like_type
--    , CATEGORY = category
--    , PREFERRED = preferred
--    , DEFAULT = default
--    , ELEMENT = element
--    , DELIMITER = delimiter
--    , COLLATABLE = collatable

-- )
''')

    def TemplateAlterType(self):
        return Template('''ALTER TYPE #type_name#
--ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
--ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
--OWNER TO new_owner
--RENAME TO new_name
--SET SCHEMA new_schema
--ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } existing_enum_value ]
''')

    def TemplateDropType(self):
        return Template('''DROP TYPE #type_name#
--CASCADE
''')

    def TemplateCreateDomain(self):
        return Template('''CREATE DOMAIN #schema_name#.name AS data_type
--COLLATE collation
--DEFAULT expression
-- [ CONSTRAINT constraint_name ] NOT NULL
-- [ CONSTRAINT constraint_name ] NULL
-- [ CONSTRAINT constraint_name ] CHECK (expression)
''')

    def TemplateAlterDomain(self):
        return Template('''ALTER DOMAIN #domain_name#
--SET DEFAULT expression
--DROP DEFAULT
--SET NOT NULL
--DROP NOT NULL
--ADD domain_constraint [ NOT VALID ]
--DROP CONSTRAINT constraint_name [ CASCADE ]
--RENAME CONSTRAINT constraint_name TO new_constraint_name
--VALIDATE CONSTRAINT constraint_name
--OWNER TO new_owner
--RENAME TO new_name
--SET SCHEMA new_schema
''')

    def TemplateDropDomain(self):
        return Template('''DROP DOMAIN #domain_name#
--CASCADE
''')

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

    def TemplateAnalyze(self):
        return Template('ANALYZE')

    def TemplateAnalyzeTable(self):
        return Template('''ANALYZE #table_name#
--(column_name, [, ...])
''')

    def TemplateSelect(self, p_schema, p_table, p_kind):
        if p_kind == 't':
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
        elif p_kind == 'v':
            v_sql = 'SELECT t.'
            v_fields = self.QueryViewFields(p_table, False, p_schema)
            if len(v_fields.Rows) > 0:
                v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])
            v_sql += '\nFROM {0}.{1} t'.format(p_schema, p_table)
        elif p_kind == 'm':
            v_sql = 'SELECT t.'
            v_fields = self.QueryMaterializedViewFields(p_table, False, p_schema)
            if len(v_fields.Rows) > 0:
                v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])
            v_sql += '\nFROM {0}.{1} t'.format(p_schema, p_table)
        elif p_kind == 'f':
            v_sql = 'SELECT t.'
            v_fields = self.QueryForeignTablesFields(p_table, False, p_schema)
            if len(v_fields.Rows) > 0:
                v_sql += '\n     , t.'.join([r['column_name'] for r in v_fields.Rows])
            v_sql += '\nFROM {0}.{1} t'.format(p_schema, p_table)
        else:
            v_sql = 'SELECT t.*\nFROM {0}.{1} t'.format(p_schema, p_table)
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

    def TemplateDelete(self):
        return Template('''DELETE FROM
--ONLY
#table_name#
WHERE condition
--WHERE CURRENT OF cursor_name
--RETURNING *
''')

    def TemplateTruncate(self):
        return Template('''TRUNCATE
--ONLY
#table_name#
--RESTART IDENTITY
--CASCADE
''')

    def TemplateSelectFunction(self, p_schema, p_function, p_functionid):
        v_table = self.v_connection.Query('''
            select p.proretset
            from pg_proc p,
                 pg_namespace n
            where p.pronamespace = n.oid
              and n.nspname = '{0}'
              and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
        '''.format(p_schema, p_functionid))
        if len(v_table.Rows) > 0:
            v_retset = v_table.Rows[0][0]
        else:
            v_retset = False
        v_fields = self.QueryFunctionFields(p_functionid, p_schema)
        if len(v_fields.Rows) > 1:
            if v_retset:
                v_sql = 'SELECT * FROM {0}.{1}(\n    '.format(p_schema, p_function)
            else:
                v_sql = 'SELECT {0}.{1}(\n    '.format(p_schema, p_function)
            v_first = True
            for r in v_fields.Rows:
                if r['name'].split(' ')[0] != '"returns':
                    if r['type'] == 'I':
                        v_type = 'IN'
                    elif r['type'] == 'O':
                        v_type = 'OUT'
                    else:
                        v_type = 'INOUT'
                    if v_first:
                        v_sql += '? -- {0} {1}'.format(r['name'], v_type)
                        v_first = False
                    else:
                        v_sql += '\n  , ? -- {0} {1}'.format(r['name'], v_type)
            v_sql += '\n)'
        else:
            if v_retset:
                v_sql = 'SELECT * FROM {0}.{1}()'.format(p_schema, p_function)
            else:
                v_sql = 'SELECT {0}.{1}()'.format(p_schema, p_function)
        return Template(v_sql)

    def TemplateCallProcedure(self, p_schema, p_procedure, p_procedureid):
        v_fields = self.QueryProcedureFields(p_procedureid, p_schema)
        if len(v_fields.Rows) > 0:
            v_sql = 'CALL {0}.{1}(\n    '.format(p_schema, p_procedure)
            v_first = True
            for r in v_fields.Rows:
                if r['type'] == 'I':
                    v_type = 'IN'
                elif r['type'] == 'O':
                    v_type = 'OUT'
                else:
                    v_type = 'INOUT'
                if v_first:
                    v_sql += '? -- {0} {1}'.format(r['name'], v_type)
                    v_first = False
                else:
                    v_sql += '\n  , ? -- {0} {1}'.format(r['name'], v_type)
            v_sql += '\n)'
        else:
            v_sql = 'CALL {0}.{1}()'.format(p_schema, p_procedure)
        return Template(v_sql)

    def TemplateCreatePhysicalReplicationSlot(self):
        return Template('''SELECT * FROM pg_create_physical_replication_slot('slot_name')''')

    def TemplateDropPhysicalReplicationSlot(self):
        return Template('''SELECT pg_drop_replication_slot('#slot_name#')''')

    def TemplateCreateLogicalReplicationSlot(self):
        if int(self.v_version_num) >= 100000:
            return Template('''SELECT * FROM pg_create_logical_replication_slot('slot_name', 'pgoutput')''')
        else:
            return Template('''SELECT * FROM pg_create_logical_replication_slot('slot_name', 'test_decoding')''')

    def TemplateDropLogicalReplicationSlot(self):
        return Template('''SELECT pg_drop_replication_slot('#slot_name#')''')

    def TemplateCreatePublication(self):
        return Template('''CREATE PUBLICATION name
--FOR TABLE [ ONLY ] table_name [ * ] [, ...]
--FOR ALL TABLES
--WITH ( publish = 'insert, update, delete, truncate' )
''')

    def TemplateAlterPublication(self):
        return Template('''ALTER PUBLICATION #pub_name#
--ADD TABLE [ ONLY ] table_name [ * ] [, ...]
--SET TABLE [ ONLY ] table_name [ * ] [, ...]
--DROP TABLE [ ONLY ] table_name [ * ] [, ...]
--SET ( publish = 'insert, update, delete, truncate' )
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

    def TemplateCreateForeignDataWrapper(self):
        return Template('''CREATE FOREIGN DATA WRAPPER name
--HANDLER handler_function
--NO HANDLER
--VALIDATOR validator_function
--NO VALIDATOR
--OPTIONS ( option 'value' [, ... ] )
''')

    def TemplateAlterForeignDataWrapper(self):
        return Template('''ALTER FOREIGN DATA WRAPPER #fdwname#
--HANDLER handler_function
--NO HANDLER
--VALIDATOR validator_function
--NO VALIDATOR
--OPTIONS ( [ ADD ] option ['value'] [, ... ] )
--OPTIONS ( SET option ['value'] )
--OPTIONS ( DROP option )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''')

    def TemplateDropForeignDataWrapper(self):
        return Template('''DROP FOREIGN DATA WRAPPER #fdwname#
--CASCADE
''')

    def TemplateCreateForeignServer(self):
        return Template('''CREATE SERVER server_name
--TYPE 'server_type'
--VERSION 'server_version'
FOREIGN DATA WRAPPER #fdwname#
--OPTIONS ( option 'value' [, ... ] )
''')

    def TemplateAlterForeignServer(self):
        return Template('''ALTER SERVER #srvname#
--VERSION 'new_version'
--OPTIONS ( [ ADD ] option ['value'] [, ... ] )
--OPTIONS ( SET option ['value'] )
--OPTIONS ( DROP option )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''')

    def TemplateDropForeignServer(self):
        return Template('''DROP SERVER #srvname#
--CASCADE
''')

    def TemplateCreateUserMapping(self):
        return Template('''CREATE USER MAPPING
--FOR user_name
--FOR CURRENT_USER
--FOR PUBLIC
SERVER #srvname#
--OPTIONS ( option 'value' [ , ... ] )
''')

    def TemplateAlterUserMapping(self):
        return Template('''ALTER USER MAPPING FOR #user_name#
SERVER #srvname#
--OPTIONS ( [ ADD ] option ['value'] [, ... ] )
--OPTIONS ( SET option ['value'] )
--OPTIONS ( DROP option )
''')

    def TemplateImportForeignSchema(self):
        return Template('''IMPORT FOREIGN SCHEMA remote_schema
--LIMIT TO ( table_name [, ...] )
--EXCEPT ( table_name [, ...] )
FROM SERVER #srvname#
INTO local_schema
--OPTIONS ( option 'value' [, ... ] )
''')

    def TemplateDropUserMapping(self):
        return Template('DROP USER MAPPING #user_name# SERVER #srvname#')

    def TemplateCreateForeignTable(self):
        return Template('''CREATE FOREIGN TABLE #schema_name#.table_name
--PARTITION OF parent_table
(
    column_name data_type
    --OPTIONS ( option 'value' [, ... ] )
    --COLLATE collation
    --CONSTRAINT constraint_name
    --NOT NULL
    --CHECK ( expression )
    --NO INHERIT
    --DEFAULT default_expr
)
--INHERITS ( parent_table [, ... ] )
SERVER server_name
--partition_bound_spec
--OPTIONS ( option 'value' [, ... ] )
''')

    def TemplateAlterForeignTable(self):
        return Template('''ALTER FOREIGN TABLE #table_name#
--ADD COLUMN column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
--DROP COLUMN column_name [ CASCADE ]
--ALTER [ COLUMN column_name [ SET DATA ] TYPE data_type [ COLLATE collation ]
--ALTER COLUMN column_name SET DEFAULT expression
--ALTER COLUMN column_name DROP DEFAULT
--ALTER COLUMN column_name { SET | DROP } NOT NULL
--ALTER COLUMN column_name SET STATISTICS integer
--ALTER COLUMN column_name SET ( attribute_option = value [, ... ] )
--ALTER COLUMN column_name RESET ( attribute_option [, ... ] )
--ALTER COLUMN column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
--ALTER COLUMN column_name OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )
--ADD table_constraint [ NOT VALID ]
--VALIDATE CONSTRAINT constraint_name
--DROP CONSTRAINT constraint_name [ CASCADE ]
--DISABLE TRIGGER [ trigger_name | ALL | USER ]
--ENABLE TRIGGER [ trigger_name | ALL | USER ]
--ENABLE REPLICA TRIGGER trigger_name
--ENABLE ALWAYS TRIGGER trigger_name
--SET WITH OIDS
--SET WITHOUT OIDS
--INHERIT parent_table
--NO INHERIT parent_table
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )
--RENAME COLUMN column_name TO new_column_name
--RENAME TO new_name
--SET SCHEMA new_schema
''')

    def TemplateDropForeignTable(self):
        return Template('''DROP FOREIGN TABLE #table_name#
--CASCADE
''')

    def TemplateCreateForeignColumn(self):
        return Template('''ALTER FOREIGN TABLE #table_name#
ADD COLUMN name data_type
--COLLATE collation
--column_constraint [ ... ] ]
''')

    def TemplateAlterForeignColumn(self):
        return Template('''ALTER FOREIGN TABLE #table_name#
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
--OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )
'''
)

    def TemplateDropForeignColumn(self):
        return Template('''ALTER FOREIGN TABLE #table_name#
DROP COLUMN #column_name#
--CASCADE
''')

    def GetPropertiesRole(self, p_object):
        return self.v_connection.Query('''
            select rolname as "Role",
                   oid as "OID",
                   rolsuper as "Super User",
                   rolinherit as "Inherit",
                   rolcreaterole as "Can Create Role",
                   rolcreatedb as "Can Create Database",
                   rolcanlogin as "Can Login",
                   rolreplication as "Replication",
                   rolconnlimit as "Connection Limit",
                   rolvaliduntil as "Valid Until"
            from pg_roles
            where quote_ident(rolname) = '{0}'
        '''.format(p_object))

    def GetPropertiesTablespace(self, p_object):
        return self.v_connection.Query('''
            select t.spcname as "Tablespace",
                   r.rolname as "Owner",
                   t.oid as "OID",
                   pg_tablespace_location(t.oid) as "Location",
                   t.spcacl as "ACL",
                   t.spcoptions as "Options"
            from pg_tablespace t
            inner join pg_roles r
            on r.oid = t.spcowner
            where quote_ident(t.spcname) = '{0}'
        '''.format(p_object))

    def GetPropertiesDatabase(self, p_object):
        return self.v_connection.Query('''
            select d.datname as "Database",
                   r.rolname as "Owner",
                   pg_size_pretty(pg_database_size(d.oid)) as "Size",
                   pg_encoding_to_char(d.encoding) as "Encoding",
                   d.datcollate as "LC_COLLATE",
                   d.datctype as "LC_CTYPE",
                   d.datistemplate as "Is Template",
                   d.datallowconn as "Allows Connections",
                   d.datconnlimit as "Connection Limit",
                   t.spcname as "Tablespace",
                   d.datacl as "ACL"
            from pg_database d
            inner join pg_roles r
            on r.oid = d.datdba
            inner join pg_tablespace t
            on t.oid = d.dattablespace
            where quote_ident(d.datname) = '{0}'
        '''.format(p_object))

    def GetPropertiesExtension(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   e.extname as "Extension",
                   r.rolname as "Owner",
                   n.nspname as "Schema",
                   e.extrelocatable as "Relocatable",
                   e.extversion as "Version"
            from pg_extension e
            inner join pg_roles r
            on r.oid = e.extowner
            inner join pg_namespace n
            on n.oid = e.extnamespace
            where e.extname = '{0}'
        '''.format(p_object))

    def GetPropertiesSchema(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   r.rolname as "Owner",
                   n.nspacl as "ACL"
            from pg_namespace n
            inner join pg_roles r
            on r.oid = n.nspowner
            where quote_ident(n.nspname) = '{0}'
        '''.format(p_object))

    def GetPropertiesTable(self, p_schema, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhaspkey as "Has Primary Key",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000 and int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhaspkey as "Has Primary Key",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass",
                       c.relkind = 'p' as "Is Partitioned",
                       c.relispartition as "Is Partition",
                       (case when c.relispartition then po.parent_table else '' end) as "Partition Of"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                left join (
                select quote_ident(n2.nspname) || '.' || quote_ident(c2.relname) as parent_table
                from pg_inherits i
                inner join pg_class c2
                on c2.oid = i.inhparent
                inner join pg_namespace n2
                on n2.oid = c2.relnamespace
                where i.inhrelid = '{0}.{1}'::regclass
                ) po
                on 1 = 1
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))
        else:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass",
                       c.relkind = 'p' as "Is Partitioned",
                       c.relispartition as "Is Partition",
                       (case when c.relispartition then po.parent_table else '' end) as "Partition Of"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                left join (
                select quote_ident(n2.nspname) || '.' || quote_ident(c2.relname) as parent_table
                from pg_inherits i
                inner join pg_class c2
                on c2.oid = i.inhparent
                inner join pg_namespace n2
                on n2.oid = c2.relnamespace
                where i.inhrelid = '{0}.{1}'::regclass
                ) po
                on 1 = 1
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))

    def GetPropertiesIndex(self, p_schema, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   c.relname as "Index",
                   c.oid as "OID",
                   r.rolname as "Owner",
                   pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                   a.amname as "Access Method",
                   coalesce(t1.spcname, t2.spcname) as "Tablespace",
                   pg_relation_filepath(c.oid) as "Filenode"
            from pg_class c
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_roles r
            on r.oid = c.relowner
            left join pg_tablespace t1
            on t1.oid = c.reltablespace
            inner join (
            select t.spcname
            from pg_database d
            inner join pg_tablespace t
            on t.oid = d.dattablespace
            where d.datname = current_database()
            ) t2
            on 1 = 1
            inner join pg_am a
            on a.oid = c.relam
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(c.relname) = '{1}'
        '''.format(p_schema, p_object))

    def GetPropertiesSequence(self, p_schema, p_object):
        v_table1 = self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   c.relname as "Sequence",
                   c.oid as "OID",
                   r.rolname as "Owner",
                   coalesce(t1.spcname, t2.spcname) as "Tablespace",
                   pg_relation_filepath(c.oid) as "Filenode"
            from pg_class c
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_roles r
            on r.oid = c.relowner
            left join pg_tablespace t1
            on t1.oid = c.reltablespace
            inner join (
            select t.spcname
            from pg_database d
            inner join pg_tablespace t
            on t.oid = d.dattablespace
            where d.datname = current_database()
            ) t2
            on 1 = 1
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(c.relname) = '{1}'
        '''.format(p_schema, p_object)).Transpose('Property', 'Value')
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            v_table2 = self.v_connection.Query('''
                select last_value as "Last Value",
                       start_value as "Start Value",
                       increment_by as "Increment By",
                       max_value as "Max Value",
                       min_value as "Min Value",
                       cache_value as "Cache Value",
                       is_cycled as "Is Cycled",
                       is_called as "Is Called"
                from {0}.{1}
            '''.format(p_schema, p_object)).Transpose('Property', 'Value')
        else:
            v_table2 = self.v_connection.Query('''
                select data_type as "Data Type",
                       last_value as "Last Value",
                       start_value as "Start Value",
                       increment_by as "Increment By",
                       max_value as "Max Value",
                       min_value as "Min Value",
                       cache_size as "Cache Size",
                       cycle as "Is Cycled"
                from pg_sequences
                where schemaname = '{0}'
                  and sequencename = '{1}'
            '''.format(p_schema, p_object)).Transpose('Property', 'Value')
            v_table1.Merge(v_table2)
        v_table1.Merge(v_table2)
        return v_table1

    def GetPropertiesView(self, p_schema, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   c.relname as "View",
                   c.oid as "OID",
                   r.rolname as "Owner"
            from pg_class c
            inner join pg_namespace n
            on n.oid = c.relnamespace
            inner join pg_roles r
            on r.oid = c.relowner
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(c.relname) = '{1}'
        '''.format(p_schema, p_object))

    def GetPropertiesFunction(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       p.proname as "Function",
                       quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as "Function ID",
                       p.oid as "OID",
                       r.rolname as "Owner",
                       l.lanname as "Language",
                       p.procost as "Estimated Execution Cost",
                       p.prorows as "Estimated Returned Rows",
                       p.proisagg as "Is Aggregate",
                       p.proiswindow as "Is Window",
                       p.prosecdef as "Security Definer",
                       p.proleakproof as "Leak Proof",
                       p.proisstrict as "Is Strict",
                       p.proretset as "Returns Set",
                       (case p.provolatile when 'i' then 'Immutable' when 's' then 'Stable' when 'v' then 'Volatile' end) as "Volatile",
                       p.pronargs as "Number of Arguments",
                       p.pronargdefaults as "Number of Default Arguments",
                       p.probin as "Invoke",
                       p.proconfig as "Configuration",
                       p.proacl as "ACL"
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                inner join pg_roles r
                on r.oid = p.proowner
                inner join pg_language l
                on l.oid = p.prolang
                where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
            '''.format(p_object))
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       p.proname as "Function",
                       quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as "Function ID",
                       p.oid as "OID",
                       r.rolname as "Owner",
                       l.lanname as "Language",
                       p.procost as "Estimated Execution Cost",
                       p.prorows as "Estimated Returned Rows",
                       p.proisagg as "Is Aggregate",
                       p.proiswindow as "Is Window",
                       p.prosecdef as "Security Definer",
                       p.proleakproof as "Leak Proof",
                       p.proisstrict as "Is Strict",
                       p.proretset as "Returns Set",
                       (case p.provolatile when 'i' then 'Immutable' when 's' then 'Stable' when 'v' then 'Volatile' end) as "Volatile",
                       (case p.proparallel when 's' then 'Safe' when 'r' then 'Restricted' when 'u' then 'Unsafe' end) as "Parallel",
                       p.pronargs as "Number of Arguments",
                       p.pronargdefaults as "Number of Default Arguments",
                       p.probin as "Invoke",
                       p.proconfig as "Configuration",
                       p.proacl as "ACL"
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                inner join pg_roles r
                on r.oid = p.proowner
                inner join pg_language l
                on l.oid = p.prolang
                where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
            '''.format(p_object))
        else:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       p.proname as "Function",
                       quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as "Function ID",
                       p.oid as "OID",
                       r.rolname as "Owner",
                       (case p.prokind when 'f' then 'Normal' when 'a' then 'Aggregate' when 'w' then 'Window' end) as "Function Kind",
                       l.lanname as "Language",
                       p.procost as "Estimated Execution Cost",
                       p.prorows as "Estimated Returned Rows",
                       p.prosecdef as "Security Definer",
                       p.proleakproof as "Leak Proof",
                       p.proisstrict as "Is Strict",
                       p.proretset as "Returns Set",
                       (case p.provolatile when 'i' then 'Immutable' when 's' then 'Stable' when 'v' then 'Volatile' end) as "Volatile",
                       (case p.proparallel when 's' then 'Safe' when 'r' then 'Restricted' when 'u' then 'Unsafe' end) as "Parallel",
                       p.pronargs as "Number of Arguments",
                       p.pronargdefaults as "Number of Default Arguments",
                       p.probin as "Invoke",
                       p.proconfig as "Configuration",
                       p.proacl as "ACL"
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                inner join pg_roles r
                on r.oid = p.proowner
                inner join pg_language l
                on l.oid = p.prolang
                where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
                  and p.prokind = 'f'
            '''.format(p_object))

    def GetPropertiesProcedure(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   p.proname as "Procedure",
                   quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as "Procedure ID",
                   p.oid as "OID",
                   r.rolname as "Owner",
                   l.lanname as "Language",
                   p.procost as "Estimated Execution Cost",
                   p.prorows as "Estimated Returned Rows",
                   p.prosecdef as "Security Definer",
                   p.proleakproof as "Leak Proof",
                   p.proisstrict as "Is Strict",
                   (case p.provolatile when 'i' then 'Immutable' when 's' then 'Stable' when 'v' then 'Volatile' end) as "Volatile",
                   (case p.proparallel when 's' then 'Safe' when 'r' then 'Restricted' when 'u' then 'Unsafe' end) as "Parallel",
                   p.pronargs as "Number of Arguments",
                   p.pronargdefaults as "Number of Default Arguments",
                   p.probin as "Invoke",
                   p.proconfig as "Configuration",
                   p.proacl as "ACL"
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            inner join pg_roles r
            on r.oid = p.proowner
            inner join pg_language l
            on l.oid = p.prolang
            where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
              and p.prokind = 'p'
        '''.format(p_object))

    def GetPropertiesTrigger(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   y.schema_name as "Schema",
                   y.table_name as "Table",
                   y.trigger_name as "Trigger",
                   y.oid as "OID",
                   y.trigger_enabled as "Enabled",
                   y.trigger_function_name as "Trigger Function",
                   x.action_timing as "Action Timing",
                   x.event_manipulation as "Action Manipulation",
                   x.action_orientation as "Action Orientation",
                   x.action_condition as "Action Condition",
                   x.action_statement as "Action Statement"
            from (
            select distinct quote_ident(t.event_object_schema) as schema_name,
                   quote_ident(t.event_object_table) as table_name,
                   quote_ident(t.trigger_name) as trigger_name,
                   t.action_timing,
                   array_to_string(array(
                   select t2.event_manipulation::text
                   from information_schema.triggers t2
                   where t2.event_object_schema = t.event_object_schema
                     and t2.event_object_table = t.event_object_table
                     and t2.trigger_name = t.trigger_name
                   ), ' OR ') as event_manipulation,
                   t.action_orientation,
                   t.action_condition,
                   t.action_statement
            from information_schema.triggers t
            where quote_ident(t.event_object_schema) = '{0}'
              and quote_ident(t.event_object_table) = '{1}'
              and quote_ident(t.trigger_name) = '{2}'
            ) x
            inner join (
            select t.oid,
                   quote_ident(n.nspname) as schema_name,
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
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(c.relname) = '{1}'
              and quote_ident(t.tgname) = '{2}'
            ) y
            on y.schema_name = x.schema_name
            and y.table_name = x.table_name
            and y.trigger_name = x.trigger_name
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesPK(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_constraint_attrs(text, text, text)
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
            where contype = 'p'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
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
            select current_database() as "Database",
                   quote_ident(n.nspname) as "Schema",
                   quote_ident(t.relname) as "Table",
                   quote_ident(c.conname) as "Constraint Name",
                   c.oid as "OID",
                   (case c.contype when 'c' then 'Check' when 'f' then 'Foreign Key' when 'p' then 'Primary Key' when 'u' then 'Unique' when 'x' then 'Exclusion' end) as "Constraint Type",
                   pg_temp.fnc_omnidb_constraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Constrained Columns",
                   quote_ident(i.relname) as "Index",
                   c.condeferrable as "Deferrable",
                   c.condeferred as "Deferred by Default",
                   c.convalidated as "Validated",
                   c.conislocal as "Is Local",
                   c.coninhcount as "Number of Ancestors",
                   c.connoinherit as "Non-Inheritable"
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            join pg_class i
            on i.oid = c.conindid
            where contype = 'p'
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(t.relname) = '{1}'
              and quote_ident(c.conname) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesFK(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_constraint_attrs(text, text, text)
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
            where contype = 'f'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
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
            create or replace function pg_temp.fnc_omnidb_rconstraint_attrs(text, text, text)
            returns text as $$
            select array_to_string(array(
            select a.attname
            from (
            select unnest(c.confkey) as confkey
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'f'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_attribute a
            on a.attnum = x.confkey
            inner join pg_class r
            on r.oid = a.attrelid
            inner join pg_namespace n
            on n.oid = r.relnamespace
            where quote_ident(n.nspname) = $1
              and quote_ident(r.relname) = $2
            ), ',')
            $$ language sql;
            create or replace function pg_temp.fnc_omnidb_pfconstraint_ops(text, text, text)
            returns text as $$
            select array_to_string(array(
            select oprname
            from (
            select o.oprname
            from (
            select unnest(c.conpfeqop) as conpfeqop
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_operator o
            on o.oid = x.conpfeqop
            ) t
            ), ',')
            $$ language sql;
            create or replace function pg_temp.fnc_omnidb_ppconstraint_ops(text, text, text)
            returns text as $$
            select array_to_string(array(
            select oprname
            from (
            select o.oprname
            from (
            select unnest(c.conppeqop) as conppeqop
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_operator o
            on o.oid = x.conppeqop
            ) t
            ), ',')
            $$ language sql;
            create or replace function pg_temp.fnc_omnidb_ffconstraint_ops(text, text, text)
            returns text as $$
            select array_to_string(array(
            select oprname
            from (
            select o.oprname
            from (
            select unnest(c.conffeqop) as conffeqop
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_operator o
            on o.oid = x.conffeqop
            ) t
            ), ',')
            $$ language sql;
            select current_database() as "Database",
                   quote_ident(n.nspname) as "Schema",
                   quote_ident(t.relname) as "Table",
                   quote_ident(c.conname) as "Constraint Name",
                   c.oid as "OID",
                   (case c.contype when 'c' then 'Check' when 'f' then 'Foreign Key' when 'p' then 'Primary Key' when 'u' then 'Unique' when 'x' then 'Exclusion' end) as "Constraint Type",
                   pg_temp.fnc_omnidb_constraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Constrained Columns",
                   quote_ident(i.relname) as "Index",
                   quote_ident(nr.nspname) as "Referenced Schema",
                   quote_ident(tr.relname) as "Referenced Table",
                   pg_temp.fnc_omnidb_rconstraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Referenced Columns",
                   (case c.confupdtype when 'a' then 'No Action' when 'r' then 'Restrict' when 'c' then 'Cascade' when 'n' then 'Set Null' when 'd' then 'Set Default' end) as "Update Action",
                   (case c.confdeltype when 'a' then 'No Action' when 'r' then 'Restrict' when 'c' then 'Cascade' when 'n' then 'Set Null' when 'd' then 'Set Default' end) as "Delete Action",
                   (case c.confmatchtype when 'f' then 'Full' when 'p' then 'Partial' when 's' then 'Simple' end) as "Match Type",
                   c.condeferrable as "Deferrable",
                   c.condeferred as "Deferred by Default",
                   c.convalidated as "Validated",
                   c.conislocal as "Is Local",
                   c.coninhcount as "Number of Ancestors",
                   c.connoinherit as "Non-Inheritable",
                   pg_temp.fnc_omnidb_pfconstraint_ops(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "PK=FK Equality Operators",
                   pg_temp.fnc_omnidb_ppconstraint_ops(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "PK=PK Equality Operators",
                   pg_temp.fnc_omnidb_ffconstraint_ops(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "FK=FK Equality Operators"
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            join pg_class i
            on i.oid = c.conindid
            join pg_class tr
            on tr.oid = c.confrelid
            join pg_namespace nr
            on tr.relnamespace = nr.oid
            where contype = 'f'
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(t.relname) = '{1}'
              and quote_ident(c.conname) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesUnique(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_constraint_attrs(text, text, text)
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
            where contype = 'u'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
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
            select current_database() as "Database",
                   quote_ident(n.nspname) as "Schema",
                   quote_ident(t.relname) as "Table",
                   quote_ident(c.conname) as "Constraint Name",
                   c.oid as "OID",
                   (case c.contype when 'c' then 'Check' when 'f' then 'Foreign Key' when 'p' then 'Primary Key' when 'u' then 'Unique' when 'x' then 'Exclusion' end) as "Constraint Type",
                   pg_temp.fnc_omnidb_constraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Constrained Columns",
                   quote_ident(i.relname) as "Index",
                   c.condeferrable as "Deferrable",
                   c.condeferred as "Deferred by Default",
                   c.convalidated as "Validated",
                   c.conislocal as "Is Local",
                   c.coninhcount as "Number of Ancestors",
                   c.connoinherit as "Non-Inheritable"
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            join pg_class i
            on i.oid = c.conindid
            where contype = 'u'
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(t.relname) = '{1}'
              and quote_ident(c.conname) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesCheck(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_constraint_attrs(text, text, text)
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
            where contype = 'c'
              and quote_ident(n.nspname) = $1
              and quote_ident(t.relname) = $2
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
            select current_database() as "Database",
                   quote_ident(n.nspname) as "Schema",
                   quote_ident(t.relname) as "Table",
                   quote_ident(c.conname) as "Constraint Name",
                   c.oid as "OID",
                   (case c.contype when 'c' then 'Check' when 'f' then 'Foreign Key' when 'p' then 'Primary Key' when 'u' then 'Unique' when 'x' then 'Exclusion' end) as "Constraint Type",
                   pg_temp.fnc_omnidb_constraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Constrained Columns",
                   c.condeferrable as "Deferrable",
                   c.condeferred as "Deferred by Default",
                   c.convalidated as "Validated",
                   c.conislocal as "Is Local",
                   c.coninhcount as "Number of Ancestors",
                   c.connoinherit as "Non-Inheritable",
                   c.consrc as "Constraint Source"
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'c'
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(t.relname) = '{1}'
              and quote_ident(c.conname) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesExclude(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            create or replace function pg_temp.fnc_omnidb_constraint_ops(text, text, text)
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
              and quote_ident(t.relname) = $2
              and quote_ident(c.conname) = $3
            ) x
            inner join pg_operator o
            on o.oid = x.conexclop
            ) t
            ), ',')
            $$ language sql;
            create or replace function pg_temp.fnc_omnidb_constraint_attrs(text, text, text)
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
              and quote_ident(t.relname) = $2
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
            select current_database() as "Database",
                   quote_ident(n.nspname) as "Schema",
                   quote_ident(t.relname) as "Table",
                   quote_ident(c.conname) as "Constraint Name",
                   c.oid as "OID",
                   (case c.contype when 'c' then 'Check' when 'f' then 'Foreign Key' when 'p' then 'Primary Key' when 'u' then 'Unique' when 'x' then 'Exclusion' end) as "Constraint Type",
                   pg_temp.fnc_omnidb_constraint_attrs(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Constrained Columns",
                   pg_temp.fnc_omnidb_constraint_ops(
                       quote_ident(n.nspname),
                       quote_ident(t.relname),
                       quote_ident(c.conname)
                   ) as "Exclusion Operators",
                   c.condeferrable as "Deferrable",
                   c.condeferred as "Deferred by Default",
                   c.convalidated as "Validated",
                   c.conislocal as "Is Local",
                   c.coninhcount as "Number of Ancestors",
                   c.connoinherit as "Non-Inheritable"
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
              and quote_ident(n.nspname) = '{0}'
              and quote_ident(t.relname) = '{1}'
              and quote_ident(c.conname) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesRule(self, p_schema, p_table, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   quote_ident(schemaname) as "Schema",
                   quote_ident(tablename) as "Table",
                   quote_ident(rulename) as "Rule Name"
            from pg_rules
            where quote_ident(schemaname) = '{0}'
              and quote_ident(tablename) = '{1}'
              and quote_ident(rulename) = '{2}'
        '''.format(p_schema, p_table, p_object))

    def GetPropertiesForeignTable(self, p_schema, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhaspkey as "Has Primary Key",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass",
                       array_to_string(f.ftoptions, ',') as "Foreign Table Options",
                       s.srvname as "Foreign Server",
                       w.fdwname as "Foreign Data Wrapper"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                inner join pg_foreign_table f
                on f.ftrelid = c.oid
                inner join pg_foreign_server s
                on s.oid = f.ftserver
                inner join pg_foreign_data_wrapper w
                on w.oid = s.srvfdw
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000 and int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass",
                       c.relkind = 'p' as "Is Partitioned",
                       c.relispartition as "Is Partition",
                       (case when c.relispartition then po.parent_table else '' end) as "Partition Of",
                       array_to_string(f.ftoptions, ',') as "Foreign Table Options",
                       s.srvname as "Foreign Server",
                       w.fdwname as "Foreign Data Wrapper"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                left join (
                select quote_ident(n2.nspname) || '.' || quote_ident(c2.relname) as parent_table
                from pg_inherits i
                inner join pg_class c2
                on c2.oid = i.inhparent
                inner join pg_namespace n2
                on n2.oid = c2.relnamespace
                where i.inhrelid = '{0}.{1}'::regclass
                ) po
                on 1 = 1
                inner join pg_foreign_table f
                on f.ftrelid = c.oid
                inner join pg_foreign_server s
                on s.oid = f.ftserver
                inner join pg_foreign_data_wrapper w
                on w.oid = s.srvfdw
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))
        else:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       n.nspname as "Schema",
                       c.relname as "Table",
                       c.oid as "OID",
                       r.rolname as "Owner",
                       pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                       coalesce(t1.spcname, t2.spcname) as "Tablespace",
                       c.relacl as "ACL",
                       c.reloptions as "Options",
                       pg_relation_filepath(c.oid) as "Filenode",
                       c.reltuples as "Estimate Count",
                       c.relhasindex as "Has Index",
                       (case c.relpersistence when 'p' then 'Permanent' when 'u' then 'Unlogged' when 't' then 'Temporary' end) as "Persistence",
                       c.relnatts as "Number of Attributes",
                       c.relchecks as "Number of Checks",
                       c.relhasoids as "Has OIDs",
                       c.relhasrules as "Has Rules",
                       c.relhastriggers as "Has Triggers",
                       c.relhassubclass as "Has Subclass",
                       c.relkind = 'p' as "Is Partitioned",
                       c.relispartition as "Is Partition",
                       (case when c.relispartition then po.parent_table else '' end) as "Partition Of",
                       array_to_string(f.ftoptions, ',') as "Foreign Table Options",
                       s.srvname as "Foreign Server",
                       w.fdwname as "Foreign Data Wrapper"
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                inner join pg_roles r
                on r.oid = c.relowner
                left join pg_tablespace t1
                on t1.oid = c.reltablespace
                inner join (
                select t.spcname
                from pg_database d
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                where d.datname = current_database()
                ) t2
                on 1 = 1
                left join (
                select quote_ident(n2.nspname) || '.' || quote_ident(c2.relname) as parent_table
                from pg_inherits i
                inner join pg_class c2
                on c2.oid = i.inhparent
                inner join pg_namespace n2
                on n2.oid = c2.relnamespace
                where i.inhrelid = '{0}.{1}'::regclass
                ) po
                on 1 = 1
                inner join pg_foreign_table f
                on f.ftrelid = c.oid
                inner join pg_foreign_server s
                on s.oid = f.ftserver
                inner join pg_foreign_data_wrapper w
                on w.oid = s.srvfdw
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(c.relname) = '{1}'
            '''.format(p_schema, p_object))

    def GetPropertiesUserMapping(self, p_server, p_object):
        if p_object == 'PUBLIC':
            return self.v_connection.Query('''
                select current_database() as "Database",
                       u.oid as "OID",
                       'PUBLIC' as "User",
                       array_to_string(u.umoptions, ',') as "Options",
                       s.srvname as "Foreign Server",
                       w.fdwname as "Foreign Wrapper"
                from pg_user_mapping u
                inner join pg_foreign_server s
                on s.oid = u.umserver
                inner join pg_foreign_data_wrapper w
                on w.oid = s.srvfdw
                where u.umuser = 0
                  and quote_ident(s.srvname) = '{0}'
            '''.format(p_server))
        else:
            return self.v_connection.Query('''
                select current_database() as "Database",
                       u.oid as "OID",
                       r.rolname as "User",
                       array_to_string(u.umoptions, ',') as "Options",
                       s.srvname as "Foreign Server",
                       w.fdwname as "Foreign Wrapper"
                from pg_user_mapping u
                inner join pg_foreign_server s
                on s.oid = u.umserver
                inner join pg_foreign_data_wrapper w
                on w.oid = s.srvfdw
                inner join pg_roles r
                on r.oid = u.umuser
                where quote_ident(s.srvname) = '{0}'
                  and quote_ident(r.rolname) = '{1}'
            '''.format(p_server, p_object))

    def GetPropertiesForeignServer(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   s.srvname as "Name",
                   s.oid as "OID",
                   r.rolname as "Owner",
                   s.srvtype as "Type",
                   s.srvversion as "Version",
                   array_to_string(srvoptions, ',') as "Options",
                   w.fdwname as "Foreign Wrapper"
            from pg_foreign_server s
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            inner join pg_roles r
            on r.oid = s.srvowner
            where quote_ident(s.srvname) = '{0}'
        '''.format(p_object))

    def GetPropertiesForeignDataWrapper(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   w.fdwname as "Name",
                   w.oid as "OID",
                   r.rolname as "Owner",
                   h.proname as "Handler",
                   v.proname as "Validator",
                   array_to_string(w.fdwoptions, ',') as "Options"
            from pg_foreign_data_wrapper w
            inner join pg_roles r
            on r.oid = w.fdwowner
            left join pg_proc h
            on h.oid = w.fdwhandler
            left join pg_proc v
            on v.oid = w.fdwvalidator
            where quote_ident(w.fdwname) = '{0}'
        '''.format(p_object))

    def GetPropertiesType(self, p_schema, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   t.typname as "Internal Type Name",
                   format_type(t.oid, null) as "SQL Type Name",
                   oid as "OID",
                   r.rolname as "Owner",
                   (case when t.typlen = -2 then 'Variable (null-terminated C string)'
                         when t.typlen = -1 then 'Variable (varlena type)'
                         else format('%s bytes', t.typlen)
                    end) as "Size",
                   t.typbyval as "Passed by Value",
                   (case t.typtype
                      when 'b' then 'Base'
                      when 'c' then 'Composite'
                      when 'd' then 'Domain'
                      when 'e' then 'Enum'
                      when 'p' then 'Pseudo'
                      when 'r' then 'Range'
                      else 'Undefined'
                    end) as "Type",
                   (case t.typcategory
                      when 'A' then 'A - Array'
                      when 'B' then 'B - Boolean'
                      when 'C' then 'C - Composite'
                      when 'D' then 'D - Date/Time'
                      when 'E' then 'E - Enum'
                      when 'G' then 'G - Geometric'
                      when 'I' then 'I - Network Address'
                      when 'N' then 'N - Numeric'
                      when 'P' then 'P - Pseudo'
                      when 'R' then 'R - Range'
                      when 'S' then 'S - String'
                      when 'T' then 'T - Timespan'
                      when 'U' then 'U - User-defined'
                      when 'V' then 'V - Bit-string'
                      else 'X - Unknown'
                    end) as "Category",
                   t.typispreferred as "Is Preferred",
                   t.typisdefined as "Is Defined",
                   t.typdelim as "Delimiter",
                   nrelid.nspname || '.' || crelid.relname as "Corresponding Table",
                   nelem.nspname || '.' || telem.typname as "Element Type",
                   narray.nspname || '.' || tarray.typname as "Array Type",
                   ninput.nspname || '.' || pinput.proname as "Input Conversion Function (Text Format)",
                   noutput.nspname || '.' || poutput.proname as "Output Conversion Function (Text Format)",
                   nreceive.nspname || '.' || preceive.proname as "Input Conversion Function (Binary Format)",
                   nsend.nspname || '.' || psend.proname as "Output Conversion Function (Binary Format)",
                   nmodin.nspname || '.' || pmodin.proname as "Type Modifier Input Function",
                   nmodout.nspname || '.' || pmodout.proname as "Type Modifier Input Function",
                   nanalyze.nspname || '.' || panalyze.proname as "Custom Analyze Function",
                   (case t.typalign
                      when 'c' then 'char'
                      when 's' then 'int2'
                      when 'i' then 'int4'
                      when 'd' then 'double'
                    end) as "Alignment",
                   (case t.typstorage
                      when 'p' then 'plain'
                      when 'e' then 'extended'
                      when 'm' then 'main'
                      when 'x' then 'external'
                    end) as "Storage",
                   t.typnotnull as "Not Null",
                   nbase.nspname || '.' || tbase.typname as "Base Type",
                   t.typtypmod as "Type Modifier",
                   t.typndims as "Number of Array Dimensions",
                   coll.collname as "Collation",
                   t.typdefault as "Default Value",
                   t.typacl as "ACL"
            from pg_type t
            inner join pg_roles r on r.oid = t.typowner
            inner join pg_namespace n on n.oid = t.typnamespace
            left join pg_class crelid on crelid.oid = t.typrelid
            left join pg_namespace nrelid on nrelid.oid = crelid.relnamespace
            left join pg_type telem on telem.oid = t.typelem
            left join pg_namespace nelem on nelem.oid = telem.typnamespace
            left join pg_type tarray on tarray.oid = t.typarray
            left join pg_namespace narray on narray.oid = tarray.typnamespace
            left join pg_proc pinput on pinput.oid = t.typinput
            left join pg_namespace ninput on ninput.oid = pinput.pronamespace
            left join pg_proc poutput on poutput.oid = t.typoutput
            left join pg_namespace noutput on noutput.oid = poutput.pronamespace
            left join pg_proc preceive on preceive.oid = t.typreceive
            left join pg_namespace nreceive on nreceive.oid = preceive.pronamespace
            left join pg_proc psend on psend.oid = t.typsend
            left join pg_namespace nsend on nsend.oid = psend.pronamespace
            left join pg_proc pmodin on pmodin.oid = t.typmodin
            left join pg_namespace nmodin on nmodin.oid = pmodin.pronamespace
            left join pg_proc pmodout on pmodout.oid = t.typmodout
            left join pg_namespace nmodout on nmodout.oid = pmodout.pronamespace
            left join pg_proc panalyze on panalyze.oid = t.typanalyze
            left join pg_namespace nanalyze on nanalyze.oid = panalyze.pronamespace
            left join pg_type tbase on tbase.oid = t.typbasetype
            left join pg_namespace nbase on nbase.oid = tbase.typnamespace
            left join pg_collation coll on coll.oid = t.typcollation
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(t.typname) = '{1}'
        '''.format(p_schema, p_object))

    def GetProperties(self, p_schema, p_table, p_object, p_type):
        try:
            if p_type == 'role':
                return self.GetPropertiesRole(p_object).Transpose('Property', 'Value')
            elif p_type == 'tablespace':
                return self.GetPropertiesTablespace(p_object).Transpose('Property', 'Value')
            elif p_type == 'database':
                return self.GetPropertiesDatabase(p_object).Transpose('Property', 'Value')
            elif p_type == 'extension':
                return self.GetPropertiesExtension(p_object).Transpose('Property', 'Value')
            elif p_type == 'schema':
                return self.GetPropertiesSchema(p_object).Transpose('Property', 'Value')
            elif p_type == 'table':
                return self.GetPropertiesTable(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'index':
                return self.GetPropertiesIndex(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'sequence':
                return self.GetPropertiesSequence(p_schema, p_object)
            elif p_type == 'view':
                return self.GetPropertiesView(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'mview':
                return self.GetPropertiesView(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'function':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'procedure':
                return self.GetPropertiesProcedure(p_object).Transpose('Property', 'Value')
            elif p_type == 'trigger':
                return self.GetPropertiesTrigger(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'triggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'direct_triggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'pk':
                return self.GetPropertiesPK(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'foreign_key':
                return self.GetPropertiesFK(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'unique':
                return self.GetPropertiesUnique(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'check':
                return self.GetPropertiesCheck(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'exclude':
                return self.GetPropertiesExclude(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'rule':
                return self.GetPropertiesRule(p_schema, p_table, p_object).Transpose('Property', 'Value')
            elif p_type == 'foreign_table':
                return self.GetPropertiesForeignTable(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'user_mapping':
                return self.GetPropertiesUserMapping(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'foreign_server':
                return self.GetPropertiesForeignServer(p_object).Transpose('Property', 'Value')
            elif p_type == 'fdw':
                return self.GetPropertiesForeignDataWrapper(p_object).Transpose('Property', 'Value')
            elif p_type == 'type':
                return self.GetPropertiesType(p_schema, p_object).Transpose('Property', 'Value')
            elif p_type == 'domain':
                return self.GetPropertiesType(p_schema, p_object).Transpose('Property', 'Value')
            else:
                return None
        except Spartacus.Database.Exception as exc:
            if str(exc) == 'Can only transpose a table with a single row.':
                raise Exception('Object {0} does not exist anymore. Please refresh the tree view.'.format(p_object))
            else:
                raise exc

    def GetDDLRole(self, p_object):
        return self.v_connection.ExecuteScalar('''
            with
            q1 as (
             select
               'CREATE ' || case when rolcanlogin then 'USER' else 'GROUP' end
               ||' '||quote_ident(rolname)|| E';\n' ||
               'ALTER ROLE '|| quote_ident(rolname) || E' WITH\n  ' ||
               case when rolcanlogin then 'LOGIN' else 'NOLOGIN' end || E'\n  ' ||
               case when rolsuper then 'SUPERUSER' else 'NOSUPERUSER' end || E'\n  ' ||
               case when rolinherit then 'INHERIT' else 'NOINHERIT' end || E'\n  ' ||
               case when rolcreatedb then 'CREATEDB' else 'NOCREATEDB' end || E'\n  ' ||
               case when rolcreaterole then 'CREATEROLE' else 'NOCREATEROLE' end || E'\n  ' ||
               case when rolreplication then 'REPLICATION' else 'NOREPLICATION' end || E';\n  ' ||
               case
                 when description is not null
                 then E'\n'
                      ||'COMMENT ON ROLE '||quote_ident(rolname)
                      ||' IS '||quote_literal(description)||E';\n'
                 else ''
               end || E'\n' ||
               case when rolpassword is not null
                    then 'ALTER ROLE '|| quote_ident(rolname)||
                         ' ENCRYPTED PASSWORD '||quote_literal(rolpassword)||E';\n'
                    else ''
               end ||
               case when rolvaliduntil is not null
                    then 'ALTER ROLE '|| quote_ident(rolname)||
                         ' VALID UNTIL '||quote_nullable(rolvaliduntil)||E';\n'
                    else ''
               end ||
               case when rolconnlimit>=0
                    then 'ALTER ROLE '|| quote_ident(rolname)||
                         ' CONNECTION LIMIT '||rolconnlimit||E';\n'
                    else ''
               end ||
               E'\n' as ddl
               from pg_roles a
               left join pg_shdescription d on d.objoid=a.oid
              where quote_ident(a.rolname) = '{0}'
             ),
            q2 as (
             select string_agg('ALTER ROLE ' || quote_ident(rolname)
                               ||' SET '||pg_roles.rolconfig[i]||E';\n','')
                as ddl_config
              from pg_roles,
              generate_series(
                 (select array_lower(rolconfig,1) from pg_roles where quote_ident(rolname)='{0}'),
                 (select array_upper(rolconfig,1) from pg_roles where quote_ident(rolname)='{0}')
              ) as generate_series(i)
             where quote_ident(rolname) = '{0}'
             )
            select ddl||coalesce(ddl_config||E'\n','')
              from q1,q2
        '''.format(p_object))

    def GetDDLTablespace(self, p_object):
        return self.v_connection.ExecuteScalar('''
            select format(E'CREATE TABLESPACE %s\nLOCATION %s\nOWNER %s;',
                         quote_ident(t.spcname),
                         chr(39) || pg_tablespace_location(t.oid) || chr(39),
                         quote_ident(r.rolname))
            from pg_tablespace t
            inner join pg_roles r
            on r.oid = t.spcowner
            where quote_ident(t.spcname) = '{0}'
        '''.format(p_object))

    def GetDDLDatabase(self, p_object):
        return self.v_connection.ExecuteScalar('''
            select format(E'CREATE DATABASE %s\nOWNER %s\nTABLESPACE %s;',
                          quote_ident(d.datname),
                          quote_ident(r.rolname),
                          quote_ident(t.spcname))
            from pg_database d
            inner join pg_roles r
            on r.oid = d.datdba
            inner join pg_tablespace t
            on t.oid = d.dattablespace
            where quote_ident(d.datname) = '{0}'
        '''.format(p_object))

    def GetDDLExtension(self, p_object):
        return 'CREATE EXTENSION {0};'.format(p_object)

    def GetDDLSchema(self, p_object):
        return self.v_connection.ExecuteScalar('''
            with obj as (
               SELECT n.oid,
                     'pg_namespace'::regclass,
                     n.nspname as name,
                     current_database() as namespace,
                     case
                       when n.nspname like 'pg_%' then 'SYSTEM'
                       when n.nspname = r.rolname then 'AUTHORIZATION'
                       else 'NAMESPACE'
                     end as kind,
                     pg_get_userbyid(n.nspowner) AS owner,
                     'SCHEMA' as sql_kind,
                     quote_ident(n.nspname) as sql_identifier
                FROM pg_namespace n join pg_roles r on r.oid = n.nspowner
               WHERE quote_ident(n.nspname) = '{0}'
            ),
            comment as (
                select format(
                       E'COMMENT ON %s %s IS %L;\n\n',
                       obj.sql_kind, sql_identifier, obj_description(oid)) as text
                from obj
            ),
            alterowner as (
                select format(
                       E'ALTER %s %s OWNER TO %s;\n\n',
                       obj.sql_kind, sql_identifier, quote_ident(owner)) as text
                from obj
            ),
            privileges as (
                select (u_grantor.rolname)::information_schema.sql_identifier as grantor,
                       (grantee.rolname)::information_schema.sql_identifier as grantee,
                       (n.privilege_type)::information_schema.character_data as privilege_type,
                       (case when (pg_has_role(grantee.oid, n.nspowner, 'USAGE'::text) or n.is_grantable)
                             then 'YES'::text
                             else 'NO'::text
                        end)::information_schema.yes_or_no AS is_grantable
                from (
                    select n.nspname,
                           n.nspowner,
                           (aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner)))).grantor as grantor,
                           (aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner)))).grantee as grantee,
                           (aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner)))).privilege_type as privilege_type,
                           (aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner)))).is_grantable as is_grantable
                    from pg_namespace n
                    where quote_ident(n.nspname) = '{0}'
                ) n
                inner join pg_roles u_grantor
                on u_grantor.oid = n.grantor
                inner join (
                    select r.oid,
                           r.rolname
                    from pg_roles r
                    union all
                    select (0)::oid AS oid,
                           'PUBLIC'::name
                ) grantee
                on grantee.oid = n.grantee
            ),
            grants as (
                select coalesce(
                        string_agg(format(
                    	E'GRANT %s ON SCHEMA {0} TO %s%s;\n',
                        privilege_type,
                        case grantee
                          when 'PUBLIC' then 'PUBLIC'
                          else quote_ident(grantee)
                        end,
                    	case is_grantable
                          when 'YES' then ' WITH GRANT OPTION'
                          else ''
                        end), ''),
                       '') as text
                from privileges
            )
            select format(E'CREATE SCHEMA %s;\n\n',quote_ident(n.nspname))
            	   || comment.text
                   || alterowner.text
                   || grants.text
              from pg_namespace n
              inner join comment on 1=1
              inner join alterowner on 1=1
              inner join grants on 1=1
             where quote_ident(n.nspname) = '{0}'
        '''.format(p_object))

    def GetDDLClass(self, p_schema, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.ExecuteScalar('''
                with obj as (
                   SELECT c.oid,
                         'pg_class'::regclass,
                         c.relname AS name,
                         n.nspname AS namespace,
                         coalesce(cc.column2,c.relkind::text) AS kind,
                         pg_get_userbyid(c.relowner) AS owner,
                         coalesce(cc.column2,c.relkind::text) AS sql_kind,
                         cast('{0}.{1}'::regclass AS text) AS sql_identifier
                    FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
                    LEFT join (
                         values ('r','TABLE'),
                                ('v','VIEW'),
                                ('i','INDEX'),
                                ('S','SEQUENCE'),
                                ('s','SPECIAL'),
                                ('m','MATERIALIZED VIEW'),
                                ('c','TYPE'),
                                ('t','TOAST'),
                                ('f','FOREIGN TABLE')
                    ) as cc on cc.column1 = c.relkind
                   WHERE c.oid = '{0}.{1}'::regclass
                ),
                columns as (
                    SELECT a.attname AS name, format_type(t.oid, NULL::integer) AS type,
                        CASE
                            WHEN (a.atttypmod - 4) > 0 THEN a.atttypmod - 4
                            ELSE NULL::integer
                        END AS size,
                        a.attnotnull AS not_null,
                        def.adsrc AS "default",
                        col_description(c.oid, a.attnum::integer) AS comment,
                        con.conname AS primary_key,
                        a.attislocal AS is_local,
                        a.attstorage::text AS storage,
                        nullif(col.collcollate::text,'') AS collation,
                        a.attnum AS ord,
                        s.nspname AS namespace,
                        c.relname AS class_name,
                        format('%s.%I',text(c.oid::regclass),a.attname) AS sql_identifier,
                        c.oid,
                        format('%I %s%s%s',
                        	a.attname::text,
                        	format_type(t.oid, a.atttypmod),
                	        CASE
                    	      WHEN length(col.collcollate) > 0
                        	  THEN ' COLLATE ' || quote_ident(col.collcollate::text)
                              ELSE ''
                        	END,
                        	CASE
                              WHEN a.attnotnull THEN ' NOT NULL'::text
                              ELSE ''::text
                        	END)
                        AS definition
                   FROM pg_class c
                   JOIN pg_namespace s ON s.oid = c.relnamespace
                   JOIN pg_attribute a ON c.oid = a.attrelid
                   LEFT JOIN pg_attrdef def ON c.oid = def.adrelid AND a.attnum = def.adnum
                   LEFT JOIN pg_constraint con
                        ON con.conrelid = c.oid AND (a.attnum = ANY (con.conkey)) AND con.contype = 'p'
                   LEFT JOIN pg_type t ON t.oid = a.atttypid
                   LEFT JOIN pg_collation col ON col.oid = a.attcollation
                   JOIN pg_namespace tn ON tn.oid = t.typnamespace
                  WHERE c.relkind IN ('r','v','c','f') AND a.attnum > 0 AND NOT a.attisdropped
                    AND has_table_privilege(c.oid, 'select') AND has_schema_privilege(s.oid, 'usage')
                    AND c.oid = '{0}.{1}'::regclass
                  ORDER BY s.nspname, c.relname, a.attnum
                ),
                comments as (
                   select 'COMMENT ON COLUMN ' || text('{0}.{1}') || '.' || quote_ident(name) ||
                          ' IS ' || quote_nullable(comment) || ';' as cc
                     from columns
                    where comment IS NOT NULL
                ),
                settings as (
                   select 'ALTER ' || obj.kind || ' ' || text('{0}.{1}') || ' SET (' ||
                          quote_ident(option_name)||'='||quote_nullable(option_value) ||');' as ss
                     from pg_options_to_table((select reloptions from pg_class where oid = '{0}.{1}'::regclass))
                     join obj on (true)
                ),
                constraints as (
                   SELECT nc.nspname AS namespace,
                        r.relname AS class_name,
                        c.conname AS constraint_name,
                        case c.contype
                            when 'c'::"char" then 'CHECK'::text
                            when 'f'::"char" then 'FOREIGN KEY'::text
                            when 'p'::"char" then 'PRIMARY KEY'::text
                            when 'u'::"char" then 'UNIQUE'::text
                            when 't'::"char" then 'TRIGGER'::text
                            when 'x'::"char" then 'EXCLUDE'::text
                            else c.contype::text
                        end AS constraint_type,
                        pg_get_constraintdef(c.oid,true) AS constraint_definition,
                        c.condeferrable AS is_deferrable,
                        c.condeferred  AS initially_deferred,
                        r.oid as regclass, c.oid AS sysid
                   FROM pg_namespace nc, pg_namespace nr, pg_constraint c, pg_class r
                  WHERE nc.oid = c.connamespace AND nr.oid = r.relnamespace AND c.conrelid = r.oid
                    AND coalesce(r.oid='{0}.{1}'::regclass,true)
                ),
                indexes as (
                   SELECT DISTINCT
                        c.oid AS oid,
                        n.nspname::text AS namespace,
                        c.relname::text AS class,
                        i.relname::text AS name,
                        NULL::text AS tablespace,
                        CASE d.refclassid
                            WHEN 'pg_constraint'::regclass
                            THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                 || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                 || ' ' || pg_get_constraintdef(cc.oid)
                            ELSE pg_get_indexdef(i.oid)
                        END AS indexdef,
                        cc.conname::text AS constraint_name
                   FROM pg_index x
                   JOIN pg_class c ON c.oid = x.indrelid
                   JOIN pg_namespace n ON n.oid = c.relnamespace
                   JOIN pg_class i ON i.oid = x.indexrelid
                   JOIN pg_depend d ON d.objid = x.indexrelid
                   LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                  WHERE c.relkind in ('r','m') AND i.relkind = 'i'::"char"
                    AND coalesce(c.oid = '{0}.{1}'::regclass,true)
                ),
                triggers as (
                   SELECT
                        CASE t.tgisinternal
                            WHEN true THEN 'CONSTRAINT'::text
                            ELSE NULL::text
                        END AS is_constraint, t.tgname::text AS trigger_name,
                        CASE (t.tgtype::integer & 64) <> 0
                            WHEN true THEN 'INSTEAD'::text
                            ELSE CASE t.tgtype::integer & 2
                              WHEN 2 THEN 'BEFORE'::text
                              WHEN 0 THEN 'AFTER'::text
                              ELSE NULL::text
                            END
                        END AS action_order,
                        array_to_string(array[
                          case when (t.tgtype::integer &  4) <> 0 then 'INSERT'   end,
                          case when (t.tgtype::integer &  8) <> 0 then 'DELETE'   end,
                          case when (t.tgtype::integer & 16) <> 0 then 'UPDATE'   end,
                          case when (t.tgtype::integer & 32) <> 0 then 'TRUNCATE' end
                        ],' OR ') AS event_manipulation,
                        c.oid::regclass::text AS event_object_sql_identifier,
                        p.oid::regprocedure::text AS action_statement,
                        CASE t.tgtype::integer & 1
                            WHEN 1 THEN 'ROW'::text
                            ELSE 'STATEMENT'::text
                        END AS action_orientation,
                        pg_get_triggerdef(t.oid,true) as trigger_definition,
                        c.oid::regclass AS regclass,
                        p.oid::regprocedure AS regprocedure,
                        s.nspname::text AS event_object_schema,
                        c.relname::text AS event_object_table,
                        (quote_ident(t.tgname::text) || ' ON ') || c.oid::regclass::text AS sql_identifier
                   FROM pg_trigger t
                   LEFT JOIN pg_class c ON c.oid = t.tgrelid
                   LEFT JOIN pg_namespace s ON s.oid = c.relnamespace
                   LEFT JOIN pg_proc p ON p.oid = t.tgfoid
                   LEFT JOIN pg_namespace s1 ON s1.oid = p.pronamespace
                   WHERE coalesce(c.oid='{0}.{1}'::regclass,true)
                ),
                rules as (
                   SELECT n.nspname::text AS namespace,
                        c.relname::text AS class_name,
                        r.rulename::text AS rule_name,
                        CASE
                            WHEN r.ev_type = '1'::"char" THEN 'SELECT'::text
                            WHEN r.ev_type = '2'::"char" THEN 'UPDATE'::text
                            WHEN r.ev_type = '3'::"char" THEN 'INSERT'::text
                            WHEN r.ev_type = '4'::"char" THEN 'DELETE'::text
                            ELSE 'UNKNOWN'::text
                        END AS rule_event,
                        r.is_instead,
                        pg_get_ruledef(r.oid, true) AS rule_definition,
                        c.oid::regclass AS regclass
                   FROM pg_rewrite r
                   JOIN pg_class c ON c.oid = r.ev_class
                   JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE coalesce(c.oid='{0}.{1}'::regclass,true)
                    AND NOT (r.ev_type = '1'::"char" AND r.rulename = '_RETURN'::name)
                  ORDER BY r.oid
                ),
                createview as (
                    select
                     'CREATE '||
                      case relkind
                        when 'v' THEN 'OR REPLACE VIEW '
                        when 'm' THEN 'MATERIALIZED VIEW '
                      end || (oid::regclass::text) || E' AS\n'||
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n' as text
                     FROM pg_class t
                     WHERE oid = '{0}.{1}'::regclass
                       AND relkind in ('v','m')
                ),
                createtable as (
                    select
                        'CREATE '||
                      case relpersistence
                        when 'u' then 'UNLOGGED '
                        when 't' then 'TEMPORARY '
                        else ''
                      end
                      || obj.kind || ' ' || obj.sql_identifier
                      || case obj.kind when 'TYPE' then ' AS' else '' end
                      ||
                      E' (\n'||
                        coalesce(''||(
                          SELECT coalesce(string_agg('    '||definition,E',\n'),'')
                            FROM columns WHERE is_local
                        )||E'\n','')||')'
                      ||
                      (SELECT
                        coalesce(' INHERITS(' || string_agg(i.inhparent::regclass::text,', ') || ')', '')
                         FROM pg_inherits i WHERE i.inhrelid = '{0}.{1}'::regclass)
                      ||
                      CASE relhasoids WHEN true THEN ' WITH OIDS' ELSE '' END
                      ||
                      coalesce(
                        E'\nSERVER '||quote_ident(fs.srvname)
                        ,'')
                      ||
                      coalesce(
                        E'\nOPTIONS (\n'||
                        (select string_agg(
                                  '    '||quote_ident(option_name)||' '||quote_nullable(option_value),
                                  E',\n')
                           from pg_options_to_table(ft.ftoptions))||E'\n)'
                        ,'')
                      ||
                      E';\n' as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    select
                     'CREATE SEQUENCE '||(oid::regclass::text) || E';\n'
                     ||'ALTER SEQUENCE '||(oid::regclass::text)
                     ||E'\n INCREMENT BY '||increment
                     ||E'\n MINVALUE '||minimum_value
                     ||E'\n MAXVALUE '||maximum_value
                     ||E'\n START WITH '||start_value
                     ||E'\n '|| case cycle_option when 'YES' then 'CYCLE' else 'NO CYCLE' end
                     ||E';\n' as text
                     FROM information_schema.sequences s JOIN obj ON (true)
                     WHERE sequence_schema = obj.namespace
                       AND sequence_name = obj.name
                       AND obj.kind = 'SEQUENCE'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid)
                            END AS indexdef
                       FROM pg_index x
                       JOIN pg_class c ON c.oid = x.indrelid
                       JOIN pg_class i ON i.oid = x.indexrelid
                       JOIN pg_depend d ON d.objid = x.indexrelid
                       LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                      WHERE c.relkind in ('r','m') AND i.relkind = 'i'::"char"
                        AND i.oid = '{0}.{1}'::regclass
                    )
                     SELECT indexdef || E';\n' as text
                       FROM ii
                ),
                createclass as (
                    select format(E'--\n-- Type: %s ; Name: %s; Owner: %s\n--\n\n', obj.kind,obj.name,obj.owner)
                    ||
                     case
                      when obj.kind in ('VIEW','MATERIALIZED VIEW') then (select text from createview)
                      when obj.kind in ('TABLE','TYPE','FOREIGN TABLE') then (select text from createtable)
                      when obj.kind in ('SEQUENCE') then (select text from createsequence)
                      when obj.kind in ('INDEX') then (select text from createindex)
                      else '-- UNSUPPORTED CLASS: '||obj.kind
                     end
                      || E'\n' ||
                      coalesce((select string_agg(cc,E'\n')||E'\n' from comments),'')
                      ||
                      coalesce(E'\n'||(select string_agg(ss,E'\n')||E'\n' from settings),'')
                      || E'\n' as text
                    from obj
                ),
                altertabledefaults as (
                    select
                        coalesce(
                          string_agg(
                            'ALTER TABLE '||text('{0}.{1}')||
                              ' ALTER '||quote_ident(name)||
                              ' SET DEFAULT '||"default",
                            E';\n') || E';\n\n',
                        '') as text
                       from columns
                      where "default" is not null
                ),
                createconstraints as (
                    with cs as (
                      select
                       'ALTER TABLE ' || text(regclass(regclass)) ||
                       ' ADD CONSTRAINT ' || quote_ident(constraint_name) ||
                       E'\n  ' || constraint_definition as sql
                        from constraints
                       order by constraint_type desc, sysid
                     )
                     select coalesce(string_agg(sql,E';\n') || E';\n\n','') as text
                       from cs
                ),
                createindexes as (
                    with ii as (select * from indexes order by name)
                     SELECT coalesce(string_agg(indexdef||E';\n','') || E'\n' , '') as text
                       FROM ii
                      WHERE constraint_name is null
                ),
                createtriggers as (
                    with tg as (
                      select trigger_definition as sql
                     from triggers where is_constraint is null
                     order by trigger_name
                     -- per SQL triggers get called in order created vs name as in PostgreSQL
                     )
                     select coalesce(string_agg(sql,E';\n')||E';\n\n','') as text
                       from tg
                ),
                createrules as (
                    select coalesce(string_agg(rule_definition,E'\n')||E'\n\n','') as text
                    from rules
                   where regclass = '{0}.{1}'::regclass
                     and rule_definition is not null
                ),
                alterowner as (
                    select
                       case
                         when obj.kind = 'INDEX' then ''
                         else 'ALTER '||sql_kind||' '||sql_identifier||
                              ' OWNER TO '||quote_ident(owner)||E';\n\n'
                       end as text
                      from obj
                ),
                privileges as (
                    SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                            (grantee.rolname)::information_schema.sql_identifier AS grantee,
                            (current_database())::information_schema.sql_identifier AS table_catalog,
                            (nc.nspname)::information_schema.sql_identifier AS table_schema,
                            (c.relname)::information_schema.sql_identifier AS table_name,
                            (c.prtype)::information_schema.character_data AS privilege_type,
                            (
                                CASE
                                    WHEN (pg_has_role(grantee.oid, c.relowner, 'USAGE'::text) OR c.grantable) THEN 'YES'::text
                                    ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS is_grantable,
                            (
                                CASE
                                    WHEN (c.prtype = 'SELECT'::text) THEN 'YES'::text
                                    ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS with_hierarchy
                           FROM ( SELECT pg_class.oid,
                                         pg_class.relname,
                                         pg_class.relnamespace,
                                         pg_class.relkind,
                                         pg_class.relowner,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).grantor AS grantor,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).grantee AS grantee,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).privilege_type AS privilege_type,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).is_grantable AS is_grantable
                                  FROM pg_class
                                  WHERE pg_class.relkind <> 'S'
                                  UNION
                                  SELECT pg_class.oid,
                                         pg_class.relname,
                                         pg_class.relnamespace,
                                         pg_class.relkind,
                                         pg_class.relowner,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).grantor AS grantor,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).grantee AS grantee,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).privilege_type AS privilege_type,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).is_grantable AS is_grantable
                                  FROM pg_class
                                  WHERE pg_class.relkind = 'S') c(oid, relname, relnamespace, relkind, relowner, grantor, grantee, prtype, grantable),
                            pg_namespace nc,
                            pg_roles u_grantor,
                            ( SELECT pg_roles.oid,
                                    pg_roles.rolname
                                   FROM pg_roles
                                UNION ALL
                                 SELECT (0)::oid AS oid,
                                    'PUBLIC'::name) grantee(oid, rolname)
                          WHERE ((c.relnamespace = nc.oid) AND (c.grantee = grantee.oid) AND (c.grantor = u_grantor.oid)
                            AND (c.prtype = ANY (ARRAY['INSERT'::text, 'SELECT'::text, 'UPDATE'::text, 'DELETE'::text, 'TRUNCATE'::text, 'REFERENCES'::text, 'TRIGGER'::text]))
                            AND (pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(grantee.oid, 'USAGE'::text) OR (grantee.rolname = 'PUBLIC'::name)))
                ),
                grants as (
                    select
                       coalesce(
                        string_agg(format(
                        	E'GRANT %s ON %s TO %s%s;\n',
                            privilege_type,
                            '{0}.{1}',
                            case grantee
                              when 'PUBLIC' then 'PUBLIC'
                              else quote_ident(grantee)
                            end,
                    		case is_grantable
                              when 'YES' then ' WITH GRANT OPTION'
                              else ''
                            end), ''),
                        '') as text
                     FROM privileges g
                     join obj on (true)
                     WHERE table_schema=obj.namespace
                       AND table_name=obj.name
                       AND grantee<>obj.owner
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants)
        '''.format(p_schema, p_object))
        else:
            return self.v_connection.ExecuteScalar('''
                with obj as (
                   SELECT c.oid,
                         'pg_class'::regclass,
                         c.relname AS name,
                         n.nspname AS namespace,
                         coalesce(cc.column2,c.relkind::text) AS kind,
                         pg_get_userbyid(c.relowner) AS owner,
                         coalesce(cc.column2,c.relkind::text) AS sql_kind,
                         cast('{0}.{1}'::regclass AS text) AS sql_identifier
                    FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
                    LEFT join (
                         values ('r','TABLE'),
                                ('v','VIEW'),
                                ('i','INDEX'),
                                ('S','SEQUENCE'),
                                ('s','SPECIAL'),
                                ('m','MATERIALIZED VIEW'),
                                ('c','TYPE'),
                                ('t','TOAST'),
                                ('f','FOREIGN TABLE'),
                                ('p','PARTITIONED TABLE')
                    ) as cc on cc.column1 = c.relkind
                   WHERE c.oid = '{0}.{1}'::regclass
                ),
                columns as (
                    SELECT a.attname AS name, format_type(t.oid, NULL::integer) AS type,
                        CASE
                            WHEN (a.atttypmod - 4) > 0 THEN a.atttypmod - 4
                            ELSE NULL::integer
                        END AS size,
                        a.attnotnull AS not_null,
                        def.adsrc AS "default",
                        col_description(c.oid, a.attnum::integer) AS comment,
                        con.conname AS primary_key,
                        a.attislocal AS is_local,
                        a.attstorage::text AS storage,
                        nullif(col.collcollate::text,'') AS collation,
                        a.attnum AS ord,
                        s.nspname AS namespace,
                        c.relname AS class_name,
                        format('%s.%I',text(c.oid::regclass),a.attname) AS sql_identifier,
                        c.oid,
                        format('%I %s%s%s%s',
                        	a.attname::text,
                        	format_type(t.oid, a.atttypmod),
                	        CASE
                    	      WHEN length(col.collcollate) > 0
                        	  THEN ' COLLATE ' || quote_ident(col.collcollate::text)
                              ELSE ''
                        	END,
                        	CASE
                              WHEN a.attnotnull THEN ' NOT NULL'::text
                              ELSE ''::text
                        	END,
                            CASE
                              WHEN a.attidentity = 'a' THEN ' GENERATED ALWAYS AS IDENTITY'::text
                              WHEN a.attidentity = 'd' THEN ' GENERATED BY DEFAULT AS IDENTITY'::text
                              ELSE ''::text
                            END)
                        AS definition
                   FROM pg_class c
                   JOIN pg_namespace s ON s.oid = c.relnamespace
                   JOIN pg_attribute a ON c.oid = a.attrelid
                   LEFT JOIN pg_attrdef def ON c.oid = def.adrelid AND a.attnum = def.adnum
                   LEFT JOIN pg_constraint con
                        ON con.conrelid = c.oid AND (a.attnum = ANY (con.conkey)) AND con.contype = 'p'
                   LEFT JOIN pg_type t ON t.oid = a.atttypid
                   LEFT JOIN pg_collation col ON col.oid = a.attcollation
                   JOIN pg_namespace tn ON tn.oid = t.typnamespace
                  WHERE c.relkind IN ('r','v','c','f','p') AND a.attnum > 0 AND NOT a.attisdropped
                    AND has_table_privilege(c.oid, 'select') AND has_schema_privilege(s.oid, 'usage')
                    AND c.oid = '{0}.{1}'::regclass
                  ORDER BY s.nspname, c.relname, a.attnum
                ),
                comments as (
                   select 'COMMENT ON COLUMN ' || text('{0}.{1}') || '.' || quote_ident(name) ||
                          ' IS ' || quote_nullable(comment) || ';' as cc
                     from columns
                    where comment IS NOT NULL
                ),
                settings as (
                   select 'ALTER ' || obj.kind || ' ' || text('{0}.{1}') || ' SET (' ||
                          quote_ident(option_name)||'='||quote_nullable(option_value) ||');' as ss
                     from pg_options_to_table((select reloptions from pg_class where oid = '{0}.{1}'::regclass))
                     join obj on (true)
                ),
                constraints as (
                   SELECT nc.nspname AS namespace,
                        r.relname AS class_name,
                        c.conname AS constraint_name,
                        case c.contype
                            when 'c'::"char" then 'CHECK'::text
                            when 'f'::"char" then 'FOREIGN KEY'::text
                            when 'p'::"char" then 'PRIMARY KEY'::text
                            when 'u'::"char" then 'UNIQUE'::text
                            when 't'::"char" then 'TRIGGER'::text
                            when 'x'::"char" then 'EXCLUDE'::text
                            else c.contype::text
                        end AS constraint_type,
                        pg_get_constraintdef(c.oid,true) AS constraint_definition,
                        c.condeferrable AS is_deferrable,
                        c.condeferred  AS initially_deferred,
                        r.oid as regclass, c.oid AS sysid
                   FROM pg_namespace nc, pg_namespace nr, pg_constraint c, pg_class r
                  WHERE nc.oid = c.connamespace AND nr.oid = r.relnamespace AND c.conrelid = r.oid
                    AND coalesce(r.oid='{0}.{1}'::regclass,true)
                ),
                indexes as (
                   SELECT DISTINCT
                        c.oid AS oid,
                        n.nspname::text AS namespace,
                        c.relname::text AS class,
                        i.relname::text AS name,
                        NULL::text AS tablespace,
                        CASE d.refclassid
                            WHEN 'pg_constraint'::regclass
                            THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                 || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                 || ' ' || pg_get_constraintdef(cc.oid)
                            ELSE pg_get_indexdef(i.oid)
                        END AS indexdef,
                        cc.conname::text AS constraint_name
                   FROM pg_index x
                   JOIN pg_class c ON c.oid = x.indrelid
                   JOIN pg_namespace n ON n.oid = c.relnamespace
                   JOIN pg_class i ON i.oid = x.indexrelid
                   JOIN pg_depend d ON d.objid = x.indexrelid
                   LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                  WHERE c.relkind in ('r','m') AND i.relkind = 'i'::"char"
                    AND coalesce(c.oid = '{0}.{1}'::regclass,true)
                ),
                triggers as (
                   SELECT
                        CASE t.tgisinternal
                            WHEN true THEN 'CONSTRAINT'::text
                            ELSE NULL::text
                        END AS is_constraint, t.tgname::text AS trigger_name,
                        CASE (t.tgtype::integer & 64) <> 0
                            WHEN true THEN 'INSTEAD'::text
                            ELSE CASE t.tgtype::integer & 2
                              WHEN 2 THEN 'BEFORE'::text
                              WHEN 0 THEN 'AFTER'::text
                              ELSE NULL::text
                            END
                        END AS action_order,
                        array_to_string(array[
                          case when (t.tgtype::integer &  4) <> 0 then 'INSERT'   end,
                          case when (t.tgtype::integer &  8) <> 0 then 'DELETE'   end,
                          case when (t.tgtype::integer & 16) <> 0 then 'UPDATE'   end,
                          case when (t.tgtype::integer & 32) <> 0 then 'TRUNCATE' end
                        ],' OR ') AS event_manipulation,
                        c.oid::regclass::text AS event_object_sql_identifier,
                        p.oid::regprocedure::text AS action_statement,
                        CASE t.tgtype::integer & 1
                            WHEN 1 THEN 'ROW'::text
                            ELSE 'STATEMENT'::text
                        END AS action_orientation,
                        pg_get_triggerdef(t.oid,true) as trigger_definition,
                        c.oid::regclass AS regclass,
                        p.oid::regprocedure AS regprocedure,
                        s.nspname::text AS event_object_schema,
                        c.relname::text AS event_object_table,
                        (quote_ident(t.tgname::text) || ' ON ') || c.oid::regclass::text AS sql_identifier
                   FROM pg_trigger t
                   LEFT JOIN pg_class c ON c.oid = t.tgrelid
                   LEFT JOIN pg_namespace s ON s.oid = c.relnamespace
                   LEFT JOIN pg_proc p ON p.oid = t.tgfoid
                   LEFT JOIN pg_namespace s1 ON s1.oid = p.pronamespace
                   WHERE coalesce(c.oid='{0}.{1}'::regclass,true)
                ),
                rules as (
                   SELECT n.nspname::text AS namespace,
                        c.relname::text AS class_name,
                        r.rulename::text AS rule_name,
                        CASE
                            WHEN r.ev_type = '1'::"char" THEN 'SELECT'::text
                            WHEN r.ev_type = '2'::"char" THEN 'UPDATE'::text
                            WHEN r.ev_type = '3'::"char" THEN 'INSERT'::text
                            WHEN r.ev_type = '4'::"char" THEN 'DELETE'::text
                            ELSE 'UNKNOWN'::text
                        END AS rule_event,
                        r.is_instead,
                        pg_get_ruledef(r.oid, true) AS rule_definition,
                        c.oid::regclass AS regclass
                   FROM pg_rewrite r
                   JOIN pg_class c ON c.oid = r.ev_class
                   JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE coalesce(c.oid='{0}.{1}'::regclass,true)
                    AND NOT (r.ev_type = '1'::"char" AND r.rulename = '_RETURN'::name)
                  ORDER BY r.oid
                ),
                createview as (
                    select
                     'CREATE '||
                      case relkind
                        when 'v' THEN 'OR REPLACE VIEW '
                        when 'm' THEN 'MATERIALIZED VIEW '
                      end || (oid::regclass::text) || E' AS\n'||
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n' as text
                     FROM pg_class t
                     WHERE oid = '{0}.{1}'::regclass
                       AND relkind in ('v','m')
                ),
                createtable as (
                    select
                        'CREATE '||
                      case relpersistence
                        when 'u' then 'UNLOGGED '
                        when 't' then 'TEMPORARY '
                        else ''
                      end
                      || case obj.kind when 'PARTITIONED TABLE' then 'TABLE' else obj.kind end || ' ' || obj.sql_identifier
                      || case obj.kind when 'TYPE' then ' AS' else '' end
                      || case when c.relispartition
                      then
                          E'\n' ||
                          (SELECT
                             coalesce(' PARTITION OF ' || string_agg(i.inhparent::regclass::text,', '), '')
                             FROM pg_inherits i WHERE i.inhrelid = '{0}.{1}'::regclass) ||
                          E'\n'||
                            coalesce(' '||(
                              pg_get_expr(c.relpartbound, c.oid, true)
                            ),'')
                      else
                          E' (\n'||
                            coalesce(''||(
                              SELECT coalesce(string_agg('    '||definition,E',\n'),'')
                                FROM columns WHERE is_local
                            )||E'\n','')||')'
                          ||
                          (SELECT
                            coalesce(' INHERITS(' || string_agg(i.inhparent::regclass::text,', ') || ')', '')
                             FROM pg_inherits i WHERE i.inhrelid = '{0}.{1}'::regclass)
                      end
                      ||
                      case when c.relkind = 'p'
                      then E'\n' || ' PARTITION BY ' || pg_get_partkeydef('{0}.{1}'::regclass)
                      else '' end
                      ||
                      CASE relhasoids WHEN true THEN ' WITH OIDS' ELSE '' END
                      ||
                      coalesce(
                        E'\nSERVER '||quote_ident(fs.srvname)
                        ,'')
                      ||
                      coalesce(
                        E'\nOPTIONS (\n'||
                        (select string_agg(
                                  '    '||quote_ident(option_name)||' '||quote_nullable(option_value),
                                  E',\n')
                           from pg_options_to_table(ft.ftoptions))||E'\n)'
                        ,'')
                      ||
                      E';\n' as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    select
                     'CREATE SEQUENCE '||(oid::regclass::text) || E';\n'
                     ||'ALTER SEQUENCE '||(oid::regclass::text)
                     ||E'\n INCREMENT BY '||increment
                     ||E'\n MINVALUE '||minimum_value
                     ||E'\n MAXVALUE '||maximum_value
                     ||E'\n START WITH '||start_value
                     ||E'\n '|| case cycle_option when 'YES' then 'CYCLE' else 'NO CYCLE' end
                     ||E';\n' as text
                     FROM information_schema.sequences s JOIN obj ON (true)
                     WHERE sequence_schema = obj.namespace
                       AND sequence_name = obj.name
                       AND obj.kind = 'SEQUENCE'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid)
                            END AS indexdef
                       FROM pg_index x
                       JOIN pg_class c ON c.oid = x.indrelid
                       JOIN pg_class i ON i.oid = x.indexrelid
                       JOIN pg_depend d ON d.objid = x.indexrelid
                       LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                      WHERE c.relkind in ('r','m') AND i.relkind = 'i'::"char"
                        AND i.oid = '{0}.{1}'::regclass
                    )
                     SELECT indexdef || E';\n' as text
                       FROM ii
                ),
                createclass as (
                    select format(E'--\n-- Type: %s ; Name: %s; Owner: %s\n--\n\n', obj.kind,obj.name,obj.owner)
                    ||
                     case
                      when obj.kind in ('VIEW','MATERIALIZED VIEW') then (select text from createview)
                      when obj.kind in ('TABLE','TYPE','FOREIGN TABLE','PARTITIONED TABLE') then (select text from createtable)
                      when obj.kind in ('SEQUENCE') then (select text from createsequence)
                      when obj.kind in ('INDEX') then (select text from createindex)
                      else '-- UNSUPPORTED CLASS: '||obj.kind
                     end
                      || E'\n' ||
                      coalesce((select string_agg(cc,E'\n')||E'\n' from comments),'')
                      ||
                      coalesce(E'\n'||(select string_agg(ss,E'\n')||E'\n' from settings),'')
                      || E'\n' as text
                    from obj
                ),
                altertabledefaults as (
                    select
                        coalesce(
                          string_agg(
                            'ALTER TABLE '||text('{0}.{1}')||
                              ' ALTER '||quote_ident(name)||
                              ' SET DEFAULT '||"default",
                            E';\n') || E';\n\n',
                        '') as text
                       from columns
                      where "default" is not null
                ),
                createconstraints as (
                    with cs as (
                      select
                       'ALTER TABLE ' || text(regclass(regclass)) ||
                       ' ADD CONSTRAINT ' || quote_ident(constraint_name) ||
                       E'\n  ' || constraint_definition as sql
                        from constraints
                       order by constraint_type desc, sysid
                     )
                     select coalesce(string_agg(sql,E';\n') || E';\n\n','') as text
                       from cs
                ),
                createindexes as (
                    with ii as (select * from indexes order by name)
                     SELECT coalesce(string_agg(indexdef||E';\n','') || E'\n' , '') as text
                       FROM ii
                      WHERE constraint_name is null
                ),
                createtriggers as (
                    with tg as (
                      select trigger_definition as sql
                     from triggers where is_constraint is null
                     order by trigger_name
                     -- per SQL triggers get called in order created vs name as in PostgreSQL
                     )
                     select coalesce(string_agg(sql,E';\n')||E';\n\n','') as text
                       from tg
                ),
                createrules as (
                    select coalesce(string_agg(rule_definition,E'\n')||E'\n\n','') as text
                    from rules
                   where regclass = '{0}.{1}'::regclass
                     and rule_definition is not null
                ),
                alterowner as (
                    select
                       case
                         when obj.kind = 'INDEX' then ''
                         when obj.kind = 'PARTITIONED TABLE'
                         then 'ALTER TABLE '||sql_identifier||
                              ' OWNER TO '||quote_ident(owner)||E';\n\n'
                         else 'ALTER '||sql_kind||' '||sql_identifier||
                              ' OWNER TO '||quote_ident(owner)||E';\n\n'
                       end as text
                      from obj
                ),
                privileges as (
                    SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                            (grantee.rolname)::information_schema.sql_identifier AS grantee,
                            (current_database())::information_schema.sql_identifier AS table_catalog,
                            (nc.nspname)::information_schema.sql_identifier AS table_schema,
                            (c.relname)::information_schema.sql_identifier AS table_name,
                            (c.prtype)::information_schema.character_data AS privilege_type,
                            (
                                CASE
                                    WHEN (pg_has_role(grantee.oid, c.relowner, 'USAGE'::text) OR c.grantable) THEN 'YES'::text
                                    ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS is_grantable,
                            (
                                CASE
                                    WHEN (c.prtype = 'SELECT'::text) THEN 'YES'::text
                                    ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS with_hierarchy
                           FROM ( SELECT pg_class.oid,
                                         pg_class.relname,
                                         pg_class.relnamespace,
                                         pg_class.relkind,
                                         pg_class.relowner,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).grantor AS grantor,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).grantee AS grantee,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).privilege_type AS privilege_type,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('r', pg_class.relowner)))).is_grantable AS is_grantable
                                  FROM pg_class
                                  WHERE pg_class.relkind <> 'S'
                                  UNION
                                  SELECT pg_class.oid,
                                         pg_class.relname,
                                         pg_class.relnamespace,
                                         pg_class.relkind,
                                         pg_class.relowner,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).grantor AS grantor,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).grantee AS grantee,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).privilege_type AS privilege_type,
                                         (aclexplode(COALESCE(pg_class.relacl, acldefault('S', pg_class.relowner)))).is_grantable AS is_grantable
                                  FROM pg_class
                                  WHERE pg_class.relkind = 'S') c(oid, relname, relnamespace, relkind, relowner, grantor, grantee, prtype, grantable),
                            pg_namespace nc,
                            pg_roles u_grantor,
                            ( SELECT pg_roles.oid,
                                    pg_roles.rolname
                                   FROM pg_roles
                                UNION ALL
                                 SELECT (0)::oid AS oid,
                                    'PUBLIC'::name) grantee(oid, rolname)
                          WHERE ((c.relnamespace = nc.oid) AND (c.grantee = grantee.oid) AND (c.grantor = u_grantor.oid)
                            AND (c.prtype = ANY (ARRAY['INSERT'::text, 'SELECT'::text, 'UPDATE'::text, 'DELETE'::text, 'TRUNCATE'::text, 'REFERENCES'::text, 'TRIGGER'::text]))
                            AND (pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(grantee.oid, 'USAGE'::text) OR (grantee.rolname = 'PUBLIC'::name)))
                ),
                grants as (
                    select
                       coalesce(
                        string_agg(format(
                        	E'GRANT %s ON %s TO %s%s;\n',
                            privilege_type,
                            '{0}.{1}',
                            case grantee
                              when 'PUBLIC' then 'PUBLIC'
                              else quote_ident(grantee)
                            end,
                    		case is_grantable
                              when 'YES' then ' WITH GRANT OPTION'
                              else ''
                            end), ''),
                        '') as text
                     FROM privileges g
                     join obj on (true)
                     WHERE table_schema=obj.namespace
                       AND table_name=obj.name
                       AND grantee<>obj.owner
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants)
            '''.format(p_schema, p_object))

    def GetDDLFunction(self, p_function):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.ExecuteScalar('''
                with obj as (
                    SELECT p.oid,
                           p.proname AS name,
                           n.nspname AS namespace,
                           pg_get_userbyid(p.proowner) AS owner,
                           '{0}'::text AS sql_identifier
                    FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                    WHERE p.oid = '{0}'::text::regprocedure
                ),
                createfunction as (
                    select substring(body from 1 for length(body)-1) || E';\n\n' as text
                    from (
                        select pg_get_functiondef(sql_identifier::regprocedure) as body
                        from obj
                    ) x
                ),
                alterowner as (
                    select
                       'ALTER FUNCTION '||sql_identifier||
                              ' OWNER TO '||quote_ident(owner)||E';\n\n' as text
                      from obj
                ),
                privileges as (
                select (u_grantor.rolname)::information_schema.sql_identifier as grantor,
                       (grantee.rolname)::information_schema.sql_identifier as grantee,
                       (p.privilege_type)::information_schema.character_data as privilege_type,
                       (case when (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) or p.is_grantable)
                             then 'YES'::text
                             else 'NO'::text
                        end)::information_schema.yes_or_no AS is_grantable
                from (
                    select p.pronamespace,
                           p.proowner,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor as grantor,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee as grantee,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type as privilege_type,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable as is_grantable
                    from pg_proc p
                    where not p.proisagg
                      and p.oid = '{0}'::regprocedure
                ) p
                inner join pg_namespace n
                on n.oid = p.pronamespace
                inner join pg_roles u_grantor
                on u_grantor.oid = p.grantor
                inner join (
                    select r.oid,
                           r.rolname
                    from pg_roles r
                    union all
                    select (0)::oid AS oid,
                           'PUBLIC'::name
                ) grantee
                on grantee.oid = p.grantee
                ),
                grants as (
                select coalesce(
                        string_agg(format(
                    	E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                        privilege_type,
                        case grantee
                          when 'PUBLIC' then 'PUBLIC'
                          else quote_ident(grantee)
                        end,
                    	case is_grantable
                          when 'YES' then ' WITH GRANT OPTION'
                          else ''
                        end), ''),
                       '') as text
                from privileges
                )
                select (select text from createfunction) ||
                       (select text from alterowner) ||
                       (select text from grants)
'''.format(p_function))
        else:
            return self.v_connection.ExecuteScalar('''
                with obj as (
                    SELECT p.oid,
                           p.proname AS name,
                           n.nspname AS namespace,
                           pg_get_userbyid(p.proowner) AS owner,
                           '{0}'::text AS sql_identifier
                    FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                    WHERE p.prokind = 'f' AND p.oid = '{0}'::text::regprocedure
                ),
                createfunction as (
                    select substring(body from 1 for length(body)-1) || E';\n\n' as text
                    from (
                        select pg_get_functiondef(sql_identifier::regprocedure) as body
                        from obj
                    ) x
                ),
                alterowner as (
                    select
                       'ALTER FUNCTION '||sql_identifier||
                              ' OWNER TO '||quote_ident(owner)||E';\n\n' as text
                      from obj
                ),
                privileges as (
                select (u_grantor.rolname)::information_schema.sql_identifier as grantor,
                       (grantee.rolname)::information_schema.sql_identifier as grantee,
                       (p.privilege_type)::information_schema.character_data as privilege_type,
                       (case when (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) or p.is_grantable)
                             then 'YES'::text
                             else 'NO'::text
                        end)::information_schema.yes_or_no AS is_grantable
                from (
                    select p.pronamespace,
                           p.proowner,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor as grantor,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee as grantee,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type as privilege_type,
                           (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable as is_grantable
                    from pg_proc p
                    where p.prokind = 'f'
                      and p.oid = '{0}'::regprocedure
                ) p
                inner join pg_namespace n
                on n.oid = p.pronamespace
                inner join pg_roles u_grantor
                on u_grantor.oid = p.grantor
                inner join (
                    select r.oid,
                           r.rolname
                    from pg_roles r
                    union all
                    select (0)::oid AS oid,
                           'PUBLIC'::name
                ) grantee
                on grantee.oid = p.grantee
                ),
                grants as (
                select coalesce(
                        string_agg(format(
                    	E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                        privilege_type,
                        case grantee
                          when 'PUBLIC' then 'PUBLIC'
                          else quote_ident(grantee)
                        end,
                    	case is_grantable
                          when 'YES' then ' WITH GRANT OPTION'
                          else ''
                        end), ''),
                       '') as text
                from privileges
                )
                select (select text from createfunction) ||
                       (select text from alterowner) ||
                       (select text from grants)
'''.format(p_function))

    def GetDDLProcedure(self, p_procedure):
        return self.v_connection.ExecuteScalar('''
            with obj as (
                SELECT p.oid,
                       p.proname AS name,
                       n.nspname AS namespace,
                       pg_get_userbyid(p.proowner) AS owner,
                       '{0}'::text AS sql_identifier
                FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                WHERE p.prokind = 'p' AND p.oid = '{0}'::text::regprocedure
            ),
            createfunction as (
                select substring(body from 1 for length(body)-1) || E';\n\n' as text
                from (
                    select pg_get_functiondef(sql_identifier::regprocedure) as body
                    from obj
                ) x
            ),
            alterowner as (
                select
                   'ALTER PROCEDURE '||sql_identifier||
                          ' OWNER TO '||quote_ident(owner)||E';\n\n' as text
                  from obj
            ),
            privileges as (
            select (u_grantor.rolname)::information_schema.sql_identifier as grantor,
                   (grantee.rolname)::information_schema.sql_identifier as grantee,
                   (p.privilege_type)::information_schema.character_data as privilege_type,
                   (case when (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) or p.is_grantable)
                         then 'YES'::text
                         else 'NO'::text
                    end)::information_schema.yes_or_no AS is_grantable
            from (
                select p.pronamespace,
                       p.proowner,
                       (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor as grantor,
                       (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee as grantee,
                       (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type as privilege_type,
                       (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable as is_grantable
                from pg_proc p
                where p.prokind = 'p'
                  and p.oid = '{0}'::regprocedure
            ) p
            inner join pg_namespace n
            on n.oid = p.pronamespace
            inner join pg_roles u_grantor
            on u_grantor.oid = p.grantor
            inner join (
                select r.oid,
                       r.rolname
                from pg_roles r
                union all
                select (0)::oid AS oid,
                       'PUBLIC'::name
            ) grantee
            on grantee.oid = p.grantee
            ),
            grants as (
            select coalesce(
                    string_agg(format(
                	E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                    privilege_type,
                    case grantee
                      when 'PUBLIC' then 'PUBLIC'
                      else quote_ident(grantee)
                    end,
                	case is_grantable
                      when 'YES' then ' WITH GRANT OPTION'
                      else ''
                    end), ''),
                   '') as text
            from privileges
            )
            select (select text from createfunction) ||
                   (select text from alterowner) ||
                   (select text from grants)
'''.format(p_procedure))

    def GetDDLConstraint(self, p_schema, p_table, p_object):
        return self.v_connection.ExecuteScalar('''
            with cs as (
              select
               'ALTER TABLE ' || text(regclass(c.conrelid)) ||
               ' ADD CONSTRAINT ' || quote_ident(c.conname) ||
               E'\n  ' || pg_get_constraintdef(c.oid, true) as sql
                from pg_constraint c
               join pg_class t
               on t.oid = c.conrelid
               join pg_namespace n
               on t.relnamespace = n.oid
               where quote_ident(n.nspname) = '{0}'
                 and quote_ident(t.relname) = '{1}'
                 and quote_ident(c.conname) = '{2}'
            )
            select coalesce(string_agg(sql,E';\n') || E';\n\n','') as text
            from cs
        '''.format(p_schema, p_table, p_object))

    def GetDDLUserMapping(self, p_server, p_object):
        if p_object == 'PUBLIC':
            return self.v_connection.ExecuteScalar('''
                select format(E'CREATE USER MAPPING FOR PUBLIC\n  SERVER %s%s;\n',
                         quote_ident(s.srvname),
                         (select (case when s is not null and s <> ''
                                       then format(E'\n  OPTIONS (%s)', s)
                                       else ''
                                  end)
                          from (
                          select array_to_string(array(
                          select format('%s %s', a[1], quote_literal(a[2]))
                          from (
                          select string_to_array(unnest(u.umoptions), '=') as a
                          from pg_user_mapping u
                          inner join pg_foreign_server s
                          on s.oid = u.umserver
                          where u.umuser = 0
                            and quote_ident(s.srvname) = '{0}'
                          ) x
                          ), ', ') as s) x))
                from pg_user_mapping u
                inner join pg_foreign_server s
                on s.oid = u.umserver
                where u.umuser = 0
                  and quote_ident(s.srvname) = '{0}'
            '''.format(p_server))
        else:
            return self.v_connection.ExecuteScalar('''
                select format(E'CREATE USER MAPPING FOR %s\n  SERVER %s%s;\n',
                         quote_ident(r.rolname),
                         quote_ident(s.srvname),
                         (select (case when s is not null and s <> ''
                                       then format(E'\n  OPTIONS (%s)', s)
                                       else ''
                                  end)
                          from (
                          select array_to_string(array(
                          select format('%s %s', a[1], quote_literal(a[2]))
                          from (
                          select string_to_array(unnest(u.umoptions), '=') as a
                          from pg_user_mapping u
                          inner join pg_foreign_server s
                          on s.oid = u.umserver
                          inner join pg_roles r
                          on r.oid = u.umuser
                          where quote_ident(s.srvname) = '{0}'
                            and quote_ident(r.rolname) = '{1}'
                          ) x
                          ), ', ') as s) x))
                from pg_user_mapping u
                inner join pg_foreign_server s
                on s.oid = u.umserver
                inner join pg_roles r
                on r.oid = u.umuser
                where quote_ident(s.srvname) = '{0}'
                  and quote_ident(r.rolname) = '{1}'
            '''.format(p_server, p_object))

    def GetDDLForeignServer(self, p_object):
        return self.v_connection.ExecuteScalar('''
            WITH privileges AS (
                SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                       (grantee.rolname)::information_schema.sql_identifier AS grantee,
                       (current_database())::information_schema.sql_identifier AS srv_catalog,
                       (c.srvname)::information_schema.sql_identifier AS srv_name,
                       (c.prtype)::information_schema.character_data AS privilege_type,
                       (
                           CASE
                               WHEN (pg_has_role(grantee.oid, c.srvowner, 'USAGE'::text) OR c.grantable) THEN 'YES'::text
                               ELSE 'NO'::text
                           END)::information_schema.yes_or_no AS is_grantable,
                       (
                           CASE
                               WHEN (c.prtype = 'SELECT'::text) THEN 'YES'::text
                               ELSE 'NO'::text
                           END)::information_schema.yes_or_no AS with_hierarchy
                FROM ( SELECT s.oid,
                              s.srvname,
                              s.srvowner,
                              (aclexplode(COALESCE(s.srvacl, acldefault('r', s.srvowner)))).grantor AS grantor,
                              (aclexplode(COALESCE(s.srvacl, acldefault('r', s.srvowner)))).grantee AS grantee,
                              (aclexplode(COALESCE(s.srvacl, acldefault('r', s.srvowner)))).privilege_type AS privilege_type,
                              (aclexplode(COALESCE(s.srvacl, acldefault('r', s.srvowner)))).is_grantable AS is_grantable
                      FROM pg_foreign_server s
                      WHERE s.srvname = '{0}') c(oid, srvname, srvowner, grantor, grantee, prtype, grantable),
                     pg_roles u_grantor,
                     ( SELECT pg_roles.oid,
                              pg_roles.rolname
                       FROM pg_roles
                       UNION ALL
                       SELECT (0)::oid AS oid,
                              'PUBLIC'::name) grantee(oid, rolname)
                WHERE (c.grantee = grantee.oid) AND (c.grantor = u_grantor.oid)
                  AND (pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(grantee.oid, 'USAGE'::text) OR (grantee.rolname = 'PUBLIC'::name))
            ),
            grants as (
                SELECT
                  coalesce(
                   string_agg(format(
                   	E'GRANT %s ON %s TO %s%s;\n',
                       privilege_type,
                       'FOREIGN SERVER {0}',
                       case grantee
                         when 'PUBLIC' then 'PUBLIC'
                         else quote_ident(grantee)
                       end,
                	   case is_grantable
                         when 'YES' then ' WITH GRANT OPTION'
                         else ''
                       end), ''),
                    '') as text
                FROM privileges g
                INNER JOIN pg_foreign_server s
                ON s.srvname = g.srv_name
                INNER JOIN pg_roles r
                ON r.oid = s.srvowner
                WHERE g.grantee <> r.rolname
            )
            select format(E'CREATE SERVER %s%s%s\n  FOREIGN DATA WRAPPER %s%s;\n\nALTER SERVER %s OWNER TO %s;\n\n%s',
                     quote_ident(s.srvname),
                     (case when s.srvtype is not null
                           then format(E'\n  TYPE %s\n', quote_literal(s.srvtype))
                           else ''
                      end),
                     (case when s.srvversion is not null
                           then format(E'\n  VERSION %s\n', quote_literal(s.srvversion))
                           else ''
                      end),
                     w.fdwname,
                     (case when (select array_to_string(array(
                                 select format('%s %s', a[1], quote_literal(a[2]))
                                 from (
                                 select string_to_array(unnest(s.srvoptions), '=') as a
                                 from pg_foreign_server s
                                 inner join pg_foreign_data_wrapper w
                                 on w.oid = s.srvfdw
                                 inner join pg_roles r
                                 on r.oid = s.srvowner
                                 where quote_ident(s.srvname) = '{0}'
                                 ) x
                                 ), ', ')) != ''
                           then format('\n  OPTIONS ( %s )',
                                (select array_to_string(array(
                                 select format('%s %s', a[1], quote_literal(a[2]))
                                 from (
                                 select string_to_array(unnest(s.srvoptions), '=') as a
                                 from pg_foreign_server s
                                 inner join pg_foreign_data_wrapper w
                                 on w.oid = s.srvfdw
                                 inner join pg_roles r
                                 on r.oid = s.srvowner
                                 where quote_ident(s.srvname) = '{0}'
                                 ) x
                                 ), ', ')))
                           else ''
                      end),
                     quote_ident(s.srvname),
                     quote_ident(r.rolname),
                     g.text
                   )
            from pg_foreign_server s
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            inner join pg_roles r
            on r.oid = s.srvowner
            inner join grants g on 1=1
            where quote_ident(s.srvname) = '{0}'
        '''.format(p_object))

    def GetDDLForeignDataWrapper(self, p_object):
        return self.v_connection.ExecuteScalar('''
            WITH privileges AS (
                SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                       (grantee.rolname)::information_schema.sql_identifier AS grantee,
                       (current_database())::information_schema.sql_identifier AS fdw_catalog,
                       (c.fdwname)::information_schema.sql_identifier AS fdw_name,
                       (c.prtype)::information_schema.character_data AS privilege_type,
                       (
                           CASE
                               WHEN (pg_has_role(grantee.oid, c.fdwowner, 'USAGE'::text) OR c.grantable) THEN 'YES'::text
                               ELSE 'NO'::text
                           END)::information_schema.yes_or_no AS is_grantable,
                       (
                           CASE
                               WHEN (c.prtype = 'SELECT'::text) THEN 'YES'::text
                               ELSE 'NO'::text
                           END)::information_schema.yes_or_no AS with_hierarchy
                FROM ( SELECT w.oid,
                              w.fdwname,
                              w.fdwowner,
                              (aclexplode(COALESCE(w.fdwacl, acldefault('r', w.fdwowner)))).grantor AS grantor,
                              (aclexplode(COALESCE(w.fdwacl, acldefault('r', w.fdwowner)))).grantee AS grantee,
                              (aclexplode(COALESCE(w.fdwacl, acldefault('r', w.fdwowner)))).privilege_type AS privilege_type,
                              (aclexplode(COALESCE(w.fdwacl, acldefault('r', w.fdwowner)))).is_grantable AS is_grantable
                      FROM pg_foreign_data_wrapper w
                      WHERE w.fdwname = '{0}') c(oid, fdwname, fdwowner, grantor, grantee, prtype, grantable),
                     pg_roles u_grantor,
                     ( SELECT pg_roles.oid,
                              pg_roles.rolname
                       FROM pg_roles
                       UNION ALL
                       SELECT (0)::oid AS oid,
                              'PUBLIC'::name) grantee(oid, rolname)
                WHERE (c.grantee = grantee.oid) AND (c.grantor = u_grantor.oid)
                  AND (pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(grantee.oid, 'USAGE'::text) OR (grantee.rolname = 'PUBLIC'::name))
            ),
            grants as (
                SELECT
                  coalesce(
                   string_agg(format(
                   	E'GRANT %s ON %s TO %s%s;\n',
                       privilege_type,
                       'FOREIGN DATA WRAPPER {0}',
                       case grantee
                         when 'PUBLIC' then 'PUBLIC'
                         else quote_ident(grantee)
                       end,
                	   case is_grantable
                         when 'YES' then ' WITH GRANT OPTION'
                         else ''
                       end), ''),
                    '') as text
                FROM privileges g
                INNER JOIN pg_foreign_data_wrapper w
                ON w.fdwname = g.fdw_name
                INNER JOIN pg_roles r
                ON r.oid = w.fdwowner
                WHERE g.grantee <> r.rolname
            )
            select format(E'CREATE FOREIGN DATA WRAPPER %s%s%s%s;\n\nALTER FOREIGN DATA WRAPPER %s OWNER TO %s;\n\n%s',
                     w.fdwname,
                     (case when w.fdwhandler <> 0
                           then format(E'\n  HANDLER %s', quote_literal(h.proname))
                           else E'\n  NO HANDLER'
                      end),
                     (case when w.fdwvalidator <> 0
                           then format(E'\n  VALIDATOR %s', quote_literal(v.proname))
                           else E'\n  NO VALIDATOR'
                      end),
                     (case when (select array_to_string(array(
                                 select format('%s %s', a[1], quote_literal(a[2]))
                                 from (
                                 select string_to_array(unnest(w.fdwoptions), '=') as a
                                 from pg_foreign_data_wrapper w
                                 inner join pg_roles r
                                 on r.oid = w.fdwowner
                                 where w.fdwname = '{0}'
                                 ) x
                                 ), ', ')) <> ''::text
                           then format('\n  OPTIONS ( %s )',
                                (select array_to_string(array(
                                 select format('%s %s', a[1], quote_literal(a[2]))
                                 from (
                                 select string_to_array(unnest(w.fdwoptions), '=') as a
                                 from pg_foreign_data_wrapper w
                                 inner join pg_roles r
                                 on r.oid = w.fdwowner
                                 where w.fdwname = '{0}'
                                 ) x
                                 ), ', ')))
                           else ''
                      end),
                     w.fdwname,
                     quote_ident(r.rolname),
                     g.text
                   )
            from pg_foreign_data_wrapper w
            left join pg_proc h
            on h.oid = w.fdwhandler
            left join pg_proc v
            on v.oid = w.fdwvalidator
            inner join pg_roles r
            on r.oid = w.fdwowner
            inner join grants g on 1=1
            where quote_ident(w.fdwname) = '{0}'
        '''.format(p_object))

    def GetDDLType(self, p_schema, p_object):
        v_type = self.v_connection.ExecuteScalar('''
            select t.typtype
            from pg_type t
            inner join pg_namespace n
            on n.oid = t.typnamespace
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(t.typname) = '{1}'
        '''.format(p_schema, p_object))
        if v_type == 'c':
            return self.GetDDLClass(p_schema, p_object)
        elif v_type == 'e':
            return self.v_connection.ExecuteScalar('''
                select format(
                           E'CREATE TYPE %s.%s AS ENUM (\n%s\n);\n\nALTER TYPE %s.%s OWNER TO %s;\n',
                           quote_ident(n.nspname),
                           quote_ident(t.typname),
                           string_agg(format('    ' || chr(39) || '%s' || chr(39), e.enumlabel), E',\n'),
                           quote_ident(n.nspname),
                           quote_ident(t.typname),
                           quote_ident(r.rolname)
                       )
                from pg_type t
                inner join pg_namespace n on n.oid = t.typnamespace
                inner join pg_enum e on e.enumtypid = t.oid
                inner join pg_roles r on r.oid = t.typowner
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(t.typname) = '{1}'
                group by n.nspname,
                         t.typname,
                         r.rolname
            '''.format(p_schema, p_object))
        elif v_type == 'r':
            return self.v_connection.ExecuteScalar('''
                select format(
                         E'CREATE TYPE %s.%s AS RANGE (\n  SUBTYPE = %s.%s\n%s%s%s%s);\n\nALTER TYPE %s.%s OWNER TO %s;\n',
                         quote_ident(n.nspname),
                         quote_ident(t.typname),
                         quote_ident(sn.nspname),
                         quote_ident(st.typname),
                         (case when o.opcname is not null then format(E'  , SUBTYPE_OPCLASS = %s\n', quote_ident(o.opcname)) else '' end),
                         (case when c.collname is not null then format(E'  , COLLATION = %s\n', quote_ident(c.collname)) else '' end),
                         (case when pc.proname is not null then format(E'  , CANONICAL = %s.%s\n', quote_ident(nc.nspname), quote_ident(pc.proname)) else '' end),
                         (case when ps.proname is not null then format(E'  , SUBTYPE_DIFF = %s.%s\n', quote_ident(ns.nspname), quote_ident(ps.proname)) else '' end),
                         quote_ident(n.nspname),
                         quote_ident(t.typname),
                         quote_ident(ro.rolname)
                       )
                from pg_type t
                inner join pg_namespace n on n.oid = t.typnamespace
                inner join pg_range r on r.rngtypid = t.oid
                inner join pg_type st on st.oid = r.rngsubtype
                inner join pg_namespace sn on sn.oid = st.typnamespace
                left join pg_collation c on c.oid = r.rngcollation
                left join pg_opclass o on o.oid = r.rngsubopc
                left join pg_proc pc on pc.oid = r.rngcanonical
                left join pg_namespace nc on nc.oid = pc.pronamespace
                left join pg_proc ps on ps.oid = r.rngsubdiff
                left join pg_namespace ns on ns.oid = ps.pronamespace
                inner join pg_roles ro on ro.oid = t.typowner
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(t.typname) = '{1}'
            '''.format(p_schema, p_object))
        else:
            return self.v_connection.ExecuteScalar('''
                select format(
                         E'CREATE TYPE %s (\n  INPUT = %s,\n  , OUTPUT = %s\n%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s);\n\nALTER TYPE %s OWNER TO %s;\n',
                         quote_ident(n.nspname) || '.' || quote_ident(t.typname),
                         quote_ident(ninput.nspname) || '.' || quote_ident(pinput.proname),
                         quote_ident(noutput.nspname) || '.' || quote_ident(poutput.proname),
                         (case when preceive.proname is not null then format(E'  , RECEIVE = %s\n', quote_ident(nreceive.nspname) || '.' || quote_ident(preceive.proname)) else '' end),
                         (case when psend.proname is not null then format(E'  , SEND = %s\n', quote_ident(nsend.nspname) || '.' || quote_ident(psend.proname)) else '' end),
                         (case when pmodin.proname is not null then format(E'  , TYPMOD_IN = %s\n', quote_ident(nmodin.nspname) || '.' || quote_ident(pmodin.proname)) else '' end),
                         (case when pmodout.proname is not null then format(E'  , TYPMOD_OUT = %s\n', quote_ident(nmodout.nspname) || '.' || quote_ident(pmodout.proname)) else '' end),
                         (case when panalyze.proname is not null then format(E'  , ANALYZE = %s\n', quote_ident(nanalyze.nspname) || '.' || quote_ident(panalyze.proname)) else '' end),
                         (case when t.typlen > 0 then format(E'  , INTERNALLENGTH = %s\n', t.typlen) else '' end),
                         (case when t.typbyval then E'  , PASSEDBYVALUE\n' else '' end),
                         (case t.typalign
                            when 'c' then E'  , ALIGNMENT = char\n'
                            when 's' then E'  , ALIGNMENT = int2\n'
                            when 'i' then E'  , ALIGNMENT = int4\n'
                            when 'd' then E'  , ALIGNMENT = double\n'
                            else ''
                          end),
                         (case t.typstorage
                            when 'p' then E'  , STORAGE = plain\n'
                            when 'e' then E'  , STORAGE = extended\n'
                            when 'm' then E'  , STORAGE = main\n'
                            when 'x' then E'  , STORAGE = external\n'
                          end),
                         format(E'  , CATEGORY = ' || chr(39) || '%s' || chr(39) || E'\n', t.typcategory),
                         (case when t.typispreferred then E'  , PREFERRED = true\n' else '' end),
                         (case when t.typdefault is not null then format('  , DEFAULT = ' || chr(39) || '%s' || chr(39) || E'\n', t.typdefault) else '' end),
                         (case when telem.typname is not null then format(E'  , ELEMENT = %s\n', nelem.nspname || '.' || telem.typname) else '' end),
                         (case when t.typdelim is not null then format(E'  , DELIMITER = ' || chr(39) || '%s' || chr(39) || E'\n', t.typdelim) else '' end),
                         (case when coll.collname is not null then E'  , COLLATABLE = true\n' else '' end),
                         quote_ident(n.nspname) || '.' || quote_ident(t.typname),
                         quote_ident(r.rolname)
                       )
                from pg_type t
                inner join pg_roles r on r.oid = t.typowner
                inner join pg_namespace n on n.oid = t.typnamespace
                left join pg_type telem on telem.oid = t.typelem
                left join pg_namespace nelem on nelem.oid = telem.typnamespace
                left join pg_proc pinput on pinput.oid = t.typinput
                left join pg_namespace ninput on ninput.oid = pinput.pronamespace
                left join pg_proc poutput on poutput.oid = t.typoutput
                left join pg_namespace noutput on noutput.oid = poutput.pronamespace
                left join pg_proc preceive on preceive.oid = t.typreceive
                left join pg_namespace nreceive on nreceive.oid = preceive.pronamespace
                left join pg_proc psend on psend.oid = t.typsend
                left join pg_namespace nsend on nsend.oid = psend.pronamespace
                left join pg_proc pmodin on pmodin.oid = t.typmodin
                left join pg_namespace nmodin on nmodin.oid = pmodin.pronamespace
                left join pg_proc pmodout on pmodout.oid = t.typmodout
                left join pg_namespace nmodout on nmodout.oid = pmodout.pronamespace
                left join pg_proc panalyze on panalyze.oid = t.typanalyze
                left join pg_namespace nanalyze on nanalyze.oid = panalyze.pronamespace
                left join pg_collation coll on coll.oid = t.typcollation
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(t.typname) = '{1}'
            '''.format(p_schema, p_object))

    def GetDDLDomain(self, p_schema, p_object):
        return self.v_connection.ExecuteScalar('''
            with domain as (
                select t.oid,
                       quote_ident(n.nspname) || '.' || quote_ident(t.typname) as name,
                       format_type(t.typbasetype, null) as basetype,
                       quote_ident(cn.nspname) || '.' || quote_ident(c.collname) as collation,
                       t.typdefault as defaultvalue,
                       t.typnotnull as notnull,
                       quote_ident(r.rolname) as domainowner
                from pg_type t
                inner join pg_namespace n on n.oid = t.typnamespace
                left join pg_collation c on c.oid = t.typcollation
                left join pg_namespace cn on cn.oid = c.collnamespace
                inner join pg_roles r on r.oid = t.typowner
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(t.typname) = '{1}'
            ),
            constraints as (
                select d.oid,
                       quote_ident(c.conname) as name,
                       pg_get_constraintdef(c.oid, true) as def
                from domain d
                inner join pg_constraint c on c.contypid = d.oid
            ),
            create_domain as (
                select format(
                         E'CREATE DOMAIN %s\n  AS %s\n%s%s%s\n', d.name, d.basetype,
                         (case when d.collation is not null then format(E'  COLLATION %s', d.collation) else '' end),
                         (case when d.defaultvalue is not null then format(E'  DEFAULT %s\n', d.defaultvalue) else '' end),
                         (case when d.notnull then E'  NOT NULL' else '' end)
                       ) as sql
                from domain d
            ),
            create_constraints as (
                select string_agg(format(E'  CONSTRAINT %s %s\n', c.name, c.def), '') as sql
                from constraints c
            ),
            alter_domain as (
                select format(E'ALTER DOMAIN %s OWNER TO %s;\n', d.name, d.domainowner) as sql
                from domain d
            )
            select format(E'%s%s;\n\n%s',
                     (select sql from create_domain),
                     (select substring(sql from 1 for length(sql)-1) from create_constraints),
                     (select sql from alter_domain)
                   )
        '''.format(p_schema, p_object))

    def GetDDL(self, p_schema, p_table, p_object, p_type):
        if p_type == 'role':
            return self.GetDDLRole(p_object)
        elif p_type == 'tablespace':
            return self.GetDDLTablespace(p_object)
        elif p_type == 'database':
            return self.GetDDLDatabase(p_object)
        elif p_type == 'extension':
            return self.GetDDLExtension(p_object)
        elif p_type == 'schema':
            return self.GetDDLSchema(p_object)
        elif p_type == 'table':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'index':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'sequence':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'view':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'mview':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'function':
            return self.GetDDLFunction(p_object)
        elif p_type == 'procedure':
            return self.GetDDLProcedure(p_object)
        elif p_type == 'trigger':
            return self.GetTriggerDefinition(p_object, p_table, p_schema)
        elif p_type == 'triggerfunction':
            return self.GetDDLFunction(p_object)
        elif p_type == 'direct_triggerfunction':
            return self.GetDDLFunction(p_object)
        elif p_type == 'pk':
            return self.GetDDLConstraint(p_schema, p_table, p_object)
        elif p_type == 'foreign_key':
            return self.GetDDLConstraint(p_schema, p_table, p_object)
        elif p_type == 'unique':
            return self.GetDDLConstraint(p_schema, p_table, p_object)
        elif p_type == 'check':
            return self.GetDDLConstraint(p_schema, p_table, p_object)
        elif p_type == 'exclude':
            return self.GetDDLConstraint(p_schema, p_table, p_object)
        elif p_type == 'rule':
            return self.GetRuleDefinition(p_object, p_table, p_schema)
        elif p_type == 'foreign_table':
            return self.GetDDLClass(p_schema, p_object)
        elif p_type == 'user_mapping':
            return self.GetDDLUserMapping(p_schema, p_object)
        elif p_type == 'foreign_server':
            return self.GetDDLForeignServer(p_object)
        elif p_type == 'fdw':
            return self.GetDDLForeignDataWrapper(p_object)
        elif p_type == 'type':
            return self.GetDDLType(p_schema, p_object)
        elif p_type == 'domain':
            return self.GetDDLDomain(p_schema, p_object)
        else:
            return ''


    def GetAutocompleteValues(self, p_columns, p_filter):
        return self.v_connection.Query('''
            select {0}
            from (
            select 'database' as type,
                   0 as sequence,
                   0 as num_dots,
                   quote_ident(datname) as result,
                   quote_ident(datname) as result_complete,
                   quote_ident(datname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_database

            UNION ALL

            select 'tablespace' as type,
                   2 as sequence,
                   0 as num_dots,
                   quote_ident(spcname) as result,
                   quote_ident(spcname) as result_complete,
                   quote_ident(spcname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_tablespace

            UNION ALL

            select 'role' as type,
                   1 as sequence,
                   0 as num_dots,
                   quote_ident(rolname) as result,
                   quote_ident(rolname) as result_complete,
                   quote_ident(rolname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_roles

            UNION ALL

            select 'extension' as type,
                   4 as sequence,
                   0 as num_dots,
                   quote_ident(extname) as result,
                   quote_ident(extname) as result_complete,
                   quote_ident(extname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_extension

            UNION ALL

            select 'schema' as type,
                   3 as sequence,
                   0 as num_dots,
                   quote_ident(nspname) as result,
                   quote_ident(nspname) as result_complete,
                   quote_ident(nspname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_catalog.pg_namespace
            where nspname not in ('pg_toast') and nspname not like 'pg%%temp%%'

            UNION ALL

            select 'table' as type,
                   5 as sequence,
                   1 as num_dots,
                   quote_ident(c.relname) as result,
                   quote_ident(n.nspname) || '.' || quote_ident(c.relname) as result_complete,
                   quote_ident(n.nspname) || '.' || quote_ident(c.relname) as select_value,
                   quote_ident(n.nspname) as complement,

                   '' as complement_complete
            from pg_class c
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where c.relkind in ('r', 'p')

            UNION ALL

            select 'view' as type,
                   6 as sequence,
                   1 as num_dots,
                   quote_ident(table_name) as result,
                   quote_ident(table_schema) || '.' || quote_ident(table_name) as result_complete,
                   quote_ident(table_schema) || '.' || quote_ident(table_name) as select_value,
                   quote_ident(table_schema) as complement,
                   '' as complement_complete
            from information_schema.views

            UNION ALL

            select 'function' as type,
                   8 as sequence,
                   1 as num_dots,
                   quote_ident(p.proname) as result,
                   quote_ident(n.nspname) || '.' || quote_ident(p.proname) as result_complete,
                   quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' as select_value,
                   quote_ident(n.nspname) as complement,
                   '' as complement_complete
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where format_type(p.prorettype, null) <> 'trigger'

            UNION ALL

            select 'index' as type,
                   9 as sequence,
                   1 as num_dots,
                   quote_ident(i.indexname) as result,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.indexname) as result_complete,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.indexname) as select_value,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.tablename) as complement,
                   quote_ident(i.tablename) as complement_complete
            from pg_indexes i) search
            {1}
            order by sequence,result_complete
        '''.format(p_columns,p_filter), True)
