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
from OmniDB_app.include.Session import Session
from datetime import datetime

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, full_write_guard, \
        guarded_iter_unpack_sequence, guarded_unpack_sequence
from RestrictedPython.Utilities import utility_builtins
from RestrictedPython.Eval import default_guarded_getitem
from RestrictedPython.Eval import RestrictionCapableEval

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
            from mon_nodes
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

    v_database = v_session.v_databases[v_database_index]['database']

    v_query = '''
        select unit_id,
        title,
        case type
          when 'chart' then 'Chart'
          when 'chart_append' then 'Chart (Append)'
          when 'grid' then 'Grid'
        end type,
        user_id
        from mon_units
        where dbt_st_name = '{0}'
        and (user_id is null or user_id = {1})
        order by user_id desc, type
    '''.format(v_database.v_db_type,v_session.v_user_id)


    v_return['v_data'] = []
    v_data = []
    v_id_list = []

    try:
        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:
            v_actions = '<img src="/static/OmniDB_app/images/select.png" class="img_ht" onclick="includeMonitorUnit({0})"/>'.format(v_unit['unit_id'])
            #custom unit, add edit and delete actions
            if v_unit['user_id']!=None:
                v_actions += '''<img src="/static/OmniDB_app/images/text_edit.png" class="img_ht" onclick="editMonitorUnit({0})"/>
                <img src="/static/OmniDB_app/images/tab_close.png" class="img_ht" onclick="deleteMonitorUnit({0})"/>'''.format(v_unit['unit_id'])

            v_data.append([v_actions,v_unit['title'],v_unit['type']])
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
        select title,type,script
        from mon_units
        where unit_id = {0}
    '''.format(v_unit_id)


    try:
        v_unit_details = v_session.v_omnidb_database.v_connection.Query(v_query).Rows[0]
        v_return['v_data'] = { 'title': v_unit_details['title'], 'type': v_unit_details['type'], 'script': v_unit_details['script'] }

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

    v_database = v_session.v_databases[v_database_index]['database']

    v_query = '''
        select unit_id, title
        from mon_units where dbt_st_name = '{0}'
        and is_default = 1
    '''.format(v_database.v_db_type)


    v_return['v_data'] = []

    try:
        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:
            v_unit_data = {
                'v_id': v_unit['unit_id'],
                'v_title': v_unit['title']
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

    v_query = '''
        select script, type
        from mon_units where unit_id = '{0}'
    '''.format(v_unit_id)

    v_return['v_data'] = ''

    try:
        v_return['v_data'] = v_session.v_omnidb_database.v_connection.Query(v_query).Rows[0]

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

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
    v_unit_script = json_object['p_unit_script']
    v_database_index = json_object['p_database_index']

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        #new unit
        if not v_unit_id:
            v_session.v_omnidb_database.v_connection.Open()
            v_session.v_omnidb_database.v_connection.Execute('''
                insert into mon_units values (
                (select coalesce(max(unit_id), 0) + 1 from mon_units),'{0}','{1}','{2}','{3}',0,0,{4})
            '''.format(v_database.v_db_type,v_unit_script.replace("'","''"),v_unit_type,v_unit_name,v_session.v_user_id))
            v_inserted_id = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
            select coalesce(max(unit_id), 0) from mon_units
            ''')
            v_session.v_omnidb_database.v_connection.Close()
            v_return['v_data'] = v_inserted_id
        #existing unit
        else:
            v_session.v_omnidb_database.v_connection.Execute('''
                update mon_units
                set dbt_st_name = '{0}',
                    script = '{1}',
                    type = '{2}',
                    title = '{3}'
                where unit_id = {4}
            '''.format(v_database.v_db_type,v_unit_script.replace("'", "''"),v_unit_type,v_unit_name,v_unit_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
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
    v_ids = json_object['p_ids']

    v_database = v_session.v_databases[v_database_index]['database']

    v_query = '''
        select unit_id, -1 as 'index', script, type, title, append
        from mon_units where dbt_st_name = '{0}'
    '''.format(v_database.v_db_type)
    if len(v_ids) > 0:
        v_first = True
        v_query = ''
        for v_id in v_ids:
            if not v_first:
                v_query += ' union all '
            v_first = False
            v_query += '''
                select unit_id, {0} as 'index', script, type, title, append
                from mon_units where unit_id = '{1}'
            '''.format(v_id['index'], v_id['id'])

    v_return['v_data'] = []

    try:
        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:

            output = ''

            try:
                loc = {"connection": v_database.v_connection}
                
                byte_code = compile_restricted(v_unit['script'], '<inline>', 'exec')

                builtins = safe_builtins.copy()
                builtins['_getiter_'] = iter
                builtins['_getitem_'] = default_guarded_getitem

                exec(byte_code, builtins, loc)

                v_unit_data = {
                    'v_id': v_unit['unit_id'],
                    'v_index': v_unit['index'],
                    'v_type': v_unit['type'],
                    'v_title': v_unit['title'],
                    'v_object': loc['result'],
                    'v_error': False
                }
                v_return['v_data'].append(v_unit_data)
            except Exception as exc:
                v_unit_data = {
                    'v_id': v_unit['unit_id'],
                    'v_index': v_unit['index'],
                    'v_type': v_unit['type'],
                    'v_title': v_unit['title'],
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
    v_script = json_object['p_script']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        loc = {"connection": v_database.v_connection}
        byte_code = compile_restricted(v_script, '<inline>', 'exec')

        builtins = safe_builtins.copy()
        builtins['_getiter_'] = iter
        builtins['_getitem_'] = default_guarded_getitem

        exec(byte_code, builtins, loc)
        v_unit_data = {
            'v_object': loc['result'],
            'v_error': False
        }
        v_return['v_data'] = v_unit_data
    except Exception as exc:
        v_unit_data = {
            'v_object': None,
            'v_error': True,
            'v_message': str(exc)
        }
        v_return['v_data'] = v_unit_data


    return JsonResponse(v_return)
