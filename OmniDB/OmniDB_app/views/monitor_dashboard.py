from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
import json

import sys
import io
from contextlib import redirect_stdout

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB_app.include.Session import Session
from datetime import datetime

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, full_write_guard, \
        guarded_iter_unpack_sequence, guarded_unpack_sequence
from RestrictedPython.Utilities import utility_builtins
from RestrictedPython.Eval import default_guarded_getitem
from RestrictedPython.Eval import RestrictionCapableEval

#load plugins to retrieve list of monitoring units of all loaded plugins
from OmniDB_app.views.plugins import monitoring_units

def get_monitor_nodes(request):

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

    v_return['v_data'] = []

    try:
        #Child nodes
        v_nodes = v_session.v_omnidb_database.v_connection.Query('''
            select node_id, node_name, dbt_st_name, server, port, service, user
            from pmon_nodes
        ''')
        for v_node in v_nodes.Rows:
            v_node_data = {
                'v_id': v_node['node_id'],
                'v_name': v_node['node_name'],
                'v_technology': v_node['dbt_st_name'],
                'v_server': v_node['server'],
                'v_port': v_node['port'],
                'v_service': v_node['service'],
                'v_user': v_node['user']
            }
            v_return['v_data'].append(v_node_data)

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_monitor_unit_list(request):

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
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_mode = json_object['p_mode']

    v_database = v_session.v_tab_connections[v_tab_id]

    v_query = '''
        select unit_id,
        title,
        case type
          when 'chart' then 'Chart'
          when 'chart_append' then 'Chart (Append)'
          when 'grid' then 'Grid'
        end type,
        user_id,
        interval
        from mon_units
        where dbt_st_name = '{0}'
        and (user_id is null or user_id = {1})
        order by user_id desc, type
    '''.format(v_database.v_db_type,v_session.v_user_id)


    v_return['v_data'] = []
    v_data = []
    v_id_list = []

    try:
        #plugins units
        for mon_unit in monitoring_units:
            if mon_unit['dbms'] == v_database.v_db_type:
                v_actions = '''
                <i title='Edit' class='fas fa-check-circle action-grid action-check' onclick='includeMonitorUnit({0},"{1}")'></i>
                '''.format(mon_unit['id'],mon_unit['plugin_name'])
                if mon_unit['type'] == 'chart':
                    v_type = 'Chart'
                elif mon_unit['type'] == 'chart_append':
                    v_type = 'Chart (Append)'
                elif mon_unit['type'] == 'grid':
                    v_type = 'Grid'
                if v_mode==0:
                    v_data.append([v_actions,mon_unit['title'],v_type,mon_unit['interval']])
                else:
                    v_data.append([mon_unit['plugin_name'],mon_unit['title'],v_type])
                v_id_list.append(mon_unit['id'])


        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:
            v_actions = '''
            <i title='Edit' class='fas fa-check-circle action-grid action-check' onclick='includeMonitorUnit({0})'></i>
            '''.format(v_unit['unit_id'])
            #custom unit, add edit and delete actions
            if v_unit['user_id']!=None:
                v_actions += '''
                <i title='Edit' class='fas fa-edit action-grid action-edit-monitor' onclick='editMonitorUnit({0})'></i>
                <i title='Delete' class='fas fa-times action-grid action-close' onclick='deleteMonitorUnit({0})'></i>
                '''.format(v_unit['unit_id'])

            if v_mode==0:
                v_data.append([v_actions,v_unit['title'],v_unit['type'],v_unit['interval']])
            else:
                v_data.append(['',v_unit['title'],v_unit['type']])

            v_id_list.append(v_unit['unit_id'])
        v_return['v_data'] = { 'id_list': v_id_list, 'data': v_data }

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_monitor_unit_details(request):

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
    v_unit_id = json_object['p_unit_id']

    v_query = '''
        select title,
               type,
               interval,
               coalesce(script_chart,'') as script_chart,
               coalesce(script_data,'') as script_data
        from mon_units
        where unit_id = {0}
    '''.format(v_unit_id)


    try:
        v_unit_details = v_session.v_omnidb_database.v_connection.Query(v_query).Rows[0]
        v_return['v_data'] = { 'title': v_unit_details['title'], 'type': v_unit_details['type'], 'interval': v_unit_details['interval'], 'script_chart': v_unit_details['script_chart'], 'script_data': v_unit_details['script_data'] }

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_monitor_units(request):

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
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    v_return['v_data'] = []

    #saving units for current user/connection if there are none
    v_query = '''
        select *
        from (
        select uuc.uuc_id,mu.unit_id, mu.title, uuc.interval, uuc.plugin_name
            from mon_units mu,units_users_connections uuc
            where mu.dbt_st_name = '{0}'
              and uuc.unit_id = mu.unit_id
              and uuc.user_id = {1}
              and uuc.conn_id = {2}
              and uuc.plugin_name = ''
        union all
        select uuc.uuc_id,uuc.unit_id, '' as title, uuc.interval, uuc.plugin_name
            from units_users_connections uuc
            where uuc.user_id = {1}
              and uuc.conn_id = {2}
              and uuc.plugin_name <> '')
        order by uuc_id desc;
    '''.format(v_database.v_db_type,v_session.v_user_id,v_database.v_conn_id)

    try:
        v_count = 0
        v_existing_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        v_existing_data = []

        for v_unit in v_existing_units.Rows:
            if v_unit['plugin_name']=='':
                v_existing_data.append(
                {
                    'uuc_id': v_unit['uuc_id'],
                    'unit_id': v_unit['unit_id'],
                    'title': v_unit['title'],
                    'interval': v_unit['interval'],
                    'plugin_name': v_unit['plugin_name'],
                }
                )
            else:
                #search plugin data
                unit_data = None
                for mon_unit in monitoring_units:
                    if mon_unit['id'] == v_unit['unit_id'] and mon_unit['plugin_name'] == v_unit['plugin_name'] and mon_unit['dbms'] == v_database.v_db_type:
                        v_existing_data.append(
                        {
                            'uuc_id': v_unit['uuc_id'],
                            'unit_id': v_unit['unit_id'],
                            'title': mon_unit['title'],
                            'interval': v_unit['interval'],
                            'plugin_name': v_unit['plugin_name'],
                        }
                        )
                        break

        #save default units
        if len(v_existing_data) == 0:
            v_query = '''
                select mu.unit_id, mu.interval
                from mon_units mu
                where mu.dbt_st_name = '{0}'
                  and mu.is_default = 1
            '''.format(v_database.v_db_type)

            v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
            v_session.v_omnidb_database.v_connection.Open();
            v_session.v_omnidb_database.v_connection.Execute('BEGIN TRANSACTION;');
            for v_unit in v_units.Rows:
                v_session.v_omnidb_database.v_connection.Execute('''
                    insert into units_users_connections values
                        ((select coalesce(max(uuc_id), 0) + 1 from units_users_connections),
                        {0},
                        {1},
                        {2},
                        {3},
                        '');
                '''.format(v_unit['unit_id'],v_session.v_user_id,v_database.v_conn_id,v_unit['interval']));

            v_session.v_omnidb_database.v_connection.Execute('COMMIT;');
            v_session.v_omnidb_database.v_connection.Close();

            v_query = '''
                select uuc.uuc_id,mu.unit_id, mu.title, uuc.interval, uuc.plugin_name
                from mon_units mu,units_users_connections uuc
                where mu.dbt_st_name = '{0}'
                  and uuc.unit_id = mu.unit_id
                  and uuc.user_id = {1}
                  and uuc.conn_id = {2}
                order by uuc_id desc
            '''.format(v_database.v_db_type,v_session.v_user_id,v_database.v_conn_id)

            v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
            for v_unit in v_units.Rows:
                v_unit_data = {
                    'v_saved_id': v_unit['uuc_id'],
                    'v_id': v_unit['unit_id'],
                    'v_title': v_unit['title'],
                    'v_plugin_name': v_unit['plugin_name'],
                    'v_interval': v_unit['interval']
                }
                v_return['v_data'].append(v_unit_data)

        else:

            for v_unit in v_existing_data:
                v_unit_data = {
                    'v_saved_id': v_unit['uuc_id'],
                    'v_id': v_unit['unit_id'],
                    'v_title': v_unit['title'],
                    'v_plugin_name': v_unit['plugin_name'],
                    'v_interval': v_unit['interval']
                }
                v_return['v_data'].append(v_unit_data)

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)


    return JsonResponse(v_return)

def get_monitor_unit_template(request):

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
    v_unit_id = json_object['p_unit_id']
    v_unit_plugin_name = json_object['p_unit_plugin_name']

    if v_unit_plugin_name=='':
        v_query = '''
            select coalesce(script_chart,'') as script_chart, coalesce(script_data,'') as script_data, type, interval
            from mon_units where unit_id = '{0}'
        '''.format(v_unit_id)

        v_return['v_data'] = ''

        try:
            v_return['v_data'] = v_session.v_omnidb_database.v_connection.Query(v_query).Rows[0]

        except Exception as exc:
            v_return['v_data'] = str(exc)
            v_return['v_error'] = True
            return JsonResponse(v_return)
    else:
        #search plugin data
        for mon_unit in monitoring_units:
            if mon_unit['id'] == v_unit_id and mon_unit['plugin_name'] == v_unit_plugin_name:
                unit_data = mon_unit
                v_return['v_data'] = {
                    'interval': unit_data['interval'],
                    'script_chart': unit_data['script_chart'],
                    'script_data': unit_data['script_data'],
                    'type': unit_data['type']
                }
                break

    return JsonResponse(v_return)

def save_monitor_unit(request):

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
    v_unit_id = json_object['p_unit_id']
    v_unit_name = json_object['p_unit_name']
    v_unit_type = json_object['p_unit_type']
    v_unit_interval = json_object['p_unit_interval']
    v_unit_script_chart = json_object['p_unit_script_chart']
    v_unit_script_data = json_object['p_unit_script_data']
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    if v_unit_interval==None:
        v_unit_interval = 30

    try:
        #new unit
        if not v_unit_id:
            v_session.v_omnidb_database.v_connection.Open()
            v_session.v_omnidb_database.v_connection.Execute('''
                insert into mon_units values (
                (select coalesce(max(unit_id), 0) + 1 from mon_units),'{0}','{1}','{2}','{3}','{4}',0,{5},{6})
            '''.format(v_database.v_db_type,v_unit_script_chart.replace("'","''"),v_unit_script_data.replace("'","''"),v_unit_type,v_unit_name,v_session.v_user_id,v_unit_interval))
            v_inserted_id = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
            select coalesce(max(unit_id), 0) from mon_units
            ''')
            v_session.v_omnidb_database.v_connection.Close()
            v_return['v_data'] = v_inserted_id
        #existing unit
        else:
            v_return['v_data'] = v_unit_id
            v_session.v_omnidb_database.v_connection.Execute('''
                update mon_units
                set dbt_st_name = '{0}',
                    script_chart = '{1}',
                    script_data = '{2}',
                    type = '{3}',
                    title = '{4}',
                    interval = {5}
                where unit_id = {6}
            '''.format(v_database.v_db_type,v_unit_script_chart.replace("'", "''"),v_unit_script_data.replace("'", "''"),v_unit_type,v_unit_name,v_unit_interval,v_unit_id))


    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def delete_monitor_unit(request):

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
    v_unit_id = json_object['p_unit_id']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
                delete from mon_units
                where unit_id = {0}
            '''.format(v_unit_id))
        v_session.v_omnidb_database.v_connection.Execute('''
                delete from units_users_connections
                where unit_id = {0}
                  and plugin_name = ''
            '''.format(v_unit_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def remove_saved_monitor_unit(request):

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
    v_saved_id = json_object['p_saved_id']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
                delete from units_users_connections
                where uuc_id = {0}
            '''.format(v_saved_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def update_saved_monitor_unit_interval(request):

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
    v_saved_id = json_object['p_saved_id']
    v_interval = json_object['p_interval']

    try:
        v_session.v_omnidb_database.v_connection.Execute('''
                update units_users_connections
                    set interval = {0}
                where uuc_id = {1}
            '''.format(v_interval,v_saved_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def refresh_monitor_units(request):

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
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_ids = json_object['p_ids']

    v_database_orig = v_session.v_tab_connections[v_tab_id]
    v_database = OmniDatabase.Generic.InstantiateDatabase(
        v_database_orig.v_db_type,
        v_database_orig.v_connection.v_host,
        str(v_database_orig.v_connection.v_port),
        v_database_orig.v_active_service,
        v_database_orig.v_active_user,
        v_database_orig.v_connection.v_password,
        v_database_orig.v_conn_id,
        v_database_orig.v_alias,
        p_conn_string = v_database_orig.v_conn_string,
        p_parse_conn_string = False
    )
    v_return['v_data'] = []

    if len(v_ids) > 0:
        v_first = True
        v_query = ''
        for v_id in v_ids:

            #save new user/connection unit
            if v_id['saved_id'] == -1:
                try:
                    v_session.v_omnidb_database.v_connection.Open()
                    v_session.v_omnidb_database.v_connection.Execute('BEGIN TRANSACTION;')
                    v_session.v_omnidb_database.v_connection.Execute('''
                        insert into units_users_connections values
                            ((select coalesce(max(uuc_id), 0) + 1 from units_users_connections),
                            {0},
                            {1},
                            {2},
                            {3},
                            '{4}');
                    '''.format(v_id['id'],v_session.v_user_id,v_database_orig.v_conn_id,v_id['interval'],v_id['plugin_name']));
                    v_id['saved_id'] =  v_session.v_omnidb_database.v_connection.ExecuteScalar('''
                    select coalesce(max(uuc_id), 0) from units_users_connections
                    ''')
                    v_session.v_omnidb_database.v_connection.Execute('COMMIT;')
                    v_session.v_omnidb_database.v_connection.Close()
                except Exception as exc:
                    v_return['v_data'] = str(exc)
                    v_return['v_error'] = True
                    return JsonResponse(v_return)

            if v_id['plugin_name']=='':
                if not v_first:
                    v_query += ' union all '
                v_first = False
                v_query += '''
                    select unit_id, {0} as 'sequence', {1} as rendered, {2} as saved_id, script_chart, script_data, type, title, interval
                    from mon_units where unit_id = '{3}'
                '''.format(v_id['sequence'], v_id['rendered'], v_id['saved_id'], v_id['id'])

            #plugin unit
            else:
                #search plugin data
                unit_data = None
                for mon_unit in monitoring_units:
                    if mon_unit['id'] == v_id['id'] and mon_unit['plugin_name'] == v_id['plugin_name']:
                        unit_data = mon_unit
                        break

                try:
                    v_unit_data = {
                        'v_saved_id': v_id['saved_id'],
                        'v_id': unit_data['id'],
                        'v_sequence': v_id['sequence'],
                        'v_type': unit_data['type'],
                        'v_title': unit_data['title'],
                        'v_interval': unit_data['interval'],
                        'v_object': None,
                        'v_error': False
                    }

                    loc = {"connection": v_database.v_connection}

                    builtins = safe_builtins.copy()
                    builtins['_getiter_'] = iter
                    builtins['_getitem_'] = default_guarded_getitem

                    byte_code = compile_restricted(unit_data['script_data'], '<inline>', 'exec')
                    exec(byte_code, builtins, loc)
                    data = loc['result']

                    if unit_data['type']  == 'grid' or v_id['rendered'] == 1:
                        v_unit_data['v_object'] = data
                    else:
                        byte_code = compile_restricted(unit_data['script_chart'], '<inline>', 'exec')
                        exec(byte_code, builtins, loc)
                        result = loc['result']
                        result['data'] = data
                        v_unit_data['v_object'] = result


                    v_return['v_data'].append(v_unit_data)
                except Exception as exc:
                    v_unit_data = {
                        'v_saved_id': v_id['saved_id'],
                        'v_id': unit_data['id'],
                        'v_sequence': v_id['sequence'],
                        'v_type': unit_data['type'],
                        'v_title': unit_data['title'],
                        'v_interval': unit_data['interval'],
                        'v_object': None,
                        'v_error': True,
                        'v_message': str(exc)
                    }
                    v_return['v_data'].append(v_unit_data)


        if v_query != '':
            try:
                v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
                for v_unit in v_units.Rows:

                    try:
                        v_unit_data = {
                            'v_saved_id': v_unit['saved_id'],
                            'v_id': v_unit['unit_id'],
                            'v_sequence': v_unit['sequence'],
                            'v_type': v_unit['type'],
                            'v_title': v_unit['title'],
                            'v_interval': v_unit['interval'],
                            'v_object': None,
                            'v_error': False
                        }

                        loc = {"connection": v_database.v_connection}

                        builtins = safe_builtins.copy()
                        builtins['_getiter_'] = iter
                        builtins['_getitem_'] = default_guarded_getitem

                        byte_code = compile_restricted(v_unit['script_data'], '<inline>', 'exec')
                        exec(byte_code, builtins, loc)
                        data = loc['result']

                        if v_unit['type']  == 'grid' or v_unit['rendered'] == 1:
                            v_unit_data['v_object'] = data
                        else:
                            byte_code = compile_restricted(v_unit['script_chart'], '<inline>', 'exec')
                            exec(byte_code, builtins, loc)
                            result = loc['result']
                            result['data'] = data
                            v_unit_data['v_object'] = result


                        v_return['v_data'].append(v_unit_data)
                    except Exception as exc:
                        v_unit_data = {
                            'v_saved_id': v_unit['saved_id'],
                            'v_id': v_unit['unit_id'],
                            'v_sequence': v_unit['sequence'],
                            'v_type': v_unit['type'],
                            'v_title': v_unit['title'],
                            'v_interval': v_unit['interval'],
                            'v_object': None,
                            'v_error': True,
                            'v_message': str(exc)
                        }
                        v_return['v_data'].append(v_unit_data)



            except Exception as exc:
                v_return['v_data'] = str(exc)
                v_return['v_error'] = True
                return JsonResponse(v_return)

        return JsonResponse(v_return)

def test_monitor_script(request):

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
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_script_chart = json_object['p_script_chart']
    v_script_data = json_object['p_script_data']
    v_type = json_object['p_type']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_return['v_data'] = {
        'v_object': None,
        'v_error': False
    }

    try:
        loc = {"connection": v_database.v_connection}

        builtins = safe_builtins.copy()
        builtins['_getiter_'] = iter
        builtins['_getitem_'] = default_guarded_getitem

        byte_code = compile_restricted(v_script_data, '<inline>', 'exec')
        exec(byte_code, builtins, loc)
        data = loc['result']

        if v_type == 'grid':
            v_return['v_data']['v_object'] = data
        else:
            byte_code = compile_restricted(v_script_chart, '<inline>', 'exec')
            exec(byte_code, builtins, loc)
            result = loc['result']
            result['data'] = data
            v_return['v_data']['v_object'] = result

    except Exception as exc:
        v_unit_data = {
            'v_object': None,
            'v_error': True,
            'v_message': str(exc)
        }
        v_return['v_data'] = v_unit_data


    return JsonResponse(v_return)
