from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
import json

import sys
sys.path.append("OmniDB_app/include")

import Spartacus.Database, Spartacus.Utils
from OmniDB import sessions
from Session import Session
from datetime import datetime

def get_tree_info(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    v_return['v_data'] = {
        'v_mode': 'database',
        'v_database_return': {
            'v_database': v_database.GetName(),
            'create_tablespace': v_database.TemplateCreateTablespace().v_text,
            'alter_tablespace': v_database.TemplateAlterTablespace().v_text,
            'drop_tablespace': v_database.TemplateDropTablespace().v_text,
            'create_role': v_database.TemplateCreateRole().v_text,
            'alter_role': v_database.TemplateAlterRole().v_text,
            'drop_role': v_database.TemplateDropRole().v_text,
            'create_database': v_database.TemplateCreateDatabase().v_text,
            'alter_database': v_database.TemplateAlterDatabase().v_text,
            'drop_database': v_database.TemplateDropDatabase().v_text,
            'create_schema': v_database.TemplateCreateSchema().v_text,
            'alter_schema': v_database.TemplateAlterSchema().v_text,
            'drop_schema': v_database.TemplateDropSchema().v_text,
            #create_table
            #alter_table
            'drop_table': v_database.TemplateDropTable().v_text,
            'create_sequence': v_database.TemplateCreateSequence().v_text,
            'alter_sequence': v_database.TemplateAlterSequence().v_text,
            'drop_sequence': v_database.TemplateDropSequence().v_text,
            'create_function': v_database.TemplateCreateFunction().v_text,
            'drop_function': v_database.TemplateDropFunction().v_text,
            'create_view': v_database.TemplateCreateView().v_text,
            'drop_view': v_database.TemplateDropView().v_text
        }
    }

    return JsonResponse(v_return)

def get_tables(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryTables(False,v_schema)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name'],
                'v_has_primary_keys': v_database.v_has_primary_keys,
                'v_has_foreign_keys': v_database.v_has_foreign_keys,
                'v_has_uniques': v_database.v_has_uniques,
                'v_has_indexes': v_database.v_has_indexes
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_views(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryViews(False,v_schema)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name'],
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_schemas(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_schemas = []

    try:
        v_schemas = v_database.QuerySchemas()
        for v_schema in v_schemas.Rows:
            v_schema_data = {
                'v_name': v_schema['schema_name']
            }
            v_list_schemas.append(v_schema_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_schemas

    return JsonResponse(v_return)

def get_databases(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_databases = []

    try:
        v_databases = v_database.QueryDatabases()
        for v_database in v_databases.Rows:
            v_database_data = {
                'v_name': v_database['database_name']
            }
            v_list_databases.append(v_database_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_databases

    return JsonResponse(v_return)

def get_tablespaces(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tablespaces = []

    try:
        v_tablespaces = v_database.QueryTablespaces()
        for v_tablespace in v_tablespaces.Rows:
            v_tablespace_data = {
                'v_name': v_tablespace['tablespace_name']
            }
            v_list_tablespaces.append(v_tablespace_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tablespaces

    return JsonResponse(v_return)

def get_roles(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_roles = []

    try:
        v_roles = v_database.QueryRoles()
        for v_role in v_roles.Rows:
            v_role_data = {
                'v_name': v_role['role_name']
            }
            v_list_roles.append(v_role_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_roles

    return JsonResponse(v_return)


def get_columns(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryTablesFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
                'v_nullable': v_column['nullable']
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)

def get_views_columns(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryViewFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)

def get_pk(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_pk = []

    try:
        v_tables = v_database.QueryTablesPrimaryKeys(v_table,False,v_schema)
        for v_table in v_tables.Rows:
            v_pk_data = []
            v_pk_data.append(v_table['constraint_name'])
            v_pk_data.append(v_table['column_name'])
            v_list_pk.append(v_pk_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_pk

    return JsonResponse(v_return)

def get_fks(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fk = []

    try:
        v_tables = v_database.QueryTablesForeignKeys(v_table, False, v_schema)
        for v_table in v_tables.Rows:
            v_fk_data = []
            v_fk_data.append(v_table['constraint_name'])
            v_fk_data.append(v_table['column_name'])
            v_fk_data.append(v_table['r_table_name'])
            v_fk_data.append(v_table['r_column_name'])
            v_fk_data.append(v_table['delete_rule'])
            v_fk_data.append(v_table['update_rule'])
            v_list_fk.append(v_fk_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fk

    return JsonResponse(v_return)

def get_uniques(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_unique = []

    try:
        v_tables = v_database.QueryTablesUniques(v_table,False,v_schema)
        for v_table in v_tables.Rows:
            v_unique_data = []
            v_unique_data.append(v_table['constraint_name'])
            v_unique_data.append(v_table['column_name'])
            v_list_unique.append(v_unique_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_unique

    return JsonResponse(v_return)

def get_indexes(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_index = []

    try:
        v_tables = v_database.QueryTablesIndexes(v_table, False, v_schema)
        for v_table in v_tables.Rows:
            v_index_data = []
            v_index_data.append(v_table['index_name'])
            v_index_data.append(v_table['uniqueness'])
            v_index_data.append(v_table['column_name'])
            v_list_index.append(v_index_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_index

    return JsonResponse(v_return)

def get_functions(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_functions = []

    try:
        v_functions = v_database.QueryFunctions(False,v_schema)
        for v_function in v_functions.Rows:
            v_function_data = {
                'v_name': v_function['name'],
                'v_id': v_function['id']
            }
            v_list_functions.append(v_function_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_functions

    return JsonResponse(v_return)

def get_function_fields(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_function = json_object['p_function']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fields = []

    try:
        v_fields = v_database.QueryFunctionFields(v_function,v_schema)
        for v_field in v_fields.Rows:
            v_field_data = {
                'v_name': v_field['name'],
                'v_id': v_field['type']
            }
            v_list_fields.append(v_field_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fields

    return JsonResponse(v_return)

def get_function_definition(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_function = json_object['p_function']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetFunctionDefinition(v_function)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_sequences(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_sequences = []

    try:
        v_sequences = v_database.QuerySequences(False,v_schema)
        for v_sequence in v_sequences.Rows:
            v_list_sequences.append(v_sequence['sequence_name'])
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_sequences

    return JsonResponse(v_return)

def get_view_definition(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_view = json_object['p_view']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(v_database_index):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.QueryViewDefinition(v_view, v_schema)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
