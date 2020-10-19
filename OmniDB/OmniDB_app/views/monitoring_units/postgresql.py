monitoring_units = [{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 0,
'title': 'Transaction Rate',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":False
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
                    "labelString": "TPS"
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

if previous_data != None:
    query = "select round((sum(xact_commit+xact_rollback) - " + previous_data["current_count"] + ")/(extract(epoch from now()::time - '" + previous_data["current_time"] + "'::time))::numeric,2) as tps, sum(xact_commit+xact_rollback) as current_count, now()::time as current_time FROM pg_stat_database"
else:
    query = 'select 0 as tps, sum(xact_commit+xact_rollback) as current_count, now()::time as current_time FROM pg_stat_database'

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Rate',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['tps']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_count": query_data.Rows[0]['current_count'],
    'current_time': query_data.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 1,
'title': 'Backends',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
max_connections = connection.ExecuteScalar('SHOW max_connections')

result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"Backends (max_connections: " + str(max_connections) + ")"
        },
        "legend": {
            "display": False
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
                    "max": int(max_connections)
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint

backends = connection.Query('''
SELECT count(*) as count
FROM pg_stat_activity
''')

datasets = []
datasets.append({
        "label": 'Backends',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [backends.Rows[0]["count"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 2,
'title': 'Autovacuum Workers Usage',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":False
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
                    "labelString": "%"
                },
                "ticks": {
                    "beginAtZero": True,
                    "max": 100.0
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint

query_data = connection.Query('''
SELECT current_setting('autovacuum_max_workers')::bigint - (SELECT count(*) FROM pg_stat_activity WHERE query LIKE 'autovacuum: %') free,
(SELECT count(*) FROM pg_stat_activity WHERE query LIKE 'autovacuum: %') used,
current_setting('autovacuum_max_workers')::bigint total
''')

perc = round((float(query_data.Rows[0]['used']))/(float(query_data.Rows[0]['total']))*100,1)

datasets = []
datasets.append({
        "label": 'Workers busy (%)',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [perc]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 3,
'title': 'WAL Production Rate',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":False
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

version = int(connection.Query('show server_version_num').Rows[0][0])

if version < 100000:
    if previous_data == None:
        r = connection.Query(\"\"\"
        SELECT 0 as rate,
               current_lsn,
               current_time::text
        FROM (
        SELECT CASE WHEN pg_is_in_recovery() THEN null
               ELSE pg_current_xlog_location()
               END as current_lsn,
               now()::text as current_time) t
        \"\"\")
    else:
        r = connection.Query(\"\"\"
        SELECT round((pg_xlog_location_diff(current_lsn,'\"\"\" + previous_data["current_lsn"] + \"\"\"')/1048576.0)/(extract(epoch from now()::time - '\"\"\" + previous_data["current_time"] + \"\"\"'::time))::numeric,2) as rate,
               current_lsn,
               current_time::text
        FROM (
        SELECT CASE WHEN pg_is_in_recovery() THEN null
               ELSE pg_current_xlog_location()
               END as current_lsn,
               now() as current_time) t
        \"\"\")
else:
    if previous_data == None:
        r = connection.Query(\"\"\"
        SELECT 0 as rate,
               current_lsn,
               current_time::text
        FROM (
        SELECT CASE WHEN pg_is_in_recovery() THEN null
               ELSE pg_current_wal_lsn()
               END as current_lsn,
               now() as current_time) t
        \"\"\")
    else:
        r = connection.Query(\"\"\"
        SELECT round((pg_wal_lsn_diff(current_lsn,'\"\"\" + previous_data["current_lsn"] + \"\"\"')/1048576.0)/(extract(epoch from now()::time - '\"\"\" + previous_data["current_time"] + \"\"\"'::time))::numeric,2) as rate,
               current_lsn,
               current_time::text
        FROM (
        SELECT CASE WHEN pg_is_in_recovery() THEN null
               ELSE pg_current_wal_lsn()
               END as current_lsn,
               now() as current_time) t
        \"\"\")

datasets = []
datasets.append({
        "label": 'Rate (MB/s)',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [r.Rows[0]['rate']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_lsn": r.Rows[0]['current_lsn'],
    'current_time': r.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 4,
'title': 'Temp Files Creation Rate',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":False
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

if previous_data == None:
    r = connection.Query(\"\"\"
    SELECT 0 as rate,
           sum(temp_bytes) current_temp_bytes,
           now()::text as current_time
    FROM pg_stat_database
    \"\"\")
else:
    r = connection.Query(\"\"\"
    SELECT round(((sum(temp_bytes) - \"\"\" + previous_data["current_temp_bytes"] + \"\"\")/1048576.0)/(extract(epoch from now()::time - '\"\"\" + previous_data["current_time"] + \"\"\"'::time))::numeric,2) as rate,
           sum(temp_bytes) current_temp_bytes,
           now()::text as current_time
    FROM pg_stat_database
    \"\"\")

datasets = []
datasets.append({
        "label": 'Rate (MB/s)',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [r.Rows[0]['rate']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_temp_bytes": r.Rows[0]['current_temp_bytes'],
    'current_time': r.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 5,
'title': 'Autovacuum Freeze',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
max_age = connection.ExecuteScalar('SHOW autovacuum_freeze_max_age')

result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text":"Autovacuum Freeze (autovacuum_freeze_max_age: " + str(max_age) + ")"
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
                    "display": True,
                    "labelString": "Time"
                }
            }],
            "yAxes": [{
                "display": True,
                "scaleLabel": {
                    "display": True,
                    "labelString": "%"
                },
                "ticks": {
                    "beginAtZero": True,
                    "max": 100.0
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime
from random import randint

r = connection.Query('''
    SELECT round(max(t.perc::numeric),2) as perc
    FROM (
    SELECT (greatest(age(c.relfrozenxid), age(t.relfrozenxid))::INT8 / current_setting('autovacuum_freeze_max_age')::FLOAT)*100 as perc
    FROM (pg_class c
          JOIN pg_namespace n ON (c.relnamespace=n.oid))
    LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
    WHERE c.relkind = 'r') t
''')

datasets = []
datasets.append({
        "label": 'Freeze (%)',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [r.Rows[0]['perc']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 6,
'title': 'Blocked Locks',
'type': 'timeseries',
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
            "text":"Locks Blocked"
        },
        "legend": {
            "display": False
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
                    "beginAtZero": True
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime

query_data = connection.Query('''
    SELECT count(*)
    FROM  pg_catalog.pg_locks blocked_locks
    WHERE NOT blocked_locks.GRANTED;
''')

datasets = []
datasets.append({
        "label": 'Locks Blocked',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]["count"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 7,
'title': 'Database Size',
'type': 'timeseries',
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
            "text":"Database Size"
        },
        "legend": {
            "display": False
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
                    "labelString": "Size (MB)"
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
from decimal import Decimal

query_data = connection.Query('''
    SELECT sum(pg_database_size(datname)) AS sum
    FROM pg_stat_database
    WHERE datname IS NOT NULL
''')

datasets = []
datasets.append({
        "label": 'Database Size',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [round(query_data.Rows[0]["sum"] / Decimal(1048576.0),1)]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 8,
'title': 'Database Growth Rate',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text": "Database Growth Rate"
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

if previous_data != None:
    query = '''
        SELECT round(
                   ((sum(pg_database_size(datname)) - {0})/1048576.0) / (extract(epoch from now()::time - '{1}'::time))::numeric,
                   2
               ) AS database_growth,
               sum(pg_database_size(datname)) AS current_sum,
               now()::text AS current_time
        FROM pg_stat_database
        WHERE datname IS NOT NULL
    '''.format(
        previous_data['current_sum'],
        previous_data['current_time']
    )
else:
    query = '''
        SELECT 0 AS database_growth,
               sum(pg_database_size(datname)) AS current_sum,
               now()::text AS current_time
        FROM pg_stat_database
        WHERE datname IS NOT NULL
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Rate',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['database_growth']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_sum": query_data.Rows[0]['current_sum'],
    'current_time': query_data.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 9,
'title': 'Heap Cache Miss Ratio',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
database_name = connection.ExecuteScalar('SELECT current_database()')

result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"Heap Cache Miss Ratio (Database: {0})".format(database_name)
        },
        "legend": {
            "display": False
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
                    "labelString": "%"
                },
                "ticks": {
                    "beginAtZero": True,
                    "max": 100.0
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime

if previous_data != None:
    query = '''
        SELECT sum(heap_blks_read) AS current_reads,
               sum(heap_blks_hit) AS current_hits,
               now()::time AS current_time,
               round(
                   (sum(heap_blks_read) - {0}) / (sum(heap_blks_read) + sum(heap_blks_hit) - {1}),
                   2
               ) AS miss_ratio
        FROM pg_statio_all_tables
    '''.format(
        previous_data['current_reads'],
        previous_data['current_hits'] + previous_data['current_reads']
    )
else:
    query = '''
        SELECT sum(heap_blks_read) AS current_reads,
               sum(heap_blks_hit) AS current_hits,
               now()::time AS current_time,
               0.0 AS miss_ratio
        FROM pg_statio_all_tables
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Miss Ratio',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]["miss_ratio"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_reads": query_data.Rows[0]['current_reads'],
    "current_hits": query_data.Rows[0]['current_hits'],
    'current_time': query_data.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 10,
'title': 'Index Cache Miss Ratio',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
database_name = connection.ExecuteScalar('SELECT current_database()')

result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"Index Cache Miss Ratio (Database: {0})".format(database_name)
        },
        "legend": {
            "display": False
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
                    "labelString": "%"
                },
                "ticks": {
                    "beginAtZero": True,
                    "max": 100.0
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime

if previous_data != None:
    query = '''
        SELECT sum(idx_blks_read) AS current_reads,
               sum(idx_blks_hit) AS current_hits,
               now()::time AS current_time,
               round(
                   (sum(idx_blks_read) - {0}) / (sum(idx_blks_read) + sum(idx_blks_hit) - {1}),
                   2
               ) AS miss_ratio
        FROM pg_statio_all_tables
    '''.format(
        previous_data['current_reads'],
        previous_data['current_hits'] + previous_data['current_reads']
    )
else:
    query = '''
        SELECT sum(idx_blks_read) AS current_reads,
               sum(idx_blks_hit) AS current_hits,
               now()::time AS current_time,
               0.0 AS miss_ratio
        FROM pg_statio_all_tables
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Miss Ratio',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]["miss_ratio"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_reads": query_data.Rows[0]['current_reads'],
    "current_hits": query_data.Rows[0]['current_hits'],
    'current_time': query_data.Rows[0]['current_time']
}
"""
},
{
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 11,
'title': 'Seq Scan Ratio',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
database_name = connection.ExecuteScalar('SELECT current_database()')

result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"Seq Scan Ratio (Database: {0})".format(database_name)
        },
        "legend": {
            "display": False
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
                    "labelString": "%"
                },
                "ticks": {
                    "beginAtZero": True,
                    "max": 100.0
                }
            }]
        }
    }
}
""",
'script_data': """
from datetime import datetime

if previous_data != None:
    query = '''
        SELECT sum(seq_scan) as current_seq,
               sum(idx_scan) as current_idx,
               now()::time AS current_time,
               round(
                   (sum(seq_scan) - {1}) / (sum(seq_scan) + sum(idx_scan) - {1}),
                   2
               ) AS ratio
        FROM pg_stat_all_tables
    '''.format(
        previous_data['current_seq'],
        previous_data['current_seq'] + previous_data['current_idx']
    )
else:
    query = '''
        SELECT sum(seq_scan) as current_seq,
               sum(idx_scan) as current_idx,
               now()::time AS current_time,
               0.0 AS ratio
        FROM pg_stat_all_tables
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Seq Scan Ratio',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]["ratio"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_seq": query_data.Rows[0]['current_seq'],
    "current_idx": query_data.Rows[0]['current_idx'],
    'current_time': query_data.Rows[0]['current_time']
}
"""
}, {
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 12,
'title': 'Long Transaction',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text": "Long Transaction"
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
                    "labelString": "Seconds"
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

if int(connection.ExecuteScalar('show server_version_num')) < 100000:
    query = '''
        SELECT seconds
        FROM (
            SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-xact_start))::numeric,2) as seconds
            FROM pg_stat_activity
            WHERE xact_start is not null
              AND datid is not null
              AND query NOT LIKE 'autovacuum: %'
        ) x
        ORDER BY seconds DESC
        LIMIT 1
    '''
else:
    query = '''
        SELECT seconds
        FROM (
            SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-xact_start))::numeric,2) as seconds
            FROM pg_stat_activity
            WHERE xact_start is not null
              AND datid is not null
              AND backend_type NOT IN ('walreceiver','walsender','walwriter','autovacuum worker')
        ) x
        ORDER BY seconds DESC
        LIMIT 1
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Seconds',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['seconds']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 13,
'title': 'Long Query',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text": "Long Query"
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
                    "labelString": "Seconds"
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

if int(connection.ExecuteScalar('show server_version_num')) < 100000:
    query = '''
        SELECT seconds
            FROM (
                SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-query_start))::numeric,2) as seconds
                FROM pg_stat_activity
                WHERE state='active'
                  AND query_start is not null
                  AND datid is not null
                  AND query NOT LIKE 'autovacuum: %'
                UNION ALL
                SELECT 0.0
            ) x
            ORDER BY seconds DESC
            LIMIT 1
    '''
else:
    query = '''
        SELECT seconds
        FROM (
            SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-query_start))::numeric,2) as seconds
            FROM pg_stat_activity
            WHERE state='active'
              AND query_start is not null
              AND datid is not null
              AND backend_type NOT IN ('walreceiver','walsender','walwriter','autovacuum worker')
            UNION ALL
            SELECT 0.0
        ) x
        ORDER BY seconds DESC
        LIMIT 1
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Seconds',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['seconds']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 14,
'title': 'Long Autovacuum',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text": "Long Autovacuum"
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
                    "labelString": "Seconds"
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

if int(connection.ExecuteScalar('show server_version_num')) < 100000:
    query = '''
        SELECT seconds
        FROM (
            SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-query_start))::numeric,2) as seconds
            FROM pg_stat_activity
            WHERE state='active'
              AND query_start is not null
              AND datid is not null
              AND query LIKE 'autovacuum: %'
            UNION ALL
            SELECT 0.0
        ) x
        ORDER BY seconds DESC
        LIMIT 1
    '''
else:
    query = '''
        SELECT seconds
        FROM (
            SELECT ROUND(EXTRACT(EPOCH FROM (clock_timestamp()-query_start))::numeric,2) as seconds
            FROM pg_stat_activity
            WHERE state='active'
              AND query_start is not null
              AND datid is not null
              AND backend_type = 'autovacuum worker'
            UNION ALL
            SELECT 0.0
        ) x
        ORDER BY seconds DESC
        LIMIT 1
    '''

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Seconds',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['seconds']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}, {
'dbms': 'postgresql',
'plugin_name': 'postgresql',
'id': 15,
'title': 'Checkpoints',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """
result = {
    "type": "line",
    "data": None,
    "options": {
        "legend": {
            "display": False
        },
        "responsive": True,
        "title":{
            "display":True,
            "text": "Checkpoints"
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
                    "labelString": "Checkpoints"
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

if previous_data != None:
    query = "select (checkpoints_timed+checkpoints_req) - " + str(previous_data["current_checkpoints"]) + " as checkpoints_diff, (checkpoints_timed+checkpoints_req) as current_checkpoints FROM pg_stat_bgwriter"
else:
    query = 'select 0 as checkpoints_diff, (checkpoints_timed+checkpoints_req) as current_checkpoints FROM pg_stat_bgwriter'

query_data = connection.Query(query)

datasets = []
datasets.append({
        "label": 'Checkpoints',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [query_data.Rows[0]['checkpoints_diff']]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets,
    "current_checkpoints": query_data.Rows[0]['current_checkpoints']
}
"""
}]
