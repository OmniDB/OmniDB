from enum import Enum

class TemplateType(Enum):
    EXECUTE = 1
    SCRIPT = 2

class Template:
    def __init__(self, p_text, p_type=TemplateType.EXECUTE):
        self.v_text = p_text
        self.v_type = p_type

def GetBDR3Version(p_database_object):
    return p_database_object.v_connection.ExecuteScalar('''
        select extversion
        from pg_extension
        where extname = 'bdr'
    ''')

def GetBDR3NodeName(p_database_object):
    return p_database_object.v_connection.ExecuteScalar('''
        select quote_ident(n.node_name) as node_name
        from bdr.node b
        inner join pglogical.node n
        on n.node_id = b.node_id
        inner join pglogical.local_node l
        on l.node_id = n.node_id
        where bdr.peer_state_name(b.node_state) not like '%PART%'
        limit 1
    ''')

def QueryBDR3Properties(p_database_object):
    return p_database_object.v_connection.Query('''
        select (select extversion
                from pg_extension
                where extname = 'bdr') as version,
               (select count(*)
                from bdr.node b
                inner join bdr.node_group g
                on g.node_group_id = b.node_group_id
                inner join pglogical.node n
                on n.node_id = b.node_id
                inner join pglogical.local_node l
                on l.node_id = n.node_id
                where bdr.peer_state_name(b.node_state) not like '%PART%'
                limit 1) >= 1 as active,
               coalesce((select quote_ident(n.node_name)
                         from bdr.node b
                         inner join pglogical.node n
                         on n.node_id = b.node_id
                         inner join pglogical.local_node l
                         on l.node_id = n.node_id
                         where bdr.peer_state_name(b.node_state) not like '%PART%'
                         limit 1), 'Not set') as node_name,
               False as paused,
               (select bdr.peer_state_name(b.node_state)
                from bdr.node b
                inner join pglogical.node n
                on n.node_id = b.node_id
                inner join pglogical.local_node l
                on l.node_id = n.node_id
                where bdr.peer_state_name(b.node_state) not like '%PART%'
                limit 1) as node_state
    ''')

def QueryBDR3Groups(p_database_object):
    return p_database_object.v_connection.Query('''
        select quote_ident(node_group_name) as group_name
        from bdr.node_group
        order by 1
    ''')

def QueryBDR3GroupNodes(p_database_object, p_group):
    return p_database_object.v_connection.Query('''
        select quote_ident(n.node_name) || (case when l.node_id is not null then ' (local)' else '' end) as node_name,
               bdr.peer_state_name(b.node_state) as node_state,
               l.node_id is not null as node_is_local
        from bdr.node b
        inner join bdr.node_group g
        on g.node_group_id = b.node_group_id
        inner join pglogical.node n
        on n.node_id = b.node_id
        left join pglogical.local_node l
        on l.node_id = n.node_id
        where bdr.peer_state_name(b.node_state) not like '%PART%'
          and g.node_group_name = '{0}'
        order by 1
    '''.format(p_group))

def QueryBDR3ReplicationSets(p_database_object):
    return p_database_object.v_connection.Query('''
        select quote_ident(set_name) as set_name,
               replicate_insert,
               replicate_update,
               replicate_delete,
               replicate_truncate,
               set_autoadd_tables,
               set_autoadd_seqs
        from pglogical.replication_set
        where set_isinternal
        order by 1
    ''')

def QueryBDR3ReplicationSetTables(p_database_object, p_repset):
    return p_database_object.v_connection.Query('''
        select quote_ident(n.nspname) || '.' || quote_ident(c.relname) as table_name
        from pglogical.replication_set_table t
        inner join pglogical.replication_set r
        on r.set_id = t.set_id
        inner join pg_class c
        on c.oid = t.set_reloid
        inner join pg_namespace n
        on n.oid = c.relnamespace
        where quote_ident(r.set_name) = '{0}'
        order by 1
    '''.format(p_repset))

def QueryBDR3Subscriptions(p_database_object):
    return p_database_object.v_connection.Query('''
        select quote_ident(s.sub_name) as sub_name,
               (select status from pglogical.show_subscription_status(s.sub_name)) as sub_status,
               quote_ident(n.node_name) as sub_origin,
               s.sub_enabled,
               s.sub_apply_delay::text as sub_apply_delay
        from pglogical.subscription s
        inner join pglogical.node n
        on n.node_id = s.sub_origin
        inner join bdr.subscription b
        on b.pgl_subscription_id = s.sub_id
        order by 1
    ''')

def QueryBDR3SubscriptionReplicationSets(p_database_object, p_subscription):
    return p_database_object.v_connection.Query('''
        select quote_ident(unnest(s.sub_replication_sets)) as set_name
        from pglogical.subscription s
        inner join pglogical.node n
        on n.node_id = s.sub_origin
        inner join bdr.subscription b
        on b.pgl_subscription_id = s.sub_id
        where quote_ident(s.sub_name) = '{0}'
    '''.format(p_subscription))

def TemplateBDR3CreateLocalNode(p_database_object):
    return Template('''select bdr.create_node(
'node_name'
, 'host={0} port={1} dbname={2}'
)
'''.format(p_database_object.v_server, p_database_object.v_port, p_database_object.v_service))

def TemplateBDR3PromoteLocalNode(p_database_object):
    return Template('select bdr.promote_node()')

def TemplateBDR3CreateGroup(p_database_object):
    return Template('''select bdr.create_node_group('group_name')''')

def TemplateBDR3JoinGroup(p_database_object):
    return Template('''select bdr.join_node_group(
join_target_dsn := 'host= port= dbname='
, node_group_name := 'group_name'
--, pause_in_standby := false
)
''')

def TemplateBDR3JoinWait(p_database_object):
    return Template('''select bdr.wait_for_join_completion(
-- verbose_progress := false
)
''')

def TemplateBDR3ReplicateDDLCommand(p_database_object):
    return Template('''select bdr.replicate_ddl_command(
$$ DDL command here... $$
--, replication_sets := null::text[]
)
''')

def TemplateBDR3PartNode(p_database_object):
    return Template('''select bdr.part_node(
node_name := '#node_name#'
--, wait_for_completion := true
)
''')

def TemplateBDR3AlterNodeReplicationSets(p_database_object):
    return Template('''select bdr.alter_node_replication_sets(
node_name := '#node_name#',
set_names := null::text[])
''')

def TemplateBDR3CreateReplicationSet(p_database_object):
    return Template('''select bdr.create_replication_set(
set_name := 'name',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true,
autoadd_tables := false,
autoadd_existing := true
)''')

def TemplateBDR3AlterReplicationSet(p_database_object):
    return Template('''select bdr.alter_replication_set(
set_name := '#repset_name#',
replicate_insert := true,
replicate_update := true,
replicate_delete := true,
replicate_truncate := true,
autoadd_tables := false
)''')

def TemplateBDR3DropReplicationSet(p_database_object):
    return Template('''select bdr.drop_replication_set(
set_name := '#repset_name#'
)''')

def TemplateBDR3ReplicationSetAddTable(p_database_object):
    return Template('''select bdr.replication_set_add_table(
relation := 'schema.table'::regclass,
set_name := '#repset_name#'
)''')

def TemplateBDR3ReplicationSetRemoveTable(p_database_object):
    return Template('''select bdr.replication_set_remove_table(
relation := '#table_name#'::regclass,
set_name := '#repset_name#'
)''')

def TemplateBDR3AlterSequenceKind(p_database_object):
    return Template('''select bdr.alter_sequence_set_kind(
seqoid := '#seq_name#'::regclass,
seqkind := 'timeshard'
--seqkind := 'local'
)''')
