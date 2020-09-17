from enum import Enum

class TemplateType(Enum):
    EXECUTE = 1
    SCRIPT = 2

class Template:
    def __init__(self, p_text, p_type=TemplateType.EXECUTE):
        self.v_text = p_text
        self.v_type = p_type

def GetBDRVersion(p_database_object):
    return p_database_object.v_connection.ExecuteScalar('''
        select extversion
        from pg_extension
        where extname = 'bdr'
    ''')

def GetBDRNodeName(p_database_object):
    return p_database_object.v_connection.ExecuteScalar('select bdr.bdr_get_local_node_name()')

def QueryBDRProperties(p_database_object):
    try:
        v_tmp = p_database_object.v_connection.ExecuteScalar('select bdr.bdr_is_active_in_db()')
        v_test = True
    except Spartacus.Database.Exception as exc:
        v_test = False
    if v_test:
        return p_database_object.v_connection.Query('''
            select bdr.bdr_version() as version,
                   bdr.bdr_is_active_in_db() as active,
                   coalesce(bdr.bdr_get_local_node_name(), 'Not set') as node_name,
                   bdr.bdr_apply_is_paused() as paused,
                   null as node_state
        ''')
    else:
        return p_database_object.v_connection.Query('''
            select bdr.bdr_version() as version,
                   (coalesce(bdr.bdr_get_local_node_name(), 'Not set') != 'Not set') as active,
                   coalesce(bdr.bdr_get_local_node_name(), 'Not set') as node_name,
                   bdr.bdr_apply_is_paused() as paused,
                   null as node_state
        ''')

def QueryBDRNodes(p_database_object):
    return p_database_object.v_connection.Query('''
        select quote_ident(node_name) as node_name,
               bdr.bdr_get_local_node_name() = node_name as node_is_local
        from bdr.bdr_nodes
        where node_status <> 'k'
        order by 1
    ''')

def QueryBDRReplicationSets(p_database_object):
    return p_database_object.v_connection.Query('''
        select quote_ident(set_name) as set_name,
               replicate_inserts,
               replicate_updates,
               replicate_deletes
        from bdr.bdr_replication_set_config
        order by 1
    ''')

def QueryBDRTableReplicationSets(p_database_object, p_table):
    return p_database_object.v_connection.Query("select unnest(bdr.table_get_replication_sets('{0}')) as set_name".format(p_table))

def QueryBDRTableConflictHandlers(p_database_object, p_table, p_schema):
    return p_database_object.v_connection.Query('''
        select quote_ident(t.ch_name) as ch_name,
               t.ch_type::text as ch_type,
               t.ch_fun::text as ch_fun
        from bdr.bdr_conflict_handlers t
        inner join pg_class c
        on c.oid = t.ch_reloid
        inner join pg_namespace n
        on n.oid = c.relnamespace
        where n.nspname = '{0}'
          and c.relname = '{1}'
    '''.format(p_schema, p_table))

def TemplateBDRCreateGroup(p_database_object):
    return Template('''select bdr.bdr_group_create(
local_node_name := 'node_name'
, node_external_dsn := 'host={0} port={1} dbname={2}'
, node_local_dsn := 'dbname={2}'
--, apply_delay := NULL
--, replication_sets := ARRAY['default']
)
'''.format(p_database_object.v_server, p_database_object.v_port, p_database_object.v_service))

def TemplateBDRJoinGroup(p_database_object):
    return Template('''select bdr.bdr_group_join(
local_node_name := 'node_name'
, node_external_dsn := 'host={0} port={1} dbname={2}'
, join_using_dsn := 'host= port= dbname='
, node_local_dsn := 'dbname={2}'
--, apply_delay := NULL
--, replication_sets := ARRAY['default']
)
'''.format(p_database_object.v_server, p_database_object.v_port, p_database_object.v_service))

def TemplateBDRJoinWait(p_database_object):
    return Template('select bdr.bdr_node_join_wait_for_ready()')

def TemplateBDRPause(p_database_object):
    return Template('select bdr.bdr_apply_pause()')

def TemplateBDRResume(p_database_object):
    return Template('select bdr.bdr_apply_resume()')

def TemplateBDRReplicateDDLCommand(p_database_object):
    return Template("select bdr.bdr_replicate_ddl_command('DDL command here...')")

def TemplateBDRPartNode(p_database_object):
    return Template("select bdr.bdr_part_by_node_names('{#node_name#}')")

def TemplateBDRInsertReplicationSet(p_database_object):
    return Template('''INSERT INTO bdr.bdr_replication_set_config (set_name, replicate_inserts, replicate_updates, replicate_deletes)
VALUES ('set_name', 't', 't', 't')
''')

def TemplateBDRUpdateReplicationSet(p_database_object):
    return Template('''UPDATE bdr.bdr_replication_set_config SET
--replicate_inserts = { 't' | 'f' }
--, replicate_updates = { 't' | 'f' }
--, replicate_deletes = { 't' | 'f' }
WHERE set_name = '#set_name#'
''')

def TemplateBDRDeleteReplicationSet(p_database_object):
    return Template('''DELETE
FROM bdr.bdr_replication_set_config
WHERE set_name = '#set_name#'
''')

def TemplateBDRSetTableReplicationSets(p_database_object):
    return Template("select bdr.table_set_replication_sets('#table_name#', '{repset1,repset2,...}')")

def TemplateBDRCreateConflictHandler(p_database_object):
    return Template('''CREATE OR REPLACE FUNCTION #table_name#_fnc_conflict_handler (
row1 #table_name#,
row2 #table_name#,
table_name text,
table_regclass regclass,
conflict_type bdr.bdr_conflict_type, /* [insert_insert | insert_update | update_update | update_delete | delete_delete | unhandled_tx_abort] */
OUT row_out #table_name#,
OUT handler_action bdr.bdr_conflict_handler_action) /* [IGNORE | ROW | SKIP] */
RETURNS record AS
$BODY$
BEGIN
raise warning 'conflict detected for #table_name#, old_row: %, incoming_row: %', row1, row2;
-- sample code to choose the output row or to merge values
row_out := row1;
handler_action := 'ROW';
END;
$BODY$
LANGUAGE plpgsql;

-- after writing the handler procedure we also need to register it as an handler
select *
from bdr.bdr_create_conflict_handler(
ch_rel := '#table_name#',
ch_name := '#table_name#_conflict_handler',
ch_proc := '#table_name#_fnc_conflict_handler(#table_name#, #table_name#, text, regclass, bdr.bdr_conflict_type)',
ch_type := 'insert_insert' /* [insert_insert | insert_update | update_update | update_delete | delete_delete | unhandled_tx_abort] */
)
''')

def TemplateBDRDropConflictHandler(p_database_object):
    return Template("select bdr.bdr_drop_conflict_handler('#table_name#', '#ch_name#')")

def TemplateBDRTerminateApplyWorkers(p_database_object):
    return Template("select bdr.terminate_apply_workers('{#node_name#}')")

def TemplateBDRTerminateWalsenderWorkers(p_database_object):
    return Template("select bdr.terminate_walsender_workers('{#node_name#}')")

def TemplateBDRRemove(p_database_object):
    return Template('''select bdr.remove_bdr_from_local_node(
force := False
, convert_global_sequences := True
)
''')
