monitoring_units = [{
'dbms': 'mysql',
'plugin_name': 'mysql',
'id': 0,
'title': 'Thread Count',
'type': 'timeseries',
'interval': 10,
'default': True,
'script_chart': """

max_connections = connection.Query('show variables like "max_connections"').Rows[0]['Value']

result = {
    "type": "line",
    "data": None,
    "options": {
        "responsive": True,
        "title":{
            "display":True,
            "text":"Threads (max_connections: " + str(max_connections) + ")"
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
show status where `variable_name` = 'Threads_connected';
''')

datasets = []
datasets.append({
        "label": 'Backends',
        "backgroundColor": 'rgba(129,223,129,0.4)',
        "borderColor": 'rgba(129,223,129,1)',
        "lineTension": 0,
        "pointRadius": 0,
        "borderWidth": 1,
        "data": [backends.Rows[0]["Value"]]
    })

result = {
    "labels": [datetime.now().strftime('%H:%M:%S')],
    "datasets": datasets
}
"""
}]
