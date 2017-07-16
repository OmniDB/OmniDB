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
from OmniDB import settings
from datetime import datetime

def index(request):

    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    v_session = request.session.get('omnidb_session')

    context = {
        'session' : v_session,
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
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    v_cryptor = request.session.get('cryptor')

    #sessions.omnidb_sessions[v_session.v_user_key] = v_session
    #ws_core.omnidb_sessions[v_session.v_user_key] = v_session

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
    for v_connection_object in v_session.v_databases:
        v_connection = v_connection_object['database']
        v_connection_data_list = []
        v_connection_data_list.append(v_connection.v_db_type)
        v_connection_data_list.append(v_connection.v_server)
        v_connection_data_list.append(v_connection.v_port)
        v_connection_data_list.append(v_connection.v_service)
        v_connection_data_list.append(v_connection.v_user)
        v_connection_data_list.append(v_connection.v_alias)
        v_connection_data_list.append('''<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConnection()'/><img src='/static/OmniDB_app/images/test.png' class='img_ht' onclick='testConnection({0})'/>'''.format(v_index))

        v_index = v_index+1
        v_connection_list.append(v_connection_data_list)
        v_conn_id_list.append({'id': v_connection.v_conn_id, 'mode': 0, 'old_mode': -1 })

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_technologies': v_tech_list,
        'v_conn_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def save_connections(request):

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
    v_cryptor = request.session.get('cryptor')

    json_object = json.loads(request.POST.get('data', None))
    v_data_list = json_object['p_data_list']
    v_conn_id_list = json_object['p_conn_id_list']


    v_index = 0

    try:
        v_session.v_omnidb_database.v_connection.Open();
        v_session.v_omnidb_database.v_connection.Execute('BEGIN');
        for r in v_data_list:
            if v_conn_id_list[v_index]['mode'] == 1:
                v_session.v_omnidb_database.v_connection.Execute('''
                    update connections
                    set dbt_st_name = '{0}',
                        server = '{1}',
                        port = '{2}',
                        service = '{3}',
                        user = '{4}',
                        alias = '{5}'
                    where conn_id = {6}
                '''.format(r[0],v_cryptor.Encrypt(r[1]),v_cryptor.Encrypt(r[2]),v_cryptor.Encrypt(r[3]),v_cryptor.Encrypt(r[4]),v_cryptor.Encrypt(r[5]),v_conn_id_list[v_index]['id']))
                v_index = v_index + 1
            elif v_conn_id_list[v_index]['mode'] == 2:
                v_session.v_omnidb_database.v_connection.Execute('''
                    insert into connections values (
                    (select coalesce(max(conn_id), 0) + 1 from connections),
                    {0},
                    '{1}',
                    '{2}',
                    '{3}',
                    '{4}',
                    '{5}',
                    '',
                    '{6}')
                '''.format(v_session.v_user_id,r[0],v_cryptor.Encrypt(r[1]),v_cryptor.Encrypt(r[2]),v_cryptor.Encrypt(r[3]),v_cryptor.Encrypt(r[4]),v_cryptor.Encrypt(r[5])))
                v_index = v_index + 1
            elif v_conn_id_list[v_index]['mode'] == -1:
                v_session.v_omnidb_database.v_connection.Execute('''
                    delete from connections
                    where conn_id = {0}
                '''.format(v_conn_id_list[v_index]['id']))
                v_index = v_index + 1
        v_session.v_omnidb_database.v_connection.Close();
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_session.RefreshDatabaseList()
    request.session['omnidb_session'] = v_session

    return JsonResponse(v_return)

def test_connection(request):

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
    p_index = json_object['p_index']

    #Check database prompt timeout
    if v_session.DatabaseReachPasswordTimeout(int(p_index)):
        v_return['v_data'] = {'password_timeout': True, 'message': '' }
        v_return['v_error'] = True
        return JsonResponse(v_return)
    else:
        v_session.v_databases[int(p_index)]['prompt_timeout'] = datetime.now()

    v_return['v_data'] = v_session.v_databases [int(p_index)]['database'].TestConnection()

    return JsonResponse(v_return)
