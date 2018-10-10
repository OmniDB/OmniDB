import OmniDB_app.plugins.bdr.metadata as metadata

def get_bdr_version(p_database_object, p_data):
    return { 'bdr_version': metadata.GetBDRVersion(p_database_object) }

def get_bdr_templates(p_database_object, p_data):
    return {
        'bdr_create_group': metadata.TemplateBDRCreateGroup(p_database_object).v_text,
        'bdr_join_group': metadata.TemplateBDRJoinGroup(p_database_object).v_text,
        'bdr_join_wait': metadata.TemplateBDRJoinWait(p_database_object).v_text,
        'bdr_pause': metadata.TemplateBDRPause(p_database_object).v_text,
        'bdr_resume': metadata.TemplateBDRResume(p_database_object).v_text,
        'bdr_replicate_ddl_command': metadata.TemplateBDRReplicateDDLCommand(p_database_object).v_text,
        'bdr_part_node': metadata.TemplateBDRPartNode(p_database_object).v_text,
        'bdr_insert_repset': metadata.TemplateBDRInsertReplicationSet(p_database_object).v_text,
        'bdr_update_repset': metadata.TemplateBDRUpdateReplicationSet(p_database_object).v_text,
        'bdr_delete_repset': metadata.TemplateBDRDeleteReplicationSet(p_database_object).v_text,
        'bdr_set_repsets': metadata.TemplateBDRSetTableReplicationSets(p_database_object).v_text,
        'bdr_create_confhand': metadata.TemplateBDRCreateConflictHandler(p_database_object).v_text,
        'bdr_drop_confhand': metadata.TemplateBDRDropConflictHandler(p_database_object).v_text,
        'bdr_terminate_apply': metadata.TemplateBDRTerminateApplyWorkers(p_database_object).v_text,
        'bdr_terminate_walsender': metadata.TemplateBDRTerminateWalsenderWorkers(p_database_object).v_text,
        'bdr_remove': metadata.TemplateBDRRemove(p_database_object).v_text
    }

def get_bdr_properties(p_database_object, p_data):
    try:
        v_list_bdr = []
        v_bdrs = metadata.QueryBDRProperties(p_database_object)
        for v_bdr in v_bdrs.Rows:
            v_bdr_data = {
                'v_version': v_bdr['version'],
                'v_active': v_bdr['active'],
                'v_node_name': v_bdr['node_name'],
                'v_paused': v_bdr['paused'],
                'v_state': v_bdr['node_state']
            }
            v_list_bdr.append(v_bdr_data)
        return v_list_bdr
    except Exception as exc:
        raise exc

def get_bdr_nodes(p_database_object, p_data):
    try:
        v_list_nodes = []
        v_nodes = metadata.QueryBDRNodes(p_database_object)
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name'],
                'v_is_local': v_node['node_is_local']
            }
            v_list_nodes.append(v_node_data)
        return v_list_nodes
    except Exception as exc:
        raise exc

def get_bdr_replicationsets(p_database_object, p_data):
    try:
        v_list_repsets = []
        v_repsets = metadata.QueryBDRReplicationSets(p_database_object)
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name'],
                'v_inserts': v_repset['replicate_inserts'],
                'v_updates': v_repset['replicate_updates'],
                'v_deletes': v_repset['replicate_deletes'],
            }
            v_list_repsets.append(v_repset_data)
        return v_list_repsets
    except Exception as exc:
        raise exc

def get_bdr_table_replicationsets(p_database_object, p_data):
    try:
        v_list_repsets = []
        v_repsets = metadata.QueryBDRTableReplicationSets(p_database_object, p_data['p_schema'] + '.' + p_data['p_table'])
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name']
            }
            v_list_repsets.append(v_repset_data)
        return v_list_repsets
    except Exception as exc:
        raise exc

def get_bdr_table_conflicthandlers(p_database_object, p_data):
    try:
        v_list_chs = []
        v_chs = metadata.QueryBDRTableConflictHandlers(p_database_object, p_data['p_table'], p_data['p_schema'])
        for v_ch in v_chs.Rows:
            v_ch_data = {
                'v_name': v_ch['ch_name'],
                'v_type': v_ch['ch_type'],
                'v_function': v_ch['ch_fun']
            }
            v_list_chs.append(v_ch_data)
        return v_list_chs
    except Exception as exc:
        raise exc
