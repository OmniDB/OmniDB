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
    SELECT round((sum(temp_bytes) - \"\"\" + previous_data["current_temp_bytes"] + \"\"\")/(extract(epoch from now()::time - '\"\"\" + previous_data["current_time"] + \"\"\"'::time))::numeric,2) as rate,
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
}]
