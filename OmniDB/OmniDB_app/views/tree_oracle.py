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

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = {
            'v_mode': 'database',
            'v_database_return': {
                'v_database': v_database.GetName(),
                'version': v_database.GetVersion(),
                'v_username': v_database.GetUserName(),
                'superuser': v_database.GetUserSuper(),
                'create_role': v_database.TemplateCreateRole().v_text,
                'alter_role': v_database.TemplateAlterRole().v_text,
                'drop_role': v_database.TemplateDropRole().v_text,
                'create_tablespace': v_database.TemplateCreateTablespace().v_text,
                'alter_tablespace': v_database.TemplateAlterTablespace().v_text,
                'drop_tablespace': v_database.TemplateDropTablespace().v_text,
                'create_database': v_database.TemplateCreateDatabase().v_text,
                'alter_database': v_database.TemplateAlterDatabase().v_text,
                'drop_database': v_database.TemplateDropDatabase().v_text,
                'create_sequence': v_database.TemplateCreateSequence().v_text,
                'alter_sequence': v_database.TemplateAlterSequence().v_text,
                'drop_sequence': v_database.TemplateDropSequence().v_text,
                'create_function': v_database.TemplateCreateFunction().v_text,
                'drop_function': v_database.TemplateDropFunction().v_text,
                'create_triggerfunction': v_database.TemplateCreateTriggerFunction().v_text,
                'drop_triggerfunction': v_database.TemplateDropTriggerFunction().v_text,
                'create_view': v_database.TemplateCreateView().v_text,
                'drop_view': v_database.TemplateDropView().v_text,
                'create_mview': v_database.TemplateCreateMaterializedView().v_text,
                'refresh_mview': v_database.TemplateRefreshMaterializedView().v_text,
                'drop_mview': v_database.TemplateDropMaterializedView().v_text,
                #create_table
                #alter_table
                'drop_table': v_database.TemplateDropTable().v_text,
                'create_column': v_database.TemplateCreateColumn().v_text,
                'alter_column': v_database.TemplateAlterColumn().v_text,
                'drop_column': v_database.TemplateDropColumn().v_text,
                'create_primarykey': v_database.TemplateCreatePrimaryKey().v_text,
                'drop_primarykey': v_database.TemplateDropPrimaryKey().v_text,
                'create_unique': v_database.TemplateCreateUnique().v_text,
                'drop_unique': v_database.TemplateDropUnique().v_text,
                'create_foreignkey': v_database.TemplateCreateForeignKey().v_text,
                'drop_foreignkey': v_database.TemplateDropForeignKey().v_text,
                'create_index': v_database.TemplateCreateIndex().v_text,
                'alter_index': v_database.TemplateAlterIndex().v_text,
                'drop_index': v_database.TemplateDropIndex().v_text,
                'create_check': v_database.TemplateCreateCheck().v_text,
                'drop_check': v_database.TemplateDropCheck().v_text,
                'create_exclude': v_database.TemplateCreateExclude().v_text,
                'drop_exclude': v_database.TemplateDropExclude().v_text,
                'create_rule': v_database.TemplateCreateRule().v_text,
                'alter_rule': v_database.TemplateAlterRule().v_text,
                'drop_rule': v_database.TemplateDropRule().v_text,
                'create_trigger': v_database.TemplateCreateTrigger().v_text,
                'create_view_trigger': v_database.TemplateCreateViewTrigger().v_text,
                'alter_trigger': v_database.TemplateAlterTrigger().v_text,
                'enable_trigger': v_database.TemplateEnableTrigger().v_text,
                'disable_trigger': v_database.TemplateDisableTrigger().v_text,
                'drop_trigger': v_database.TemplateDropTrigger().v_text,
                'create_partition': v_database.TemplateCreatePartition().v_text,
                'noinherit_partition': v_database.TemplateNoInheritPartition().v_text,
                'drop_partition': v_database.TemplateDropPartition().v_text
            }
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryTables(False,v_schema)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['TABLE_NAME'],
                'v_has_primary_keys': v_database.v_has_primary_keys,
                'v_has_foreign_keys': v_database.v_has_foreign_keys,
                'v_has_uniques': v_database.v_has_uniques,
                'v_has_indexes': v_database.v_has_indexes,
                'v_has_checks': v_database.v_has_checks,
                'v_has_excludes': v_database.v_has_excludes,
                'v_has_rules': v_database.v_has_rules,
                'v_has_triggers': v_database.v_has_triggers,
                'v_has_partitions': v_database.v_has_partitions
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryTablesFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['COLUMN_NAME'],
                'v_data_type': v_column['DATA_TYPE'],
                'v_data_length': v_column['DATA_LENGTH'],
                'v_nullable': v_column['NULLABLE']
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_pk = []

    try:
        v_pks = v_database.QueryTablesPrimaryKeys(v_table,False,v_schema)
        for v_pk in v_pks.Rows:
            v_pk_data = []
            v_pk_data.append(v_pk['CONSTRAINT_NAME'])
            v_pk_data.append(v_pk['COLUMN_NAME'])
            v_list_pk.append(v_pk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fk = []

    try:
        v_fks = v_database.QueryTablesForeignKeys(v_table, False, v_schema)
        for v_fk in v_fks.Rows:
            v_fk_data = []
            v_fk_data.append(v_fk['CONSTRAINT_NAME'])
            v_fk_data.append(v_fk['COLUMN_NAME'])
            v_fk_data.append(v_fk['R_TABLE_NAME'])
            v_fk_data.append(v_fk['R_COLUMN_NAME'])
            v_fk_data.append(v_fk['DELETE_RULE'])
            v_fk_data.append(v_fk['UPDATE_RULE'])
            v_list_fk.append(v_fk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_uniques = []

    try:
        v_uniques = v_database.QueryTablesUniques(v_table,False,v_schema)
        for v_unique in v_uniques.Rows:
            v_unique_data = []
            v_unique_data.append(v_unique['CONSTRAINT_NAME'])
            v_unique_data.append(v_unique['COLUMN_NAME'])
            v_list_uniques.append(v_unique_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_uniques

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_indexes = []

    try:
        v_indexes = v_database.QueryTablesIndexes(v_table, False, v_schema)
        for v_index in v_indexes.Rows:
            v_index_data = []
            v_index_data.append(v_index['INDEX_NAME'])
            v_index_data.append(v_index['UNIQUENESS'])
            v_index_data.append(v_index['COLUMN_NAME'])
            v_list_indexes.append(v_index_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_indexes

    return JsonResponse(v_return)

def get_checks(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_checks = []

    try:
        v_checks = v_database.QueryTablesChecks(v_table,False,v_schema)
        for v_check in v_checks.Rows:
            v_check_data = []
            v_check_data.append(v_check['CONSTRAINT_NAME'])
            v_check_data.append(v_check['CONSTRAINT_SOURCE'])
            v_list_checks.append(v_check_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_checks

    return JsonResponse(v_return)

def get_excludes(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_excludes = []

    try:
        v_excludes = v_database.QueryTablesExcludes(v_table,False,v_schema)
        for v_exclude in v_excludes.Rows:
            v_exclude_data = []
            v_exclude_data.append(v_exclude['CONSTRAINT_NAME'])
            v_exclude_data.append(v_exclude['ATTRIBUTES'])
            v_exclude_data.append(v_exclude['OPERATIONS'])
            v_list_excludes.append(v_exclude_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_excludes

    return JsonResponse(v_return)

def get_rules(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_rules = []

    try:
        v_rules = v_database.QueryTablesRules(v_table,False,v_schema)
        for v_rule in v_rules.Rows:
            v_rule_data = []
            v_rule_data.append(v_rule['CONSTRAINT_NAME'])
            v_list_rules.append(v_rule_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_rules

    return JsonResponse(v_return)

def get_triggers(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_triggers = []

    try:
        v_triggers = v_database.QueryTablesTriggers(v_table,False,v_schema)
        for v_trigger in v_triggers.Rows:
            v_trigger_data = []
            v_trigger_data.append(v_trigger['TRIGGER_NAME'])
            v_trigger_data.append(v_trigger['TRIGGER_ENABLED'])
            v_trigger_data.append(v_trigger['TRIGGER_FUNCTION_NAME'])
            v_trigger_data.append(v_trigger['TRIGGER_FUNCTION_ID'])
            v_list_triggers.append(v_trigger_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_triggers

    return JsonResponse(v_return)

def get_partitions(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_partitions = []

    try:
        v_partitions = v_database.QueryTablesPartitions(v_table,False,v_schema)
        for v_partition in v_partitions.Rows:
            v_partition_data = []
            v_partition_data.append(v_partition['CHILD_SCHEMA'] + '.' + v_partition['CHILD_TABLE'])
            v_list_partitions.append(v_partition_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_partitions

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryViews(False,v_schema)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['TABLE_NAME'],
                'v_has_triggers': v_database.v_has_triggers,
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryViewFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['COLUMN_NAME'],
                'v_data_type': v_column['DATA_TYPE'],
                'v_data_length': v_column['DATA_LENGTH'],
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetViewDefinition(v_view, v_schema)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_mviews(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryMaterializedViews(False,v_schema)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['TABLE_NAME'],
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_mviews_columns(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryMaterializedViewFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['COLUMN_NAME'],
                'v_data_type': v_column['DATA_TYPE'],
                'v_data_length': v_column['DATA_LENGTH'],
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)

def get_mview_definition(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetMaterializedViewDefinition(v_view, v_schema)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_databases = []

    try:
        v_databases = v_database.QueryDatabases()
        for v_database in v_databases.Rows:
            v_database_data = {
                'v_name': v_database['DATABASE_NAME']
            }
            v_list_databases.append(v_database_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tablespaces = []

    try:
        v_tablespaces = v_database.QueryTablespaces()
        for v_tablespace in v_tablespaces.Rows:
            v_tablespace_data = {
                'v_name': v_tablespace['TABLESPACE_NAME']
            }
            v_list_tablespaces.append(v_tablespace_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_roles = []

    try:
        v_roles = v_database.QueryRoles()
        for v_role in v_roles.Rows:
            v_role_data = {
                'v_name': v_role['ROLE_NAME']
            }
            v_list_roles.append(v_role_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_roles

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_functions = []

    try:
        v_functions = v_database.QueryFunctions(False,v_schema)
        for v_function in v_functions.Rows:
            v_function_data = {
                'v_name': v_function['NAME'],
                'v_id': v_function['ID']
            }
            v_list_functions.append(v_function_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fields = []

    try:
        v_fields = v_database.QueryFunctionFields(v_function,v_schema)
        for v_field in v_fields.Rows:
            v_field_data = {
                'v_name': v_field['NAME'],
                'v_type': v_field['TYPE']
            }
            v_list_fields.append(v_field_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetFunctionDefinition(v_function)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_function_debug(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetFunctionDebug(v_function)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_triggerfunctions(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_functions = []

    try:
        v_functions = v_database.QueryTriggerFunctions(False,v_schema)
        for v_function in v_functions.Rows:
            v_function_data = {
                'v_name': v_function['NAME'],
                'v_id': v_function['ID']
            }
            v_list_functions.append(v_function_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_functions

    return JsonResponse(v_return)

def get_triggerfunction_definition(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetTriggerFunctionDefinition(v_function)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_sequences = []

    try:
        v_sequences = v_database.QuerySequences(False,v_schema)
        for v_sequence in v_sequences.Rows:
            v_sequence_data = {
                'v_sequence_name': v_sequence['SEQUENCE_NAME']
            }
            v_list_sequences.append(v_sequence_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_sequences

    return JsonResponse(v_return)

def get_sequence_values(request):

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
    v_sequence = json_object['p_sequence']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_values = []

    try:
        v_values = v_database.QuerySequenceValues(v_sequence, v_schema)
        for v_value in v_values.Rows:
            v_value_data = {
                'v_minimum_value': v_value['MINIMUM_VALUE'],
                'v_maximum_value': v_value['MAXIMUM_VALUE'],
                'v_current_value': v_value['CURRENT_VALUE'],
                'v_increment': v_value['INCREMENT']
            }
            v_list_values.append(v_value_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_values

    return JsonResponse(v_return)

def kill_backend(request):

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
    v_pid            = json_object['p_pid']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_data = v_database.v_connection.Terminate(v_pid)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
