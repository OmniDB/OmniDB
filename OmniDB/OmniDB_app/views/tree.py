from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
import json

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
from OmniDB_app.include.Session import Session

def get_tree_info(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]

    v_return['v_data'] = {
        'v_mode': 'database',
        'v_database_return': {
            'v_database': v_database.GetName(),
            'v_has_schema': v_database.v_has_schema,
			'v_has_functions': v_database.v_has_functions,
            'v_has_procedures': v_database.v_has_procedures,
			'v_has_sequences': v_database.v_has_sequences,
            'v_schema': v_database.v_schema
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]
    v_list_tables = []

    try:
        v_tables = v_database.QueryTables(False)
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


def get_columns(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_table = json_object['p_table']

    v_database = v_session.v_databases[v_database_index]
    v_list_columns = []

    try:
        v_columns = v_database.QueryTablesFields(v_table)
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

def get_pk(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_table = json_object['p_table']

    v_database = v_session.v_databases[p_database_index]
    v_list_pk = []

    try:
        v_tables = v_database.QueryTablesPrimaryKeys("", p_table)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_table = json_object['p_table']

    v_database = v_session.v_databases[p_database_index]
    v_list_fk = []

    try:
        v_tables = v_database.QueryTablesForeignKeys(p_table)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_table = json_object['p_table']

    v_database = v_session.v_databases[p_database_index]
    v_list_unique = []

    try:
        v_tables = v_database.QueryTablesUniques("",p_table)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_table = json_object['p_table']

    v_database = v_session.v_databases[p_database_index]
    v_list_index = []

    try:
        v_tables = v_database.QueryTablesIndexes(p_table)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]
    v_list_functions = []

    try:
        v_functions = v_database.QueryFunctions()
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    p_function = json_object['p_function']

    v_database = v_session.v_databases[v_database_index]
    v_list_fields = []

    try:
        v_fields = v_database.QueryFunctionFields(p_function)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    p_function = json_object['p_function']

    v_database = v_session.v_databases[v_database_index]
    v_list_fields = []

    try:
        v_return['v_data'] = v_database.GetFunctionDefinition(p_function)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_procedures(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]
    v_list_procedures = []

    try:
        v_procedures = v_database.QueryProcedures()
        for v_procedure in v_procedures.Rows:
            v_procedure_data = {
                'v_name': v_procedure['name'],
                'v_id': v_procedure['id']
            }
            v_list_procedures.append(v_procedure_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_procedures

    return JsonResponse(v_return)

def get_procedure_fields(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    p_procedure = json_object['p_procedure']

    v_database = v_session.v_databases[v_database_index]
    v_list_fields = []

    try:
        v_fields = v_database.QueryProcedureFields(p_procedure)
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

def get_procedure_definition(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    p_procedure = json_object['p_procedure']

    v_database = v_session.v_databases[v_database_index]
    v_list_fields = []

    try:
        v_return['v_data'] = v_database.GetProcedureDefinition(p_procedure)
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
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]
    v_list_sequences = []

    try:
        v_sequences = v_database.QuerySequences(None)
        for v_sequence in v_sequences.Rows:
            v_list_sequences.append(v_sequence['sequence_name'])
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_sequences

    return JsonResponse(v_return)
