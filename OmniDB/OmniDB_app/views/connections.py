from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
import json

import sys
sys.path.append("OmniDB_app/include")

import Spartacus.Database, Spartacus.Utils
import OmniDatabase
from Session import Session
from OmniDB import ws_core, settings

def index(request):

    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    context = {
        'session' : request.session.get('omnidb_session'),
        'menu_item': 'connections',
        'omnidb_version': settings.OMNIDB_VERSION
    }

    template = loader.get_template('OmniDB_app/connections.html')
    return HttpResponse(template.render(context, request))

def get_connections(request):

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
    v_cryptor = request.session.get('cryptor')

    v_session.RefreshDatabaseList()
    request.session['omnidb_session'] = v_session
    ws_core.omnidb_sessions[v_session.v_user_key] = v_session

    try:
        v_technologies = v_session.v_omnidb_database.v_connection.Query('''
            select dbt_st_name
            from db_type
            where dbt_in_enabled = 1
        ''')
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_connection_list = []
    v_conn_id_list = []
    v_tech_list = []
    for r in v_technologies.Rows:
        v_tech_list.append(r['dbt_st_name'])


    v_index = 0
    for v_connection in v_session.v_databases:
        v_connection_data_list = []
        v_connection_data_list.append(v_connection.v_db_type)
        v_connection_data_list.append(v_connection.v_server)
        v_connection_data_list.append(v_connection.v_port)
        v_connection_data_list.append(v_connection.v_service)
        v_connection_data_list.append(v_connection.v_user)
        v_connection_data_list.append(v_connection.v_connection.v_password)
        v_connection_data_list.append(v_connection.v_alias)
        v_connection_data_list.append('''<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='removeConnection({0})'/><img src='/static/OmniDB_app/images/test.png' class='img_ht' onclick='testConnection({1})'/>'''.format(v_connection.v_conn_id,v_index))

        v_index = v_index+1
        v_connection_list.append(v_connection_data_list)
        v_conn_id_list.append(v_connection.v_conn_id)

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_technologies': v_tech_list,
        'v_conn_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def new_connection(request):

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

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
            insert into connections values (
            (select coalesce(max(conn_id), 0) + 1 from connections),{0},'postgresql','','','','','','')
        '''.format(v_session.v_user_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def remove_connection(request):

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

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
            delete from connections
            where conn_id = {0}
        '''.format(v_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def save_connections(request):

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
    v_cryptor = request.session.get('cryptor')

    json_object = json.loads(request.POST.get('data', None))
    v_data = json_object['p_data']
    v_conn_id_list = json_object['p_conn_id_list']

    v_index = 0

    try:
        for r in v_data:
            v_session.v_omnidb_database.v_connection.Execute('''
                update connections
                set dbt_st_name = '{0}',
                    server = '{1}',
                    port = '{2}',
                    service = '{3}',
                    user = '{4}',
                    password = '{5}',
                    alias = '{6}'
                where conn_id = {7}
            '''.format(r[0],v_cryptor.Encrypt(r[1]),v_cryptor.Encrypt(r[2]),v_cryptor.Encrypt(r[3]),v_cryptor.Encrypt(r[4]),v_cryptor.Encrypt(r[5]),v_cryptor.Encrypt(r[6]),v_conn_id_list[v_index]))
            v_index = v_index + 1
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def test_connection(request):

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
    p_index = json_object['p_index']

    v_return['v_data'] = v_session.v_databases [int(p_index)].TestConnection()

    return JsonResponse(v_return)
