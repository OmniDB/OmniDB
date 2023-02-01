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
from datetime import datetime

from OmniDB_app.views.memory_objects import user_authenticated, database_required


@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_tree_info(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    try:
        v_return['v_data'] = {
            'v_mode': 'database',
            'v_database_return': {
                'v_database': v_database.GetName(),
                'version': v_database.GetVersion(),
                'create_view': v_database.TemplateCreateView().v_text,
                'drop_view': v_database.TemplateDropView().v_text,
                'create_table': v_database.TemplateCreateTable().v_text,
                'alter_table': v_database.TemplateAlterTable().v_text,
                'drop_table': v_database.TemplateDropTable().v_text,
                'create_column': v_database.TemplateCreateColumn().v_text,
                'create_index': v_database.TemplateCreateIndex().v_text,
                'reindex': v_database.TemplateReindex().v_text,
                'drop_index': v_database.TemplateDropIndex().v_text,
                'delete': v_database.TemplateDelete().v_text,
                'create_trigger': v_database.TemplateCreateTrigger().v_text,
                'drop_trigger': v_database.TemplateDropTrigger().v_text
            }
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_tables(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    v_list_tables = []

    try:
        v_tables = v_database.QueryTables()

        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name'],
                'v_has_primary_keys': v_database.v_has_primary_keys,
                'v_has_foreign_keys': v_database.v_has_foreign_keys,
                'v_has_uniques': v_database.v_has_uniques,
                'v_has_indexes': v_database.v_has_indexes,
                'v_has_checks': v_database.v_has_checks,
                'v_has_excludes': v_database.v_has_excludes,
                'v_has_rules': v_database.v_has_rules,
                'v_has_triggers': v_database.v_has_triggers,
                'v_has_partitions': v_database.v_has_partitions,
                'v_has_statistics': v_database.v_has_statistics
            }

            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_columns(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

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
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_pk(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_pk = []

    try:
        v_pks = v_database.QueryTablesPrimaryKeys(v_table)

        for v_pk in v_pks.Rows:
            v_pk_data = []
            v_pk_data.append(v_pk['constraint_name'])

            v_list_pk.append(v_pk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_pk

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_pk_columns(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_pk = []

    try:
        v_pk = v_database.QueryTablesPrimaryKeysColumns(v_table)

        for v_row in v_pk.Rows:
            v_pk_data = []
            v_pk_data.append(v_row['column_name'])

            v_list_pk.append(v_pk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_pk

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_fks(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_fk = []

    try:
        v_fks = v_database.QueryTablesForeignKeys(v_table)

        for v_fk in v_fks.Rows:
            v_fk_data = []
            v_fk_data.append(v_fk['constraint_name'])
            v_fk_data.append(v_fk['r_table_name'])
            v_fk_data.append(v_fk['delete_rule'])
            v_fk_data.append(v_fk['update_rule'])

            v_list_fk.append(v_fk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fk

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_fks_columns(request, v_database):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_fkey = json_object['p_fkey']
    v_table = json_object['p_table']

    v_list_fk = []

    try:
        v_fks = v_database.QueryTablesForeignKeysColumns(v_fkey, v_table)

        for v_fk in v_fks.Rows:
            v_fk_data = []
            v_fk_data.append(v_fk['r_table_name'])
            v_fk_data.append(v_fk['delete_rule'])
            v_fk_data.append(v_fk['update_rule'])
            v_fk_data.append(v_fk['column_name'])
            v_fk_data.append(v_fk['r_column_name'])

            v_list_fk.append(v_fk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fk

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_uniques(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_uniques = []

    try:
        v_uniques = v_database.QueryTablesUniques(v_table)

        for v_unique in v_uniques.Rows:
            v_unique_data = []
            v_unique_data.append(v_unique['constraint_name'])

            v_list_uniques.append(v_unique_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_uniques

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_uniques_columns(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_unique = json_object['p_unique']
    v_table = json_object['p_table']

    v_list_uniques = []

    try:
        v_uniques = v_database.QueryTablesUniquesColumns(v_unique, v_table)

        print(v_uniques.Rows)

        for v_unique in v_uniques.Rows:
            v_unique_data = []
            v_unique_data.append(v_unique['column_name'])

            v_list_uniques.append(v_unique_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_uniques

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_indexes(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_indexes = []

    try:
        v_indexes = v_database.QueryTablesIndexes(v_table)

        for v_index in v_indexes.Rows:
            v_index_data = []
            v_index_data.append(v_index['index_name'])
            v_index_data.append(v_index['uniqueness'])

            v_list_indexes.append(v_index_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_indexes

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_indexes_columns(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_index = json_object['p_index']
    v_table = json_object['p_table']

    v_list_indexes = []

    try:
        v_indexes = v_database.QueryTablesIndexesColumns(v_index, v_table)

        for v_index in v_indexes.Rows:
            v_index_data = []
            v_index_data.append(v_index['column_name'])

            v_list_indexes.append(v_index_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_indexes

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_views(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    v_list_tables = []

    try:
        v_tables = v_database.QueryViews()

        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name']
            }

            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_views_columns(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_columns = []

    try:
        v_columns = v_database.QueryViewFields(v_table)

        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
            }

            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_view_definition(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_view = json_object['p_view']

    try:
        v_return['v_data'] = v_database.GetViewDefinition(v_view)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_triggers(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    v_list_triggers = []

    try:
        v_triggers = v_database.QueryTablesTriggers(v_table)

        for v_trigger in v_triggers.Rows:
            v_trigger_data = {
                'v_name': v_trigger['trigger_name']
            }

            v_list_triggers.append(v_trigger_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_triggers

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def template_select(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_kind = json_object['p_kind']

    try:
        v_template = v_database.TemplateSelect(v_table, v_kind).v_text
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def template_insert(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    try:
        v_template = v_database.TemplateInsert(v_table).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def template_update(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']

    try:
        v_template = v_database.TemplateUpdate(v_table).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_version(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    try:
        v_return['v_data'] = {
            'v_version': v_database.GetVersion()
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout=False, p_open_connection=True)
def get_properties(request, v_database):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_data = json_object['p_data']

    v_list_properties = []
    v_ddl = ''

    try:
        v_properties = v_database.GetProperties(v_data['p_table'], v_data['p_object'], v_data['p_type'])

        for v_property in v_properties.Rows:
            v_list_properties.append([v_property['Property'], v_property['Value']])

        v_ddl = v_database.GetDDL(v_data['p_table'], v_data['p_object'], v_data['p_type'])
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
        v_return['v_data'] = {'password_timeout': False, 'message': str(exc)}
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'properties': v_list_properties,
        'ddl': v_ddl
    }

    return JsonResponse(v_return)
