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
                'drop_partition': v_database.TemplateDropPartition().v_text,
                'vacuum': v_database.TemplateVacuum().v_text,
                'vacuum_table': v_database.TemplateVacuumTable().v_text,
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
                'pglogical_version': v_database.GetPglogicalVersion(),
                'pglogical_create_node': v_database.TemplatePglogicalCreateNode().v_text,
                'pglogical_drop_node': v_database.TemplatePglogicalDropNode().v_text,
                'pglogical_add_interface': v_database.TemplatePglogicalNodeAddInterface().v_text,
                'pglogical_drop_interface': v_database.TemplatePglogicalNodeDropInterface().v_text,
                'pglogical_create_repset': v_database.TemplatePglogicalCreateReplicationSet().v_text,
                'pglogical_alter_repset': v_database.TemplatePglogicalAlterReplicationSet().v_text,
                'pglogical_drop_repset': v_database.TemplatePglogicalDropReplicationSet().v_text,
                'pglogical_repset_add_table': v_database.TemplatePglogicalReplicationSetAddTable().v_text,
                'pglogical_repset_add_all_tables': v_database.TemplatePglogicalReplicationSetAddAllTables().v_text,
                'pglogical_repset_remove_table': v_database.TemplatePglogicalReplicationSetRemoveTable().v_text,
                'pglogical_repset_add_seq': v_database.TemplatePglogicalReplicationSetAddSequence().v_text,
                'pglogical_repset_add_all_seqs': v_database.TemplatePglogicalReplicationSetAddAllSequences().v_text,
                'pglogical_repset_remove_seq': v_database.TemplatePglogicalReplicationSetRemoveSequence().v_text,
                'pglogical_create_sub': v_database.TemplatePglogicalCreateSubscription().v_text,
                'pglogical_enable_sub': v_database.TemplatePglogicalEnableSubscription().v_text,
                'pglogical_disable_sub': v_database.TemplatePglogicalDisableSubscription().v_text,
                'pglogical_sync_sub': v_database.TemplatePglogicalSynchronizeSubscription().v_text,
                'pglogical_drop_sub': v_database.TemplatePglogicalDropSubscription().v_text,
                'pglogical_sub_add_repset': v_database.TemplatePglogicalSubscriptionAddReplicationSet().v_text,
                'pglogical_sub_remove_repset': v_database.TemplatePglogicalSubscriptionRemoveReplicationSet().v_text,
                'bdr_version': v_database.GetBDRVersion(),
                'bdr_create_group': v_database.TemplateBDRCreateGroup().v_text,
                'bdr_join_group': v_database.TemplateBDRJoinGroup().v_text,
                'bdr_join_wait': v_database.TemplateBDRJoinWait().v_text,
                'bdr_pause': v_database.TemplateBDRPause().v_text,
                'bdr_resume': v_database.TemplateBDRResume().v_text,
                'bdr_replicate_ddl_command': v_database.TemplateBDRReplicateDDLCommand().v_text,
                'bdr_part_node': v_database.TemplateBDRPartNode().v_text,
                'bdr_insert_repset': v_database.TemplateBDRInsertReplicationSet().v_text,
                'bdr_update_repset': v_database.TemplateBDRUpdateReplicationSet().v_text,
                'bdr_delete_repset': v_database.TemplateBDRDeleteReplicationSet().v_text,
                'bdr_set_repsets': v_database.TemplateBDRSetTableReplicationSets().v_text,
                'bdr_create_confhand': v_database.TemplateBDRCreateConflictHandler().v_text,
                'bdr_drop_confhand': v_database.TemplateBDRDropConflictHandler().v_text,
                # only in BDR >= 1
                'bdr_terminate_apply': v_database.TemplateBDRTerminateApplyWorkers().v_text,
                'bdr_terminate_walsender': v_database.TemplateBDRTerminateWalsenderWorkers().v_text,
                'bdr_remove': v_database.TemplateBDRRemove().v_text,
                'xl_pause_cluster': v_database.TemplateXLPauseCluster().v_text,
                'xl_unpause_cluster': v_database.TemplateXLUnpauseCluster().v_text,
                'xl_clean_connection': v_database.TemplateXLCleanConnection().v_text,
                'xl_create_group': v_database.TemplateXLCreateGroup().v_text,
                'xl_drop_group': v_database.TemplateXLDropGroup().v_text,
                'xl_create_node': v_database.TemplateXLCreateNode().v_text,
                'xl_alter_node': v_database.TemplateXLAlterNode().v_text,
                'xl_drop_node': v_database.TemplateXLDropNode().v_text,
                'xl_execute_direct': v_database.TemplateXLExecuteDirect().v_text,
                'xl_pool_reload': v_database.TemplateXLPoolReload().v_text,
                'xl_altertable_distribution': v_database.TemplateXLAlterTableDistribution().v_text,
                'xl_altertable_location': v_database.TemplateXLAlterTableLocation().v_text,
                'xl_altertable_addnode': v_database.TemplateXLALterTableAddNode().v_text,
                'xl_altertable_deletenode': v_database.TemplateXLAlterTableDeleteNode().v_text
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
                'v_name': v_table['table_name'],
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
            v_pk_data.append(v_pk['constraint_name'])
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
            v_fk_data.append(v_fk['constraint_name'])
            v_fk_data.append(v_fk['column_name'])
            v_fk_data.append(v_fk['r_table_name'])
            v_fk_data.append(v_fk['r_column_name'])
            v_fk_data.append(v_fk['delete_rule'])
            v_fk_data.append(v_fk['update_rule'])
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
            v_unique_data.append(v_unique['constraint_name'])
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
            v_index_data.append(v_index['index_name'])
            v_index_data.append(v_index['uniqueness'])
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
            v_rule_data.append(v_rule['constraint_name'])
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
            v_trigger_data.append(v_trigger['trigger_name'])
            v_trigger_data.append(v_trigger['trigger_enabled'])
            v_trigger_data.append(v_trigger['trigger_function_name'])
            v_trigger_data.append(v_trigger['trigger_function_id'])
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
                'v_name': v_table['table_name'],
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
                'v_name': v_table['table_name'],
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
                'v_sequence_name': v_sequence['sequence_name']
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
                'v_minimum_value': v_value['minimum_value'],
                'v_maximum_value': v_value['maximum_value'],
                'v_current_value': v_value['current_value'],
                'v_increment': v_value['increment']
            }
            v_list_values.append(v_value_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_values

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

    v_database = v_session.v_databases[v_database_index]['database']

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

    v_database = v_session.v_databases[v_database_index]['database']

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

    v_database = v_session.v_databases[v_database_index]['database']

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

    v_database = v_session.v_databases[v_database_index]['database']

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
                'v_delete': v_pub['pubdelete']
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

    v_database = v_session.v_databases[v_database_index]['database']
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

    v_database = v_session.v_databases[v_database_index]['database']

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

    v_database = v_session.v_databases[v_database_index]['database']
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

def get_pglogical_nodes(request):

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

    v_list_nodes = []

    try:
        v_nodes = v_database.QueryPglogicalNodes()
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name']
            }
            v_list_nodes.append(v_node_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_nodes

    return JsonResponse(v_return)

def get_pglogical_interfaces(request):

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
    v_node = json_object['p_node']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_ifaces = []

    try:
        v_ifaces = v_database.QueryPglogicalNodeInterfaces(v_node)
        for v_iface in v_ifaces.Rows:
            v_iface_data = {
                'v_name': v_iface['if_name'],
                'v_dsn': v_iface['if_dsn']
            }
            v_list_ifaces.append(v_iface_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_ifaces

    return JsonResponse(v_return)

def get_pglogical_replicationsets(request):

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

    v_list_repsets = []

    try:
        v_repsets = v_database.QueryPglogicalReplicationSets()
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name'],
                'v_insert': v_repset['replicate_insert'],
                'v_update': v_repset['replicate_update'],
                'v_delete': v_repset['replicate_delete'],
                'v_truncate': v_repset['replicate_truncate']
            }
            v_list_repsets.append(v_repset_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repsets

    return JsonResponse(v_return)

def get_pglogical_repset_tables(request):

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
    v_repset = json_object['p_repset']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_tables = []

    try:
        v_tables = v_database.QueryPglogicalReplicationSetTables(v_repset)
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

def get_pglogical_repset_seqs(request):

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
    v_repset = json_object['p_repset']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_seqs = []

    try:
        v_seqs = v_database.QueryPglogicalReplicationSetSequences(v_repset)
        for v_seq in v_seqs.Rows:
            v_seq_data = {
                'v_name': v_seq['sequence_name']
            }
            v_list_seqs.append(v_seq_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_seqs

    return JsonResponse(v_return)

def get_pglogical_subscriptions(request):

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

    v_list_subs = []

    try:
        v_subs = v_database.QueryPglogicalSubscriptions()
        for v_sub in v_subs.Rows:
            v_sub_data = {
                'v_name': v_sub['sub_name'],
                'v_status': v_sub['sub_status'],
                'v_origin': v_sub['sub_origin'],
                'v_enabled': v_sub['sub_enabled'],
                'v_delay': v_sub['sub_apply_delay']
            }
            v_list_subs.append(v_sub_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_subs

    return JsonResponse(v_return)

def get_pglogical_subscription_repsets(request):

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
    v_sub = json_object['p_sub']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_repsets = []

    try:
        v_repsets = v_database.QueryPglogicalSubscriptionReplicationSets(v_sub)
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name']
            }
            v_list_repsets.append(v_repset_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repsets

    return JsonResponse(v_return)

def get_bdr_properties(request):

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

    v_list_bdr = []

    try:
        v_bdrs = v_database.QueryBDRProperties()
        for v_bdr in v_bdrs.Rows:
            v_bdr_data = {
                'v_version': v_bdr['version'],
                'v_active': v_bdr['active'],
                'v_node_name': v_bdr['node_name'],
                'v_paused': v_bdr['paused']
            }
            v_list_bdr.append(v_bdr_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_bdr

    return JsonResponse(v_return)

def get_bdr_nodes(request):

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

    v_list_nodes = []

    try:
        v_nodes = v_database.QueryBDRNodes()
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name']
            }
            v_list_nodes.append(v_node_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_nodes

    return JsonResponse(v_return)

def get_bdr_replicationsets(request):

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

    v_list_repsets = []

    try:
        v_repsets = v_database.QueryBDRReplicationSets()
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name'],
                'v_inserts': v_repset['replicate_inserts'],
                'v_updates': v_repset['replicate_updates'],
                'v_deletes': v_repset['replicate_deletes'],
            }
            v_list_repsets.append(v_repset_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repsets

    return JsonResponse(v_return)

def get_bdr_table_replicationsets(request):

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
    v_schema = json_object['p_schema']
    v_table = json_object['p_table']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_repsets = []

    try:
        v_repsets = v_database.QueryBDRTableReplicationSets(v_schema + '.' + v_table)
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name']
            }
            v_list_repsets.append(v_repset_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_repsets

    return JsonResponse(v_return)

def get_bdr_table_conflicthandlers(request):

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
    v_schema = json_object['p_schema']
    v_table = json_object['p_table']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_chs = []

    try:
        v_chs = v_database.QueryBDRTableConflictHandlers(v_table, v_schema)
        for v_ch in v_chs.Rows:
            v_ch_data = {
                'v_name': v_ch['ch_name'],
                'v_type': v_ch['ch_type'],
                'v_function': v_ch['ch_fun']
            }
            v_list_chs.append(v_ch_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_chs

    return JsonResponse(v_return)

def get_xl_nodes(request):

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

    v_list_nodes = []

    try:
        v_nodes = v_database.QueryXLNodes()
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name'],
                'v_type': v_node['node_type'],
                'v_host': v_node['node_host'],
                'v_port': v_node['node_port'],
                'v_primary': v_node['nodeis_primary'],
                'v_preferred': v_node['nodeis_preferred'],
            }
            v_list_nodes.append(v_node_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_nodes

    return JsonResponse(v_return)

def get_xl_groups(request):

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

    v_list_groups = []

    try:
        v_groups = v_database.QueryXLGroups()
        for v_group in v_groups.Rows:
            v_group_data = {
                'v_name': v_group['group_name']
            }
            v_list_groups.append(v_group_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_groups

    return JsonResponse(v_return)

def get_xl_group_nodes(request):

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
    v_group = json_object['p_group']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_nodes = []

    try:
        v_nodes = v_database.QueryXLGroupNodes(v_group)
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name']
            }
            v_list_nodes.append(v_node_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_nodes

    return JsonResponse(v_return)

def get_xl_table_properties(request):

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
    v_table = json_object['p_table']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_props = []

    try:
        v_props = v_database.QueryTablesXLProperties(v_table, False, v_schema)
        for v_prop in v_props.Rows:
            v_prop_data = {
                'v_distributed_by': v_prop['distributed_by'],
                'v_all_nodes': v_prop['all_nodes']
            }
            v_list_props.append(v_prop_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_props

    return JsonResponse(v_return)

def get_xl_table_nodes(request):

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
    v_table = json_object['p_table']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_list_nodes = []

    try:
        v_nodes = v_database.QueryTablesXLNodes(v_table, False, v_schema)
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name']
            }
            v_list_nodes.append(v_node_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = v_list_nodes

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
        v_database.Terminate(v_pid)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
