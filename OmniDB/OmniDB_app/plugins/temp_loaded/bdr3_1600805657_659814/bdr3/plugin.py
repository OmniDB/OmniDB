from . import metadata as metadata

def get_bdr3_version(p_database_object, p_data):
    return { 'bdr3_version': metadata.GetBDR3Version(p_database_object) }

def get_bdr3_templates(p_database_object, p_data):
    return {
        'bdr3_create_local_node': metadata.TemplateBDR3CreateLocalNode(p_database_object).v_text,
        'bdr3_promote_local_node': metadata.TemplateBDR3PromoteLocalNode(p_database_object).v_text,
        'bdr3_create_group': metadata.TemplateBDR3CreateGroup(p_database_object).v_text,
        'bdr3_join_group': metadata.TemplateBDR3JoinGroup(p_database_object).v_text,
        'bdr3_join_wait': metadata.TemplateBDR3JoinWait(p_database_object).v_text,
        'bdr3_replicate_ddl_command': metadata.TemplateBDR3ReplicateDDLCommand(p_database_object).v_text,
        'bdr3_alter_node_repsets': metadata.TemplateBDR3AlterNodeReplicationSets(p_database_object).v_text,
        'bdr3_part_node': metadata.TemplateBDR3PartNode(p_database_object).v_text,
        'bdr3_create_repset': metadata.TemplateBDR3CreateReplicationSet(p_database_object).v_text,
        'bdr3_alter_repset': metadata.TemplateBDR3AlterReplicationSet(p_database_object).v_text,
        'bdr3_drop_repset': metadata.TemplateBDR3DropReplicationSet(p_database_object).v_text,
        'bdr3_repset_add_table': metadata.TemplateBDR3ReplicationSetAddTable(p_database_object).v_text,
        'bdr3_repset_remove_table': metadata.TemplateBDR3ReplicationSetRemoveTable(p_database_object).v_text,
        'bdr3_alter_seq_kind': metadata.TemplateBDR3AlterSequenceKind(p_database_object).v_text,
    }

def get_bdr3_properties(p_database_object, p_data):
    try:
        v_list_bdr = []
        v_bdrs = metadata.QueryBDR3Properties(p_database_object)
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

def get_bdr3_groups(p_database_object, p_data):
    try:
        v_list_nodes = []
        v_nodes = metadata.QueryBDR3Groups(p_database_object)
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['group_name']
            }
            v_list_nodes.append(v_node_data)
        return v_list_nodes
    except Exception as exc:
        raise exc

def get_bdr3_group_nodes(p_database_object, p_data):
    try:
        v_list_nodes = []
        v_nodes = metadata.QueryBDR3GroupNodes(p_database_object, p_data['p_group'])
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_name': v_node['node_name'],
                'v_state': v_node['node_state'],
                'v_is_local': v_node['node_is_local']
            }
            v_list_nodes.append(v_node_data)
        return v_list_nodes
    except Exception as exc:
        raise exc

def get_bdr3_replicationsets(p_database_object, p_data):
    try:
        v_list_repsets = []
        v_repsets = metadata.QueryBDR3ReplicationSets(p_database_object)
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name'],
                'v_insert': v_repset['replicate_insert'],
                'v_update': v_repset['replicate_update'],
                'v_delete': v_repset['replicate_delete'],
                'v_truncate': v_repset['replicate_truncate'],
                'v_autoadd_tables': v_repset['set_autoadd_tables'],
                'v_autoadd_seqs': v_repset['set_autoadd_seqs']
            }
            v_list_repsets.append(v_repset_data)
        return v_list_repsets
    except Exception as exc:
        raise exc

def get_bdr3_repset_tables(p_database_object, p_data):
    try:
        v_list_tables = []
        v_tables = metadata.QueryBDR3ReplicationSetTables(p_database_object, p_data['p_repset'])
        for v_table in v_tables.Rows:
            v_table_data = {
                'v_name': v_table['table_name']
            }
            v_list_tables.append(v_table_data)
        return v_list_tables
    except Exception as exc:
        raise exc

def get_bdr3_subscriptions(p_database_object, p_data):
    try:
        v_list_subs = []
        v_subs = metadata.QueryBDR3Subscriptions(p_database_object)
        for v_sub in v_subs.Rows:
            v_sub_data = {
                'v_name': v_sub['sub_name'],
                'v_status': v_sub['sub_status'],
                'v_origin': v_sub['sub_origin'],
                'v_enabled': v_sub['sub_enabled'],
                'v_delay': v_sub['sub_apply_delay']
            }
            v_list_subs.append(v_sub_data)
        return v_list_subs
    except Exception as exc:
        raise exc

def get_bdr3_subscription_repsets(p_database_object, p_data):
    try:
        v_list_repsets = []
        v_repsets = metadata.QueryBDR3SubscriptionReplicationSets(p_database_object, p_data['p_sub'])
        for v_repset in v_repsets.Rows:
            v_repset_data = {
                'v_name': v_repset['set_name']
            }
            v_list_repsets.append(v_repset_data)
        return v_list_repsets
    except Exception as exc:
        raise exc

monitoring_units = [{
'dbms': 'postgresql',
'id': 0,
'title': 'BDR write lag (seconds)',
'type': 'chart_append',
'interval': 10,
'default': False,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR write lag (seconds)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(extract(seconds from t.write_lag)::numeric + extract(minutes from t.write_lag)::numeric*60 + extract(hours from t.write_lag)::numeric*3600,2) as write_lag '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['write_lag']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 1,
'title': 'BDR flush lag (seconds)',
'type': 'chart_append',
'interval': 10,
'default': False,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR flush lag (seconds)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(extract(seconds from t.flush_lag)::numeric + extract(minutes from t.flush_lag)::numeric*60 + extract(hours from t.flush_lag)::numeric*3600,2) as flush_lag '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['flush_lag']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 2,
'title': 'BDR replay lag (seconds)',
'type': 'chart_append',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR replay lag (seconds)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(extract(seconds from t.replay_lag)::numeric + extract(minutes from t.replay_lag)::numeric*60 + extract(hours from t.replay_lag)::numeric*3600,2) as replay_lag '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['replay_lag']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 3,
'title': 'BDR write lag (MB)',
'type': 'chart_append',
'interval': 10,
'default': False,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR write lag (MB)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(t.write_lag_bytes/1048576.0,2) as write_lag_size '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['write_lag_size']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 4,
'title': 'BDR flush lag (MB)',
'type': 'chart_append',
'interval': 10,
'default': False,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR flush lag (MB)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(t.flush_lag_bytes/1048576.0,2) as flush_lag_size '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['flush_lag_size']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 5,
'title': 'BDR replay lag (MB)',
'type': 'chart_append',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR replay lag (MB)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": False
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       round(t.replay_lag_bytes/1048576.0,2) as replay_lag_size '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['replay_lag_size']]
                })
    except:
        None

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 6,
'title': 'BDR throughput',
'type': 'chart_append',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR throughput"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": True
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "MB/s"
                },
                "ticks": {
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    previous_data
except:
    previous_data = None

if previous_data != None:
    try:
        query = '''select bdr.run_on_all_nodes( ' SELECT * FROM ( ' '''
        count = 0

        for prev_element in previous_data['previous_data']:

            if count > 0:
                query = query + ''' ' UNION ALL ' '''
            query = query + '''
'SELECT origin_name || '' - '' || target_name as stream, '
'       t.write_lsn, '
'       round(pg_wal_lsn_diff(t.write_lsn,\\'\\'''' + prev_element["write_lsn"] + '''\\'\\')/(1048576.0*extract(epoch from now()::time - \\'\\'''' + prev_element["current_time"] + '''\\'\\'::time))::numeric,2) as throughput, '
'       now()::time as current_time '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND origin_name || '' - '' || target_name = \\'\\'''' + prev_element['stream'] + '''\\'\\' '
            '''
            count = count + 1
        query = query + ''' ' ) x ' ) '''
        lag = connection.Query(query)

        parsed_lag = loads(lag.Rows[0][0])

    except:
        raise
else:
    try:
        lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       t.write_lsn, '
'       0 as throughput, '
'       now()::time as current_time '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.write_lsn IS NOT NULL '
'ORDER BY n.node_name '
)
        ''')
        parsed_lag = loads(lag.Rows[0][0])
    except:
        raise

datasets = []
previous_data = []

for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                "label": data['stream'],
                "fill": False,
                "backgroundColor": color,
                "borderColor": color,
                "lineTension": 0,
                "pointRadius": 1,
                "borderWidth": 1,
                "data": [data['throughput']]
            })
            previous_data.append({
                'stream': data['stream'],
                'write_lsn': data['write_lsn'],
                'current_time': data['current_time']
            })
    except:
        raise


result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    'previous_data': previous_data
}
"""
}, {
'dbms': 'postgresql',
'id': 7,
'title': 'BDR commit lag',
'type': 'chart_append',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"BDR commit lag (seconds)"
        },
        "tooltips": {
            "mode": "index",
            "intersect": False
        },
        "hover": {
            "mode": "nearest",
            "intersect": True
        },
        "scales": {
            "xAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": False,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "Value"
                },
                "ticks": {
                    "beginAtZero": True,
                    "suggestedMax": 1
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

try:
    lag = connection.Query('''
select bdr.run_on_all_nodes(
'SELECT stream, '
'       round(extract(seconds from replay_gap)::numeric + extract(minutes from replay_gap)::numeric*60 + extract(hours from replay_gap)::numeric*3600,2) as commit_lag '
'FROM ( '
'SELECT origin_name || '' - '' || target_name as stream, '
'       now() - last_xact_replay_timestamp as replay_gap '
'FROM bdr.subscription_summary t) t '
)
    ''')
    parsed_lag = loads(lag.Rows[0][0])
except:
    None

datasets = []
for node in parsed_lag:
    try:
        for data in node['response']:
            color = "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")"
            datasets.append({
                    "label": data['stream'],
                    "fill": False,
                    "backgroundColor": color,
                    "borderColor": color,
                    "lineTension": 0,
                    "pointRadius": 0,
                    "borderWidth": 1,
                    "data": [data['commit_lag']]
                })
    except:
        raise

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'id': 8,
'title': 'BDR replication',
'type': 'graph',
'interval': 10,
'default': True,
'script_chart': """
from random import randint

result = {
	"container": None,
	"boxSelectionEnabled": False,
	"autounselectify": True,
	"layout": {
		"name": "spread"
	},
	"style": [
		{
			"selector": "node",
			"style": {
				"content": "data(label)",
				"text-opacity": 1,
				"text-valign": "top",
				"text-halign": "right",
				"text-wrap": "wrap",
				"color": "gray",
				"text-rotation": "autorotate",
		        "font-size": 11
			}
		},
		{
			"selector": "node.node_local",
			"style": {
				"background-color": "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")",
				"shape": 'square'
			}
		},
		{
			"selector": "node.node_remote",
			"style": {
				"background-color": "rgb(" + str(randint(65, 225)) + "," + str(randint(65, 225)) + "," + str(randint(65, 225)) + ")",
			}
		},
		{
			"selector": "edge",
			"style": {
				"curve-style": "bezier",
				"control-point-step-size": 40,
		        "target-arrow-shape": "triangle",
		        "text-opacity": 1,
		        "width": 2,
		        "control-point-distances": 30,
		        "content": "data(label)",
		        "text-wrap": "wrap",
		        "line-style": "solid",
		        "width": 1,
		        "color": "gray",
		        "text-outline-color": 'gray',
		        "text-outline-width": 0,
		        "font-size": 11
			}
		}
	],
	"elements": {
		"nodes": None,
		"edges": None
	}
}
""",
'script_data': """
from datetime import datetime
from random import randint
from json import loads

nodes = []
edges = []

try:
    lag = connection.Query('''
SELECT
(SELECT array_to_json(array_agg(row_to_json(t)))
FROM (
  SELECT node_name FROM bdr.node_summary
) t),
bdr.run_on_all_nodes(
'SELECT origin_name || '' - '' || target_name as stream, '
'       origin_name, '
'       target_name, '
'       pg_size_pretty(replay_lag_bytes) as replay_lag_size '
'FROM bdr.node_slots t '
'INNER JOIN pglogical.node n ON n.node_id = t.target_id '
'LEFT JOIN pglogical.local_node l ON l.node_id = n.node_id '
'WHERE l.node_id IS NULL '
'  AND t.replay_lag_bytes IS NOT NULL '
)
    ''')
    parsed_nodes = loads(lag.Rows[0][0])
    parsed_lag = loads(lag.Rows[0][1])
except Exception as exc:
    None
    raise exc

for node in parsed_nodes:
    nodes.append({
            "data": {
                "id": node['node_name'],
                "label": node['node_name'],
            },
            "classes": 'node_remote'
        })

for node in parsed_lag:
    try:
        for data in node['response']:
            edges.append({
                "data": {
                    "id": 'edge_' + data['origin_name'] + '_' + data['target_name'],
                    "label": data['replay_lag_size'],
                    "source": data['origin_name'],
                    "target": data['target_name']
                }
            })
    except:
        None

result = {
    "nodes": nodes,
	"edges": edges
}
"""
}]
