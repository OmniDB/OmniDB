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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                #'superuser': v_database.GetUserSuper(),
                'create_role': v_database.TemplateCreateRole().v_text,
                'alter_role': v_database.TemplateAlterRole().v_text,
                'drop_role': v_database.TemplateDropRole().v_text,
                'create_tablespace': v_database.TemplateCreateTablespace().v_text,
                'alter_tablespace': v_database.TemplateAlterTablespace().v_text,
                'drop_tablespace': v_database.TemplateDropTablespace().v_text,
                'create_database': v_database.TemplateCreateDatabase().v_text,
                'alter_database': v_database.TemplateAlterDatabase().v_text,
                'drop_database': v_database.TemplateDropDatabase().v_text,
                'create_extension': v_database.TemplateCreateExtension().v_text,
                'alter_extension': v_database.TemplateAlterExtension().v_text,
                'drop_extension': v_database.TemplateDropExtension().v_text,
                'create_schema': v_database.TemplateCreateSchema().v_text,
                'alter_schema': v_database.TemplateAlterSchema().v_text,
                'drop_schema': v_database.TemplateDropSchema().v_text,
                'create_sequence': v_database.TemplateCreateSequence().v_text,
                'alter_sequence': v_database.TemplateAlterSequence().v_text,
                'drop_sequence': v_database.TemplateDropSequence().v_text,
                'create_function': v_database.TemplateCreateFunction().v_text,
                'drop_function': v_database.TemplateDropFunction().v_text,
                'create_procedure': v_database.TemplateCreateProcedure().v_text,
                'drop_procedure': v_database.TemplateDropProcedure().v_text,
                'create_triggerfunction': v_database.TemplateCreateTriggerFunction().v_text,
                'drop_triggerfunction': v_database.TemplateDropTriggerFunction().v_text,
                'create_view': v_database.TemplateCreateView().v_text,
                'drop_view': v_database.TemplateDropView().v_text,
                'create_mview': v_database.TemplateCreateMaterializedView().v_text,
                'refresh_mview': v_database.TemplateRefreshMaterializedView().v_text,
                'drop_mview': v_database.TemplateDropMaterializedView().v_text,
                'create_table': v_database.TemplateCreateTable().v_text,
                'alter_table': v_database.TemplateAlterTable().v_text,
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
                'create_inherited': v_database.TemplateCreateInherited().v_text,
                'noinherit_partition': v_database.TemplateNoInheritPartition().v_text,
                'create_partition': v_database.TemplateCreatePartition().v_text,
                'detach_partition': v_database.TemplateDetachPartition().v_text,
                'drop_partition': v_database.TemplateDropPartition().v_text,
                'vacuum': v_database.TemplateVacuum().v_text,
                'vacuum_table': v_database.TemplateVacuumTable().v_text,
                'analyze': v_database.TemplateAnalyze().v_text,
                'analyze_table': v_database.TemplateAnalyzeTable().v_text,
                'delete': v_database.TemplateDelete().v_text,
                'truncate': v_database.TemplateTruncate().v_text,
                'create_physicalreplicationslot': v_database.TemplateCreatePhysicalReplicationSlot().v_text,
                'drop_physicalreplicationslot': v_database.TemplateDropPhysicalReplicationSlot().v_text,
                'create_logicalreplicationslot': v_database.TemplateCreateLogicalReplicationSlot().v_text,
                'drop_logicalreplicationslot': v_database.TemplateDropLogicalReplicationSlot().v_text,
                'create_publication': v_database.TemplateCreatePublication().v_text,
                'alter_publication': v_database.TemplateAlterPublication().v_text,
                'drop_publication': v_database.TemplateDropPublication().v_text,
                'add_pubtable': v_database.TemplateAddPublicationTable().v_text,
                'drop_pubtable': v_database.TemplateDropPublicationTable().v_text,
                'create_subscription': v_database.TemplateCreateSubscription().v_text,
                'alter_subscription': v_database.TemplateAlterSubscription().v_text,
                'drop_subscription': v_database.TemplateDropSubscription().v_text,
                'create_fdw': v_database.TemplateCreateForeignDataWrapper().v_text,
                'alter_fdw': v_database.TemplateAlterForeignDataWrapper().v_text,
                'drop_fdw': v_database.TemplateDropForeignDataWrapper().v_text,
                'create_foreign_server': v_database.TemplateCreateForeignServer().v_text,
                'alter_foreign_server': v_database.TemplateAlterForeignServer().v_text,
                'import_foreign_schema': v_database.TemplateImportForeignSchema().v_text,
                'drop_foreign_server': v_database.TemplateDropForeignServer().v_text,
                'create_foreign_table': v_database.TemplateCreateForeignTable().v_text,
                'alter_foreign_table': v_database.TemplateAlterForeignTable().v_text,
                'drop_foreign_table': v_database.TemplateDropForeignTable().v_text,
                'create_foreign_column': v_database.TemplateCreateForeignColumn().v_text,
                'alter_foreign_column': v_database.TemplateAlterForeignColumn().v_text,
                'drop_foreign_column': v_database.TemplateDropForeignColumn().v_text,
                'create_user_mapping': v_database.TemplateCreateUserMapping().v_text,
                'alter_user_mapping': v_database.TemplateAlterUserMapping().v_text,
                'drop_user_mapping': v_database.TemplateDropUserMapping().v_text,
                'create_type': v_database.TemplateCreateType().v_text,
                'alter_type': v_database.TemplateAlterType().v_text,
                'drop_type': v_database.TemplateDropType().v_text,
                'create_domain': v_database.TemplateCreateDomain().v_text,
                'alter_domain': v_database.TemplateAlterDomain().v_text,
                'drop_domain': v_database.TemplateDropDomain().v_text,
            }
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_database_objects(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = {}
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_properties(request):

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
    v_tab_id = json_object['p_tab_id']
    v_data = json_object['p_data']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_properties = []
    v_ddl = ''

    try:
        v_properties = v_database.GetProperties(v_data['p_schema'],v_data['p_table'],v_data['p_object'],v_data['p_type'])
        for v_property in v_properties.Rows:
            v_list_properties.append([v_property['Property'],v_property['Value']])
        v_ddl = v_database.GetDDL(v_data['p_schema'],v_data['p_table'],v_data['p_object'],v_data['p_type'])
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'properties': v_list_properties,
        'ddl': v_ddl
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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            if v_table['is_partition'] == 'False' and v_table['is_partitioned'] == 'False':
                v_icon = 'table'
            elif v_table['is_partition'] == 'False' and v_table['is_partitioned'] == 'True':
                v_icon = 'table_partitioned'
            elif v_table['is_partition'] == 'True' and v_table['is_partitioned'] == 'False':
                v_icon = 'table_partition'
            else:
                v_icon = 'table_partitioned_partition'

            v_table_data = {
                'v_name': v_table['table_name'],
                'v_icon': v_icon,
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
                'v_nullable': v_column['nullable']
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_pk = []

    try:
        v_pks = v_database.QueryTablesPrimaryKeys(v_table, False, v_schema)
        for v_pk in v_pks.Rows:
            v_pk_data = []
            v_pk_data.append(v_pk['constraint_name'])
            v_list_pk.append(v_pk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_pk

    return JsonResponse(v_return)

def get_pk_columns(request):

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
    v_tab_id = json_object['p_tab_id']
    v_pkey = json_object['p_key']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_pk = []

    try:
        v_pks = v_database.QueryTablesPrimaryKeysColumns(v_pkey, v_table, False, v_schema)
        for v_pk in v_pks.Rows:
            v_pk_data = []
            v_pk_data.append(v_pk['column_name'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_fk_data.append(v_fk['constraint_name'])
            v_fk_data.append(v_fk['r_table_name'])
            v_fk_data.append(v_fk['delete_rule'])
            v_fk_data.append(v_fk['update_rule'])
            v_list_fk.append(v_fk_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fk

    return JsonResponse(v_return)

def get_fks_columns(request):

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
    v_tab_id = json_object['p_tab_id']
    v_fkey = json_object['p_fkey']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fk = []

    try:
        v_fks = v_database.QueryTablesForeignKeysColumns(v_fkey, v_table, False, v_schema)
        for v_fk in v_fks.Rows:
            v_fk_data = []
            v_fk_data.append(v_fk['r_table_name'])
            v_fk_data.append(v_fk['delete_rule'])
            v_fk_data.append(v_fk['update_rule'])
            v_fk_data.append(v_fk['column_name'])
            v_fk_data.append(v_fk['r_column_name'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_uniques = []

    try:
        v_uniques = v_database.QueryTablesUniques(v_table, False, v_schema)
        for v_unique in v_uniques.Rows:
            v_unique_data = []
            v_unique_data.append(v_unique['constraint_name'])
            v_list_uniques.append(v_unique_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_uniques

    return JsonResponse(v_return)

def get_uniques_columns(request):

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
    v_tab_id = json_object['p_tab_id']
    v_unique = json_object['p_unique']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_uniques = []

    try:
        v_uniques = v_database.QueryTablesUniquesColumns(v_unique, v_table, False, v_schema)
        for v_unique in v_uniques.Rows:
            v_unique_data = []
            v_unique_data.append(v_unique['column_name'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_index_data.append(v_index['index_name'])
            v_index_data.append(v_index['uniqueness'])
            v_list_indexes.append(v_index_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_indexes

    return JsonResponse(v_return)

def get_indexes_columns(request):

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
    v_tab_id = json_object['p_tab_id']
    v_index = json_object['p_index']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_indexes = []

    try:
        v_indexes = v_database.QueryTablesIndexesColumns(v_index, v_table, False, v_schema)
        for v_index in v_indexes.Rows:
            v_index_data = []
            v_index_data.append(v_index['column_name'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_check_data.append(v_check['constraint_name'])
            v_check_data.append(v_check['constraint_source'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_exclude_data.append(v_exclude['constraint_name'])
            v_exclude_data.append(v_exclude['attributes'])
            v_exclude_data.append(v_exclude['operations'])
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_rule_data.append(v_rule['rule_name'])
            v_list_rules.append(v_rule_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_rules

    return JsonResponse(v_return)

def get_rule_definition(request):

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
    v_tab_id = json_object['p_tab_id']
    v_rule = json_object['p_rule']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetRuleDefinition(v_rule, v_table, v_schema)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_trigger_data = {
                'v_name': v_trigger['trigger_name'],
                'v_enabled': v_trigger['trigger_enabled'],
                'v_function': v_trigger['trigger_function'],
                'v_id': v_trigger['id']
            }
            v_list_triggers.append(v_trigger_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_triggers

    return JsonResponse(v_return)

def get_inheriteds(request):

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_partitions = []

    try:
        v_partitions = v_database.QueryTablesInheriteds(v_table,False,v_schema)
        for v_partition in v_partitions.Rows:
            v_partition_data = []
            v_partition_data.append(v_partition['child_schema'] + '.' + v_partition['child_table'])
            v_list_partitions.append(v_partition_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_partitions

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
            v_partition_data.append(v_partition['child_schema'] + '.' + v_partition['child_table'])
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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_table['table_name'],
                'v_has_rules': v_database.v_has_rules,
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
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
    v_tab_id = json_object['p_tab_id']
    v_view = json_object['p_view']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_table['table_name'],
                'v_has_indexes': v_database.v_has_indexes
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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
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
    v_tab_id = json_object['p_tab_id']
    v_view = json_object['p_view']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
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
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_database['database_name']
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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_tablespace['tablespace_name']
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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_role['role_name']
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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_function['name'],
                'v_id': v_function['id']
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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_function']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_field['name'],
                'v_type': v_field['type']
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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_function']

    v_database = v_session.v_tab_connections[v_tab_id]

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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_function']

    v_database = v_session.v_tab_connections[v_tab_id]

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

def get_procedures(request):

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_functions = []

    try:
        v_functions = v_database.QueryProcedures(False,v_schema)
        for v_function in v_functions.Rows:
            v_function_data = {
                'v_name': v_function['name'],
                'v_id': v_function['id']
            }
            v_list_functions.append(v_function_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_functions

    return JsonResponse(v_return)

def get_procedure_fields(request):

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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_procedure']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fields = []

    try:
        v_fields = v_database.QueryProcedureFields(v_function,v_schema)
        for v_field in v_fields.Rows:
            v_field_data = {
                'v_name': v_field['name'],
                'v_type': v_field['type']
            }
            v_list_fields.append(v_field_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
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
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_procedure']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetProcedureDefinition(v_function)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_procedure_debug(request):

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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_procedure']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_return['v_data'] = v_database.GetProcedureDebug(v_function)
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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_name': v_function['name'],
                'v_id': v_function['id']
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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_function']

    v_database = v_session.v_tab_connections[v_tab_id]

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

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
                'v_sequence_name': v_sequence['sequence_name']
            }
            v_list_sequences.append(v_sequence_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_sequences

    return JsonResponse(v_return)

def get_extensions(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_extensions = []

    try:
        v_extensions = v_database.QueryExtensions()
        for v_extension in v_extensions.Rows:
            v_extension_data = {
                'v_name': v_extension['extension_name']
            }
            v_list_extensions.append(v_extension_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_extensions

    return JsonResponse(v_return)

def get_physicalreplicationslots(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_repslots = []

    try:
        v_repslots = v_database.QueryPhysicalReplicationSlots()
        for v_repslot in v_repslots.Rows:
            v_repslot_data = {
                'v_name': v_repslot['slot_name']
            }
            v_list_repslots.append(v_repslot_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repslots

    return JsonResponse(v_return)

def get_logicalreplicationslots(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_repslots = []

    try:
        v_repslots = v_database.QueryLogicalReplicationSlots()
        for v_repslot in v_repslots.Rows:
            v_repslot_data = {
                'v_name': v_repslot['slot_name']
            }
            v_list_repslots.append(v_repslot_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repslots

    return JsonResponse(v_return)

def get_publications(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_pubs = []

    try:
        v_pubs = v_database.QueryPublications()
        for v_pub in v_pubs.Rows:
            v_pub_data = {
                'v_name': v_pub['pubname'],
                'v_alltables': v_pub['puballtables'],
                'v_insert': v_pub['pubinsert'],
                'v_update': v_pub['pubupdate'],
                'v_delete': v_pub['pubdelete'],
                'v_truncate': v_pub['pubtruncate']
            }
            v_list_pubs.append(v_pub_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_pubs

    return JsonResponse(v_return)

def get_publication_tables(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]
    v_pub = json_object['p_pub']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryPublicationTables(v_pub)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name']
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_subscriptions(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_subs = []

    try:
        v_subs = v_database.QuerySubscriptions()
        for v_sub in v_subs.Rows:
            v_sub_data = {
                'v_name': v_sub['subname'],
                'v_enabled': v_sub['subenabled'],
                'v_conninfo': v_sub['subconninfo'],
                'v_publications': v_sub['subpublications']
            }
            v_list_subs.append(v_sub_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_subs

    return JsonResponse(v_return)

def get_subscription_tables(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]
    v_sub = json_object['p_sub']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QuerySubscriptionTables(v_sub)
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name']
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_foreign_data_wrappers(request):

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
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_fdws = []

    try:
        v_fdws = v_database.QueryForeignDataWrappers()
        for v_fdw in v_fdws.Rows:
            v_fdw_data = {
                'v_name': v_fdw['fdwname']
            }
            v_list_fdws.append(v_fdw_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_fdws

    return JsonResponse(v_return)

def get_foreign_servers(request):

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
    v_tab_id = json_object['p_tab_id']
    v_fdw = json_object['p_fdw']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_servers = []

    try:
        v_servers = v_database.QueryForeignServers(v_fdw)
        for v_server in v_servers.Rows:
            v_server_data = {
                'v_name': v_server['srvname'],
                'v_type': v_server['srvtype'],
                'v_version': v_server['srvversion'],
                'v_options': v_server['srvoptions']
            }
            v_list_servers.append(v_server_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_servers

    return JsonResponse(v_return)

def get_user_mappings(request):

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
    v_tab_id = json_object['p_tab_id']
    v_foreign_server = json_object['p_foreign_server']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_mappings = []

    try:
        v_mappings = v_database.QueryUserMappings(v_foreign_server)
        for v_mapping in v_mappings.Rows:
            v_mapping_data = {
                'v_name': v_mapping['rolname'],
                'v_options': v_mapping['umoptions']
            }
            v_list_mappings.append(v_mapping_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_mappings

    return JsonResponse(v_return)

def get_foreign_tables(request):

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryForeignTables(False,v_schema)
        for v_table in v_tables.Rows:
            if v_table['is_partition'] == 'False' and v_table['is_partitioned'] == 'False':
                v_icon = 'table'
            elif v_table['is_partition'] == 'False' and v_table['is_partitioned'] == 'True':
                v_icon = 'table_partitioned'
            elif v_table['is_partition'] == 'True' and v_table['is_partitioned'] == 'False':
                v_icon = 'table_partition'
            else:
                v_icon = 'table_partitioned_partition'

            v_table_data = {
                'v_name': v_table['table_name'],
                'v_icon': v_icon
            }
            v_list_tables.append(v_table_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_tables

    return JsonResponse(v_return)

def get_foreign_columns(request):

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_columns = []

    try:
        v_columns = v_database.QueryForeignTablesFields(v_table,False,v_schema)
        for v_column in v_columns.Rows:
            v_column_data = {
                'v_column_name': v_column['column_name'],
                'v_data_type': v_column['data_type'],
                'v_data_length': v_column['data_length'],
                'v_nullable': v_column['nullable'],
                'v_options': v_column['attfdwoptions'],
                'v_tableoptions': v_column['ftoptions'],
                'v_server': v_column['srvname'],
                'v_fdw': v_column['fdwname']
            }
            v_list_columns.append(v_column_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_columns

    return JsonResponse(v_return)


def get_types(request):

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_types = []

    try:
        v_types = v_database.QueryTypes(False,v_schema)
        for v_type in v_types.Rows:
            v_type_data = {
                'v_type_name': v_type['type_name']
            }
            v_list_types.append(v_type_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_types

    return JsonResponse(v_return)


def get_domains(request):

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
    v_tab_id = json_object['p_tab_id']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_domains = []

    try:
        v_domains = v_database.QueryDomains(False,v_schema)
        for v_domain in v_domains.Rows:
            v_domain_data = {
                'v_domain_name': v_domain['domain_name']
            }
            v_list_domains.append(v_domain_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_domains

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
    v_tab_id = json_object['p_tab_id']
    v_pid            = json_object['p_pid']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_database.v_connection.Terminate(v_pid)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def template_select(request):

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']
    v_kind = json_object['p_kind']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_template = v_database.TemplateSelect(v_schema, v_table, v_kind).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

def template_insert(request):

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_template = v_database.TemplateInsert(v_schema, v_table).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

def template_update(request):

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
    v_tab_id = json_object['p_tab_id']
    v_table = json_object['p_table']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_template = v_database.TemplateUpdate(v_schema, v_table).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

def template_select_function(request):

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
    v_tab_id = json_object['p_tab_id']
    v_function = json_object['p_function']
    v_functionid = json_object['p_functionid']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_template = v_database.TemplateSelectFunction(v_schema, v_function, v_functionid).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)

def template_call_procedure(request):

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
    v_tab_id = json_object['p_tab_id']
    v_procedure = json_object['p_procedure']
    v_procedureid = json_object['p_procedureid']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_template = v_database.TemplateCallProcedure(v_schema, v_procedure, v_procedureid).v_text
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_template': v_template
    }

    return JsonResponse(v_return)
