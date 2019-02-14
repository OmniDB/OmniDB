from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
import json

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB_app.include.Session import Session
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
        'desktop_mode': settings.DESKTOP_MODE,
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

    json_object = json.loads(request.POST.get('data', None))
    v_tab_conn_id_list = json_object['p_conn_id_list']

    #sessions.omnidb_sessions[v_session.v_user_key] = v_session
    #ws_core.omnidb_sessions[v_session.v_user_key] = v_session

    try:
        v_technologies = v_session.v_omnidb_database.v_connection.Query('''
            select dbt_st_name
            from (
            select dbt_st_name,
                   sort
            from (
            select dbt_st_name,
                   1 as sort
            from db_type
            where dbt_in_enabled = 1
              and dbt_st_name = 'postgresql'
            union
            select a.dbt_st_name,
                   (select count(*)
                    from db_type b
                    where b.dbt_in_enabled = 1
                      and b.dbt_st_name <> 'postgresql'
                      and a.dbt_st_name >= b.dbt_st_name)+1 as sort
            from db_type a
            where a.dbt_in_enabled = 1
              and a.dbt_st_name <> 'postgresql'
            )
            order by sort
            )
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

    for key,v_connection_object in v_session.v_databases.items():
        v_connection = v_connection_object['database']
        v_tunnel     = v_connection_object['tunnel']
        v_connection_data_list = []
        v_connection_data_list.append(False)
        v_connection_data_list.append(v_connection.v_db_type)
        v_connection_data_list.append(v_connection.v_conn_string)
        v_connection_data_list.append(v_connection.v_server)
        v_connection_data_list.append(v_connection.v_port)
        v_connection_data_list.append(v_connection.v_service)
        v_connection_data_list.append(v_connection.v_user)
        v_connection_data_list.append(v_connection.v_alias)
        v_connection_data_list.append(v_tunnel['enabled'])
        v_connection_data_list.append(v_tunnel['server'])
        v_connection_data_list.append(v_tunnel['port'])
        v_connection_data_list.append(v_tunnel['user'])
        v_connection_data_list.append(v_tunnel['password'])
        v_connection_data_list.append(v_tunnel['key'])

        v_conn_object = {
            'id': v_connection.v_conn_id,
            'mode': 0,
            'old_mode': -1,
            'locked': False,
            'group_changed': False
        }

        if v_connection.v_conn_id in v_tab_conn_id_list:
            v_connection_data_list.append('''<i title="Connection Locked" class='fas fa-lock action-grid action-locked' onclick='showConnectionLocked()'></i>''')
            v_conn_object['locked'] = True
        else:
            v_connection_data_list.append('''<i title="Remove Connection" class='fas fa-times action-grid action-close' onclick='dropConnection()'></i>
            <i title="Test Connection" class='fas fa-plug action-grid action-test' onclick='testConnection({0})''></i>
            <i title="Select Connection" class='fas fa-check-circle action-grid action-check' onclick='selectConnection({0})''></i>'''.format(v_connection.v_conn_id))

        v_conn_id_list.append(v_conn_object)

        v_connection_list.append(v_connection_data_list)

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_technologies': v_tech_list,
        'v_conn_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def get_groups(request):

    v_return = {}
    v_return['v_data'] = []
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')


    try:
        v_groups_connections = v_session.v_omnidb_database.v_connection.Query('''
            select c.cgroup_id as cgroup_id,
                   c.cgroup_name as cgroup_name,
                   cc.conn_id as conn_id
            from cgroups c
            left join cgroups_connections cc on c.cgroup_id = cc.cgroup_id
            where c.user_id = {0}
            order by c.cgroup_id
        '''.format(v_session.v_user_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    if len(v_groups_connections.Rows)==0:
        return JsonResponse(v_return)

    v_group_list = []

    v_current_group_data = {
        'id': None,
        'name': None,
        'conn_list': []
    }

    for r in v_groups_connections.Rows:
        if v_current_group_data['id'] != r['cgroup_id']:
            if v_current_group_data['id'] != None:
                v_group_list.append(v_current_group_data)
            v_current_group_data = {
                'id': r['cgroup_id'],
                'name':  r['cgroup_name'],
                'conn_list': []
            }
        if r['conn_id']!=None:
            v_current_group_data['conn_list'].append(r['conn_id'])

    v_group_list.append(v_current_group_data)

    v_return['v_data'] = v_group_list

    return JsonResponse(v_return)

def new_group(request):
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
    p_name = json_object['p_name']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
            insert into cgroups values (
            (select coalesce(max(cgroup_id), 0) + 1 from cgroups),
            {0},
            '{1}')
        '''.format(v_session.v_user_id,p_name))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def edit_group(request):
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
    p_id = json_object['p_id']
    p_name = json_object['p_name']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
            update cgroups
            set cgroup_name = '{0}'
            where cgroup_id = {1}
        '''.format(p_name,p_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def delete_group(request):
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
    p_id = json_object['p_id']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
            delete from cgroups
            where cgroup_id = {0}
        '''.format(p_id))
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
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')
    v_cryptor = request.session.get('cryptor')

    json_object = json.loads(request.POST.get('data', None))
    v_data_list = json_object['p_data_list']
    v_conn_id_list = json_object['p_conn_id_list']
    v_group_id = json_object['p_group_id']

    v_index = 0

    try:
        v_session.v_omnidb_database.v_connection.Open();
        v_session.v_omnidb_database.v_connection.Execute('BEGIN TRANSACTION;');

        for r in v_data_list:
            is_delete = False
            conn_id = v_conn_id_list[v_index]['id']
            #update
            if v_conn_id_list[v_index]['mode'] == 1:
                if r[7]:
                    v_use_tunnel = 1
                else:
                    v_use_tunnel = 0


                v_session.v_omnidb_database.v_connection.Execute('''
                    update connections
                    set dbt_st_name = '{0}',
                        conn_string = '{1}',
                        server = '{2}',
                        port = '{3}',
                        service = '{4}',
                        user = '{5}',
                        alias = '{6}',
                        ssh_server = '{7}',
                        ssh_port = '{8}',
                        ssh_user = '{9}',
                        ssh_password = '{10}',
                        ssh_key = '{11}',
                        use_tunnel = '{12}'
                    where conn_id = {13}
                '''.format(
                    r[0],
                    v_cryptor.Encrypt(r[1]),
                    v_cryptor.Encrypt(r[2]),
                    v_cryptor.Encrypt(r[3]),
                    v_cryptor.Encrypt(r[4]),
                    v_cryptor.Encrypt(r[5]),
                    v_cryptor.Encrypt(r[6]),
                    v_cryptor.Encrypt(r[8]),
                    v_cryptor.Encrypt(r[9]),
                    v_cryptor.Encrypt(r[10]),
                    v_cryptor.Encrypt(r[11]),
                    v_cryptor.Encrypt(r[12]),
                    v_use_tunnel,
                    conn_id)
                )

                #v_session.v_databases[conn_id]['database'].v_db_type     = r[0]
                #v_session.v_databases[conn_id]['database'].v_conn_string = r[1]
                #v_session.v_databases[conn_id]['database'].v_server      = r[2]
                #v_session.v_databases[conn_id]['database'].v_port        = r[3]
                #v_session.v_databases[conn_id]['database'].v_service     = r[4]
                #v_session.v_databases[conn_id]['database'].v_user        = r[5]
                #v_session.v_databases[conn_id]['database'].v_alias       = r[6]

                v_session.v_databases[conn_id]['tunnel']['enabled'] = r[7]
                v_session.v_databases[conn_id]['tunnel']['server'] = r[8]
                v_session.v_databases[conn_id]['tunnel']['port'] = r[9]
                v_session.v_databases[conn_id]['tunnel']['user'] = r[10]
                v_session.v_databases[conn_id]['tunnel']['password'] = r[11]
                v_session.v_databases[conn_id]['tunnel']['key'] = r[12]

                database = OmniDatabase.Generic.InstantiateDatabase(
    				r[0],
    				r[2],
    				r[3],
    				r[4],
    				r[5],
                    '',
                    conn_id,
                    r[6],
                    p_conn_string = r[1],
                    p_parse_conn_string = True
                )

                v_session.v_databases[conn_id]['database'] = database
                v_session.v_databases[conn_id]['tunnel_object'] = None
            #new
            elif v_conn_id_list[v_index]['mode'] == 2:
                if r[7]:
                    v_use_tunnel = 1
                else:
                    v_use_tunnel = 0
                v_session.v_omnidb_database.v_connection.Execute('''
                    insert into connections values (
                    (select coalesce(max(conn_id), 0) + 1 from connections),
                    {0},
                    '{1}',
                    '{2}',
                    '{3}',
                    '{4}',
                    '{5}',
                    '{6}',
                    '{7}',
                    '{8}',
                    '{9}',
                    '{10}',
                    '{11}',
                    '{12}',
                    '{13}')
                '''.format(
                    v_session.v_user_id,
                    r[0],
                    v_cryptor.Encrypt(r[2]),
                    v_cryptor.Encrypt(r[3]),
                    v_cryptor.Encrypt(r[4]),
                    v_cryptor.Encrypt(r[5]),
                    v_cryptor.Encrypt(r[6]),
                    v_cryptor.Encrypt(r[8]),
                    v_cryptor.Encrypt(r[9]),
                    v_cryptor.Encrypt(r[10]),
                    v_cryptor.Encrypt(r[11]),
                    v_cryptor.Encrypt(r[12]),
                    v_use_tunnel,
                    v_cryptor.Encrypt(r[1])
                ))
                conn_id = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
                select coalesce(max(conn_id), 0) from connections
                ''')

                database = OmniDatabase.Generic.InstantiateDatabase(
    				r[0],
    				r[2],
    				r[3],
    				r[4],
    				r[5],
                    '',
                    conn_id,
                    r[6],
                    p_conn_string = r[1],
                    p_parse_conn_string = True
                )

                tunnel_information = {
                    'enabled': r[7],
                    'server': r[8],
                    'port': r[9],
                    'user': r[10],
                    'password': r[11],
                    'key': r[12]
                }

                if 1==0:
                    v_session.AddDatabase(database,False,tunnel_information)
                else:
                    v_session.AddDatabase(database,True,tunnel_information)

            #delete
            elif v_conn_id_list[v_index]['mode'] == -1:
                is_delete = True
                v_session.v_omnidb_database.v_connection.Execute('''
                    delete from connections
                    where conn_id = {0}
                '''.format(conn_id))
                del v_session.v_databases[conn_id]

            if not is_delete and v_conn_id_list[v_index]['group_changed']:
                if v_conn_id_list[v_index]['group_value']==False:
                    v_session.v_omnidb_database.v_connection.Execute('''
                        delete from cgroups_connections
                        where cgroup_id = {0}
                          and conn_id = {1}
                    '''.format(
                        v_group_id,
                        conn_id)
                    )
                else:
                    v_session.v_omnidb_database.v_connection.Execute('''
                        insert into cgroups_connections
                        select {0},{1}
                        where not exists (select 1 from cgroups_connections where cgroup_id = {0} and conn_id = {1})
                    '''.format(
                        v_group_id,
                        conn_id)
                    )


            v_index = v_index + 1
        v_session.v_omnidb_database.v_connection.Execute('COMMIT;');
        v_session.v_omnidb_database.v_connection.Close();
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    #v_session.RefreshDatabaseList()
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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)
    else:
        v_session.v_databases[int(p_index)]['prompt_timeout'] = datetime.now()


    v_return['v_data'] = v_session.v_databases [int(p_index)]['database'].TestConnection()

    return JsonResponse(v_return)

def select_connection(request):

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
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)
    else:
        v_session.v_databases[int(p_index)]['prompt_timeout'] = datetime.now()

    v_return['v_data'] = v_session.v_databases [int(p_index)]['database'].TestConnection()

    return JsonResponse(v_return)
