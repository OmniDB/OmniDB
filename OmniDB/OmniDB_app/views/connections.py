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

import time, os

from OmniDB_app.models.main import *

sys.path.append('OmniDB_app/include')
from OmniDB_app.include import paramiko
from sshtunnel import SSHTunnelForwarder

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
        v_tech       = v_connection_object['technology']
        v_alias      = v_connection_object['alias']
        v_connection_data_list = []
        v_connection_data_list.append(False)
        v_connection_data_list.append(v_tech)
        if (v_tech=='terminal'):
            v_connection_data_list.append('')
            v_connection_data_list.append('')
            v_connection_data_list.append('')
            v_connection_data_list.append('')
            v_connection_data_list.append('')

        else:
            v_connection_data_list.append(v_connection.v_conn_string)
            v_connection_data_list.append(v_connection.v_server)
            v_connection_data_list.append(v_connection.v_port)
            v_connection_data_list.append(v_connection.v_service)
            v_connection_data_list.append(v_connection.v_user)
        v_connection_data_list.append(v_alias)
        v_connection_data_list.append(v_tunnel['enabled'])
        v_connection_data_list.append(v_tunnel['server'])
        v_connection_data_list.append(v_tunnel['port'])
        v_connection_data_list.append(v_tunnel['user'])
        v_connection_data_list.append(v_tunnel['password'])
        v_connection_data_list.append(v_tunnel['key'])

        v_conn_object = {
            'id': key,
            'mode': 0,
            'old_mode': -1,
            'locked': False,
            'group_changed': False,
            'technology': v_tech
        }

        if key in v_tab_conn_id_list:
            v_connection_data_list.append('''<i title="Connection Locked" class='fas fa-lock action-grid action-locked' onclick='showConnectionLocked()'></i>''')
            v_conn_object['locked'] = True
        else:
            v_connection_data_list.append('''<i title="Remove Connection" class='fas fa-times action-grid action-close' onclick='dropConnection()'></i>
            <i title="Test Connection" class='fas fa-plug action-grid action-test' onclick='testConnection({1})''></i>
            <i title="Select Connection" class='fas fa-check-circle action-grid action-check' onclick="selectConnection('{0}',{1})"></i>'''.format(v_connection_object['technology'],key))

        v_conn_id_list.append(v_conn_object)

        v_connection_list.append(v_connection_data_list)

    v_return['v_data'] = {
        'v_data': v_connection_list,
        'v_technologies': v_tech_list,
        'v_conn_ids': v_conn_id_list
    }

    return JsonResponse(v_return)

def get_connections_new(request):

    #User not authenticated
    if not request.user.is_authenticated:
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_tab_conn_id_list = json_object['p_conn_id_list']

    v_tech_list = []
    for tech in Technology.objects.all():
        v_tech_list.append(tech.name)

    v_connection_list = []

    try:
        for conn in Connection.objects.filter(user=request.user):
            v_conn_object = {
                'id': conn.id,
                'locked': False,
                'technology': conn.technology.name,
                'alias': conn.alias,
                'conn_string': '',
                'server': '',
                'port': '',
                'service': '',
                'user': '',
                'tunnel': {
                    'enabled': conn.use_tunnel,
                    'server': conn.ssh_server,
                    'port': conn.ssh_port,
                    'user': conn.ssh_user,
                    'password': conn.ssh_password,
                    'key': conn.ssh_key
                }
            }

            if conn.id in v_tab_conn_id_list:
                v_conn_object['locked'] = True

            if (conn.technology.name!='terminal'):
                v_conn_object['conn_string'] = conn.conn_string
                v_conn_object['server'] = conn.server
                v_conn_object['port'] = conn.port
                v_conn_object['service'] = conn.database
                v_conn_object['user'] = conn.username

            v_connection_list.append(v_conn_object)
    # No connections
    except Exception as exc:
        None

    v_return['v_data'] = {
        'v_conn_list': v_connection_list,
        'v_technologies': v_tech_list
    }

    return JsonResponse(v_return)

def get_groups_new(request):

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

    v_group_list = []

    v_current_group_data = {
        'id': None,
        'name': None,
        'conn_list': []
    }

    try:
        for group in Group.objects.filter(user=request.user):
            v_current_group_data = {
                'id': group.id,
                'name':  group.name,
                'conn_list': []
            }
            for group_conn in GroupConnection.objects.filter(group=group):
                v_current_group_data['conn_list'].append(group_conn.connection.id)

            v_group_list.append(v_current_group_data)

    # No group connections
    except Exception as exc:
        None

    v_return['v_data'] = v_group_list

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

def new_group_new(request):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    p_name = json_object['p_name']

    try:
        new_group = Group(user=request.user,name=p_name)
        new_group.save()
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

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


                if r[0]=='terminal':
                    database = None
                    r[1] = ''
                    r[2] = ''
                    r[3] = ''
                    r[4] = ''
                    r[5] = ''



                else:
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

                v_session.v_databases[conn_id]['database'] = database
                v_session.v_databases[conn_id]['technology'] = r[0]
                v_session.v_databases[conn_id]['tunnel_object'] = None
                v_session.v_databases[conn_id]['alias'] = r[6]
            #new
            elif v_conn_id_list[v_index]['mode'] == 2:
                if r[7]:
                    v_use_tunnel = 1
                else:
                    v_use_tunnel = 0

                if r[0]=='terminal':
                    r[1] = ''
                    r[2] = ''
                    r[3] = ''
                    r[4] = ''
                    r[5] = ''
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

                if r[0]=='terminal':
                    database=None
                else:
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
                    v_session.AddDatabase(conn_id,r[0],database,False,tunnel_information,r[6])
                else:
                    v_session.AddDatabase(conn_id,r[0],database,True,tunnel_information,r[6])

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

def test_connection_new(request):
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
    p_type = json_object['type']
    #p_index = json_object['p_index']

    if p_type=='terminal':

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            #ssh key provided
            if json_object['tunnel']['key'].strip() != '':
                v_file_name = '{0}'.format(str(time.time())).replace('.','_')
                v_full_file_name = os.path.join(settings.TEMP_DIR, v_file_name)
                with open(v_full_file_name,'w') as f:
                    f.write(json_object['tunnel']['key'])
                client.connect(hostname=json_object['tunnel']['server'],username=json_object['tunnel']['user'],key_filename=v_full_file_name,passphrase=json_object['tunnel']['password'],port=int(json_object['tunnel']['port']))
            else:
                client.connect(hostname=json_object['tunnel']['server'],username=json_object['tunnel']['user'],password=json_object['tunnel']['password'],port=int(json_object['tunnel']['port']))

            client.close()
            v_return['v_data'] = 'Connection successful.'
        except Exception as exc:
            v_return['v_data'] = str(exc)
            v_return['v_error'] = True
    else:

        database = OmniDatabase.Generic.InstantiateDatabase(
            p_type,
            json_object['server'],
            json_object['port'],
            json_object['database'],
            json_object['user'],
            '',
            -1,
            '',
            p_conn_string = json_object['connstring'],
            p_parse_conn_string = True
        )

        # create tunnel if enabled
        if json_object['tunnel']['enabled'] == True:

            try:
                if json_object['tunnel']['key'].strip() != '':
                    v_file_name = '{0}'.format(str(time.time())).replace('.','_')
                    v_full_file_name = os.path.join(settings.TEMP_DIR, v_file_name)
                    with open(v_full_file_name,'w') as f:
                        f.write(json_object['tunnel']['key'])
                    server = SSHTunnelForwarder(
                        (json_object['tunnel']['server'], int(json_object['tunnel']['port'])),
                        ssh_username=json_object['tunnel']['user'],
                        ssh_private_key_password=json_object['tunnel']['password'],
                        ssh_pkey = v_full_file_name,
                        remote_bind_address=(database.v_active_server, int(database.v_active_port)),
                        logger=None
                    )
                else:
                    server = SSHTunnelForwarder(
                        (json_object['tunnel']['server'], int(json_object['tunnel']['port'])),
                        ssh_username=json_object['tunnel']['user'],
                        ssh_password=json_object['tunnel']['password'],
                        remote_bind_address=(database.v_active_server, int(database.v_active_port)),
                        logger=None
                    )
                server.set_keepalive = 120
                server.start()

                database.v_connection.v_host = '127.0.0.1'
                database.v_connection.v_port = server.local_bind_port

                message = database.TestConnection()
                server.close()
                v_return['v_data'] = message
                if message != 'Connection successful.':
                    v_return['v_error'] = True

            except Exception as exc:
                v_return['v_data'] = str(exc)
                v_return['v_error'] = True

        else:
            message = database.TestConnection()
            v_return['v_data'] = message
            if message != 'Connection successful.':
                v_return['v_error'] = True

    return JsonResponse(v_return)

def save_connection_new(request):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #User not authenticated
    if not request.user.is_authenticated:
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    p_id = json_object['id']
    try:
        # New connection
        if p_id == -1:
            connection = Connection(
                user=request.user,
                technology=Technology.objects.get(name=json_object['type']),
                server=json_object['server'],
                port=json_object['port'],
                database=json_object['database'],
                username=json_object['user'],
                password='',
                alias=json_object['title'],
                ssh_server=json_object['tunnel']['server'],
                ssh_port=json_object['tunnel']['port'],
                ssh_user=json_object['tunnel']['user'],
                ssh_password=json_object['tunnel']['password'],
                ssh_key=json_object['tunnel']['key'],
                use_tunnel=json_object['tunnel']['enabled'],
                conn_string=json_object['connstring'],

            )
            connection.save()
        #update
        else:
            conn = Connection.objects.get(id=p_id)
            conn.technology=Technology.objects.get(name=json_object['type'])
            conn.server=json_object['server']
            conn.port=json_object['port']
            conn.database=json_object['database']
            conn.username=json_object['user']
            conn.password=''
            conn.alias=json_object['title']
            conn.ssh_server=json_object['tunnel']['server']
            conn.ssh_port=json_object['tunnel']['port']
            conn.ssh_user=json_object['tunnel']['user']
            conn.ssh_password=json_object['tunnel']['password']
            conn.ssh_key=json_object['tunnel']['key']
            conn.use_tunnel=json_object['tunnel']['enabled']
            conn.conn_string=json_object['connstring']
            conn.save()

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def delete_connection_new(request):
    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #User not authenticated
    if not request.user.is_authenticated:
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    p_id = json_object['id']

    try:
        conn = Connection.objects.get(id=p_id)
        conn.delete()
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
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    p_index = json_object['p_index']

    v_conn_object = v_session.v_databases[p_index]

    if v_conn_object['technology']=='terminal':

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            #ssh key provided
            if v_conn_object['tunnel']['key'].strip() != '':
                v_file_name = '{0}'.format(str(time.time())).replace('.','_')
                v_full_file_name = os.path.join(settings.TEMP_DIR, v_file_name)
                with open(v_full_file_name,'w') as f:
                    f.write(v_conn_object['tunnel']['key'])
                client.connect(hostname=v_conn_object['tunnel']['server'],username=v_conn_object['tunnel']['user'],key_filename=v_full_file_name,passphrase=v_conn_object['tunnel']['password'],port=int(v_conn_object['tunnel']['port']))
            else:
                client.connect(hostname=v_conn_object['tunnel']['server'],username=v_conn_object['tunnel']['user'],password=v_conn_object['tunnel']['password'],port=int(v_conn_object['tunnel']['port']))

            client.close()
            v_return['v_data'] = 'Connection successful.'
        except Exception as exc:
            v_return['v_data'] = {'password_timeout': False, 'message': str(exc) }
            v_return['v_error'] = True
    else:
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
