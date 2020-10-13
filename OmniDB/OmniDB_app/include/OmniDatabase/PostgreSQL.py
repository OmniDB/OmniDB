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
from urllib.parse import urlparse

import threading
import hashlib

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
        self.lock = None

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

        self.v_data_types = {
            'bigint': { 'quoted': False },
            'bigserial': { 'quoted': False },
            'char': { 'quoted': True },
            'character': { 'quoted': True },
            'character varying': { 'quoted': True },
            'date': { 'quoted': True },
            'decimal': { 'quoted': False },
            'double precision': { 'quoted': False },
            'float': { 'quoted': False },
            'integer': { 'quoted': False },
            'money': { 'quoted': False },
            'numeric': { 'quoted': False },
            'real': { 'quoted': False },
            'serial': { 'quoted': False },
            'smallint': { 'quoted': False },
            'smallserial': { 'quoted': False },
            'text': { 'quoted': True },
            'time with time zone': { 'quoted': True },
            'time without time zone': { 'quoted': True },
            'timestamp with time zone': { 'quoted': True },
            'timestamp without time zone': { 'quoted': True },
            'varchar': { 'quoted': True }
        }


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
        self.v_has_statistics = True

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

    def GetName(self):
        return self.v_service

    @lock_required
    def GetVersion(self):
        self.v_version = self.v_connection.ExecuteScalar('show server_version')
        self.v_version_num = self.v_connection.ExecuteScalar('show server_version_num')
        return 'PostgreSQL ' + self.v_version.split(' ')[0]

    @lock_required
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

    @lock_required
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

    @lock_required
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        return self.v_connection.Query(p_sql, p_alltypesstr, p_simple)

    @lock_required
    def ExecuteScalar(self, p_sql):
        return self.v_connection.ExecuteScalar(p_sql)

    @lock_required
    def Execute(self, p_sql):
        return self.v_connection.Execute(p_sql)

    @lock_required
    def Terminate(self, p_type):
        return self.v_connection.Terminate(p_type)

    @lock_required
    def QueryRoles(self):
        return self.v_connection.Query('''
            select quote_ident(rolname) as role_name,
                   oid
            from pg_roles
            order by rolname
        ''', True)

    @lock_required
    def QueryTablespaces(self):
        return self.v_connection.Query('''
            select quote_ident(spcname) as tablespace_name,
                   oid
            from pg_tablespace
            order by spcname
        ''', True)

    @lock_required
    def QueryDatabases(self):
        return self.v_connection.Query('''
            select database_name,
                   oid
            from (
            select quote_ident(datname) as database_name,
                   1 as sort,
                   oid
            from pg_database
            where datname = 'postgres'
            union all
            select database_name,
                   1 + row_number() over() as sort,
                   oid
            from (
            select quote_ident(datname) as database_name,
                   oid
            from pg_database
            where not datistemplate
              and datname <> 'postgres'
            order by datname asc
            ) x
            ) y
            order by sort
        ''', True)

    @lock_required
    def QueryExtensions(self):
        return self.v_connection.Query('''
            select quote_ident(extname) as extension_name,
                   oid
            from pg_extension
            order by extname
        ''', True)

    @lock_required
    def QuerySchemas(self):
        return self.v_connection.Query('''
            select schema_name,
                   oid
            from (
            select schema_name,
                   row_number() over() as sort,
                   oid
            from (
            select quote_ident(nspname) as schema_name,
                   oid
            from pg_catalog.pg_namespace
            where nspname in ('public', 'pg_catalog', 'information_schema')
            order by nspname desc
            ) x
            union all
            select schema_name,
                   3 + row_number() over() as sort,
                   oid
            from (
            select quote_ident(nspname) as schema_name,
                   oid
            from pg_catalog.pg_namespace
            where nspname not in ('public', 'pg_catalog', 'information_schema', 'pg_toast')
              and nspname not like 'pg%%temp%%'
            order by nspname
            ) x
            ) y
            order by sort
        ''', True)

    @lock_required
    def QueryTables(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            with parents as (
                select distinct quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema
                from pg_inherits i
                inner join pg_class c on c.oid = i.inhparent
                inner join pg_namespace n on n.oid = c.relnamespace
                inner join pg_class cc on cc.oid = i.inhrelid
                inner join pg_namespace nc on nc.oid = cc.relnamespace
                where c.relkind in ('r', 'p')
                {0}
            ),
            children as (
                select distinct quote_ident(c.relname) as table_name,
                       quote_ident(n.nspname) as table_schema
                from pg_inherits i
                inner join pg_class cp on cp.oid = i.inhparent
                inner join pg_namespace np on np.oid = cp.relnamespace
                inner join pg_class c on c.oid = i.inhrelid
                inner join pg_namespace n on n.oid = c.relnamespace
                where 1=1
                {0}
            )
            select quote_ident(c.relname) as table_name,
                   quote_ident(n.nspname) as table_schema,
                   c.oid
            from pg_class c
            inner join pg_namespace n
            on n.oid = c.relnamespace
            left join parents p
            on p.table_name = quote_ident(c.relname)
            and p.table_schema = quote_ident(n.nspname)
            left join children ch
            on ch.table_name = quote_ident(c.relname)
            and ch.table_schema = quote_ident(n.nspname)
            where ch.table_name is null
              and c.relkind in ('r', 'p')
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    @lock_required
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
                   null as data_scale,
                   a.attnum AS position
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

    @lock_required
    def QueryTablesForeignKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "AND c.connamespace = '{0}'::regnamespace AND quote_ident(t.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "AND c.connamespace = '{0}'::regnamespace AND quote_ident(t.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "AND c.connamespace = '{0}'::regnamespace ".format(p_schema)
            else:
                v_filter = "AND c.connamespace = '{0}'::regnamespace ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "AND c.connamespace NOT IN ('information_schema'::regnamespace, 'pg_catalog'::regnamespace) AND quote_ident(t.relname) = {0}".format(p_table)
            else:
                v_filter = "AND c.connamespace NOT IN ('information_schema'::regnamespace, 'pg_catalog'::regnamespace) "
        return self.v_connection.Query('''
            SELECT DISTINCT quote_ident(c.conname) AS constraint_name,
                            quote_ident(t.relname) AS table_name,
                            quote_ident(rc.conname) AS r_constraint_name,
                            quote_ident(rt.relname) AS r_table_name,
                            quote_ident(tn.nspname) AS table_schema,
                            quote_ident(rtn.nspname) AS r_table_schema,
                            c.update_rule,
                            c.delete_rule,
                            c.oid
            FROM (
                SELECT oid,
                       connamespace,
                       conname,
                       conrelid,
                       confrelid,
                       (CASE confupdtype WHEN 'c'
                                         THEN 'CASCADE'
                                         WHEN 'n'
                                         THEN 'SET NULL'
                                         WHEN 'd'
                                         THEN 'SET DEFAULT'
                                         WHEN 'r'
                                         THEN 'RESTRICT'
                                         WHEN 'a'
                                         THEN 'NO ACTION'
                        END) AS update_rule,
                       (CASE confdeltype WHEN 'c'
                                         THEN 'CASCADE'
                                         WHEN 'n'
                                         THEN 'SET NULL'
                                         WHEN 'd'
                                         THEN 'SET DEFAULT'
                                         WHEN 'r'
                                         THEN 'RESTRICT'
                                         WHEN 'a'
                                         THEN 'NO ACTION'
                        END) AS delete_rule
                FROM pg_constraint
                WHERE contype = 'f'
            ) c
            INNER JOIN pg_class t
                    ON c.conrelid = t.oid
            INNER JOIN pg_namespace tn
                    ON t.relnamespace = tn.oid
            INNER JOIN (
                SELECT objid,
                       refobjid
                FROM pg_depend
                WHERE classid = 'pg_constraint'::regclass::oid
                  AND refclassid = 'pg_class'::regclass::oid
                  AND refobjsubid = 0
            ) d1
                    ON c.oid = d1.objid
            INNER JOIN (
                SELECT objid,
                       refobjid
                FROM pg_depend
                WHERE refclassid = 'pg_constraint'::regclass::oid
                  AND classid = 'pg_class'::regclass::oid
                  AND deptype = 'i'
                  AND objsubid = 0
            ) d2
                    ON d1.refobjid = d2.objid
            INNER JOIN (
                SELECT oid,
                       conrelid,
                       connamespace,
                       conname
                FROM pg_constraint
                WHERE contype IN (
                    'p',
                    'u'
                )
            ) rc
                    ON d2.refobjid = rc.oid
                   AND c.confrelid = rc.conrelid
            INNER JOIN pg_class rt
                    ON rc.conrelid = rt.oid
            INNER JOIN pg_namespace rtn
                    ON rt.relnamespace = rtn.oid
            WHERE 1 = 1
            {0}
            ORDER BY quote_ident(c.conname),
                     quote_ident(t.relname)
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def QueryTablesPrimaryKeys(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' AND quote_ident(t.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' AND quote_ident(t.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' ".format(p_schema)
            else:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) NOT IN ('information_schema','pg_catalog') AND quote_ident(t.relname) = {0}".format(p_table)
            else:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) NOT IN ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            SELECT quote_ident(c.conname) AS constraint_name,
                   quote_ident(t.relname) AS table_name,
                   quote_ident(t.relnamespace::regnamespace::text) AS table_schema,
                   c.oid
            FROM (
                SELECT oid,
                       conrelid,
                       conname
                FROM pg_constraint
                WHERE contype = 'p'
            ) c
            INNER JOIN pg_class t
                    ON c.conrelid = t.oid
            WHERE 1 = 1
              {0}
            ORDER BY quote_ident(c.conname),
                     quote_ident(t.relnamespace::regnamespace::text)
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def QueryTablesUniques(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' AND quote_ident(t.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' AND quote_ident(t.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' ".format(p_schema)
            else:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) NOT IN ('information_schema','pg_catalog') AND quote_ident(t.relname) = {0}".format(p_table)
            else:
                v_filter = "AND quote_ident(t.relnamespace::regnamespace::text) NOT IN ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            SELECT quote_ident(c.conname) AS constraint_name,
                   quote_ident(t.relname) AS table_name,
                   quote_ident(t.relnamespace::regnamespace::text) AS table_schema,
                   c.oid
            FROM (
                SELECT oid,
                       conrelid,
                       conname
                FROM pg_constraint
                WHERE contype = 'u'
            ) c
            INNER JOIN pg_class t
                    ON c.conrelid = t.oid
            WHERE 1 = 1
              {0}
            ORDER BY quote_ident(c.conname),
                     quote_ident(t.relnamespace::regnamespace::text)
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def QueryTablesIndexes(self, p_table=None, p_all_schemas=False, p_schema=None):
        return self.QueryTablesIndexesHelper(p_table, p_all_schemas, p_schema)

    def QueryTablesIndexesHelper(self, p_table=None, p_all_schemas=False, p_schema=None):
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
                   quote_ident(ci.relname) as index_name,
                   (case when i.indisunique then 'Unique' else 'Non Unique' end) as uniqueness,
                   quote_ident(n.nspname) as schema_name,
                   format(
                       '%s;',
                       pg_get_indexdef(i.indexrelid)
                   ) AS definition,
                   ci.oid
            from pg_index i
            inner join pg_class ci
            on ci.oid = i.indexrelid
            inner join pg_namespace ni
            on ni.oid = ci.relnamespace
            inner join pg_class c
            on c.oid = i.indrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where i.indisvalid
              and i.indislive
              {0}
            order by 1, 2
        '''.format(v_filter), True)

    @lock_required
    def QueryTablesIndexesColumns(self, p_index, p_table=None, p_all_schemas=False, p_schema=None):
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
        v_filter = v_filter + "and quote_ident(ci.relname) = '{0}' ".format(p_index)
        return self.v_connection.Query('''
            select unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as column_name
            from (
            select pg_get_indexdef(i.indexrelid) as indexdef
            from pg_index i
            inner join pg_class ci
            on ci.oid = i.indexrelid
            inner join pg_namespace ni
            on ni.oid = ci.relnamespace
            inner join pg_class c
            on c.oid = i.indrelid
            inner join pg_namespace n
            on n.oid = c.relnamespace
            where i.indisvalid
              and i.indislive
              {0}
            ) t
        '''.format(v_filter), True)

    @lock_required
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
                   pg_get_constraintdef(c.oid) as constraint_source,
                   c.oid
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'c'
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    @lock_required
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
                   ) as attributes,
                   c.oid
            from pg_constraint c
            join pg_class t
            on t.oid = c.conrelid
            join pg_namespace n
            on t.relnamespace = n.oid
            where contype = 'x'
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    @lock_required
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
            select quote_ident(r.schemaname) as table_schema,
                   quote_ident(r.tablename) as table_name,
                   quote_ident(r.rulename) as rule_name,
                   rw.oid
            from pg_rules r
            INNER JOIN pg_rewrite rw
                    ON r.rulename = rw.rulename
            where 1 = 1
            {0}
            order by 1, 2, 3
        '''.format(v_filter), True)

    @lock_required
    def GetRuleDefinition(self, p_rule, p_table, p_schema):
        return self.v_connection.ExecuteScalar('''
            select r.definition ||
                   (CASE WHEN obj_description(rw.oid, 'pg_rewrite') IS NOT NULL
                         THEN format(
                                 E'\n\nCOMMENT ON RULE %s ON %s IS %s;',
                                 quote_ident(r.rulename),
                                 quote_ident(rw.ev_class::regclass::text),
                                 quote_literal(obj_description(rw.oid, 'pg_rewrite'))
                             )
                         ELSE ''
                    END)
            from pg_rules r
            INNER JOIN pg_rewrite rw
                    ON r.rulename = rw.rulename
            where quote_ident(r.schemaname) = '{0}'
              and quote_ident(r.tablename) = '{1}'
              and quote_ident(r.rulename) = '{2}'
        '''.format(p_schema, p_table, p_rule)).replace('CREATE RULE', 'CREATE OR REPLACE RULE')

    @lock_required
    def QueryEventTriggers(self):
        return self.v_connection.Query('''
            select quote_ident(t.evtname) as trigger_name,
                   t.evtenabled as trigger_enabled,
                   t.evtevent as event_name,
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) as trigger_function,
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) || '()' as id,
                   p.oid AS function_oid,
                   t.oid
            from pg_event_trigger t
            inner join pg_proc p
            on p.oid = t.evtfoid
            inner join pg_namespace np
            on np.oid = p.pronamespace
        ''')

    @lock_required
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
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   p.oid AS function_oid,
                   t.oid
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

    @lock_required
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

    @lock_required
    def QueryTablesInheritedsParents(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select distinct quote_ident(cp.relname) as table_name,
                   quote_ident(np.nspname) as table_schema
            from pg_inherits i
            inner join pg_class cp on cp.oid = i.inhparent
            inner join pg_namespace np on np.oid = cp.relnamespace
            inner join pg_class c on c.oid = i.inhrelid
            inner join pg_namespace n on n.oid = c.relnamespace
            where cp.relkind = 'r'
            {0}
            order by 2, 1
        '''.format(v_filter))

    @lock_required
    def QueryTablesInheritedsChildren(self, p_table, p_schema):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000:
            return self.v_connection.Query('''
                select quote_ident(cc.relname) as table_name,
                       quote_ident(nc.nspname) as table_schema,
                       cc.oid
                from pg_inherits i
                inner join pg_class cp on cp.oid = i.inhparent
                inner join pg_namespace np on np.oid = cp.relnamespace
                inner join pg_class cc on cc.oid = i.inhrelid
                inner join pg_namespace nc on nc.oid = cc.relnamespace
                where not cc.relispartition
                  and quote_ident(np.nspname) || '.' || quote_ident(cp.relname) = '{0}'
                  and quote_ident(nc.nspname) = '{1}'
                order by 2, 1
            '''.format(p_table, p_schema))
        else:
            return self.v_connection.Query('''
                select quote_ident(cc.relname) as table_name,
                       quote_ident(nc.nspname) as table_schema,
                       cc.oid
                from pg_inherits i
                inner join pg_class cp on cp.oid = i.inhparent
                inner join pg_namespace np on np.oid = cp.relnamespace
                inner join pg_class cc on cc.oid = i.inhrelid
                inner join pg_namespace nc on nc.oid = cc.relnamespace
                where quote_ident(np.nspname) || '.' || quote_ident(cp.relname) = '{0}'
                  and quote_ident(nc.nspname) = '{1}'
                order by 2, 1
            '''.format(p_table, p_schema))

    @lock_required
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

    @lock_required
    def QueryTablesPartitionsParents(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(n.nspname) not in ('information_schema','pg_catalog') "
        return self.v_connection.Query('''
            select distinct quote_ident(cp.relname) as table_name,
                   quote_ident(np.nspname) as table_schema
            from pg_inherits i
            inner join pg_class cp on cp.oid = i.inhparent
            inner join pg_namespace np on np.oid = cp.relnamespace
            inner join pg_class c on c.oid = i.inhrelid
            inner join pg_namespace n on n.oid = c.relnamespace
            where cp.relkind = 'p'
            {0}
            order by 2, 1
        '''.format(v_filter))

    @lock_required
    def QueryTablesPartitionsChildren(self, p_table, p_schema):
        return self.v_connection.Query('''
            select quote_ident(cc.relname) as table_name,
                   quote_ident(nc.nspname) as table_schema,
                   cc.oid
            from pg_inherits i
            inner join pg_class cp on cp.oid = i.inhparent
            inner join pg_namespace np on np.oid = cp.relnamespace
            inner join pg_class cc on cc.oid = i.inhrelid
            inner join pg_namespace nc on nc.oid = cc.relnamespace
            where cc.relispartition
              and quote_ident(np.nspname) || '.' || quote_ident(cp.relname) = '{0}'
              and quote_ident(nc.nspname) = '{1}'
            order by 2, 1
        '''.format(p_table, p_schema))

    @lock_required
    def QueryTablesStatistics(self, p_table=None, p_all_schemas=False, p_schema=None):
        v_filter = ''

        if not p_all_schemas:
            if p_table and p_schema:
                v_filter = "AND quote_ident(n.nspname) = '{0}' AND quote_ident(c.relname) = '{1}' ".format(p_schema, p_table)
            elif p_table:
                v_filter = "AND quote_ident(n.nspname) = '{0}' AND quote_ident(c.relname) = '{1}' ".format(self.v_schema, p_table)
            elif p_schema:
                v_filter = "AND quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "AND quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_table:
                v_filter = "AND quote_ident(n.nspname) NOT IN ('information_schema','pg_catalog') AND quote_ident(c.relname) = {0}".format(p_table)
            else:
                v_filter = "AND quote_ident(n.nspname) NOT IN ('information_schema','pg_catalog') "

        return self.v_connection.Query(
            '''
                select quote_ident(c.relname) AS table_name,
                       quote_ident(se.stxname) AS statistic_name,
                       quote_ident(n2.nspname) AS schema_name,
                       se.oid
                FROM pg_statistic_ext se
                INNER JOIN pg_class c
                        ON se.stxrelid = c.oid
                INNER JOIN pg_namespace n
                        ON c.relnamespace = n.oid
                INNER JOIN pg_namespace n2
                        ON se.stxnamespace = n2.oid
                WHERE 1 = 1
                  {0}
                ORDER BY 1,
                         3,
                         2
            '''.format(
                v_filter
            ),
            True
        )

    @lock_required
    def QueryStatisticsFields(self, p_statistics=None, p_all_schemas=False, p_schema=None):
        v_filter = ''

        if not p_all_schemas:
            if p_statistics and p_schema:
                v_filter = "AND quote_ident(n2.nspname) = '{0}' AND quote_ident(se.stxname) = '{1}' ".format(p_schema, p_statistics)
            elif p_statistics:
                v_filter = "AND quote_ident(n2.nspname) = '{0}' AND quote_ident(se.stxname) = '{1}' ".format(self.v_schema, p_statistics)
            elif p_schema:
                v_filter = "AND quote_ident(n2.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "AND quote_ident(n2.nspname) = '{0}' ".format(self.v_schema)
        else:
            if p_statistics:
                v_filter = "AND quote_ident(n2.nspname) NOT IN ('information_schema','pg_catalog') AND quote_ident(se.stxname) = {0}".format(p_statistics)
            else:
                v_filter = "AND quote_ident(n2.nspname) NOT IN ('information_schema','pg_catalog') "

        return self.v_connection.Query(
            '''
                select quote_ident(n2.nspname) AS schema_name,
                       quote_ident(se.stxname) AS statistic_name,
                       quote_ident(a.attname) AS column_name
                FROM pg_statistic_ext se
                INNER JOIN pg_class c
                        ON se.stxrelid = c.oid
                INNER JOIN pg_namespace n
                        ON c.relnamespace = n.oid
                INNER JOIN pg_namespace n2
                        ON se.stxnamespace = n2.oid
                INNER JOIN pg_attribute a
                        ON c.oid = a.attrelid
                       AND a.attnum = ANY(se.stxkeys)
                WHERE 1 = 1
                  {0}
                ORDER BY 1,
                         2,
                         3
            '''.format(
                v_filter
            ),
            True
        )

    @lock_required
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
            ), False
        )

    @lock_required
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
                       quote_ident(n.nspname) as schema_name,
                       p.oid AS function_oid
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                where not p.proisagg
                  and format_type(p.prorettype, null) not in ('trigger', 'event_trigger')
                {0}
                order by 1
            '''.format(v_filter), True)
        else:
            return self.v_connection.Query('''
                select quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                       quote_ident(p.proname) as name,
                       quote_ident(n.nspname) as schema_name,
                       p.oid AS function_oid
                from pg_proc p
                join pg_namespace n
                on p.pronamespace = n.oid
                where p.prokind = 'f'
                  and format_type(p.prorettype, null) not in ('trigger', 'event_trigger')
                {0}
                order by 1
            '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def GetFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    @lock_required
    def GetFunctionDebug(self, p_function):
        return self.v_connection.ExecuteScalar('''
            select p.prosrc
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
        '''.format(p_function))

    @lock_required
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
                   quote_ident(n.nspname) as schema_name,
                   p.oid AS function_oid
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where p.prokind = 'p'
            {0}
            order by 1
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def GetProcedureDefinition(self, p_procedure):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_procedure))

    @lock_required
    def GetProcedureDebug(self, p_procedure):
        return self.v_connection.ExecuteScalar('''
            select p.prosrc
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' = '{0}'
        '''.format(p_procedure))

    @lock_required
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
                   quote_ident(n.nspname) as schema_name,
                   p.oid AS function_oid
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where format_type(p.prorettype, null) = 'trigger'
            {0}
            order by 1
        '''.format(v_filter), True)

    @lock_required
    def GetTriggerFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    @lock_required
    def QueryEventTriggerFunctions(self, p_all_schemas=False, p_schema=None):
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
                   quote_ident(n.nspname) as schema_name,
                   p.oid AS function_oid
            from pg_proc p
            join pg_namespace n
            on p.pronamespace = n.oid
            where format_type(p.prorettype, null) = 'event_trigger'
            {0}
            order by 1
        '''.format(v_filter), True)

    @lock_required
    def QueryAggregates(self, p_all_schemas=False, p_schema=None):
        v_filter = ''

        if not p_all_schemas:
            if p_schema:
                v_filter = "AND quote_ident(n.nspname) = '{0}' ".format(p_schema)
            else:
                v_filter = "AND quote_ident(n.nspname) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "AND quote_ident(n.nspname) NOT IN ('information_schema','pg_catalog') "

        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query(
                '''
                    SELECT quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS id,
                           quote_ident(p.proname) AS name,
                           quote_ident(n.nspname) AS schema_name,
                           p.oid
                    FROM pg_aggregate a
                    INNER JOIN pg_proc p
                            ON a.aggfnoid = p.oid
                    INNER JOIN pg_namespace n
                            ON p.pronamespace = n.oid
                    WHERE p.proisagg
                      {0}
                    ORDER BY 1
                '''.format(
                    v_filter
                ),
                True
            )
        else:
            return self.v_connection.Query(
                '''
                    SELECT quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS id,
                           quote_ident(p.proname) AS name,
                           quote_ident(n.nspname) AS schema_name,
                           p.oid
                    FROM pg_aggregate a
                    INNER JOIN pg_proc p
                            ON a.aggfnoid = p.oid
                    INNER JOIN pg_namespace n
                            ON p.pronamespace = n.oid
                    WHERE p.prokind = 'a'
                      {0}
                    ORDER BY 1
                '''.format(
                    v_filter
                ),
                True
            )

    @lock_required
    def GetEventTriggerFunctionDefinition(self, p_function):
        return self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    @lock_required
    def QuerySequences(self, p_all_schemas=False, p_schema=None):
        v_filter = ''
        if not p_all_schemas:
            if p_schema:
                v_filter = "and quote_ident(relnamespace::regnamespace::text) = '{0}' ".format(p_schema)
            else:
                v_filter = "and quote_ident(relnamespace::regnamespace::text) = '{0}' ".format(self.v_schema)
        else:
            v_filter = "and quote_ident(relnamespace::regnamespace::text) NOT IN ('information_schema','pg_catalog') "
        v_table = self.v_connection.Query('''
            SELECT quote_ident(relnamespace::regnamespace::text) AS sequence_schema,
                   quote_ident(relname) AS sequence_name,
                   oid
            FROM pg_class
            WHERE relkind = 'S'
            {0}
            order by 1, 2
        '''.format(v_filter), True)
        return v_table

    @lock_required
    def QueryViews(self, p_all_schemas=False, p_schema=None):
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
                   quote_ident(n.nspname) as table_schema,
                   t.oid
            from pg_class t
            inner join pg_namespace n
            on n.oid = t.relnamespace
            where t.relkind = 'v'
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
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

    @lock_required
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
                   quote_ident(n.nspname) as schema_name,
                   t.oid
            from pg_class t
            inner join pg_namespace n
            on n.oid = t.relnamespace
            where t.relkind = 'm'
            {0}
            order by 2, 1
        '''.format(v_filter), True)

    @lock_required
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

    @lock_required
    def GetMaterializedViewDefinition(self, p_view, p_schema):
        return '''DROP MATERIALIZED VIEW {0}.{1};

CREATE MATERIALIZED VIEW {0}.{1} AS
{2}

{3}
'''.format(
    p_schema,
    p_view,
    self.v_connection.ExecuteScalar(
        '''
            select pg_get_viewdef('{0}.{1}'::regclass)
        '''.format(
            p_schema, p_view
        )
    ),
    '\n'.join([
        v_row['definition']
        for v_row in self.QueryTablesIndexesHelper(p_view, False, p_schema).Rows
    ])
)

    @lock_required
    def QueryPhysicalReplicationSlots(self):
        return self.v_connection.Query('''
            select quote_ident(slot_name) as slot_name
            from pg_replication_slots
            where slot_type = 'physical'
            order by 1
        ''', True)

    @lock_required
    def QueryLogicalReplicationSlots(self):
        return self.v_connection.Query('''
            select quote_ident(slot_name) as slot_name
            from pg_replication_slots
            where slot_type = 'logical'
            order by 1
        ''', True)

    @lock_required
    def QueryPublications(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) >= 110000:
            return self.v_connection.Query('''
                select quote_ident(pubname) as pubname,
                       puballtables,
                       pubinsert,
                       pubupdate,
                       pubdelete,
                       pubtruncate,
                       oid
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
                       false as pubtruncate,
                       oid
                from pg_publication
                order by 1
            ''', True)

    @lock_required
    def QueryPublicationTables(self, p_pub):
        return self.v_connection.Query('''
            select quote_ident(schemaname) || '.' || quote_ident(tablename) as table_name
            from pg_publication_tables
            where quote_ident(pubname) = '{0}'
            order by 1
        '''.format(p_pub), True)

    @lock_required
    def QuerySubscriptions(self):
        return self.v_connection.Query('''
            select quote_ident(s.subname) as subname,
                   s.subenabled,
                   s.subconninfo,
                   array_to_string(s.subpublications, ',') as subpublications,
                   s.oid
            from pg_subscription s
            inner join pg_database d
            on d.oid = s.subdbid
            where d.datname = '{0}'
            order by 1
        '''.format(self.v_service), True)

    @lock_required
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

    @lock_required
    def QueryForeignDataWrappers(self):
        return self.v_connection.Query('''
            select fdwname,
                   oid
            from pg_foreign_data_wrapper
            order by 1
        ''')

    @lock_required
    def QueryForeignServers(self, v_fdw):
        return self.v_connection.Query('''
            select s.srvname,
                   s.srvtype,
                   s.srvversion,
                   array_to_string(srvoptions, ',') as srvoptions,
                   s.oid
            from pg_foreign_server s
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            where w.fdwname = '{0}'
            order by 1
        '''.format(v_fdw))

    @lock_required
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

    @lock_required
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
                       false as is_partitioned,
                       c.oid
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
                       false as is_partitioned,
                       c.oid
                from pg_class c
                inner join pg_namespace n
                on n.oid = c.relnamespace
                where c.relkind = 'f'
                {0}
                order by 2, 1
            '''.format(v_filter), True)

    @lock_required
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

    @lock_required
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
                   quote_ident(t.typname) as type_name,
                   t.oid
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

    @lock_required
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
                   quote_ident(t.typname) as domain_name,
                   t.oid
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

    def AdvancedObjectSearchData(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas, p_dataCategoryFilter):
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

    def AdvancedObjectSearchFKName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchFunctionDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchFunctionName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchProcedureDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Procedure Definition'::text as category,
                   y.schema_name::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   y.procedure_definition::text as match_value
            from (
                select pg_get_functiondef(z.procedure_oid::regprocedure) as procedure_definition,
                       *
                from (
                    select n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' as procedure_oid,
                           p.proname as procedure_name,
                           n.nspname as schema_name
                    from pg_proc p
                    inner join pg_namespace n
                               on p.pronamespace = n.oid
                    where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
                      and n.nspname not like 'pg%%temp%%'
                      and p.prokind = 'p'
                    --#FILTER_BY_SCHEMA#  and lower(n.nspname) in (#VALUE_BY_SCHEMA#)
                ) z
            ) y
            where 1 = 1
            --#FILTER_PATTERN_CASE_SENSITIVE#  and y.procedure_definition like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(y.procedure_definition) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and y.procedure_definition ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and y.procedure_definition ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
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

    def AdvancedObjectSearchProcedureName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Procedure Name'::text as category,
                   n.nspname::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   p.proname::text as match_value
            from pg_proc p
            inner join pg_namespace n
                       on p.pronamespace = n.oid
            where n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and n.nspname not like 'pg%%temp%%'
              and p.prokind = 'p'
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

    def AdvancedObjectSearchIndexName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchMaterializedViewColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchMaterializedViewName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchPKName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchSchemaName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchSequenceName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchTableColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchTableName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchTriggerName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchTriggerSource(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchUniqueName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchViewColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchViewName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchCheckName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchRuleName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchRuleDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchInheritedTableName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchPartitionName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchRoleName(self, p_textPattern, p_caseSentive, p_regex):
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

    def AdvancedObjectSearchTablespaceName(self, p_textPattern, p_caseSentive, p_regex):
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

    def AdvancedObjectSearchExtensionName(self, p_textPattern, p_caseSentive, p_regex):
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

    def AdvancedObjectSearchFKColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchPKColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchUniqueColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchIndexColumnName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchCheckDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Check Definition'::text as category,
                   quote_ident(n.nspname)::text as schema_name,
                   quote_ident(t.relname)::text as table_name,
                   ''::text as column_name,
                   pg_get_constraintdef(c.oid) as match_value
            from pg_constraint c
            inner join pg_class t
                  on t.oid = c.conrelid
            inner join pg_namespace n
                  on t.relnamespace = n.oid
            where contype = 'c'
              and quote_ident(n.nspname) not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and quote_ident(n.nspname) not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and pg_get_constraintdef(c.oid) like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(pg_get_constraintdef(c.oid)) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and pg_get_constraintdef(c.oid) ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and pg_get_constraintdef(c.oid) ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
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

    def AdvancedObjectSearchTableTriggerName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchMaterializedViewDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchViewDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
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

    def AdvancedObjectSearchTypeName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Type Name'::text as category,
                   n.nspname::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   t.typname::text as match_value
            from pg_type t
            inner join pg_namespace n
            on n.oid = t.typnamespace
            where (t.typrelid = 0 or (select c.relkind = 'c' from pg_class c where c.oid = t.typrelid))
              and not exists(select 1 from pg_type el where el.oid = t.typelem and el.typarray = t.oid)
              and t.typtype <> 'd'
              and n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and n.nspname not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and t.typname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.typname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and t.typname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and t.typname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
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

    def AdvancedObjectSearchDomainName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Domain Name'::text as category,
                   n.nspname::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   t.typname::text as match_value
            from pg_type t
            inner join pg_namespace n
            on n.oid = t.typnamespace
            where (t.typrelid = 0 or (select c.relkind = 'c' from pg_class c where c.oid = t.typrelid))
              and not exists(select 1 from pg_type el where el.oid = t.typelem and el.typarray = t.oid)
              and t.typtype = 'd'
              and n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and n.nspname not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and t.typname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.typname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE# and t.typname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE# and t.typname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
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

    def AdvancedObjectSearchEventTriggerName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Event Trigger Name'::text as category,
                   np.nspname::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   t.evtname::text as match_value
            from pg_event_trigger t
            inner join pg_proc p
                    on p.oid = t.evtfoid
            inner join pg_namespace np
                    on np.oid = p.pronamespace
            where np.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
              and np.nspname not like 'pg%%temp%%'
            --#FILTER_PATTERN_CASE_SENSITIVE#  and t.evtname like '#VALUE_PATTERN_CASE_SENSITIVE#'
            --#FILTER_PATTERN_CASE_INSENSITIVE#  and lower(t.evtname) like lower('#VALUE_PATTERN_CASE_INSENSITIVE#')
            --#FILTER_PATTERN_REGEX_CASE_SENSITIVE#  and t.evtname ~ '#VALUE_PATTERN_REGEX_CASE_SENSITIVE#'
            --#FILTER_PATTERN_REGEX_CASE_INSENSITIVE#  and t.evtname ~* '#VALUE_PATTERN_REGEX_CASE_INSENSITIVE#'
            --#FILTER_BY_SCHEMA#  and lower(np.nspname) in (#VALUE_BY_SCHEMA#)
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

    def AdvancedObjectSearchEventTriggerFunctionName(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Event Trigger Function Name'::text as category,
                   n.nspname::text as schema_name,
                   ''::text as table_name,
                   ''::text as column_name,
                   p.proname::text as match_value
            from pg_proc p
            join pg_namespace n
              on p.pronamespace = n.oid
            where format_type(p.prorettype, null) = 'event_trigger'
              and n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
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

    def AdvancedObjectSearchEventTriggerFunctionDefinition(self, p_textPattern, p_caseSentive, p_regex, p_inSchemas):
        v_sql = '''
            select 'Event Trigger Function Definition'::text as category,
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
                    join pg_namespace n
                      on p.pronamespace = n.oid
                    where format_type(p.prorettype, null) = 'event_trigger'
                      and n.nspname not in ('information_schema', 'omnidb', 'pg_catalog', 'pg_toast')
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

    def AdvancedObjectSearch(self, p_textPattern, p_caseSentive, p_regex, p_categoryList, p_schemaList, p_dataCategoryFilter):
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
                v_sqlDict[v_category] = self.AdvancedObjectSearchData(p_textPattern, p_caseSentive, p_regex, v_inSchemas, p_dataCategoryFilter)
            elif v_category == 'FK Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchFKName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Function Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchFunctionDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Function Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchFunctionName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Index Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchIndexName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchMaterializedViewColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchMaterializedViewName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'PK Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchPKName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Schema Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchSchemaName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Sequence Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchSequenceName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTableColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTableName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Trigger Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTriggerName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Trigger Source':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTriggerSource(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Unique Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchUniqueName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchViewColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchViewName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Check Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchCheckName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Rule Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchRuleName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Rule Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchRuleDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Inherited Table Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchInheritedTableName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Partition Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchPartitionName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Role Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchRoleName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'Tablespace Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTablespaceName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'Extension Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchExtensionName(p_textPattern, p_caseSentive, p_regex)
            elif v_category == 'FK Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchFKColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'PK Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchPKColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Unique Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchUniqueColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Index Column Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchIndexColumnName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Check Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchCheckDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Table Trigger Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTableTriggerName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Materialized View Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchMaterializedViewDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'View Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchViewDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Type Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchTypeName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Domain Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchDomainName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Event Trigger Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchEventTriggerName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Event Trigger Function Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchEventTriggerFunctionName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Event Trigger Function Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchEventTriggerFunctionDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Procedure Definition':
                v_sqlDict[v_category] = self.AdvancedObjectSearchProcedureDefinition(p_textPattern, p_caseSentive, p_regex, v_inSchemas)
            elif v_category == 'Procedure Name':
                v_sqlDict[v_category] = self.AdvancedObjectSearchProcedureName(p_textPattern, p_caseSentive, p_regex, v_inSchemas)

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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90500:
            return Template('''CREATE DATABASE name
--OWNER user_name
--TEMPLATE template
--ENCODING encoding
--LC_COLLATE lc_collate
--LC_CTYPE lc_ctype
--TABLESPACE tablespace
--CONNECTION LIMIT connlimit
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''CREATE DATABASE name
--OWNER user_name
--TEMPLATE template
--ENCODING encoding
--LC_COLLATE lc_collate
--LC_CTYPE lc_ctype
--TABLESPACE tablespace
--ALLOW_CONNECTIONS allowconn
--CONNECTION LIMIT connlimit
--IS_TEMPLATE istemplate
''')
        else:
            return Template('''CREATE DATABASE name
--OWNER user_name
--TEMPLATE template
--ENCODING encoding
--LOCALE locale
--LC_COLLATE lc_collate
--LC_CTYPE lc_ctype
--TABLESPACE tablespace
--ALLOW_CONNECTIONS allowconn
--CONNECTION LIMIT connlimit
--IS_TEMPLATE istemplate
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('DROP DATABASE #database_name#')
        else:
            return Template('''DROP DATABASE #database_name#
--WITH ( FORCE )
''')

    def TemplateCreateExtension(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''CREATE EXTENSION name
--SCHEMA schema_name
--VERSION VERSION
--FROM old_version
''')
        else:
            return Template('''CREATE EXTENSION name
--SCHEMA schema_name
--VERSION VERSION
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

    def TemplateAlterFunction(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        else:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
--NO DEPENDS ON EXTENSION extension_name
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

    def TemplateAlterProcedure(self):
        return Template('''ALTER PROCEDURE #procedure_name#
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
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

    def TemplateAlterTriggerFunction(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        else:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
--NO DEPENDS ON EXTENSION extension_name
''')

    def TemplateDropTriggerFunction(self):
        return Template('''DROP FUNCTION #function_name#
--CASCADE
''')

    def TemplateCreateEventTriggerFunction(self):
        return Template('''CREATE OR REPLACE FUNCTION #schema_name#.name()
RETURNS event_trigger
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

    def TemplateAlterEventTriggerFunction(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
''')
        else:
            return Template('''ALTER FUNCTION #function_name#
--CALLED ON NULL INPUT
--RETURNS NULL ON NULL INPUT
--STRICT
--IMMUTABLE
--STABLE
--VOLATILE
--NOT LEAKPROOF
--LEAKPROOF
--EXTERNAL SECURITY INVOKER
--SECURITY INVOKER
--EXTERNAL SECURITY DEFINER
--SECURITY DEFINER
--PARALLEL { UNSAFE | RESTRICTED | SAFE }
--COST execution_cost
--ROWS result_rows
--SUPPORT support_function
--SET configuration_parameter { TO | = } { value | DEFAULT }
--SET configuration_parameter FROM CURRENT
--RESET configuration_parameter
--RESET ALL
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
--DEPENDS ON EXTENSION extension_name
--NO DEPENDS ON EXTENSION extension_name
''')

    def TemplateDropEventTriggerFunction(self):
        return Template('''DROP FUNCTION #function_name#
--CASCADE
''')

    def TemplateCreateAggregate(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''CREATE AGGREGATE #schema_name#.name
--([ argmode ] [ argname ] arg_data_type [ , ... ])
--ORDER BY [ argmode ] [ argname ] arg_data_type [ , ... ] )
(
    SFUNC = sfunc,
    STYPE = state_data_type
--    , SSPACE = state_data_size
--    , FINALFUNC = ffunc
--    , FINALFUNC_EXTRA
--    , INITCOND = initial_condition
--    , MSFUNC = msfunc
--    , MINVFUNC = minvfunc
--    , MSTYPE = mstate_data_type
--    , MSSPACE = mstate_data_size
--    , MFINALFUNC = mffunc
--    , MFINALFUNC_EXTRA
--    , MINITCOND = minitial_condition
--    , SORTOP = sort_operator
)
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return Template('''CREATE AGGREGATE #schema_name#.name
--([ argmode ] [ argname ] arg_data_type [ , ... ])
--ORDER BY [ argmode ] [ argname ] arg_data_type [ , ... ] )
(
SFUNC = sfunc,
STYPE = state_data_type
--    , SSPACE = state_data_size
--    , FINALFUNC = ffunc
--    , FINALFUNC_EXTRA
--    , COMBINEFUNC = combinefunc
--    , SERIALFUNC = serialfunc
--    , DESERIALFUNC = deserialfunc
--    , INITCOND = initial_condition
--    , MSFUNC = msfunc
--    , MINVFUNC = minvfunc
--    , MSTYPE = mstate_data_type
--    , MSSPACE = mstate_data_size
--    , MFINALFUNC = mffunc
--    , MFINALFUNC_EXTRA
--    , MINITCOND = minitial_condition
--    , SORTOP = sort_operator
--    , PARALLEL = { SAFE | RESTRICTED | UNSAFE }
)
''')
        else:
            return Template('''CREATE AGGREGATE #schema_name#.name
--([ argmode ] [ argname ] arg_data_type [ , ... ])
--ORDER BY [ argmode ] [ argname ] arg_data_type [ , ... ] )
(
SFUNC = sfunc,
STYPE = state_data_type
--    , SSPACE = state_data_size
--    , FINALFUNC = ffunc
--    , FINALFUNC_EXTRA
--    , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE }
--    , COMBINEFUNC = combinefunc
--    , SERIALFUNC = serialfunc
--    , DESERIALFUNC = deserialfunc
--    , INITCOND = initial_condition
--    , MSFUNC = msfunc
--    , MINVFUNC = minvfunc
--    , MSTYPE = mstate_data_type
--    , MSSPACE = mstate_data_size
--    , MFINALFUNC = mffunc
--    , MFINALFUNC_EXTRA
--    , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE }
--    , MINITCOND = minitial_condition
--    , SORTOP = sort_operator
--    , PARALLEL = { SAFE | RESTRICTED | UNSAFE }
)
''')

    def TemplateAlterAggregate(self):
        return Template('''ALTER AGGREGATE #aggregate_name#
--RENAME TO new_name
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--SET SCHEMA new_schema
''')

    def TemplateDropAggregate(self):
        return Template('''DROP AGGREGATE #aggregate_name#
--RESTRICT
--CASCADE
''')

    def TemplateCreateView(self):
        return Template('''CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] [ RECURSIVE ] VIEW #schema_name#.name
--WITH ( check_option = local | cascaded )
--WITH ( security_barrier = true | false )
AS
SELECT ...
''')

    def TemplateAlterView(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER VIEW #view_name#
--ALTER COLUMN column_name SET DEFAULT expression
--ALTER COLUMN column_name DROP DEFAULT
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
--SET SCHEMA new_schema
--SET ( check_option = value )
--SET ( security_barrier = { true | false } )
--RESET ( check_option )
--RESET ( security_barrier )

--ALTER TABLE #view_name# RENAME COLUMN column_name TO new_column_name
''')
        else:
            return Template('''ALTER VIEW #view_name#
--ALTER COLUMN column_name SET DEFAULT expression
--ALTER COLUMN column_name DROP DEFAULT
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME COLUMN column_name TO new_column_name
--RENAME TO new_name
--SET SCHEMA new_schema
--SET ( check_option = value )
--SET ( security_barrier = { true | false } )
--RESET ( check_option )
--RESET ( security_barrier )
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

    def TemplateAlterMaterializedView(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER MATERIALIZED VIEW #view_name#
--ALTER COLUMN column_name SET STATISTICS integer
--ALTER COLUMN column_name SET ( attribute_option = value )
--ALTER COLUMN column_name RESET ( attribute_option )
--ALTER COLUMN column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
--CLUSTER ON index_name
--SET WITHOUT CLUSTER
--SET ( storage_parameter = value )
--RESET ( storage_parameter )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME COLUMN column_name TO new_column_name
--RENAME TO new_name
--SET SCHEMA new_schema
--SET TABLESPACE new_tablespace [ NOWAIT ]
''')
        else:
            return Template('''ALTER MATERIALIZED VIEW #view_name#
--ALTER COLUMN column_name SET STATISTICS integer
--ALTER COLUMN column_name SET ( attribute_option = value )
--ALTER COLUMN column_name RESET ( attribute_option )
--ALTER COLUMN column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
--CLUSTER ON index_name
--SET WITHOUT CLUSTER
--SET ( storage_parameter = value )
--RESET ( storage_parameter )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--DEPENDS ON EXTENSION extension_name
--RENAME COLUMN column_name TO new_column_name
--RENAME TO new_name
--SET SCHEMA new_schema
--SET TABLESPACE new_tablespace [ NOWAIT ]
''')

    def TemplateDropMaterializedView(self):
        return Template('''DROP MATERIALIZED VIEW #view_name#
--CASCADE
''')

    def TemplateCreateTable(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
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
    --GENERATED ALWAYS AS ( generation_expr ) STORED
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
        else:
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
    --GENERATED ALWAYS AS ( generation_expr ) STORED
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
--WITHOUT OIDS
--ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP }
--TABLESPACE tablespace_name
''')

    def TemplateAlterTable(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
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
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
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
        else:
            return Template('''ALTER TABLE
--ONLY
#table_name#
--ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
--DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
--ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ USING expression ]
--ALTER [ COLUMN ] column_name SET DEFAULT expression
--ALTER [ COLUMN ] column_name DROP DEFAULT
--ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
--ALTER [ COLUMN ] column_name DROP EXPRESSION
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return Template('''CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] name
ON #table_name#
--USING method
( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
--WITH ( storage_parameter = value [, ... ] )
--WHERE predicate
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] name
ON [ ONLY ] #table_name#
--USING method
( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
--INCLUDE ( column_name [, ...] )
--WITH ( storage_parameter = value [, ... ] )
--WHERE predicate
''')
        else:
            return Template('''CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] name
ON [ ONLY ] #table_name#
--USING method
( { column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
--INCLUDE ( column_name [, ...] )
--WITH ( storage_parameter = value [, ... ] )
--WHERE predicate
''')

    def TemplateAlterIndex(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return Template('''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--DEPENDS ON EXTENSION extension_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--ATTACH PARTITION index_name
--DEPENDS ON EXTENSION extension_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''')
        else:
            return Template('''ALTER INDEX #index_name#
--RENAME to new_name
--SET TABLESPACE tablespace_name
--ATTACH PARTITION index_name
--DEPENDS ON EXTENSION extension_name
--NO DEPENDS ON EXTENSION extension_name
--SET ( storage_parameter = value [, ... ] )
--RESET ( storage_parameter [, ... ] )
''')

    def TemplateClusterIndex(self):
        return Template('''CLUSTER
--VERBOSE
#table_name#
USING #index_name#
''')

    def TemplateReindex(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90500:
            return Template('REINDEX INDEX #index_name#')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''REINDEX
--( VERBOSE )
INDEX #index_name#
''')
        else:
            return Template('''REINDEX
--( VERBOSE )
INDEX
--CONCURRENTLY
#index_name#
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''ALTER TRIGGER #trigger_name# ON #table_name#
--RENAME TO new_name
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER TRIGGER #trigger_name# ON #table_name#
--RENAME TO new_name
--DEPENDS ON EXTENSION extension_name
''')
        else:
            return Template('''ALTER TRIGGER #trigger_name# ON #table_name#
--RENAME TO new_name
--DEPENDS ON EXTENSION extension_name
--NO DEPENDS ON EXTENSION extension_name
''')

    def TemplateEnableTrigger(self):
        return Template('''ALTER TABLE #table_name# ENABLE
--REPLICA
--ALWAYS
TRIGGER #trigger_name#
''')

    def TemplateDisableTrigger(self):
        return Template('ALTER TABLE #table_name# DISABLE TRIGGER #trigger_name#')

    def TemplateDropTrigger(self):
        return Template('''DROP TRIGGER #trigger_name# ON #table_name#
--CASCADE
''')

    def TemplateCreateEventTrigger(self):
        return Template('''CREATE EVENT TRIGGER name
--ON ddl_command_start
--ON ddl_command_end
--ON table_rewrite
--ON sql_drop
--WHEN TAG IN ( filter_value [, ...] )
EXECUTE PROCEDURE function_name()
''')

    def TemplateAlterEventTrigger(self):
        return Template('''ALTER EVENT TRIGGER #trigger_name#
--OWNER TO new_owner
--OWNER TO CURRENT_USER
--OWNER TO SESSION_USER
--RENAME TO new_name
''')

    def TemplateEnableEventTrigger(self):
        return Template('''ALTER EVENT TRIGGER #trigger_name# ENABLE
--REPLICA
--ALWAYS
''')

    def TemplateDisableEventTrigger(self):
        return Template('ALTER EVENT TRIGGER #trigger_name# DISABLE')

    def TemplateDropEventTrigger(self):
        return Template('''DROP EVENT TRIGGER #trigger_name#
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
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
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER TYPE #type_name#
--ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
--ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
--OWNER TO new_owner
--RENAME TO new_name
--SET SCHEMA new_schema
--ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } existing_enum_value ]
--RENAME VALUE existing_enum_value TO new_enum_value
''')
        else:
            return Template('''ALTER TYPE #type_name#
--ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
--ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
--RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
--OWNER TO new_owner
--RENAME TO new_name
--SET SCHEMA new_schema
--ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } existing_enum_value ]
--RENAME VALUE existing_enum_value TO new_enum_value
--SET ( RECEIVE = value )
--SET ( SEND = value )
--SET ( TYPMOD_IN = value )
--SET ( TYPMOD_OUT = value )
--SET ( ANALYZE = value )
--SET ( STORAGE = plain | extended | external | main )
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
--SKIP_LOCKED
--INDEX_CLEANUP
--TRUNCATE
''')
        else:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
--SKIP_LOCKED
--INDEX_CLEANUP
--TRUNCATE
--PARALLEL number_of_parallel_workers
''')

    def TemplateVacuumTable(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
#table_name#
--(column_name, [, ...])
''')

        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
#table_name#
--(column_name, [, ...])
''')
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
--SKIP_LOCKED
--INDEX_CLEANUP
--TRUNCATE
#table_name#
--(column_name, [, ...])
''')
        else:
            return Template('''VACUUM
--FULL
--FREEZE
--ANALYZE
--DISABLE_PAGE_SKIPPING
--SKIP_LOCKED
--INDEX_CLEANUP
--TRUNCATE
--PARALLEL number_of_parallel_workers
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
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''CREATE PUBLICATION name
--FOR TABLE [ ONLY ] table_name [ * ] [, ...]
--FOR ALL TABLES
--WITH ( publish = 'insert, update, delete, truncate' )
''')
        else:
            return Template('''CREATE PUBLICATION name
--FOR TABLE [ ONLY ] table_name [ * ] [, ...]
--FOR ALL TABLES
--WITH ( publish = 'insert, update, delete, truncate' )
--WITH ( publish_via_partition_root = true | false )
''')

    def TemplateAlterPublication(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER PUBLICATION #pub_name#
--ADD TABLE [ ONLY ] table_name [ * ] [, ...]
--SET TABLE [ ONLY ] table_name [ * ] [, ...]
--DROP TABLE [ ONLY ] table_name [ * ] [, ...]
--SET ( publish = 'insert, update, delete, truncate' )
--OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
''')
        else:
            return Template('''ALTER PUBLICATION #pub_name#
--ADD TABLE [ ONLY ] table_name [ * ] [, ...]
--SET TABLE [ ONLY ] table_name [ * ] [, ...]
--DROP TABLE [ ONLY ] table_name [ * ] [, ...]
--SET ( publish = 'insert, update, delete, truncate' )
--SET ( publish_via_partition_root = true | false )
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
        return Template('DROP USER MAPPING FOR #user_name# SERVER #srvname#')

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
    --GENERATED ALWAYS AS ( generation_expr ) STORED
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

    def TemplateCreateStatistics(self):
        return Template('''CREATE STATISTICS #schema_name#.statistics_name
--( ndistinct )
--( dependencies )
--( mcv )
ON column_name, column_name [, ...]
FROM #table_name#
''')

    def TemplateAlterStatistics(self):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return Template('''ALTER STATISTICS #statistics_name#
--OWNER to { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
--SET SCHEMA new_schema
''')
        else:
            return Template('''ALTER STATISTICS #statistics_name#
--OWNER to { new_owner | CURRENT_USER | SESSION_USER }
--RENAME TO new_name
--SET SCHEMA new_schema
--SET STATISTICS new_target
''')

    def TemplateDropStatistics(self):
        return Template('DROP STATISTICS #statistics_name#')

    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) >= 110000 and int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
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

    @lock_required
    def GetPropertiesTableField(self, p_schema, p_table, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.Query(
                '''
                    SELECT current_database() AS "Database",
                           n.nspname AS "Schema",
                           c.relname AS "Table",
                           a.attname AS "Column",
                           c.oid AS "OID",
                           r.rolname AS "Owner",
                           a.atttypid::regtype AS "Type",
                           a.attstattarget AS "Statistics Target",
                           a.attlen AS "Type Length",
                           a.attnum AS "Position",
                           a.attndims AS "Dimension",
                           a.attcacheoff AS "Cache Offset",
                           a.atttypmod AS "Type Mod",
                           a.attbyval AS "By Value",
                           a.attstorage AS "Storage Type",
                           a.attalign AS "Storage Alignment",
                           a.attnotnull AS "Not Null",
                           a.atthasdef AS "Has Default",
                           a.attisdropped AS "Is Dropped",
                           a.attislocal AS "Is Local",
                           a.attinhcount AS "Inherited Count",
                           a.attcollation AS "Collate",
                           a.attacl AS "ACL",
                           a.attoptions AS "Options",
                           a.attfdwoptions AS "FDW Options"
                    FROM pg_class c
                    INNER JOIN pg_namespace n
                            ON c.relnamespace = n.oid
                    INNER JOIN pg_roles r
                            ON c.relowner = r.oid
                    INNER JOIN pg_attribute a
                            ON c.oid = a.attrelid
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND a.attname = quote_ident('{2}')
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query(
                '''
                    SELECT current_database() AS "Database",
                           n.nspname AS "Schema",
                           c.relname AS "Table",
                           a.attname AS "Column",
                           c.oid AS "OID",
                           r.rolname AS "Owner",
                           a.atttypid::regtype AS "Type",
                           a.attstattarget AS "Statistics Target",
                           a.attlen AS "Type Length",
                           a.attnum AS "Position",
                           a.attndims AS "Dimension",
                           a.attcacheoff AS "Cache Offset",
                           a.atttypmod AS "Type Mod",
                           a.attbyval AS "By Value",
                           a.attstorage AS "Storage Type",
                           a.attalign AS "Storage Alignment",
                           a.attnotnull AS "Not Null",
                           a.atthasdef AS "Has Default",
                           a.attidentity AS "Identitiy",
                           a.attisdropped AS "Is Dropped",
                           a.attislocal AS "Is Local",
                           a.attinhcount AS "Inherited Count",
                           a.attcollation AS "Collate",
                           a.attacl AS "ACL",
                           a.attoptions AS "Options",
                           a.attfdwoptions AS "FDW Options"
                    FROM pg_class c
                    INNER JOIN pg_namespace n
                            ON c.relnamespace = n.oid
                    INNER JOIN pg_roles r
                            ON c.relowner = r.oid
                    INNER JOIN pg_attribute a
                            ON c.oid = a.attrelid
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND a.attname = quote_ident('{2}')
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
            return self.v_connection.Query(
                '''
                    SELECT current_database() AS "Database",
                           n.nspname AS "Schema",
                           c.relname AS "Table",
                           a.attname AS "Column",
                           c.oid AS "OID",
                           r.rolname AS "Owner",
                           a.atttypid::regtype AS "Type",
                           a.attstattarget AS "Statistics Target",
                           a.attlen AS "Type Length",
                           a.attnum AS "Position",
                           a.attndims AS "Dimension",
                           a.attcacheoff AS "Cache Offset",
                           a.atttypmod AS "Type Mod",
                           a.attbyval AS "By Value",
                           a.attstorage AS "Storage Type",
                           a.attalign AS "Storage Alignment",
                           a.attnotnull AS "Not Null",
                           a.atthasdef AS "Has Default",
                           a.atthasmissing AS "Has Missing",
                           a.attidentity AS "Identitiy",
                           a.attisdropped AS "Is Dropped",
                           a.attislocal AS "Is Local",
                           a.attinhcount AS "Inherited Count",
                           a.attcollation AS "Collate",
                           a.attacl AS "ACL",
                           a.attoptions AS "Options",
                           a.attfdwoptions AS "FDW Options",
                           attmissingval AS "Missing Value"
                    FROM pg_class c
                    INNER JOIN pg_namespace n
                            ON c.relnamespace = n.oid
                    INNER JOIN pg_roles r
                            ON c.relowner = r.oid
                    INNER JOIN pg_attribute a
                            ON c.oid = a.attrelid
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND a.attname = quote_ident('{2}')
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )
        else:
            return self.v_connection.Query(
                '''
                    SELECT current_database() AS "Database",
                           n.nspname AS "Schema",
                           c.relname AS "Table",
                           a.attname AS "Column",
                           c.oid AS "OID",
                           r.rolname AS "Owner",
                           a.atttypid::regtype AS "Type",
                           a.attstattarget AS "Statistics Target",
                           a.attlen AS "Type Length",
                           a.attnum AS "Position",
                           a.attndims AS "Dimension",
                           a.attcacheoff AS "Cache Offset",
                           a.atttypmod AS "Type Mod",
                           a.attbyval AS "By Value",
                           a.attstorage AS "Storage Type",
                           a.attalign AS "Storage Alignment",
                           a.attnotnull AS "Not Null",
                           a.atthasdef AS "Has Default",
                           a.atthasmissing AS "Has Missing",
                           a.attidentity AS "Identitiy",
                           a.attgenerated AS "Generated",
                           a.attisdropped AS "Is Dropped",
                           a.attislocal AS "Is Local",
                           a.attinhcount AS "Inherited Count",
                           a.attcollation AS "Collate",
                           a.attacl AS "ACL",
                           a.attoptions AS "Options",
                           a.attfdwoptions AS "FDW Options",
                           attmissingval AS "Missing Value"
                    FROM pg_class c
                    INNER JOIN pg_namespace n
                            ON c.relnamespace = n.oid
                    INNER JOIN pg_roles r
                            ON c.relowner = r.oid
                    INNER JOIN pg_attribute a
                            ON c.oid = a.attrelid
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND a.attname = quote_ident('{2}')
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )

    @lock_required
    def GetPropertiesIndex(self, p_schema, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   c.relname as "Index",
                   c.oid as "OID",
                   r.rolname as "Owner",
                   pg_size_pretty(pg_relation_size(c.oid)) as "Size",
                   i.indisunique as "Unique",
                   i.indisprimary as "Primary",
                   i.indisexclusion as "Exclusion",
                   i.indimmediate as "Immediate",
                   i.indisclustered as "Clustered",
                   i.indisvalid as "Valid",
                   i.indisready as "Ready",
                   i.indislive as "Live",
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
            inner join pg_index i
            on i.indexrelid = c.oid
            where quote_ident(n.nspname) = '{0}'
              and quote_ident(c.relname) = '{1}'
        '''.format(p_schema, p_object))
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
    def GetPropertiesEventTrigger(self, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   quote_ident(t.evtname) as "Event Trigger Name",
                   t.evtevent as "Event",
                   array_to_string(t.evttags, ', ') as "Tags",
                   t.oid as "OID",
                   t.evtenabled as "Enabled",
                   r.rolname as "Owner",
                   quote_ident(np.nspname) || '.' || quote_ident(p.proname) as "Event Trigger Function"
            from pg_event_trigger t
            inner join pg_proc p
            on p.oid = t.evtfoid
            inner join pg_namespace np
            on np.oid = p.pronamespace
            inner join pg_roles r
            on r.oid = t.evtowner
            where quote_ident(t.evtname) = '{0}'
        '''.format(p_object))

    @lock_required
    def GetPropertiesAggregate(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return self.v_connection.Query(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               r.rolname AS function_owner,
                               p.proisagg AS is_aggregate
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    )
                    SELECT current_database() as "Database",
                           p1.schema_name AS "Schema",
                           p1.function_name AS "Aggregate",
                           p1.function_id AS "Aggregate ID",
                           a.aggfnoid AS "OID",
                           p1.function_owner as "Owner",
                           a.aggkind AS "Kind",
                           a.aggnumdirectargs AS "Number of Direct Args",
                           p2.function_id AS "Transition Function ID",
                           p3.function_id AS "Final Function ID",
                           p7.function_id AS "Forward Transition Function ID",
                           p8.function_id AS "Inverse Transition Function ID",
                           p9.function_id AS "Final Moving Function ID",
                           a.aggfinalextra AS "Extra Dummy to Final Function",
                           a.aggmfinalextra AS "Extra Dummy to Final Moving Function",
                           o.operator_name AS "Sort Operator",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Data Type",
                           a.aggtransspace AS "Average Size of Transition",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Moving Data Type",
                           a.aggmtransspace AS "Average Size of Transition Moving",
                           a.agginitval AS "Transition Init Value",
                           a.aggminitval AS "Transition Moving Init Value"
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    WHERE p1.is_aggregate
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.Query(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               r.rolname AS function_owner,
                               p.proisagg AS is_aggregate,
                               p.proparallel
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    )
                    SELECT current_database() as "Database",
                           p1.schema_name AS "Schema",
                           p1.function_name AS "Aggregate",
                           p1.function_id AS "Aggregate ID",
                           a.aggfnoid AS "OID",
                           p1.function_owner as "Owner",
                           a.aggkind AS "Kind",
                           a.aggnumdirectargs AS "Number of Direct Args",
                           p2.function_id AS "Transition Function ID",
                           p3.function_id AS "Final Function ID",
                           p4.function_id AS "Combine Function ID",
                           p5.function_id AS "Serialization Function ID",
                           p6.function_id AS "Deerialization Function ID",
                           p7.function_id AS "Forward Transition Function ID",
                           p8.function_id AS "Inverse Transition Function ID",
                           p9.function_id AS "Final Moving Function ID",
                           a.aggfinalextra AS "Extra Dummy to Final Function",
                           a.aggmfinalextra AS "Extra Dummy to Final Moving Function",
                           o.operator_name AS "Sort Operator",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Data Type",
                           a.aggtransspace AS "Average Size of Transition",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Moving Data Type",
                           a.aggmtransspace AS "Average Size of Transition Moving",
                           a.agginitval AS "Transition Init Value",
                           a.aggminitval AS "Transition Moving Init Value",
                           p1.proparallel AS "Parallel Mode"
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p4
                           ON a.aggcombinefn = p4.function_oid
                    LEFT JOIN procs p5
                           ON a.aggserialfn = p5.function_oid
                    LEFT JOIN procs p6
                           ON a.aggdeserialfn = p6.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    WHERE p1.is_aggregate
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )
        else:
            return self.v_connection.Query(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               r.rolname AS function_owner,
                               p.prokind AS function_kind,
                               p.proparallel
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    )
                    SELECT current_database() as "Database",
                           p1.schema_name AS "Schema",
                           p1.function_name AS "Aggregate",
                           p1.function_id AS "Aggregate ID",
                           a.aggfnoid AS "OID",
                           p1.function_owner as "Owner",
                           a.aggkind AS "Kind",
                           a.aggnumdirectargs AS "Number of Direct Args",
                           p2.function_id AS "Transition Function ID",
                           p3.function_id AS "Final Function ID",
                           p4.function_id AS "Combine Function ID",
                           p5.function_id AS "Serialization Function ID",
                           p6.function_id AS "Deerialization Function ID",
                           p7.function_id AS "Forward Transition Function ID",
                           p8.function_id AS "Inverse Transition Function ID",
                           p9.function_id AS "Final Moving Function ID",
                           a.aggfinalextra AS "Extra Dummy to Final Function",
                           a.aggmfinalextra AS "Extra Dummy to Final Moving Function",
                           a.aggfinalmodify AS "Final Function Modifier",
                           a.aggmfinalmodify AS "Final Moving Function Modifier",
                           o.operator_name AS "Sort Operator",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Data Type",
                           a.aggtransspace AS "Average Size of Transition",
                           format('%s.%s', t1.schema_name, t1.type_name)::regtype AS "Internal Transition Moving Data Type",
                           a.aggmtransspace AS "Average Size of Transition Moving",
                           a.agginitval AS "Transition Init Value",
                           a.aggminitval AS "Transition Moving Init Value",
                           p1.proparallel AS "Parallel Mode"
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p4
                           ON a.aggcombinefn = p4.function_oid
                    LEFT JOIN procs p5
                           ON a.aggserialfn = p5.function_oid
                    LEFT JOIN procs p6
                           ON a.aggdeserialfn = p6.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    WHERE p1.function_kind = 'a'
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )

    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
                   pg_get_constraintdef(c.oid) as "Constraint Source"
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
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
    @lock_required
    def GetPropertiesType(self, p_schema, p_object):
        return self.v_connection.Query('''
            select current_database() as "Database",
                   n.nspname as "Schema",
                   t.typname as "Internal Type Name",
                   format_type(t.oid, null) as "SQL Type Name",
                   t.oid as "OID",
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

    @lock_required
    def GetPropertiesPublication(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return self.v_connection.Query('''
                SELECT current_database() as "Database",
                       p.pubname AS "Name",
                       p.oid AS "OID",
                       r.rolname as "Owner",
                       p.puballtables AS "All Tables",
                       p.pubinsert AS "Inserts",
                       p.pubupdate AS "Updates",
                       p.pubdelete AS "Deletes",
                       p.pubtruncate AS "Truncates"
                FROM pg_publication p
                INNER JOIN pg_roles r
                        ON p.pubowner = r.oid
                WHERE quote_ident(p.pubname) = '{0}'
            '''.format(p_object))
        else:
            return self.v_connection.Query('''
                SELECT current_database() as "Database",
                       p.pubname AS "Name",
                       p.oid AS "OID",
                       r.rolname as "Owner",
                       p.puballtables AS "All Tables",
                       p.pubinsert AS "Inserts",
                       p.pubupdate AS "Updates",
                       p.pubdelete AS "Deletes",
                       p.pubtruncate AS "Truncates",
                       p.pubviaroot AS "Via Partition Root"
                FROM pg_publication p
                INNER JOIN pg_roles r
                        ON p.pubowner = r.oid
                WHERE quote_ident(p.pubname) = '{0}'
            '''.format(p_object))

    @lock_required
    def GetPropertiesSubscription(self, p_object):
        return self.v_connection.Query('''
            SELECT d.datname AS "Database",
                   s.subname AS "Name",
                   s.oid AS "OID",
                   r.rolname AS "Owner",
                   s.subenabled AS "Enabled",
                   s.subconninfo AS "Connection",
                   s.subslotname AS "Slot Name",
                   s.subslotname AS "Sync Commit",
                   s.subpublications AS "Publications"
            FROM pg_subscription s
            INNER JOIN pg_database d
                    ON s.subdbid = d.oid
            INNER JOIN pg_roles r
                    ON s.subowner = r.oid
            WHERE quote_ident(s.subname) = '{0}'
        '''.format(p_object))

    @lock_required
    def GetPropertiesStatistic(self, p_schema, p_object):
        return self.v_connection.Query(
            '''
                SELECT current_database() AS "Database",
                       n.nspname AS "Schema",
                       se.stxname AS "Name",
                       se.oid AS "OID",
                       r.rolname AS "Owner",
                       se.stxstattarget AS "Statistic Target",
                       se.stxkind AS "kinds"
                FROM pg_statistic_ext se
                INNER JOIN pg_namespace n
                        ON se.stxnamespace = n.oid
                INNER JOIN pg_roles r
                        ON se.stxowner = r.oid
                WHERE quote_ident(n.nspname) = '{0}'
                  AND quote_ident(se.stxname) = '{1}'
            '''.format(
                p_schema,
                p_object
            )
        )

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
            elif p_type == 'table_field':
                return self.GetPropertiesTableField(p_schema, p_table, p_object).Transpose('Property', 'Value')
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
            elif p_type == 'eventtrigger':
                return self.GetPropertiesEventTrigger(p_object).Transpose('Property', 'Value')
            elif p_type == 'triggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'direct_triggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'eventtriggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'direct_eventtriggerfunction':
                return self.GetPropertiesFunction(p_object).Transpose('Property', 'Value')
            elif p_type == 'aggregate':
                return self.GetPropertiesAggregate(p_object).Transpose('Property', 'Value')
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
            elif p_type == 'publication':
                return self.GetPropertiesPublication(p_object).Transpose('Property', 'Value')
            elif p_type == 'subscription':
                return self.GetPropertiesSubscription(p_object).Transpose('Property', 'Value')
            elif p_type == 'statistic':
                return self.GetPropertiesStatistic(p_schema, p_object).Transpose('Property', 'Value')
            else:
                return None
        except Spartacus.Database.Exception as exc:
            if str(exc) == 'Can only transpose a table with a single row.':
                raise Exception('Object {0} does not exist anymore. Please refresh the tree view.'.format(p_object))
            else:
                raise exc
    @lock_required
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
    @lock_required
    def GetDDLTablespace(self, p_object):
        return self.v_connection.ExecuteScalar('''
            select format(E'CREATE TABLESPACE %s\nLOCATION %s\nOWNER %s;%s',
                         quote_ident(t.spcname),
                         chr(39) || pg_tablespace_location(t.oid) || chr(39),
                         quote_ident(r.rolname),
                         (CASE WHEN shobj_description(t.oid, 'pg_tablespace') IS NOT NULL
                               THEN format(
                                       E'\n\nCOMMENT ON TABLESPACE %s IS %s;',
                                       quote_ident(t.spcname),
                                       quote_literal(shobj_description(t.oid, 'pg_tablespace'))
                                   )
                               ELSE ''
                          END)
                   )
            from pg_tablespace t
            inner join pg_roles r
            on r.oid = t.spcowner
            where quote_ident(t.spcname) = '{0}'
        '''.format(p_object))
    @lock_required
    def GetDDLDatabase(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90500:
            return self.v_connection.ExecuteScalar('''
                WITH comments AS (
                    SELECT shobj_description(oid, 'pg_database') AS comment
                    FROM pg_database
                    WHERE quote_ident(datname) = '{0}'
                )
                select format(E'CREATE DATABASE %s\nOWNER %s\nENCODING %s\nLC_COLLATE ''%s''\nLC_CTYPE ''%s''\nTABLESPACE %s\CONNECTION LIMIT %s;%s',
                              quote_ident(d.datname),
                              quote_ident(r.rolname),
                              pg_encoding_to_char(encoding),
                              datcollate,
                              datctype,
                              quote_ident(t.spcname),
                              datconnlimit,
                              (CASE WHEN c.comment IS NOT NULL
                                    THEN format(
                                             E'\n\nCOMMENT ON DATABASE %s is %s;',
                                             quote_ident(d.datname),
                                             quote_literal(c.comment)
                                         )
                                    ELSE ''
                               END))
                from pg_database d
                inner join pg_roles r
                on r.oid = d.datdba
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                LEFT JOIN comments c
                       ON 1 = 1
                where quote_ident(d.datname) = '{0}'
            '''.format(p_object))
        else:
            return self.v_connection.ExecuteScalar('''
                WITH comments AS (
                    SELECT shobj_description(oid, 'pg_database') AS comment
                    FROM pg_database
                    WHERE quote_ident(datname) = '{0}'
                )
                select format(E'CREATE DATABASE %s\nOWNER %s\nENCODING %s\nLC_COLLATE ''%s''\nLC_CTYPE ''%s''\nTABLESPACE %s\nALLOW_CONNECTIONS %s\nCONNECTION LIMIT %s\nIS_TEMPLATE %s;%s',
                              quote_ident(d.datname),
                              quote_ident(r.rolname),
                              pg_encoding_to_char(encoding),
                              datcollate,
                              datctype,
                              quote_ident(t.spcname),
                              datallowconn::text,
                              datconnlimit,
                              datistemplate::text,
                              (CASE WHEN c.comment IS NOT NULL
                                    THEN format(
                                             E'\n\nCOMMENT ON DATABASE %s is %s;',
                                             quote_ident(d.datname),
                                             quote_literal(c.comment)
                                         )
                                    ELSE ''
                               END))
                from pg_database d
                inner join pg_roles r
                on r.oid = d.datdba
                inner join pg_tablespace t
                on t.oid = d.dattablespace
                LEFT JOIN comments c
                       ON 1 = 1
                where quote_ident(d.datname) = '{0}'
            '''.format(p_object))
    @lock_required
    def GetDDLExtension(self, p_object):
        return self.v_connection.ExecuteScalar(
            '''
                WITH comments AS (
                    SELECT COALESCE(obj_description(oid, 'pg_extension'), '') AS description
                    FROM pg_extension
                    WHERE quote_ident(extname) = '{0}'
                )
                SELECT format(
                           E'CREATE EXTENSION {0};%s',
                           (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON EXTENSION {0} IS %s;',
                                          description
                                      )
                                 ELSE ''
                            END)
                       ) AS sql
                FROM comments
            '''.format(
                p_object
            )
        )
        return 'CREATE EXTENSION {0};'.format(p_object)
    @lock_required
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
    @lock_required
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
                        a.attacl,
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
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'v'
                                               THEN format(
                                                        E'\n\nCOMMENT ON VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'm'
                                               THEN format(
                                                        E'\n\nCOMMENT ON MATERIALIZED VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
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
                      E';\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'r'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'f'
                                               THEN format(
                                                        E'\n\nCOMMENT ON FOREIGN TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    SELECT 'CREATE SEQUENCE '||(c.oid::regclass::text) || E';\n'
                           ||'ALTER SEQUENCE '||(c.oid::regclass::text)
                           ||E'\n INCREMENT BY '||sp.increment
                           ||E'\n MINVALUE '||sp.minimum_value
                           ||E'\n MAXVALUE '||sp.maximum_value
                           ||E'\n START WITH '||sp.start_value
                           ||E'\n '|| CASE cycle_option WHEN true THEN 'CYCLE' ELSE 'NO CYCLE' END
                           ||E';\n'||
                           (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                 THEN (CASE relkind WHEN 'S'
                                                    THEN format(
                                                             E'\n\nCOMMENT ON SEQUENCE %s IS %s;',
                                                             '{0}.{1}'::regclass,
                                                             quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                         )
                                                    ELSE ''
                                       END)
                                 ELSE ''
                            END) as text
                    FROM pg_class c,
                    LATERAL pg_sequence_parameters(c.oid) sp (start_value, minimum_value, maximum_value, increment, cycle_option)
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND c.relkind = 'S'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid) ||
                                     (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                           THEN format(
                                                    E'\n\nCOMMENT ON INDEX %s IS %s;',
                                                    '{0}.{1}'::regclass,
                                                    quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                )
                                           ELSE ''
                                      END)
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
                ),
                columnsprivileges as (
                    SELECT r.rolname AS grantee,
                           c.name AS column_name,
                           c.privilege_type
                    FROM (
                        SELECT name,
                               (aclexplode(attacl)).grantee AS grantee,
                               (aclexplode(attacl)).privilege_type AS privilege_type
                        FROM columns
                    ) c
                    INNER JOIN pg_roles r
                            ON c.grantee = r.oid
                ),
                columnsgrants as (
                    SELECT coalesce(
                               string_agg(
                                   format(
                                       E'GRANT %s(%s) ON %s TO %s;\n',
                                       privilege_type,
                                       column_name,
                                       '{0}.{1}',
                                       quote_ident(grantee)
                                   ),
                                   ''
                               ),
                               ''
                           ) AS text
                     FROM columnsprivileges
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM columnsgrants)
        '''.format(p_schema, p_object))
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) >= 100000 and int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
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
                                ('I','PARTITIONED INDEX'),
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
                        a.attacl,
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
                  WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'v'
                                               THEN format(
                                                        E'\n\nCOMMENT ON VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'm'
                                               THEN format(
                                                        E'\n\nCOMMENT ON MATERIALIZED VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
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
                      E';\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'r'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'p'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'f'
                                               THEN format(
                                                        E'\n\nCOMMENT ON FOREIGN TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    SELECT 'CREATE SEQUENCE '||(c.oid::regclass::text) || E';\n'
                           ||'ALTER SEQUENCE '||(c.oid::regclass::text)
                           ||E'\n INCREMENT BY '||sp.increment
                           ||E'\n MINVALUE '||sp.minimum_value
                           ||E'\n MAXVALUE '||sp.maximum_value
                           ||E'\n START WITH '||sp.start_value
                           ||E'\n '|| CASE cycle_option WHEN true THEN 'CYCLE' ELSE 'NO CYCLE' END
                           ||E';\n'||
                           (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                 THEN (CASE relkind WHEN 'S'
                                                    THEN format(
                                                             E'\n\nCOMMENT ON SEQUENCE %s IS %s;',
                                                             '{0}.{1}'::regclass,
                                                             quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                         )
                                                    ELSE ''
                                       END)
                                 ELSE ''
                            END) as text
                    FROM pg_class c,
                    LATERAL pg_sequence_parameters(c.oid) sp (start_value, minimum_value, maximum_value, increment, cycle_option)
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND c.relkind = 'S'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid) ||
                                     (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                           THEN format(
                                                    E'\n\nCOMMENT ON INDEX %s IS %s;',
                                                    '{0}.{1}'::regclass,
                                                    quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                )
                                           ELSE ''
                                      END)
                            END AS indexdef
                       FROM pg_index x
                       JOIN pg_class c ON c.oid = x.indrelid
                       JOIN pg_class i ON i.oid = x.indexrelid
                       JOIN pg_depend d ON d.objid = x.indexrelid
                       LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                      WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      when obj.kind in ('INDEX', 'PARTITIONED INDEX') then (select text from createindex)
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
                         when obj.kind in ('INDEX', 'PARTITIONED INDEX') then ''
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
                ),
                columnsprivileges as (
                    SELECT r.rolname AS grantee,
                           c.name AS column_name,
                           c.privilege_type
                    FROM (
                        SELECT name,
                               (aclexplode(attacl)).grantee AS grantee,
                               (aclexplode(attacl)).privilege_type AS privilege_type
                        FROM columns
                    ) c
                    INNER JOIN pg_roles r
                            ON c.grantee = r.oid
                ),
                columnsgrants as (
                    SELECT coalesce(
                               string_agg(
                                   format(
                                       E'GRANT %s(%s) ON %s TO %s;\n',
                                       privilege_type,
                                       column_name,
                                       '{0}.{1}',
                                       quote_ident(grantee)
                                   ),
                                   ''
                               ),
                               ''
                           ) AS text
                     FROM columnsprivileges
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM columnsgrants)
            '''.format(p_schema, p_object))
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) >= 110000 and int(self.v_connection.ExecuteScalar('show server_version_num')) < 120000:
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
                                ('I','PARTITIONED INDEX'),
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
                        a.attacl,
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
                  WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'v'
                                               THEN format(
                                                        E'\n\nCOMMENT ON VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'm'
                                               THEN format(
                                                        E'\n\nCOMMENT ON MATERIALIZED VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
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
                      E';\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'r'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'p'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'f'
                                               THEN format(
                                                        E'\n\nCOMMENT ON FOREIGN TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    SELECT 'CREATE SEQUENCE '||(c.oid::regclass::text) || E';\n'
                           ||'ALTER SEQUENCE '||(c.oid::regclass::text)
                           ||E'\n INCREMENT BY '||sp.increment
                           ||E'\n MINVALUE '||sp.minimum_value
                           ||E'\n MAXVALUE '||sp.maximum_value
                           ||E'\n START WITH '||sp.start_value
                           ||E'\n '|| CASE cycle_option WHEN true THEN 'CYCLE' ELSE 'NO CYCLE' END
                           ||E';\n'||
                           (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                 THEN (CASE relkind WHEN 'S'
                                                    THEN format(
                                                             E'\n\nCOMMENT ON SEQUENCE %s IS %s;',
                                                             '{0}.{1}'::regclass,
                                                             quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                         )
                                                    ELSE ''
                                       END)
                                 ELSE ''
                            END) as text
                    FROM pg_class c,
                    LATERAL pg_sequence_parameters(c.oid) sp (start_value, minimum_value, maximum_value, increment, cycle_option)
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND c.relkind = 'S'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid) ||
                                     (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                           THEN format(
                                                    E'\n\nCOMMENT ON INDEX %s IS %s;',
                                                    '{0}.{1}'::regclass,
                                                    quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                )
                                           ELSE ''
                                      END)
                            END AS indexdef
                       FROM pg_index x
                       JOIN pg_class c ON c.oid = x.indrelid
                       JOIN pg_class i ON i.oid = x.indexrelid
                       JOIN pg_depend d ON d.objid = x.indexrelid
                       LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                      WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      when obj.kind in ('INDEX', 'PARTITIONED INDEX') then (select text from createindex)
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
                         when obj.kind in ('INDEX', 'PARTITIONED INDEX') then ''
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
                ),
                columnsprivileges as (
                    SELECT r.rolname AS grantee,
                           c.name AS column_name,
                           c.privilege_type
                    FROM (
                        SELECT name,
                               (aclexplode(attacl)).grantee AS grantee,
                               (aclexplode(attacl)).privilege_type AS privilege_type
                        FROM columns
                    ) c
                    INNER JOIN pg_roles r
                            ON c.grantee = r.oid
                ),
                columnsgrants as (
                    SELECT coalesce(
                               string_agg(
                                   format(
                                       E'GRANT %s(%s) ON %s TO %s;\n',
                                       privilege_type,
                                       column_name,
                                       '{0}.{1}',
                                       quote_ident(grantee)
                                   ),
                                   ''
                               ),
                               ''
                           ) AS text
                     FROM columnsprivileges
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM columnsgrants)
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
                                ('I','PARTITIONED INDEX'),
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
                        a.attgenerated AS generated,
                        pg_get_expr(def.adbin, def.adrelid) AS "default",
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
                        a.attacl,
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
                              WHEN a.attgenerated = 's' THEN format(' GENERATED ALWAYS AS %s STORED',pg_get_expr(def.adbin, def.adrelid))::text
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
                  WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      pg_catalog.pg_get_viewdef(oid,true)||E'\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'v'
                                               THEN format(
                                                        E'\n\nCOMMENT ON VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'm'
                                               THEN format(
                                                        E'\n\nCOMMENT ON MATERIALIZED VIEW %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
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
                      E';\n'||
                      (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                            THEN (CASE relkind WHEN 'r'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'p'
                                               THEN format(
                                                        E'\n\nCOMMENT ON TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               WHEN 'f'
                                               THEN format(
                                                        E'\n\nCOMMENT ON FOREIGN TABLE %s IS %s;',
                                                        '{0}.{1}'::regclass,
                                                        quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                    )
                                               ELSE ''
                                  END)
                            ELSE ''
                       END) as text
                     FROM pg_class c JOIN obj ON (true)
                     LEFT JOIN pg_foreign_table  ft ON (c.oid = ft.ftrelid)
                     LEFT JOIN pg_foreign_server fs ON (ft.ftserver = fs.oid)
                     WHERE c.oid = '{0}.{1}'::regclass
                    -- AND relkind in ('r','c')
                ),
                createsequence as (
                    SELECT 'CREATE SEQUENCE '||(c.oid::regclass::text) || E';\n'
                           ||'ALTER SEQUENCE '||(c.oid::regclass::text)
                           ||E'\n INCREMENT BY '||sp.increment
                           ||E'\n MINVALUE '||sp.minimum_value
                           ||E'\n MAXVALUE '||sp.maximum_value
                           ||E'\n START WITH '||sp.start_value
                           ||E'\n '|| CASE cycle_option WHEN true THEN 'CYCLE' ELSE 'NO CYCLE' END
                           ||E';\n'||
                           (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                 THEN (CASE relkind WHEN 'S'
                                                    THEN format(
                                                             E'\n\nCOMMENT ON SEQUENCE %s IS %s;',
                                                             '{0}.{1}'::regclass,
                                                             quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                         )
                                                    ELSE ''
                                       END)
                                 ELSE ''
                            END) as text
                    FROM pg_class c,
                    LATERAL pg_sequence_parameters(c.oid) sp (start_value, minimum_value, maximum_value, increment, cycle_option)
                    WHERE c.oid = '{0}.{1}'::regclass
                      AND c.relkind = 'S'
                ),
                createindex as (
                    with ii as (
                     SELECT DISTINCT CASE d.refclassid
                                WHEN 'pg_constraint'::regclass
                                THEN 'ALTER TABLE ' || text(c.oid::regclass)
                                     || ' ADD CONSTRAINT ' || quote_ident(cc.conname)
                                     || ' ' || pg_get_constraintdef(cc.oid)
                                ELSE pg_get_indexdef(i.oid) ||
                                     (CASE WHEN obj_description('{0}.{1}'::regclass, 'pg_class') IS NOT NULL
                                           THEN format(
                                                    E'\n\nCOMMENT ON INDEX %s IS %s;',
                                                    '{0}.{1}'::regclass,
                                                    quote_literal(obj_description('{0}.{1}'::regclass, 'pg_class'))
                                                )
                                           ELSE ''
                                      END)
                            END AS indexdef
                       FROM pg_index x
                       JOIN pg_class c ON c.oid = x.indrelid
                       JOIN pg_class i ON i.oid = x.indexrelid
                       JOIN pg_depend d ON d.objid = x.indexrelid
                       LEFT JOIN pg_constraint cc ON cc.oid = d.refobjid
                      WHERE c.relkind in ('r','p','m') AND i.relkind in ('i'::"char", 'I'::"char")
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
                      when obj.kind in ('INDEX', 'PARTITIONED INDEX') then (select text from createindex)
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
                        and generated = ''
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
                         when obj.kind in ('INDEX', 'PARTITIONED INDEX') then ''
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
                ),
                columnsprivileges as (
                    SELECT r.rolname AS grantee,
                           c.name AS column_name,
                           c.privilege_type
                    FROM (
                        SELECT name,
                               (aclexplode(attacl)).grantee AS grantee,
                               (aclexplode(attacl)).privilege_type AS privilege_type
                        FROM columns
                    ) c
                    INNER JOIN pg_roles r
                            ON c.grantee = r.oid
                ),
                columnsgrants as (
                    SELECT coalesce(
                               string_agg(
                                   format(
                                       E'GRANT %s(%s) ON %s TO %s;\n',
                                       privilege_type,
                                       column_name,
                                       '{0}.{1}',
                                       quote_ident(grantee)
                                   ),
                                   ''
                               ),
                               ''
                           ) AS text
                     FROM columnsprivileges
                )
                select (select text from createclass) ||
                       (select text from altertabledefaults) ||
                       (select text from createconstraints) ||
                       (select text from createindexes) ||
                       (select text from createtriggers) ||
                       (select text from createrules) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM columnsgrants)
            '''.format(p_schema, p_object))
    @lock_required
    def GetDDLTrigger(self, p_trigger, p_table, p_schema):
        return self.v_connection.ExecuteScalar('''
            select 'CREATE TRIGGER ' || x.trigger_name || chr(10) ||
                   '  ' || x.action_timing || ' ' || x.event_manipulation || chr(10) ||
                   '  ON {0}.{1}' || chr(10) ||
                   '  FOR EACH ' || x.action_orientation || chr(10) ||
                   (case when length(coalesce(x.action_condition, '')) > 0 then '  WHEN ( ' || x.action_condition || ') ' || chr(10) else '' end) ||
                   '  ' || x.action_statement ||
                   (CASE WHEN obj_description(x.oid, 'pg_trigger') IS NOT NULL
                         THEN format(
                                 E'\n\nCOMMENT ON TRIGGER %s ON %s IS %s;',
                                 quote_ident(x.trigger_name),
                                 quote_ident('{0}.{1}'::regclass::text),
                                 quote_literal(obj_description(x.oid, 'pg_trigger'))
                             )
                         ELSE ''
                    END) as definition
            from (
            select distinct quote_ident(t.trigger_name) as trigger_name,
                   t.action_timing,
                   e.event as event_manipulation,
                   t.action_orientation,
                   t.action_condition,
                   t.action_statement,
                   t2.oid
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
            INNER JOIN (
                select oid
                FROM pg_trigger
                WHERE quote_ident(tgname) = '{2}'
                  AND tgrelid = '{0}.{1}'::regclass
            ) t2
                    ON 1 = 1
            where quote_ident(t.event_object_schema) = '{0}'
              and quote_ident(t.event_object_table) = '{1}'
              and quote_ident(t.trigger_name) = '{2}'
            ) x
        '''.format(p_schema, p_table, p_trigger))
    @lock_required
    def GetDDLEventTrigger(self, p_trigger):
        return self.v_connection.ExecuteScalar('''
            select format(E'CREATE EVENT TRIGGER %s\n  ON %s%s\n  EXECUTE PROCEDURE %s;\n\nALTER EVENT TRIGGER %s OWNER TO %s;\n%s',
                     quote_ident(t.evtname),
                     t.evtevent,
                     (case when t.evttags is not null
                           then E'\n  WHEN TAG IN ( '' || array_to_string(t.evttags, '', '') || '' )'
                           else ''
                      end),
                     quote_ident(np.nspname) || '.' || quote_ident(p.proname) || '()',
                     quote_ident(t.evtname),
                     r.rolname,
                     (CASE WHEN obj_description(t.oid, 'pg_event_trigger') IS NOT NULL
                           THEN format(
                                    E'\nCOMMENT ON EVENT TRIGGER %s IS %s;',
                                    quote_ident(t.evtname),
                                    quote_literal(obj_description(t.oid, 'pg_event_trigger'))
                                )
                           ELSE ''
                      END)
                   )
            from pg_event_trigger t
            inner join pg_proc p
            on p.oid = t.evtfoid
            inner join pg_namespace np
            on np.oid = p.pronamespace
            inner join pg_roles r
            on r.oid = t.evtowner
            where quote_ident(t.evtname) = '{0}'
        '''.format(p_trigger))
    @lock_required
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
                ),
                comments AS (
                    SELECT coalesce(obj_description('{0}'::regprocedure, 'pg_proc'), '') AS description
                ),
                comment_on AS (
                    SELECT (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON FUNCTION %s IS %s;',
                                          '{0}'::regprocedure,
                                          quote_literal(description)
                                      )
                                 ELSE ''
                            END) AS text
                    FROM comments
                )
                select (select text from createfunction) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM comment_on)
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
                ),
                comments AS (
                    SELECT coalesce(obj_description('{0}'::regprocedure, 'pg_proc'), '') AS description
                ),
                comment_on AS (
                    SELECT (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON FUNCTION %s IS %s;',
                                          '{0}'::regprocedure,
                                          quote_literal(description)
                                      )
                                 ELSE ''
                            END) AS text
                    FROM comments
                )
                select (select text from createfunction) ||
                       (select text from alterowner) ||
                       (select text from grants) ||
                       (SELECT text FROM comment_on)
        '''.format(p_function))
    @lock_required
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
            ),
            comments AS (
                SELECT coalesce(obj_description('{0}'::regprocedure, 'pg_proc'), '') AS description
            ),
            comment_on AS (
                SELECT (CASE WHEN description <> ''
                             THEN format(
                                      E'\n\nCOMMENT ON PROCEDURE %s IS %s;',
                                      '{0}'::regprocedure,
                                      quote_literal(description)
                                  )
                             ELSE ''
                        END) AS text
                FROM comments
            )
            select (select text from createfunction) ||
                   (select text from alterowner) ||
                   (select text from grants) ||
                   (SELECT text FROM comment_on)
        '''.format(p_procedure))
    @lock_required
    def GetDDLConstraint(self, p_schema, p_table, p_object):
        return self.v_connection.ExecuteScalar('''
            with cs as (
              select
               'ALTER TABLE ' || text(regclass(c.conrelid)) ||
               ' ADD CONSTRAINT ' || quote_ident(c.conname) ||
               E'\n  ' || pg_get_constraintdef(c.oid, true) as sql,
               c.oid,
               c.conname,
               c.conrelid
                from pg_constraint c
               join pg_class t
               on t.oid = c.conrelid
               join pg_namespace n
               on t.relnamespace = n.oid
               where quote_ident(n.nspname) = '{0}'
                 and quote_ident(t.relname) = '{1}'
                 and quote_ident(c.conname) = '{2}'
            ),
            comments AS (
                SELECT format(
                           E'\n\nCOMMENT ON CONSTRAINT %s ON %s is %s;',
                           conname,
                           conrelid::regclass,
                           quote_literal(x.description)
                       ) AS sql
                FROM (
                    SELECT oid,
                           conname,
                           conrelid,
                           obj_description(oid, 'pg_constraint') AS description
                    FROM cs
                ) x
                WHERE x.description IS NOT NULL
            )
            select format(
                       E'%s%s',
                       coalesce(string_agg(cs.sql,E';\n') || E';\n\n',''),
                       coalesce(c.sql, '')
                   ) as text
            from cs cs
            LEFT JOIN comments c
                   ON 1 = 1
            GROUP BY cs.sql,
                     c.sql
        '''.format(p_schema, p_table, p_object))
    @lock_required
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
    @lock_required
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
            select format(E'CREATE SERVER %s%s%s\n  FOREIGN DATA WRAPPER %s%s;\n\nALTER SERVER %s OWNER TO %s;\n\n%s%s',
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
                     g.text,
                     (CASE WHEN obj_description(s.oid, 'pg_foreign_server') IS NOT NULL
                           THEN format(
                                   E'\nCOMMENT ON SERVER %s IS %s;',
                                   quote_ident(s.srvname),
                                   quote_literal(obj_description(s.oid, 'pg_foreign_server'))
                               )
                           ELSE ''
                      END)
                   )
            from pg_foreign_server s
            inner join pg_foreign_data_wrapper w
            on w.oid = s.srvfdw
            inner join pg_roles r
            on r.oid = s.srvowner
            inner join grants g on 1=1
            where quote_ident(s.srvname) = '{0}'
        '''.format(p_object))
    @lock_required
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
            select format(E'CREATE FOREIGN DATA WRAPPER %s%s%s%s;\n\nALTER FOREIGN DATA WRAPPER %s OWNER TO %s;\n\n%s%s',
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
                     g.text,
                     (CASE WHEN obj_description(w.oid, 'pg_foreign_data_wrapper') IS NOT NULL
                           THEN format(
                                    E'\n\nCOMMENT ON FOREIGN DATA WRAPPER %s IS %s;',
                                    quote_ident(w.fdwname),
                                    quote_literal(obj_description(w.oid, 'pg_foreign_data_wrapper'))
                                )
                           ELSE ''
                      END)
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
    @lock_required
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
                           E'CREATE TYPE %s.%s AS ENUM (\n%s\n);\n\nALTER TYPE %s.%s OWNER TO %s;\n%s',
                           quote_ident(n.nspname),
                           quote_ident(t.typname),
                           string_agg(format('    ' || chr(39) || '%s' || chr(39), e.enumlabel), E',\n'),
                           quote_ident(n.nspname),
                           quote_ident(t.typname),
                           quote_ident(r.rolname),
                           (CASE WHEN obj_description(t.oid, 'pg_type') IS NOT NULL
                                 THEN format(
                                         E'\n\nCOMMENT ON TYPE %s IS %s;',
                                         quote_ident(t.oid::regtype::text),
                                         quote_literal(obj_description(t.oid, 'pg_type'))
                                     )
                                 ELSE ''
                            END)
                       )
                from pg_type t
                inner join pg_namespace n on n.oid = t.typnamespace
                inner join pg_enum e on e.enumtypid = t.oid
                inner join pg_roles r on r.oid = t.typowner
                where quote_ident(n.nspname) = '{0}'
                  and quote_ident(t.typname) = '{1}'
                group by n.nspname,
                         t.typname,
                         r.rolname,
                         t.oid
            '''.format(p_schema, p_object))
        elif v_type == 'r':
            return self.v_connection.ExecuteScalar('''
                select format(
                         E'CREATE TYPE %s.%s AS RANGE (\n  SUBTYPE = %s.%s\n%s%s%s%s);\n\nALTER TYPE %s.%s OWNER TO %s;\n%s',
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
                         quote_ident(ro.rolname),
                         (CASE WHEN obj_description(t.oid, 'pg_type') IS NOT NULL
                               THEN format(
                                       E'\n\nCOMMENT ON TYPE %s IS %s;',
                                       quote_ident(t.oid::regtype::text),
                                       quote_literal(obj_description(t.oid, 'pg_type'))
                                   )
                               ELSE ''
                          END)
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
                         E'CREATE TYPE %s (\n  INPUT = %s,\n  , OUTPUT = %s\n%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s);\n\nALTER TYPE %s OWNER TO %s;\n%s',
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
                         quote_ident(r.rolname),
                         (CASE WHEN obj_description(t.oid, 'pg_type') IS NOT NULL
                               THEN format(
                                       E'\n\nCOMMENT ON TYPE %s IS %s;',
                                       quote_ident(t.oid::regtype::text),
                                       quote_literal(obj_description(t.oid, 'pg_type'))
                                   )
                               ELSE ''
                          END)
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
    @lock_required
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
            comments AS (
                SELECT obj_description('{0}.{1}'::regtype, 'pg_type') AS description
            ),
            create_domain as (
                select format(
                         E'CREATE DOMAIN %s\n  AS %s\n%s%s%s\n', d.name, d.basetype,
                         (case when d.collation is not null then format(E'  COLLATE %s', d.collation) else '' end),
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
            ),
            comment_on AS (
                SELECT format(
                           E'\n\COMMENT ON DOMAIN {0}.{1} IS %s',
                           quote_literal(description)
                       ) AS sql
                FROM comments
                WHERE description IS NOT NULL
            )
            select format(E'%s%s;\n\n%s%s',
                     (select sql from create_domain),
                     (select substring(sql from 1 for length(sql)-1) from create_constraints),
                     (select sql from alter_domain),
                     (SELECT sql FROM comment_on)
                   )
        '''.format(p_schema, p_object))

    @lock_required
    def GetDDLPublication(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return self.v_connection.ExecuteScalar("""
                WITH publication AS (
                    SELECT oid,
                           pubname,
                           pubowner,
                           puballtables,
                           pubinsert,
                           pubupdate,
                           pubdelete,
                           pubtruncate
                    FROM pg_publication
                    WHERE quote_ident(pubname) = '{0}'
                ),
                tables AS (
                    SELECT string_agg(x.pubtable, ', ' ORDER BY x.pubtable) AS pubtables
                    FROM (
                        SELECT format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(c.relname)
                               )::regclass::text AS pubtable
                        FROM publication p
                        INNER JOIN pg_publication_rel pr
                                ON p.oid = pr.prpubid
                        INNER JOIN pg_class c
                                ON pr.prrelid = c.oid
                        INNER JOIN pg_namespace n
                                ON c.relnamespace = n.oid
                    ) x
                ),
                for_tables AS (
                    SELECT (CASE WHEN puballtables
                                 THEN E'  FOR ALL TABLES\n'
                                 WHEN coalesce(t.pubtables, '') <> ''
                                 THEN format(E'  FOR TABLES %s\n', t.pubtables)
                                 ELSE E''
                            END) AS text
                    FROM publication p
                    LEFT JOIN tables t
                           ON 1 = 1
                ),
                options AS (
                    SELECT (CASE WHEN z.puboptions <> ''
                                 THEN format(E'  WITH ( %s )', z.puboptions)
                                 ELSE ''
                            END) AS text
                    FROM (
                        SELECT string_agg(y.puboption, ', ') AS puboptions
                        FROM (
                            SELECT format('publish = ''%s''', x.publish) AS puboption
                            FROM (
                                SELECT array_to_string(
                                           array[
                                               (CASE WHEN pubinsert THEN 'insert' ELSE NULL END),
                                               (CASE WHEN pubupdate THEN 'update' ELSE NULL END),
                                               (CASE WHEN pubdelete THEN 'delete' ELSE NULL END),
                                               (CASE WHEN pubtruncate THEN 'truncate' ELSE NULL END)
                                           ]::text[],
                                           ', '
                                        ) AS publish
                                FROM publication
                            ) x
                            WHERE x.publish <> ''
                        ) y
                    ) z
                ),
                comments AS (
                    SELECT coalesce(obj_description(oid, 'pg_publication'), '') AS description,
                           pubname
                    FROM publication
                ),
                comment_on AS (
                    SELECT (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON PUBLICATION %s IS %s;',
                                          quote_ident(pubname),
                                          quote_literal(description)
                                      )
                                 ELSE ''
                            END) AS text
                    FROM comments
                )
                SELECT format(E'CREATE PUBLICATION %s\n%s%s;\n\nALTER PUBLICATION %s OWNER TO %s;%s',
                         quote_ident(p.pubname),
                         ft.text,
                         o.text,
                         quote_ident(p.pubname),
                         quote_ident(r.rolname),
                         c.text
                       )
                FROM publication p
                INNER JOIN pg_roles r
                        ON r.oid = p.pubowner
                INNER JOIN for_tables ft
                        ON 1 = 1
                INNER JOIN options o
                        ON 1 = 1
                INNER JOIN comment_on c
                        ON 1 = 1
            """.format(p_object))
        else:
            return self.v_connection.ExecuteScalar("""
                WITH publication AS (
                    SELECT oid,
                           pubname,
                           pubowner,
                           puballtables,
                           pubinsert,
                           pubupdate,
                           pubdelete,
                           pubtruncate,
                           pubviaroot
                    FROM pg_publication
                    WHERE quote_ident(pubname) = '{0}'
                ),
                tables AS (
                    SELECT string_agg(x.pubtable, ', ' ORDER BY x.pubtable) AS pubtables
                    FROM (
                        SELECT format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(c.relname)
                               )::regclass::text AS pubtable
                        FROM publication p
                        INNER JOIN pg_publication_rel pr
                                ON p.oid = pr.prpubid
                        INNER JOIN pg_class c
                                ON pr.prrelid = c.oid
                        INNER JOIN pg_namespace n
                                ON c.relnamespace = n.oid
                    ) x
                ),
                for_tables AS (
                    SELECT (CASE WHEN puballtables
                                 THEN E'  FOR ALL TABLES\n'
                                 WHEN coalesce(t.pubtables, '') <> ''
                                 THEN format(E'  FOR TABLES %s\n', t.pubtables)
                                 ELSE E''
                            END) AS text
                    FROM publication p
                    LEFT JOIN tables t
                           ON 1 = 1
                ),
                options AS (
                    SELECT (CASE WHEN z.puboptions <> ''
                                 THEN format(E'  WITH ( %s )', z.puboptions)
                                 ELSE ''
                            END) AS text
                    FROM (
                        SELECT string_agg(y.puboption, ', ') AS puboptions
                        FROM (
                            SELECT format('publish = ''%s''', x.publish) AS puboption
                            FROM (
                                SELECT array_to_string(
                                           array[
                                               (CASE WHEN pubinsert THEN 'insert' ELSE NULL END),
                                               (CASE WHEN pubupdate THEN 'update' ELSE NULL END),
                                               (CASE WHEN pubdelete THEN 'delete' ELSE NULL END),
                                               (CASE WHEN pubtruncate THEN 'truncate' ELSE NULL END)
                                           ]::text[],
                                           ', '
                                        ) AS publish
                                FROM publication
                            ) x
                            WHERE x.publish <> ''

                            UNION ALL

                            SELECT format('publish_via_partition_root = %s', pubviaroot::text) AS puboption
                            FROM publication
                        ) y
                    ) z
                ),
                comments AS (
                    SELECT coalesce(obj_description(oid, 'pg_publication'), '') AS description,
                           pubname
                    FROM publication
                ),
                comment_on AS (
                    SELECT (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON PUBLICATION %s IS %s;',
                                          quote_ident(pubname),
                                          quote_literal(description)
                                      )
                                 ELSE ''
                            END) AS text
                    FROM comments
                )
                SELECT format(E'CREATE PUBLICATION %s\n%s%s;\n\nALTER PUBLICATION %s OWNER TO %s;%s',
                         quote_ident(p.pubname),
                         ft.text,
                         o.text,
                         quote_ident(p.pubname),
                         quote_ident(r.rolname),
                         c.text
                       )
                FROM publication p
                INNER JOIN pg_roles r
                        ON r.oid = p.pubowner
                INNER JOIN for_tables ft
                        ON 1 = 1
                INNER JOIN options o
                        ON 1 = 1
                INNER JOIN comment_on c
                        ON 1 = 1
            """.format(p_object))

    @lock_required
    def GetDDLSubscription(self, p_object):
        return self.v_connection.ExecuteScalar("""
            WITH subscription AS (
                SELECT oid,
                       subname,
                       subowner,
                       subenabled,
                       subconninfo,
                       subslotname,
                       subsynccommit,
                       subpublications
                FROM pg_subscription
                WHERE quote_ident(subname) = '{0}'
            ),
            options AS (
                SELECT (CASE WHEN z.suboptions <> ''
                             THEN format(E'  WITH ( %s )', z.suboptions)
                             ELSE ''
                        END) AS text
                FROM (
                    SELECT array_to_string(y.suboption, ', ') AS suboptions
                    FROM (
                        SELECT array[
                                   format('enabled = %s', subenabled::text),
                                   format('slot_name = ''%s''', subslotname),
                                   format('synchronous_commit = ''%s''', subsynccommit)
                               ]::text[] AS suboption
                        FROM subscription
                    ) y
                ) z
            ),
            comments AS (
                SELECT coalesce(obj_description(oid, 'pg_subscription'), '') AS description,
                       subname
                FROM subscription
            ),
            comment_on AS (
                SELECT (CASE WHEN description <> ''
                             THEN format(
                                      E'\n\nCOMMENT ON SUBSCRIPTION %s IS %s;',
                                      quote_ident(subname),
                                      quote_literal(description)
                                  )
                             ELSE ''
                        END) AS text
                FROM comments
            )
            SELECT format(E'CREATE SUBSCRIPTION %s\n  CONNECTION ''%s''\n  PUBLICATION %s\n%s;\n\nALTER SUBSCRIPTION %s OWNER TO %s;%s',
                     quote_ident(s.subname),
                     s.subconninfo,
                     array_to_string(s.subpublications, ', '),
                     o.text,
                     quote_ident(s.subname),
                     quote_ident(r.rolname),
                     c.text
                   )
            FROM subscription s
            INNER JOIN pg_roles r
                    ON r.oid = s.subowner
            INNER JOIN options o
                    ON 1 = 1
            INNER JOIN comment_on c
                    ON 1 = 1
        """.format(p_object))

    @lock_required
    def GetDDLStatistic(self, p_schema, p_object):
        return self.v_connection.ExecuteScalar(
            """
                WITH statistics AS (
                    SELECT x.oid,
                           x.statistics_schema,
                           x.stxname,
                           x.table_schema,
                           x.table_name,
                           x.stxowner,
                           x.stxkind,
                           array_agg(x.attname) AS columns
                    FROM (
                        SELECT se.oid,
                               n2.nspname AS statistics_schema,
                               se.stxname,
                               n.nspname AS table_schema,
                               c.relname AS table_name,
                               se.stxowner,
                               se.stxkind,
                               a.attname
                        FROM pg_statistic_ext se
                        INNER JOIN pg_class c
                                ON se.stxrelid = c.oid
                        INNER JOIN pg_namespace n
                                ON c.relnamespace = n.oid
                        INNER JOIN pg_attribute a
                                ON c.oid = a.attrelid
                               AND a.attnum = ANY(se.stxkeys)
                        INNER JOIN pg_namespace n2
                                ON se.stxnamespace = n2.oid
                    ) x
                    WHERE quote_ident(x.statistics_schema) = '{0}'
                      AND quote_ident(x.stxname) = '{1}'
                    GROUP BY x.oid,
                             x.statistics_schema,
                             x.stxname,
                             x.table_schema,
                             x.table_name,
                             x.stxowner,
                             x.stxkind
                ),
                options AS (
                    SELECT format(
                               E'  ( %s )\n',
                               string_agg(y.kind, ', ')
                           ) AS text
                    FROM (
                        SELECT (CASE kind WHEN 'd'
                                          THEN 'dependencies'
                                          WHEN 'f'
                                          THEN 'ndistinct'
                                          WHEN 'm'
                                          THEN 'mcv'
                                END) AS kind
                        FROM (
                            SELECT unnest(stxkind) AS kind
                            FROM statistics
                        ) x
                    ) y
                ),
                comments AS (
                    SELECT coalesce(obj_description(oid, 'pg_statistic_ext'), '') AS description,
                           stxname,
                           statistics_schema
                    FROM statistics
                ),
                comment_on AS (
                    SELECT (CASE WHEN description <> ''
                                 THEN format(
                                          E'\n\nCOMMENT ON STATISTICS %s.%s IS %s;',
                                          quote_ident(statistics_schema),
                                          quote_ident(stxname),
                                          quote_literal(description)
                                      )
                                 ELSE ''
                            END) AS text
                    FROM comments
                )
                SELECT format(
                           E'CREATE STATISTICS %s\n%s  ON %s\n  FROM %s;\n\nALTER STATISTICS %s OWNER TO %s;%s',
                           format(
                               '%s.%s',
                               quote_ident(s.statistics_schema),
                               quote_ident(s.stxname)
                           ),
                           o.text,
                           array_to_string(s.columns, ', '),
                           format(
                               '%s.%s',
                               quote_ident(s.table_schema),
                               quote_ident(s.table_name)
                           )::regclass::text,
                           format(
                               '%s.%s',
                               quote_ident(s.statistics_schema),
                               quote_ident(s.stxname)
                           ),
                           quote_ident(r.rolname),
                           c.text
                       )
                FROM statistics s
                INNER JOIN pg_roles r
                        ON r.oid = s.stxowner
                INNER JOIN options o
                        ON 1 = 1
                INNER JOIN comment_on c
                        ON 1 = 1
            """.format(
                p_schema,
                p_object
            )
        )

    @lock_required
    def GetDDLAggregate(self, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 90600:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(p.proname)
                               ) AS function_full_name,
                               r.rolname AS function_owner,
                               p.proisagg AS is_aggregate
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(t.typname)
                               )::regtype AS type_full_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    ),
                    privileges AS (
                        SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                               (grantee.rolname)::information_schema.sql_identifier AS grantee,
                               (p.privilege_type)::information_schema.character_data AS privilege_type,
                               (CASE WHEN (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) OR p.is_grantable)
                                     THEN 'YES'::text
                                     ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS is_grantable
                        FROM (
                            SELECT p.pronamespace,
                                   p.proowner,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor AS grantor,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee AS grantee,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type AS privilege_type,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable AS is_grantable
                            FROM pg_proc p
                            WHERE p.proisagg
                              AND p.oid = '{0}'::regprocedure
                        ) p
                        INNER JOIN pg_namespace n
                                ON n.oid = p.pronamespace
                        INNER JOIN pg_roles u_grantor
                                ON u_grantor.oid = p.grantor
                        INNER JOIN (
                            SELECT r.oid,
                                   r.rolname
                            FROM pg_roles r

                            UNION ALL

                            SELECT (0)::oid AS oid,
                                   'PUBLIC'::name
                        ) grantee
                                ON grantee.oid = p.grantee
                    ),
                    grants AS (
                        SELECT coalesce(
                                   string_agg(
                                       format(
                        	               E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                                           privilege_type,
                                           (CASE grantee WHEN 'PUBLIC'
                                                         THEN 'PUBLIC'
                                                         ELSE quote_ident(grantee)
                                            END),
                        	               (CASE is_grantable WHEN 'YES'
                        	                                  THEN ' WITH GRANT OPTION'
                        	                                  ELSE ''
                                            END)
                                        ),
                                        ''
                                   ),
                                   ''
                               ) AS text
                        FROM privileges
                    ),
                    comments AS (
                        SELECT format(
                            E'\nCOMMENT ON AGGREGATE {0} is %s;',
                            quote_literal(x.description)
                        ) AS text
                        FROM (
                            SELECT obj_description ('{0}'::regprocedure, 'pg_proc') AS description
                        ) x
                        WHERE x.description IS NOT NULL
                    )
                    SELECT format(
                               E'CREATE AGGREGATE %s (\n\tSFUNC = %s\n  , STYPE = %s%s%s%s%s%s%s%s%s%s%s%s%s\n);\n\nALTER AGGREGATE %s OWNER TO %s;\n\n%s%s',
                               p1.function_id,
                               p2.function_full_name,
                               t1.type_full_name,
                               (CASE WHEN a.aggtransspace <> 0
                                     THEN format(E'\n  , SSPACE = %s', a.aggtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p3.function_id IS NOT NULL
                                     THEN format(E'\n  , FINALFUNC = %s', p3.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggfinalextra
                                     THEN E'\n  , FINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               (CASE WHEN a.agginitval IS NOT NULL
                                     THEN format(E'\n  , INITCOND = %s', a.agginitval)
                                     ELSE ''
                                END),
                               (CASE WHEN p7.function_id IS NOT NULL
                                     THEN format(E'\n  , MSFUNC = %s', p7.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p8.function_id IS NOT NULL
                                     THEN format(E'\n  , MINVFUNC = %s', p8.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN t2.type_oid IS NOT NULL
                                     THEN format(E'\n  , MSTYPE = %s', t2.type_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN a.aggmtransspace <> 0
                                     THEN format(E'\n  , MSSPACE = %s', a.aggmtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p9.function_id IS NOT NULL
                                     THEN format(E'\n  , MFINALFUNC = %s', p9.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggmfinalextra
                                     THEN E'\n  , MFINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               (CASE WHEN a.aggminitval IS NOT NULL
                                     THEN format(E'\n  , MINITCOND = %s', a.aggminitval)
                                     ELSE ''
                                END),
                               (CASE WHEN o.operator_oid IS NOT NULL
                                     THEN format(E'\n  , SORTOP = %s', o.operator_oid::regoperator)
                                     ELSE ''
                                END),
                               p1.function_id,
                               p1.function_owner,
                               g.text,
                               c.text
                           )
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    INNER JOIN grants g
                            ON 1 = 1
                    LEFT JOIN comments c
                           ON 1 = 1
                    WHERE p1.is_aggregate
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 110000:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(p.proname)
                               ) AS function_full_name,
                               r.rolname AS function_owner,
                               p.proisagg AS is_aggregate,
                               p.proparallel
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(t.typname)
                               )::regtype AS type_full_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    ),
                    privileges AS (
                        SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                               (grantee.rolname)::information_schema.sql_identifier AS grantee,
                               (p.privilege_type)::information_schema.character_data AS privilege_type,
                               (CASE WHEN (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) OR p.is_grantable)
                                     THEN 'YES'::text
                                     ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS is_grantable
                        FROM (
                            SELECT p.pronamespace,
                                   p.proowner,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor AS grantor,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee AS grantee,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type AS privilege_type,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable AS is_grantable
                            FROM pg_proc p
                            WHERE p.proisagg
                              AND p.oid = '{0}'::regprocedure
                        ) p
                        INNER JOIN pg_namespace n
                                ON n.oid = p.pronamespace
                        INNER JOIN pg_roles u_grantor
                                ON u_grantor.oid = p.grantor
                        INNER JOIN (
                            SELECT r.oid,
                                   r.rolname
                            FROM pg_roles r

                            UNION ALL

                            SELECT (0)::oid AS oid,
                                   'PUBLIC'::name
                        ) grantee
                                ON grantee.oid = p.grantee
                    ),
                    grants AS (
                        SELECT coalesce(
                                   string_agg(
                                       format(
                        	               E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                                           privilege_type,
                                           (CASE grantee WHEN 'PUBLIC'
                                                         THEN 'PUBLIC'
                                                         ELSE quote_ident(grantee)
                                            END),
                        	               (CASE is_grantable WHEN 'YES'
                        	                                  THEN ' WITH GRANT OPTION'
                        	                                  ELSE ''
                                            END)
                                        ),
                                        ''
                                   ),
                                   ''
                               ) AS text
                        FROM privileges
                    ),
                    comments AS (
                        SELECT format(
                            E'\nCOMMENT ON AGGREGATE {0} is %s;',
                            quote_literal(x.description)
                        ) AS text
                        FROM (
                            SELECT obj_description ('{0}'::regprocedure, 'pg_proc') AS description
                        ) x
                        WHERE x.description IS NOT NULL
                    )
                    SELECT format(
                               E'CREATE AGGREGATE %s (\n\tSFUNC = %s\n  , STYPE = %s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n);\n\nALTER AGGREGATE %s OWNER TO %s;\n\n%s%s',
                               p1.function_id,
                               p2.function_full_name,
                               t1.type_full_name,
                               (CASE WHEN a.aggtransspace <> 0
                                     THEN format(E'\n  , SSPACE = %s', a.aggtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p3.function_id IS NOT NULL
                                     THEN format(E'\n  , FINALFUNC = %s', p3.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggfinalextra
                                     THEN E'\n  , FINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               (CASE WHEN p4.function_id IS NOT NULL
                                     THEN format(E'\n  , COMBINEFUNC = %s', p4.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p5.function_id IS NOT NULL
                                     THEN format(E'\n  , SERIALFUNC = %s', p5.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p6.function_id IS NOT NULL
                                     THEN format(E'\n  , DESERIALFUNC = %s', p6.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN a.agginitval IS NOT NULL
                                     THEN format(E'\n  , INITCOND = %s', a.agginitval)
                                     ELSE ''
                                END),
                               (CASE WHEN p7.function_id IS NOT NULL
                                     THEN format(E'\n  , MSFUNC = %s', p7.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p8.function_id IS NOT NULL
                                     THEN format(E'\n  , MINVFUNC = %s', p8.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN t2.type_oid IS NOT NULL
                                     THEN format(E'\n  , MSTYPE = %s', t2.type_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN a.aggmtransspace <> 0
                                     THEN format(E'\n  , MSSPACE = %s', a.aggmtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p9.function_id IS NOT NULL
                                     THEN format(E'\n  , MFINALFUNC = %s', p9.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggmfinalextra
                                     THEN E'\n  , MFINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               (CASE WHEN a.aggminitval IS NOT NULL
                                     THEN format(E'\n  , MINITCOND = %s', a.aggminitval)
                                     ELSE ''
                                END),
                               (CASE WHEN o.operator_oid IS NOT NULL
                                     THEN format(E'\n  , SORTOP = %s', o.operator_oid::regoperator)
                                     ELSE ''
                                END),
                               format(
                                   E'\n  , PARALLEL = %s',
                                   (CASE p1.proparallel WHEN 's'
                                                        THEN 'SAFE'
                                                        WHEN 'r'
                                                        THEN 'RESTRICTED'
                                                        WHEN 'u'
                                                        THEN 'UNSAFE'
                                    END)
                               ),
                               p1.function_id,
                               p1.function_owner,
                               g.text,
                               c.text
                           )
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p4
                           ON a.aggcombinefn = p4.function_oid
                    LEFT JOIN procs p5
                           ON a.aggserialfn = p5.function_oid
                    LEFT JOIN procs p6
                           ON a.aggdeserialfn = p6.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    INNER JOIN grants g
                            ON 1 = 1
                    LEFT JOIN comments c
                           ON 1 = 1
                    WHERE p1.is_aggregate
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )
        else:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH procs AS (
                        SELECT p.oid AS function_oid,
                               quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || oidvectortypes(p.proargtypes) || ')' AS function_id,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(p.proname) AS function_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(p.proname)
                               ) AS function_full_name,
                               r.rolname AS function_owner,
                               p.prokind AS function_kind,
                               p.proparallel
                        FROM pg_proc p
                        INNER JOIN pg_namespace n
                                ON p.pronamespace = n.oid
                        INNER JOIN pg_roles r
                                ON p.proowner = r.oid
                    ),
                    operators AS (
                        SELECT o.oid AS operator_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(o.oprname) AS operator_name
                        FROM pg_operator o
                        INNER JOIN pg_namespace n
                                ON o.oprnamespace = n.oid
                    ),
                    types AS (
                        SELECT t.oid AS type_oid,
                               quote_ident(n.nspname) AS schema_name,
                               quote_ident(t.typname) AS type_name,
                               format(
                                   '%s.%s',
                                   quote_ident(n.nspname),
                                   quote_ident(t.typname)
                               )::regtype AS type_full_name
                        FROM pg_type t
                        INNER JOIN pg_namespace n
                                ON t.typnamespace = n.oid
                    ),
                    privileges AS (
                        SELECT (u_grantor.rolname)::information_schema.sql_identifier AS grantor,
                               (grantee.rolname)::information_schema.sql_identifier AS grantee,
                               (p.privilege_type)::information_schema.character_data AS privilege_type,
                               (CASE WHEN (pg_has_role(grantee.oid, p.proowner, 'USAGE'::text) OR p.is_grantable)
                                     THEN 'YES'::text
                                     ELSE 'NO'::text
                                END)::information_schema.yes_or_no AS is_grantable
                        FROM (
                            SELECT p.pronamespace,
                                   p.proowner,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantor AS grantor,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).grantee AS grantee,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).privilege_type AS privilege_type,
                                   (aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner)))).is_grantable AS is_grantable
                            FROM pg_proc p
                            WHERE p.prokind = 'a'
                              AND p.oid = '{0}'::regprocedure
                        ) p
                        INNER JOIN pg_namespace n
                                ON n.oid = p.pronamespace
                        INNER JOIN pg_roles u_grantor
                                ON u_grantor.oid = p.grantor
                        INNER JOIN (
                            SELECT r.oid,
                                   r.rolname
                            FROM pg_roles r

                            UNION ALL

                            SELECT (0)::oid AS oid,
                                   'PUBLIC'::name
                        ) grantee
                                ON grantee.oid = p.grantee
                    ),
                    grants AS (
                        SELECT coalesce(
                                   string_agg(
                                       format(
                        	               E'GRANT %s ON FUNCTION {0} TO %s%s;\n',
                                           privilege_type,
                                           (CASE grantee WHEN 'PUBLIC'
                                                         THEN 'PUBLIC'
                                                         ELSE quote_ident(grantee)
                                            END),
                        	               (CASE is_grantable WHEN 'YES'
                        	                                  THEN ' WITH GRANT OPTION'
                        	                                  ELSE ''
                                            END)
                                        ),
                                        ''
                                   ),
                                   ''
                               ) AS text
                        FROM privileges
                    ),
                    comments AS (
                        SELECT format(
                            E'\nCOMMENT ON AGGREGATE {0} is %s;',
                            quote_literal(x.description)
                        ) AS text
                        FROM (
                            SELECT obj_description ('{0}'::regprocedure, 'pg_proc') AS description
                        ) x
                        WHERE x.description IS NOT NULL
                    )
                    SELECT format(
                               E'CREATE AGGREGATE %s (\n\tSFUNC = %s\n  , STYPE = %s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n);\n\nALTER AGGREGATE %s OWNER TO %s;\n\n%s%s',
                               p1.function_id,
                               p2.function_full_name,
                               t1.type_full_name,
                               (CASE WHEN a.aggtransspace <> 0
                                     THEN format(E'\n  , SSPACE = %s', a.aggtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p3.function_id IS NOT NULL
                                     THEN format(E'\n  , FINALFUNC = %s', p3.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggfinalextra
                                     THEN E'\n  , FINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               format(
                                   E'\n  , FINALFUNC_MODIFY = %s',
                                   (CASE aggfinalmodify WHEN 'r'
                                                        THEN 'READ_ONLY'
                                                        WHEN 's'
                                                        THEN 'SHAREABLE'
                                                        WHEN 'w'
                                                        THEN 'READ_WRITE'
                                    END)
                               ),
                               (CASE WHEN p4.function_id IS NOT NULL
                                     THEN format(E'\n  , COMBINEFUNC = %s', p4.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p5.function_id IS NOT NULL
                                     THEN format(E'\n  , SERIALFUNC = %s', p5.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p6.function_id IS NOT NULL
                                     THEN format(E'\n  , DESERIALFUNC = %s', p6.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN a.agginitval IS NOT NULL
                                     THEN format(E'\n  , INITCOND = %s', a.agginitval)
                                     ELSE ''
                                END),
                               (CASE WHEN p7.function_id IS NOT NULL
                                     THEN format(E'\n  , MSFUNC = %s', p7.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN p8.function_id IS NOT NULL
                                     THEN format(E'\n  , MINVFUNC = %s', p8.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN t2.type_oid IS NOT NULL
                                     THEN format(E'\n  , MSTYPE = %s', t2.type_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN a.aggmtransspace <> 0
                                     THEN format(E'\n  , MSSPACE = %s', a.aggmtransspace)
                                     ELSE ''
                                END),
                               (CASE WHEN p9.function_id IS NOT NULL
                                     THEN format(E'\n  , MFINALFUNC = %s', p9.function_full_name)
                                     ELSE ''
                                END),
                               (CASE WHEN aggmfinalextra
                                     THEN E'\n  , MFINALFUNC_EXTRA'
                                     ELSE ''
                                END),
                               format(
                                   E'\n  , MFINALFUNC_MODIFY = %s',
                                   (CASE aggmfinalmodify WHEN 'r'
                                                         THEN 'READ_ONLY'
                                                         WHEN 's'
                                                         THEN 'SHAREABLE'
                                                         WHEN 'w'
                                                         THEN 'READ_WRITE'
                                    END)
                               ),
                               (CASE WHEN a.aggminitval IS NOT NULL
                                     THEN format(E'\n  , MINITCOND = %s', a.aggminitval)
                                     ELSE ''
                                END),
                               (CASE WHEN o.operator_oid IS NOT NULL
                                     THEN format(E'\n  , SORTOP = %s', o.operator_oid::regoperator)
                                     ELSE ''
                                END),
                               format(
                                   E'\n  , PARALLEL = %s',
                                   (CASE p1.proparallel WHEN 's'
                                                        THEN 'SAFE'
                                                        WHEN 'r'
                                                        THEN 'RESTRICTED'
                                                        WHEN 'u'
                                                        THEN 'UNSAFE'
                                    END)
                               ),
                               p1.function_id,
                               p1.function_owner,
                               g.text,
                               c.text
                           )
                    FROM pg_aggregate a
                    INNER JOIN procs p1
                            ON a.aggfnoid = p1.function_oid
                    LEFT JOIN procs p2
                           ON a.aggtransfn = p2.function_oid
                    LEFT JOIN procs p3
                           ON a.aggfinalfn = p3.function_oid
                    LEFT JOIN procs p4
                           ON a.aggcombinefn = p4.function_oid
                    LEFT JOIN procs p5
                           ON a.aggserialfn = p5.function_oid
                    LEFT JOIN procs p6
                           ON a.aggdeserialfn = p6.function_oid
                    LEFT JOIN procs p7
                           ON a.aggmtransfn = p7.function_oid
                    LEFT JOIN procs p8
                           ON a.aggminvtransfn = p8.function_oid
                    LEFT JOIN procs p9
                           ON a.aggmfinalfn = p9.function_oid
                    LEFT JOIN operators o
                           ON a.aggsortop = o.operator_oid
                    LEFT JOIN types t1
                           ON a.aggtranstype = t1.type_oid
                    LEFT JOIN types t2
                           ON a.aggmtranstype = t2.type_oid
                    INNER JOIN grants g
                            ON 1 = 1
                    LEFT JOIN comments c
                           ON 1 = 1
                    WHERE p1.function_kind = 'a'
                      AND p1.function_id = '{0}'
                '''.format(
                    p_object
                )
            )

    @lock_required
    def GetDDLTableField(self, p_schema, p_table, p_object):
        if int(self.v_connection.ExecuteScalar('show server_version_num')) < 100000:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH columns AS (
                        SELECT format(
                                   '%I %s%s%s',
                                   a.attname::text,
                                   format_type(t.oid, a.atttypmod),
                                   (CASE WHEN length(col.collcollate) > 0
                                         THEN ' COLLATE ' || quote_ident(col.collcollate::text)
                                         ELSE ''
                                    END),
                                   (CASE WHEN a.attnotnull
                                         THEN ' NOT NULL'::text
                                         ELSE ''::text
                                    END)
                               ) AS definition,
                               a.attname AS name,
                               col_description(c.oid, a.attnum::integer) AS comment,
                               pg_get_expr(def.adbin, def.adrelid) AS default_value,
                               a.attacl
                        FROM pg_class c
                        INNER JOIN pg_namespace s
                                ON s.oid = c.relnamespace
                        INNER JOIN pg_attribute a
                                ON c.oid = a.attrelid
                        LEFT JOIN pg_attrdef def
                               ON c.oid = def.adrelid
                              AND a.attnum = def.adnum
                        LEFT JOIN pg_constraint con
                               ON con.conrelid = c.oid
                              AND (a.attnum = ANY (con.conkey))
                              AND con.contype = 'p'
                        LEFT JOIN pg_type t
                               ON t.oid = a.atttypid
                        LEFT JOIN pg_collation col
                               ON col.oid = a.attcollation
                        INNER JOIN pg_namespace tn
                                ON tn.oid = t.typnamespace
                        WHERE c.relkind IN ('r', 'p')
                          AND a.attnum > 0
                          AND NOT a.attisdropped
                          AND has_table_privilege(c.oid, 'select')
                          AND has_schema_privilege(s.oid, 'usage')
                          AND c.oid = '{0}.{1}'::regclass
                          AND a.attname = '{2}'
                    ),
                    comments AS (
                        SELECT format(
                                   E'\n\nCOMMENT ON COLUMN %s.%s IS %s;',
                                   '{0}.{1}',
                                   quote_ident(name),
                                   quote_nullable(comment)
                               ) AS definition
                        FROM columns
                        WHERE comment IS NOT NULL
                    ),
                    defaults AS (
                        SELECT format(
                                   E'\n\nALTER TABLE %s\n\tALTER %s SET DEFAULT %s;',
                                   '{0}.{1}'::regclass,
                                   quote_ident(name),
                                   default_value
                               ) AS definition
                        FROM columns
                        WHERE default_value IS NOT NULL
                    ),
                    columnsprivileges as (
                        SELECT r.rolname AS grantee,
                               c.name AS column_name,
                               c.privilege_type
                        FROM (
                            SELECT name,
                                   (aclexplode(attacl)).grantee AS grantee,
                                   (aclexplode(attacl)).privilege_type AS privilege_type
                            FROM columns
                        ) c
                        INNER JOIN pg_roles r
                                ON c.grantee = r.oid
                    ),
                    columnsgrants as (
                        SELECT coalesce(
                                   nullif(
                                       format(
                                           E'\n\n%s',
                                           string_agg(
                                               format(
                                                   E'GRANT %s(%s) ON %s TO %s;\n',
                                                   privilege_type,
                                                   column_name,
                                                   '{0}.{1}',
                                                   quote_ident(grantee)
                                               ),
                                               ''
                                           )
                                       ),
                                       '\n\n'
                                   ),
                                   ''
                               ) AS definition
                         FROM columnsprivileges
                    )
                    SELECT format(
                                E'ALTER TABLE %s\n\tADD COLUMN %s;%s%s%s',
                                '{0}.{1}'::regclass,
                                col.definition,
                                coalesce(com.definition, ''),
                                coalesce(def.definition, ''),
                                coalesce(cg.definition, '')
                           )
                    FROM columns col
                    LEFT JOIN comments com
                           ON 1 = 1
                    LEFT JOIN defaults def
                           ON 1 = 1
                    LEFT JOIN columnsgrants cg
                           ON 1 = 1
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )
        elif int(self.v_connection.ExecuteScalar('show server_version_num')) < 130000:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH columns AS (
                        SELECT format(
                                   '%I %s%s%s%s',
                                   a.attname::text,
                                   format_type(t.oid, a.atttypmod),
                                   (CASE WHEN length(col.collcollate) > 0
                                         THEN ' COLLATE ' || quote_ident(col.collcollate::text)
                                         ELSE ''
                                    END),
                                   (CASE WHEN a.attnotnull
                                         THEN ' NOT NULL'::text
                                         ELSE ''::text
                                    END),
                                   (CASE WHEN a.attidentity = 'a'
                                         THEN ' GENERATED ALWAYS AS IDENTITY'::text
                                         WHEN a.attidentity = 'd'
                                         THEN ' GENERATED BY DEFAULT AS IDENTITY'::text
                                         ELSE ''::text
                                    END)
                               ) AS definition,
                               a.attname AS name,
                               col_description(c.oid, a.attnum::integer) AS comment,
                               pg_get_expr(def.adbin, def.adrelid) AS default_value,
                               a.attacl
                        FROM pg_class c
                        INNER JOIN pg_namespace s
                                ON s.oid = c.relnamespace
                        INNER JOIN pg_attribute a
                                ON c.oid = a.attrelid
                        LEFT JOIN pg_attrdef def
                               ON c.oid = def.adrelid
                              AND a.attnum = def.adnum
                        LEFT JOIN pg_constraint con
                               ON con.conrelid = c.oid
                              AND (a.attnum = ANY (con.conkey))
                              AND con.contype = 'p'
                        LEFT JOIN pg_type t
                               ON t.oid = a.atttypid
                        LEFT JOIN pg_collation col
                               ON col.oid = a.attcollation
                        INNER JOIN pg_namespace tn
                                ON tn.oid = t.typnamespace
                        WHERE c.relkind IN ('r', 'p')
                          AND a.attnum > 0
                          AND NOT a.attisdropped
                          AND has_table_privilege(c.oid, 'select')
                          AND has_schema_privilege(s.oid, 'usage')
                          AND c.oid = '{0}.{1}'::regclass
                          AND a.attname = '{2}'
                    ),
                    comments AS (
                        SELECT format(
                                   E'\n\nCOMMENT ON COLUMN %s.%s IS %s;',
                                   '{0}.{1}',
                                   quote_ident(name),
                                   quote_nullable(comment)
                               ) AS definition
                        FROM columns
                        WHERE comment IS NOT NULL
                    ),
                    defaults AS (
                        SELECT format(
                                   E'\n\nALTER TABLE %s\n\tALTER %s SET DEFAULT %s;',
                                   '{0}.{1}'::regclass,
                                   quote_ident(name),
                                   default_value
                               ) AS definition
                        FROM columns
                        WHERE default_value IS NOT NULL
                    ),
                    columnsprivileges as (
                        SELECT r.rolname AS grantee,
                               c.name AS column_name,
                               c.privilege_type
                        FROM (
                            SELECT name,
                                   (aclexplode(attacl)).grantee AS grantee,
                                   (aclexplode(attacl)).privilege_type AS privilege_type
                            FROM columns
                        ) c
                        INNER JOIN pg_roles r
                                ON c.grantee = r.oid
                    ),
                    columnsgrants as (
                        SELECT coalesce(
                                   nullif(
                                       format(
                                           E'\n\n%s',
                                           string_agg(
                                               format(
                                                   E'GRANT %s(%s) ON %s TO %s;\n',
                                                   privilege_type,
                                                   column_name,
                                                   '{0}.{1}',
                                                   quote_ident(grantee)
                                               ),
                                               ''
                                           )
                                       ),
                                       '\n\n'
                                   ),
                                   ''
                               ) AS definition
                         FROM columnsprivileges
                    )
                    SELECT format(
                                E'ALTER TABLE %s\n\tADD COLUMN %s;%s%s%s',
                                '{0}.{1}'::regclass,
                                col.definition,
                                coalesce(com.definition, ''),
                                coalesce(def.definition, ''),
                                coalesce(cg.definition, '')
                           )
                    FROM columns col
                    LEFT JOIN comments com
                           ON 1 = 1
                    LEFT JOIN defaults def
                           ON 1 = 1
                    LEFT JOIN columnsgrants cg
                           ON 1 = 1
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )
        else:
            return self.v_connection.ExecuteScalar(
                '''
                    WITH columns AS (
                        SELECT format(
                                   '%I %s%s%s%s',
                                   a.attname::text,
                                   format_type(t.oid, a.atttypmod),
                                   (CASE WHEN length(col.collcollate) > 0
                                         THEN ' COLLATE ' || quote_ident(col.collcollate::text)
                                         ELSE ''
                                    END),
                                   (CASE WHEN a.attnotnull
                                         THEN ' NOT NULL'::text
                                         ELSE ''::text
                                    END),
                                   (CASE WHEN a.attidentity = 'a'
                                         THEN ' GENERATED ALWAYS AS IDENTITY'::text
                                         WHEN a.attidentity = 'd'
                                         THEN ' GENERATED BY DEFAULT AS IDENTITY'::text
                                         WHEN a.attgenerated = 's'
                                         THEN format(' GENERATED ALWAYS AS %s STORED', pg_get_expr(def.adbin, def.adrelid))::text
                                         ELSE ''::text
                                    END)
                               ) AS definition,
                               a.attname AS name,
                               col_description(c.oid, a.attnum::integer) AS comment,
                               pg_get_expr(def.adbin, def.adrelid) AS default_value,
                               a.attgenerated AS generated,
                               a.attacl
                        FROM pg_class c
                        INNER JOIN pg_namespace s
                                ON s.oid = c.relnamespace
                        INNER JOIN pg_attribute a
                                ON c.oid = a.attrelid
                        LEFT JOIN pg_attrdef def
                               ON c.oid = def.adrelid
                              AND a.attnum = def.adnum
                        LEFT JOIN pg_constraint con
                               ON con.conrelid = c.oid
                              AND (a.attnum = ANY (con.conkey))
                              AND con.contype = 'p'
                        LEFT JOIN pg_type t
                               ON t.oid = a.atttypid
                        LEFT JOIN pg_collation col
                               ON col.oid = a.attcollation
                        INNER JOIN pg_namespace tn
                                ON tn.oid = t.typnamespace
                        WHERE c.relkind IN ('r', 'p')
                          AND a.attnum > 0
                          AND NOT a.attisdropped
                          AND has_table_privilege(c.oid, 'select')
                          AND has_schema_privilege(s.oid, 'usage')
                          AND c.oid = '{0}.{1}'::regclass
                          AND a.attname = '{2}'
                    ),
                    comments AS (
                        SELECT format(
                                   E'\n\nCOMMENT ON COLUMN %s.%s IS %s;',
                                   '{0}.{1}',
                                   quote_ident(name),
                                   quote_nullable(comment)
                               ) AS definition
                        FROM columns
                        WHERE comment IS NOT NULL
                    ),
                    defaults AS (
                        SELECT format(
                                   E'\n\nALTER TABLE %s\n\tALTER %s SET DEFAULT %s;',
                                   '{0}.{1}'::regclass,
                                   quote_ident(name),
                                   default_value
                               ) AS definition
                        FROM columns
                        WHERE default_value IS NOT NULL
                          AND generated = ''
                    ),
                    columnsprivileges as (
                        SELECT r.rolname AS grantee,
                               c.name AS column_name,
                               c.privilege_type
                        FROM (
                            SELECT name,
                                   (aclexplode(attacl)).grantee AS grantee,
                                   (aclexplode(attacl)).privilege_type AS privilege_type
                            FROM columns
                        ) c
                        INNER JOIN pg_roles r
                                ON c.grantee = r.oid
                    ),
                    columnsgrants as (
                        SELECT coalesce(
                                   nullif(
                                       format(
                                           E'\n\n%s',
                                           string_agg(
                                               format(
                                                   E'GRANT %s(%s) ON %s TO %s;\n',
                                                   privilege_type,
                                                   column_name,
                                                   '{0}.{1}',
                                                   quote_ident(grantee)
                                               ),
                                               ''
                                           )
                                       ),
                                       '\n\n'
                                   ),
                                   ''
                               ) AS definition
                         FROM columnsprivileges
                    )
                    SELECT format(
                                E'ALTER TABLE %s\n\tADD COLUMN %s;%s%s%s',
                                '{0}.{1}'::regclass,
                                col.definition,
                                coalesce(com.definition, ''),
                                coalesce(def.definition, ''),
                                coalesce(cg.definition, '')
                           )
                    FROM columns col
                    LEFT JOIN comments com
                           ON 1 = 1
                    LEFT JOIN defaults def
                           ON 1 = 1
                    LEFT JOIN columnsgrants cg
                           ON 1 = 1
                '''.format(
                    p_schema,
                    p_table,
                    p_object
                )
            )

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
        elif p_type == 'table_field':
            return self.GetDDLTableField(p_schema, p_table, p_object)
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
            return self.GetDDLTrigger(p_object, p_table, p_schema)
        elif p_type == 'eventtrigger':
            return self.GetDDLEventTrigger(p_object)
        elif p_type == 'triggerfunction':
            return self.GetDDLFunction(p_object)
        elif p_type == 'direct_triggerfunction':
            return self.GetDDLFunction(p_object)
        elif p_type == 'eventtriggerfunction':
            return self.GetDDLFunction(p_object)
        elif p_type == 'direct_eventtriggerfunction':
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
        elif p_type == 'publication':
            return self.GetDDLPublication(p_object)
        elif p_type == 'subscription':
            return self.GetDDLSubscription(p_object)
        elif p_type == 'statistic':
            return self.GetDDLStatistic(p_schema, p_object)
        elif p_type == 'aggregate':
            return self.GetDDLAggregate(p_object)
        else:
            return ''

    @lock_required
    def GetAutocompleteValues(self, p_columns, p_filter):
        return self.v_connection.Query('''
            select {0}
            from (
            (select *
            from (select 'database' as type,
                   0 as sequence,
                   0 as num_dots,
                   quote_ident(datname) as result,
                   quote_ident(datname) as result_complete,
                   quote_ident(datname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_database) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'tablespace' as type,
                   2 as sequence,
                   0 as num_dots,
                   quote_ident(spcname) as result,
                   quote_ident(spcname) as result_complete,
                   quote_ident(spcname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_tablespace) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'role' as type,
                   1 as sequence,
                   0 as num_dots,
                   quote_ident(rolname) as result,
                   quote_ident(rolname) as result_complete,
                   quote_ident(rolname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_roles) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'extension' as type,
                   4 as sequence,
                   0 as num_dots,
                   quote_ident(extname) as result,
                   quote_ident(extname) as result_complete,
                   quote_ident(extname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_extension) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'schema' as type,
                   3 as sequence,
                   0 as num_dots,
                   quote_ident(nspname) as result,
                   quote_ident(nspname) as result_complete,
                   quote_ident(nspname) as select_value,
                   '' as complement,
                   '' as complement_complete
            from pg_catalog.pg_namespace
            where nspname not in ('pg_toast') and nspname not like 'pg%%temp%%') search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'table' as type,
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
            where c.relkind in ('r', 'p')) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'view' as type,
                   6 as sequence,
                   1 as num_dots,
                   quote_ident(table_name) as result,
                   quote_ident(table_schema) || '.' || quote_ident(table_name) as result_complete,
                   quote_ident(table_schema) || '.' || quote_ident(table_name) as select_value,
                   quote_ident(table_schema) as complement,
                   '' as complement_complete
            from information_schema.views) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'function' as type,
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
            where format_type(p.prorettype, null) not in ('trigger', 'event_trigger')) search
            {1}
            LIMIT 500)

            UNION ALL

            (select *
            from (select 'index' as type,
                   9 as sequence,
                   1 as num_dots,
                   quote_ident(i.indexname) as result,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.indexname) as result_complete,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.indexname) as select_value,
                   quote_ident(i.schemaname) || '.' || quote_ident(i.tablename) as complement,
                   quote_ident(i.tablename) as complement_complete
            from pg_indexes i) search
            {1}
            LIMIT 500 )) search
            {1}
            order by sequence,result_complete
        '''.format(p_columns,p_filter), True)

    @lock_required
    def ChangeRolePassword(self, p_role, p_password):
        self.v_connection.Execute(
            '''
                ALTER ROLE {0}
                    WITH PASSWORD '{1}'
            '''.format(
                p_role,
                'md5{0}'.format(
                    hashlib.md5(p_password.encode('utf-8') + p_role.encode('utf-8')).hexdigest()
                )
            )
        )

    @lock_required
    def GetObjectDescriptionAggregate(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regprocedure AS id,
                       coalesce(obj_description({0}, 'pg_proc'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON AGGREGATE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionTableField(self, p_oid, p_position):
        v_row = self.v_connection.Query(
            '''
                SELECT format(
                           '%s.%s',
                           {0}::regclass,
                           attname
                       ) AS id,
                       coalesce(col_description({0}, {1}), '') AS description
                FROM pg_attribute
                WHERE attrelid = {0}::regclass
                  AND attnum = {1}
            '''.format(
                p_oid,
                p_position
            )
        ).Rows[0]

        return "COMMENT ON COLUMN {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionConstraint(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT conname AS id,
                       conrelid::regclass AS table_id,
                       coalesce(obj_description({0}, 'pg_constraint'), '') AS description
                FROM pg_constraint c
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON CONSTRAINT {0} ON {1} is '{2}'".format(
            v_row['id'],
            v_row['table_id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionDatabase(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(datname) AS id,
                       coalesce(shobj_description({0}, 'pg_database'), '') AS description
                FROM pg_database
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON DATABASE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionDomain(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT '{0}'::regtype AS id,
                       coalesce(obj_description({0}, 'pg_type'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON DOMAIN {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionExtension(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(extname) AS id,
                       coalesce(obj_description({0}, 'pg_extension'), '') AS description
                FROM pg_extension
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON EXTENSION {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionEventTrigger(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(evtname) AS id,
                       coalesce(obj_description({0}, 'pg_event_trigger'), '') AS description
                FROM pg_event_trigger
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON EVENT TRIGGER {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionForeignDataWrapper(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(fdwname) AS id,
                       coalesce(obj_description({0}, 'pg_foreign_data_wrapper'), '') AS description
                FROM pg_foreign_data_wrapper
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON FOREIGN DATA WRAPPER {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionForeignServer(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(srvname) AS id,
                       coalesce(obj_description({0}, 'pg_foreign_server'), '') AS description
                FROM pg_foreign_server
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON SERVER {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionForeignTable(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON FOREIGN TABLE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionFunction(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regprocedure AS id,
                       coalesce(obj_description({0}, 'pg_proc'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON FUNCTION {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionIndex(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON INDEX {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionMaterializedView(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON MATERIALIZED VIEW {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionProcedure(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regprocedure AS id,
                       coalesce(obj_description({0}, 'pg_proc'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON PROCEDURE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionPublication(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(pubname) AS id,
                       coalesce(obj_description({0}, 'pg_publication'), '') AS description
                FROM pg_publication
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON PUBLICATION {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionRole(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regrole AS id,
                       coalesce(shobj_description({0}, 'pg_roles'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON ROLE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionRule(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(r.rulename) AS id,
                       format('%s.%s', r.schemaname, r.tablename)::regclass AS table_id,
                       coalesce(obj_description({0}, 'pg_rewrite'), '') AS description
                FROM pg_rules r
                INNER JOIN pg_rewrite rw
                        ON r.rulename = rw.rulename
                WHERE rw.oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON RULE {0} ON {1} is '{2}'".format(
            v_row['id'],
            v_row['table_id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionSchema(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regnamespace AS id,
                       coalesce(obj_description({0}, 'pg_namespace'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON SCHEMA {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionSequence(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON SEQUENCE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionStatistic(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT format('%s.%s', quote_ident(stxnamespace::regnamespace::text), quote_ident(stxname)) AS id,
                       coalesce(obj_description({0}, 'pg_statistic_ext'), '') AS description
                FROM pg_statistic_ext
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON STATISTICS {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionSubscription(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(subname) AS id,
                       coalesce(obj_description({0}, 'pg_subscription'), '') AS description
                FROM pg_subscription
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON SUBSCRIPTION {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionTable(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON TABLE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionTablespace(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT quote_ident(spcname) AS id,
                       coalesce(shobj_description({0}, 'pg_tablespace'), '') AS description
                FROM pg_tablespace
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON TABLESPACE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionTrigger(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT tgname AS id,
                       tgrelid::regclass AS table_id,
                       coalesce(obj_description({0}, 'pg_trigger'), '') AS description
                FROM pg_trigger
                WHERE oid = {0}
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON TRIGGER {0} ON {1} is '{2}'".format(
            v_row['id'],
            v_row['table_id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionType(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT '{0}'::regtype AS id,
                       coalesce(obj_description({0}, 'pg_type'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON TYPE {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    @lock_required
    def GetObjectDescriptionView(self, p_oid):
        v_row = self.v_connection.Query(
            '''
                SELECT {0}::regclass AS id,
                       coalesce(obj_description({0}, 'pg_class'), '') AS description
            '''.format(
                p_oid
            )
        ).Rows[0]

        return "COMMENT ON VIEW {0} is '{1}'".format(
            v_row['id'],
            v_row['description']
        )

    def GetObjectDescription(self, p_type, p_oid, p_position):
        print(p_type, p_oid, p_position)
        if p_type == 'aggregate':
            return self.GetObjectDescriptionAggregate(p_oid)
        elif p_type == 'table_field':
            return self.GetObjectDescriptionTableField(p_oid, p_position)
        elif p_type in ['check', 'foreign_key', 'pk', 'unique', 'exclude']:
            return self.GetObjectDescriptionConstraint(p_oid)
        elif p_type == 'database':
            return self.GetObjectDescriptionDatabase(p_oid)
        elif p_type == 'domain':
            return self.GetObjectDescriptionDomain(p_oid)
        elif p_type == 'extension':
            return self.GetObjectDescriptionExtension(p_oid)
        elif p_type == 'eventtrigger':
            return self.GetObjectDescriptionEventTrigger(p_oid)
        elif p_type == 'fdw':
            return self.GetObjectDescriptionForeignDataWrapper(p_oid)
        elif p_type == 'foreign_server':
            return self.GetObjectDescriptionForeignServer(p_oid)
        elif p_type == 'foreign_table':
            return self.GetObjectDescriptionForeignTable(p_oid)
        elif p_type in ['function', 'triggerfunction', 'direct_triggerfunction', 'eventtriggerfunction', 'direct_eventtriggerfunction']:
            return self.GetObjectDescriptionFunction(p_oid)
        elif p_type == 'index':
            return self.GetObjectDescriptionIndex(p_oid)
        elif p_type == 'mview':
            return self.GetObjectDescriptionMaterializedView(p_oid)
        elif p_type == 'procedure':
            return self.GetObjectDescriptionProcedure(p_oid)
        elif p_type == 'publication':
            return self.GetObjectDescriptionPublication(p_oid)
        elif p_type == 'role':
            return self.GetObjectDescriptionRole(p_oid)
        elif p_type == 'rule':
            return self.GetObjectDescriptionRule(p_oid)
        elif p_type == 'schema':
            return self.GetObjectDescriptionSchema(p_oid)
        elif p_type == 'sequence':
            return self.GetObjectDescriptionSequence(p_oid)
        elif p_type == 'statistic':
            return self.GetObjectDescriptionStatistic(p_oid)
        elif p_type == 'subscription':
            return self.GetObjectDescriptionSubscription(p_oid)
        elif p_type == 'table':
            return self.GetObjectDescriptionTable(p_oid)
        elif p_type == 'tablespace':
            return self.GetObjectDescriptionTablespace(p_oid)
        elif p_type == 'trigger':
            return self.GetObjectDescriptionTrigger(p_oid)
        elif p_type == 'type':
            return self.GetObjectDescriptionType(p_oid)
        elif p_type == 'view':
            return self.GetObjectDescriptionView(p_oid)
        else:
            return ''
