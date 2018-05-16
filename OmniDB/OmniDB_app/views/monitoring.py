from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from string import ascii_letters, digits
from random import choice
from math import floor
import json

import datetime

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB import monitoring_core,settings
from OmniDB_app.include.Session import Session

def index(request):

    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    context = {
        'session' : request.session.get('omnidb_session'),
        'menu_item': 'monitoring',
        'desktop_mode': settings.DESKTOP_MODE,
        'omnidb_version': settings.OMNIDB_VERSION,
    }

    template = loader.get_template('OmniDB_app/monitoring.html')
    return HttpResponse(template.render(context, request))

def get_random_string(length):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def receive_alert_data(request):
    if request.POST:
        payload = json.loads(request.POST.get("payload", ""))

        database = OmniDatabase.Generic.InstantiateDatabase(
            'sqlite',
            '',
            '',
            settings.OMNIDB_DATABASE,
            '',
            '',
            '',
            '0',
            ''
        )

        try:
            v_alert_id = database.v_connection.ExecuteScalar('''
                select a.alert_id
                from monitor_alert a
                inner join monitor_node n on a.node_id = n.node_id
                where n.node_name = '{0}'
                  and a.alert_name = '{1}'
                  and n.node_key = '{2}'
                limit 1
            '''.format(payload['node'],payload['alert'],payload['key']))
            if v_alert_id:
                monitoring_core.receive_status(v_alert_id,payload['status'],payload['message'],payload['value'])

        except Exception as exc:
            return HttpResponse("not found")

    from django.middleware.csrf import get_token
    get_token(request)

    return HttpResponse(request)

def get_nodes(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    v_connections = v_session.v_omnidb_database.v_connection.Query('''
        select *
        from monitor_node
         where user_id = {0}
    '''.format(v_session.v_user_id))

    v_connection_list = []
    v_conn_id_list = []

    for v_connection in v_connections.Rows:
        v_connection_data_list = []
        v_connection_data_list.append(v_connection['node_name'])
        v_connection_data_list.append(v_connection['node_desc'])
        v_connection_data_list.append(v_connection['node_key'])
        v_connection_data_list.append('''<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='removeNode({0})'/><img src='/static/OmniDB_app/images/list.png' class='img_ht' onclick='viewNode({0})'/><img src='/static/OmniDB_app/images/key.png' class='img_ht' onclick='refreshNodeKey({0})'/>'''.format(v_connection['node_id']))

        v_connection_list.append(v_connection_data_list)
        v_conn_id_list.append(v_connection['node_id'])

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_node_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def new_node(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    v_session.v_omnidb_database.v_connection.Execute('''
        insert into monitor_node(node_id,node_name,node_desc,user_id,node_key) values (
        (select coalesce(max(node_id), 0) + 1 from monitor_node),'','',{0},'{1}')
    '''.format(v_session.v_user_id,get_random_string(32)))

    return JsonResponse(v_return)

def refresh_node_key(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_id = json_object['p_id']

    new_key = get_random_string(32)

    v_session.v_omnidb_database.v_connection.Execute('''
        update monitor_node
        set node_key = '{0}'
        where node_id = {1}
    '''.format(new_key,v_id))

    return JsonResponse(v_return)

def remove_node(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_id = json_object['p_id']

    v_session.v_omnidb_database.v_connection.Execute('''
        delete from monitor_alert_data
        where alert_id in ( select alert_id from monitor_alert where node_id = {0})
    '''.format(v_id))

    v_session.v_omnidb_database.v_connection.Execute('''
        delete from monitor_alert
        where node_id = {0}
    '''.format(v_id))

    v_session.v_omnidb_database.v_connection.Execute('''
        delete from monitor_node
        where node_id = {0}
    '''.format(v_id))

    return JsonResponse(v_return)

def save_nodes(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_data = json_object['p_data']
    v_node_id_list = json_object['p_node_id_list']

    v_index = 0

    for r in v_data:
        v_session.v_omnidb_database.v_connection.Execute('''
            update monitor_node
            set node_name = '{0}',
                node_desc = '{1}'
            where node_id = {2}
        '''.format(r[0],r[1],v_node_id_list[v_index]))
        v_index = v_index + 1

    return JsonResponse(v_return)

#alerts

def get_alerts(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    json_object = json.loads(request.POST.get('data', None))
    p_node_id = json_object['p_node_id']

    v_connections = v_session.v_omnidb_database.v_connection.Query('''
        select a.*,
           (select count(*) from monitor_alert_data where alert_id = a.alert_id) as num_data,
           coalesce((select t.status from monitor_alert_data t where t.alert_id = a.alert_id order by datetime(t.alert_date) desc limit 1),'') as alert_status,
           coalesce((select strftime('%Y-%m-%d %H:%M:%S',t.alert_date) from monitor_alert_data t where t.status<>'UNKNOWN' and t.alert_id = a.alert_id order by datetime(t.alert_date) desc limit 1),'') as last_date
        from monitor_alert a
        where node_id = {0}
    '''.format(p_node_id))

    v_connection_list = []
    v_conn_id_list = []

    for v_connection in v_connections.Rows:
        v_connection_data_list = []
        v_connection_data_list.append(v_connection['alert_name'])
        v_connection_data_list.append(v_connection['alert_desc'])
        v_connection_data_list.append(v_connection['alert_enabled'])
        v_connection_data_list.append(v_connection['alert_interval'])
        v_connection_data_list.append(v_connection['alert_timeout'])
        v_connection_data_list.append(v_connection['alert_min_value'])
        v_connection_data_list.append(v_connection['alert_max_value'])
        v_connection_data_list.append(v_connection['alert_status'])
        v_connection_data_list.append(v_connection['alert_ack'])
        v_connection_data_list.append(v_connection['last_date'])
        v_connection_data_list.append(v_connection['num_data'])
        v_connection_data_list.append('''<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='removeAlert({0})'/><img src='/static/OmniDB_app/images/list.png' class='img_ht' onclick='viewAlert({0},"{1}")'/><img src='/static/OmniDB_app/images/bar_chart.png' class='img_ht' onclick='viewAlertChart({0},"{1}")'/>'''.format(v_connection['alert_id'],v_connection['alert_name']))

        v_connection_list.append(v_connection_data_list)
        v_conn_id_list.append(v_connection['alert_id'])

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_alert_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def new_alert(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    json_object = json.loads(request.POST.get('data', None))
    p_node_id = json_object['p_node_id']

    v_session.v_omnidb_database.v_connection.Execute('''
        insert into monitor_alert(alert_id,node_id,alert_name,alert_desc,alert_timeout,alert_interval, alert_min_value, alert_max_value, alert_enabled, alert_ack) values (
        (select coalesce(max(alert_id), 0) + 1 from monitor_alert),{0},'','','0','0','0','100.0',0,0)
    '''.format(p_node_id))

    return JsonResponse(v_return)

def remove_alert(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_id = json_object['p_id']

    v_session.v_omnidb_database.v_connection.Execute('''
        delete from monitor_alert_data
        where alert_id = {0}
    '''.format(v_id))

    v_session.v_omnidb_database.v_connection.Execute('''
        delete from monitor_alert
        where alert_id = {0}
    '''.format(v_id))

    return JsonResponse(v_return)

def save_alerts(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_data = json_object['p_data']
    v_alert_id_list = json_object['p_alert_id_list']

    v_index = 0

    for r in v_data:

        try:
            interval = int(r[3])
            if interval < 0:
                interval = 0
        except Exception as exc:
            interval = 0

        try:
            timeout = int(r[4])
            if timeout < 0:
                timeout = 0
        except Exception as exc:
            timeout = 0

        try:
            min_value = float(r[5])
            if min_value < 0:
                min_value = 0
        except Exception as exc:
            min_value = 0

        try:
            max_value = float(r[6])
            if max_value < 0:
                max_value = 0
        except Exception as exc:
            max_value = 0

        v_session.v_omnidb_database.v_connection.Execute('''
            update monitor_alert
            set alert_name = '{0}',
                alert_desc = '{1}',
                alert_enabled = {2},
                alert_interval = '{3}',
                alert_timeout = '{4}',
                alert_min_value = '{5}',
                alert_max_value = '{6}',
                alert_ack = {7}
            where alert_id = {8}
        '''.format(r[0],r[1],r[2],interval,timeout,min_value,max_value,r[8],v_alert_id_list[v_index]))
        v_index = v_index + 1

    return JsonResponse(v_return)

#alert data
def get_alert_data_list(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    json_object = json.loads(request.POST.get('data', None))
    p_alert_id = json_object['p_alert_id']

    v_connections = v_session.v_omnidb_database.v_connection.Query('''
        select status,
               value,
               message,
               strftime('%Y-%m-%d %H:%M:%S',alert_date) as alert_date
        from monitor_alert_data
        where alert_id = {0}
        order by datetime(alert_date) DESC
    '''.format(p_alert_id))

    v_connection_list = []

    for v_connection in v_connections.Rows:
        v_connection_data_list = []
        v_connection_data_list.append(v_connection['status'])
        v_connection_data_list.append(v_connection['value'])
        v_connection_data_list.append(v_connection['message'])
        v_connection_data_list.append(v_connection['alert_date'])

        v_connection_list.append(v_connection_data_list)

    v_return['v_data'] = {
        'v_data': v_connection_list
    }

    return JsonResponse(v_return)

def get_n_values(p_list,n):
    list_length = len(p_list)
    if list_length <= n:
        return p_list

    num_elements = n-2
    num_elements_left = list_length-2
    increment = int(floor(num_elements_left/num_elements))

    new_list = []
    new_list.append(p_list[0])
    index = increment
    for i in range(num_elements):
        new_list.append(p_list[index])
        index = index + increment
    new_list.append(p_list[list_length-1])
    return new_list

def view_alert_chart(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = False
        v_return['v_error_id'] = -1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    json_object = json.loads(request.POST.get('data', None))
    p_alert_id = json_object['p_alert_id']
    p_chart_start_date = json_object['p_chart_start_date']
    p_chart_end_date = json_object['p_chart_end_date']

    v_filter = ''
    v_has_filter = False
    if p_chart_start_date:
        v_filter += " and alert_date >= '{0}'".format(p_chart_start_date)
        v_has_filter = True
    if p_chart_end_date:
        v_filter += " and alert_date <= '{0}'".format(p_chart_end_date)
        v_has_filter = True

    values_ok = []
    values_warning = []
    values_critical = []
    values_unknown = []
    labels = []

    v_alert_data = v_session.v_omnidb_database.v_connection.Query('''
        select alert_min_value,
        alert_max_value
        from monitor_alert
        where alert_id = {0}
    '''.format(p_alert_id))

    if not v_has_filter:
        v_connections = v_session.v_omnidb_database.v_connection.Query('''
            select value,status,
            strftime('%Y-%m-%d %H:%M:%S',alert_date) as alert_date
            from monitor_alert_data
            where alert_id = {0}
            {1}
            order by datetime(alert_date) DESC
            limit 30
        '''.format(p_alert_id,v_filter))

        for v_connection in v_connections.Rows:
            if v_connection['status'] == 'OK':
                values_ok.insert(0,v_connection['value'])
                values_warning.insert(0,'')
                values_critical.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'WARNING':
                values_warning.insert(0,v_connection['value'])
                values_ok.insert(0,'')
                values_critical.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'CRITICAL':
                values_critical.insert(0,v_connection['value'])
                values_warning.insert(0,'')
                values_ok.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'UNKNOWN':
                values_unknown.insert(0,'1')
                values_warning.insert(0,'')
                values_critical.insert(0,'')
                values_ok.insert(0,'')

            labels.insert(0,v_connection['alert_date'])

    else:
        v_connections = v_session.v_omnidb_database.v_connection.Query('''
            select value,status,
            strftime('%Y-%m-%d %H:%M:%S',alert_date) as alert_date
            from monitor_alert_data
            where alert_id = {0}
            {1}
            order by datetime(alert_date) DESC
        '''.format(p_alert_id,v_filter))

        for v_connection in get_n_values(v_connections.Rows,30):
            if v_connection['status'] == 'OK':
                values_ok.insert(0,v_connection['value'])
                values_warning.insert(0,'')
                values_critical.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'WARNING':
                values_warning.insert(0,v_connection['value'])
                values_ok.insert(0,'')
                values_critical.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'CRITICAL':
                values_critical.insert(0,v_connection['value'])
                values_warning.insert(0,'')
                values_ok.insert(0,'')
                values_unknown.insert(0,'')
            elif v_connection['status'] == 'UNKNOWN':
                values_unknown.insert(0,'1')
                values_warning.insert(0,'')
                values_critical.insert(0,'')
                values_ok.insert(0,'')

            labels.insert(0,v_connection['alert_date'])

    v_return['v_data'] = {
        'v_values_ok': values_ok,
        'v_values_warning': values_warning,
        'v_values_critical': values_critical,
        'v_values_unknown': values_unknown,
        'v_labels': labels,
        'v_min_value': v_alert_data.Rows[0]['alert_min_value'],
        'v_max_value': v_alert_data.Rows[0]['alert_max_value']
    }

    return JsonResponse(v_return)
