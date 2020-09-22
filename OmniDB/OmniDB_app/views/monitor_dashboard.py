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

from OmniDB_app.models.main import *
from django.contrib.auth.models import User
from django.db.models import Q

#load plugins to retrieve list of monitoring units of all loaded plugins
from OmniDB_app.views.plugins import monitoring_units

from OmniDB_app.views.memory_objects import *

monitoring_units_default = {}

def get_unit_data():
    #Retrieving non plugin monitoring units from database to use as reference
    try:
        for mon_unit in MonUnits.objects.all():
            monitoring_units_default[mon_unit.id] = mon_unit
    # No mon units connections
    except Exception as exc:
        None

get_unit_data()

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
          when 'graph' then 'Graph'
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
                v_actions = '''<i title='Edit' class='fas fa-check-circle action-grid action-check' onclick='includeMonitorUnit({0},"{1}")'></i>'''.format(mon_unit['id'],mon_unit['plugin_name'])
                if mon_unit['type'] == 'chart':
                    v_type = 'Chart'
                elif mon_unit['type'] == 'chart_append':
                    v_type = 'Chart (Append)'
                elif mon_unit['type'] == 'grid':
                    v_type = 'Grid'
                elif mon_unit['type'] == 'graph':
                    v_type = 'Graph'
                if v_mode==0:
                    v_data.append([v_actions,mon_unit['title'],v_type,mon_unit['interval']])
                else:
                    v_data.append([mon_unit['plugin_name'],mon_unit['title'],v_type])
                v_id_list.append(mon_unit['id'])

        try:
            for mon_unit in MonUnits.objects.filter(Q(user=None)|Q(user=request.user)):
                v_actions = '''<i title='Edit' class='fas fa-check-circle action-grid action-check' onclick='includeMonitorUnit({0})'></i>'''.format(mon_unit.id)
                #v_actions = '<button class="btn btn-secondary btn-sm my-1">Actions</button>'
                #custom unit, add edit and delete actions
                if mon_unit.user!=None:
                    v_actions += '''
                    <i title='Edit' class='fas fa-edit action-grid action-edit-monitor' onclick='editMonitorUnit({0})'></i>
                    <i title='Delete' class='fas fa-times action-grid action-close' onclick='deleteMonitorUnit({0})'></i>
                    '''.format(mon_unit.id)

                if v_mode==0:
                    v_data.append([v_actions,mon_unit.title,mon_unit.type,mon_unit.interval])
                else:
                    v_data.append(['',mon_unit.title,mon_unit.type])

                v_id_list.append(mon_unit.id)
        # No mon units connections
        except Exception as exc:
            print(str(exc))

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

    try:
        unit = MonUnits.objects.get(id=v_unit_id)
        v_return['v_data'] = { 'title': unit.title, 'type': unit.type, 'interval': unit.interval, 'script_chart': unit.script_chart, 'script_data': unit.script_data }

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

    try:
        user_units = MonUnitsConnections.objects.filter(user=request.user,connection=v_database.v_conn_id)
        # There are no units for this user/connection pair, create defaults
        if len(user_units)==0:
            # Non plugin defaults
            conn_object = Connection.objects.get(id=v_database.v_conn_id)
            for default_unit in MonUnits.objects.filter(user=None):
                user_unit = MonUnitsConnections(
                    unit=default_unit.id,
                    user=request.user,
                    connection=conn_object,
                    interval=default_unit.interval,
                    plugin_name=''
                )
                user_unit.save()
            # Plugin defaults
            for mon_unit in monitoring_units:
                if mon_unit['default'] == True and mon_unit['dbms'] == v_database.v_db_type:
                    user_unit = MonUnitsConnections(
                        unit=mon_unit['id'],
                        user=request.user,
                        connection=conn_object,
                        interval=mon_unit['interval'],
                        plugin_name=mon_unit['plugin_name']
                    )
                    user_unit.save()

            # Retrieve user units again
            user_units = MonUnitsConnections.objects.filter(user=request.user,connection=v_database.v_conn_id)

        for user_unit in user_units:
            if user_unit.plugin_name=='':
                unit_default_data = MonUnits.objects.get(id=user_unit.unit)
                v_unit_data = {
                    'v_saved_id': user_unit.id,
                    'v_id': unit_default_data.id,
                    'v_title': unit_default_data.title,
                    'v_plugin_name': '',
                    'v_interval': user_unit.interval
                }
                v_return['v_data'].append(v_unit_data)
            else:
                #search plugin data
                unit_data = None
                for mon_unit in monitoring_units:
                    if mon_unit['id'] == user_unit.unit and mon_unit['plugin_name'] == user_unit.plugin_name and mon_unit['dbms'] == v_database.v_db_type:
                        v_unit_data = {
                            'v_saved_id': user_unit.id,
                            'v_id': user_unit.unit,
                            'v_title': mon_unit['title'],
                            'v_plugin_name': user_unit.plugin_name,
                            'v_interval': user_unit.interval
                        }
                        v_return['v_data'].append(v_unit_data)
                        break

    # No mon units connections
    except Exception as exc:
        print(str(exc))
        None

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

        v_return['v_data'] = ''

        try:
            unit = MonUnits.objects.get(id=v_unit_id)
            v_return['v_data'] = {
                'script_chart': unit.script_chart,
                'script_data': unit.script_data,
                'type': unit.type,
                'interval': unit.interval
            }

        except Exception as exc:
            None
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

    if v_unit_interval==None:
        v_unit_interval = 30

    try:
        #new unit
        if not v_unit_id:
            unit = MonUnits(
                user=request.user,
                technology=Technology.objects.get(name=v_database.v_db_type),
                script_chart=v_unit_script_chart,
                script_data=v_unit_script_data,
                type=v_unit_type,
                title=v_unit_name,
                is_default=False,
                interval=v_unit_interval
            )
            unit.save()
            v_return['v_data'] = unit.id
        #existing unit
        else:
            v_return['v_data'] = v_unit_id
            unit = MonUnits.objects.get(id=v_unit_id)
            unit.script_chart = v_unit_script_chart
            unit.script_data = v_unit_script_data
            unit.type = v_unit_type
            unit.title = v_unit_name
            unit.interval = v_unit_interval
            unit.save()

        monitoring_units_default[unit.id] = unit

        #updating global data
        get_unit_data()
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
        MonUnits.objects.get(id=v_unit_id).delete()
        #updating global data
        get_unit_data()

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
        MonUnitsConnections.objects.get(id=v_saved_id).delete()


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
        unit = MonUnitsConnections.objects.get(id=v_saved_id)
        unit.interval = v_interval
        unit.save()


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

    v_database = get_database_object(
        p_session = request.session,
        p_tab_id = v_tab_id,
        p_attempt_to_open_connection = True
    )

    v_return['v_data'] = []

    if len(v_ids) > 0:
        v_first = True
        v_query = ''
        unit_counter = 0
        conn_object = Connection.objects.get(id=v_database.v_conn_id)

        for v_id in v_ids:
            #save new user/connection unit
            if v_id['saved_id'] == -1:
                try:
                    user_unit = MonUnitsConnections(
                        unit=v_id['id'],
                        user=request.user,
                        connection=conn_object,
                        interval=v_id['interval'],
                        plugin_name=v_id['plugin_name']
                    )
                    user_unit.save()
                    v_id['saved_id'] = user_unit.id
                except Exception as exc:
                    v_return['v_data'] = str(exc)
                    v_return['v_error'] = True
                    return JsonResponse(v_return)

            if v_id['plugin_name']=='':

                try:
                    unit_data = monitoring_units_default[v_id['id']]

                    v_unit_data = {
                        'v_saved_id': v_id['saved_id'],
                        'v_id': v_id['id'],
                        'v_sequence': v_id['sequence'],
                        'v_type': unit_data.type,
                        'v_title': unit_data.title,
                        'v_interval': unit_data.interval,
                        'v_object': None,
                        'v_error': False
                    }

                    loc = {
                        "connection": v_database,
                        "previous_data": v_ids[unit_counter]['object_data']
                    }

                    builtins = safe_builtins.copy()
                    builtins['_getiter_'] = iter
                    builtins['_getitem_'] = default_guarded_getitem

                    byte_code = compile_restricted(unit_data.script_data, '<inline>', 'exec')
                    exec(byte_code, builtins, loc)
                    data = loc['result']

                    if unit_data.type  == 'grid' or v_id['rendered'] == 1:
                        v_unit_data['v_object'] = data
                    elif unit_data.type == 'graph':
                        byte_code = compile_restricted(unit_data.script_chart, '<inline>', 'exec')
                        exec(byte_code, builtins, loc)
                        result = loc['result']
                        result['elements'] = data
                        v_unit_data['v_object'] = result
                    else:
                        byte_code = compile_restricted(unit_data.script_chart, '<inline>', 'exec')
                        exec(byte_code, builtins, loc)
                        result = loc['result']
                        result['data'] = data
                        v_unit_data['v_object'] = result


                    v_return['v_data'].append(v_unit_data)
                except Exception as exc:
                    v_unit_data = {
                        'v_saved_id': v_id['saved_id'],
                        'v_id': v_id['id'],
                        'v_sequence': v_id['sequence'],
                        'v_type': unit_data.type,
                        'v_title': unit_data.title,
                        'v_interval': unit_data.interval,
                        'v_object': None,
                        'v_error': True,
                        'v_message': str(exc)
                    }
                    v_return['v_data'].append(v_unit_data)

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

                    loc = {
                        "connection": v_database,
                        "previous_data": v_ids[unit_counter]['object_data']
                    }

                    builtins = safe_builtins.copy()
                    builtins['_getiter_'] = iter
                    builtins['_getitem_'] = default_guarded_getitem

                    byte_code = compile_restricted(unit_data['script_data'], '<inline>', 'exec')
                    exec(byte_code, builtins, loc)
                    data = loc['result']

                    if unit_data['type']  == 'grid' or v_id['rendered'] == 1:
                        v_unit_data['v_object'] = data
                    elif unit_data['type'] == 'graph':
                        byte_code = compile_restricted(unit_data['script_chart'], '<inline>', 'exec')
                        exec(byte_code, builtins, loc)
                        result = loc['result']
                        result['elements'] = data
                        v_unit_data['v_object'] = result
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

            unit_counter = unit_counter + 1

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
        loc = {
            "connection": v_database,
            "previous_data": None
        }

        builtins = safe_builtins.copy()
        builtins['_getiter_'] = iter
        builtins['_getitem_'] = default_guarded_getitem

        byte_code = compile_restricted(v_script_data, '<inline>', 'exec')
        exec(byte_code, builtins, loc)
        data = loc['result']

        if v_type == 'grid':
            v_return['v_data']['v_object'] = data
        elif v_type =='graph':
            byte_code = compile_restricted(v_script_chart, '<inline>', 'exec')
            exec(byte_code, builtins, loc)
            result = loc['result']
            result['elements'] = data
            v_return['v_data']['v_object'] = result
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

    print(v_return)


    return JsonResponse(v_return)
