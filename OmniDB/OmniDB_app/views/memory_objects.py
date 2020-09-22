import os
import json
import threading
import time
from django.http import JsonResponse
from datetime import datetime,timedelta

import OmniDB_app.include.OmniDatabase as OmniDatabase

global_object = {}
to_be_removed = []

def cleanup_thread():
    while True:
        v_remove_index = len(to_be_removed)-1
        try:
            while to_be_removed:
                conn = to_be_removed.pop(0)
                conn.v_connection.Close()
        except:
            None
        #   None
        for client in list(global_object):

            # Client reached timeout
            client_timeout_reached = datetime.now() > global_object[client]['last_update'] + timedelta(0,3600)

            for tab_id in list(global_object[client]['tab_list']):
                try:
                    # Tab reached timeout
                    tab_timeout_reached = datetime.now() > global_object[client]['tab_list'][tab_id]['last_update'] + timedelta(0,3600)

                    if client_timeout_reached or tab_timeout_reached or global_object[client]['tab_list'][tab_id]['to_be_removed'] == True:
                        close_tab_handler(global_object[client],tab_id)
                except Exception as exc:
                    None
        time.sleep(30)

t = threading.Thread(target=cleanup_thread)
t.setDaemon(True)
t.start()

def user_authenticated(function):
    def wrap(request, *args, **kwargs):
        #User not authenticated
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            v_return = {}
            v_return['v_data'] = ''
            v_return['v_error'] = True
            v_return['v_error_id'] = 1
            return JsonResponse(v_return)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def database_timeout(function):
    def wrap(request, *args, **kwargs):

        v_return = {
            'v_data': '',
            'v_error': False,
            'v_error_id': -1
        }

        v_session = request.session.get('omnidb_session')

        json_object = json.loads(request.POST.get('data', None))
        v_database_index = json_object['p_database_index']

        #Check database prompt timeout
        v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
        if v_timeout['timeout']:
            v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
            v_return['v_error'] = True
            return JsonResponse(v_return)
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def close_tab_handler(p_client_object,p_tab_object_id):
    try:
        tab_object = p_client_object['tab_list'][p_tab_object_id]
        del p_client_object['tab_list'][p_tab_object_id]
        if tab_object['type'] == 'query' or tab_object['type'] == 'connection':
            try:
                tab_object['omnidatabase'].v_connection.Cancel(False)
            except Exception:
                None
            try:
                tab_object['omnidatabase'].v_connection.Close()
            except Exception as exc:
                None
        elif tab_object['type'] == 'debug':
            tab_object['cancelled'] = True
            try:
                tab_object['omnidatabase_control'].v_connection.Cancel(False)
            except Exception:
                None
            try:
                tab_object['omnidatabase_control'].v_connection.Terminate(tab_object['debug_pid'])
            except Exception:
                None
            try:
                tab_object['omnidatabase_control'].v_connection.Close()
            except Exception:
                None
            try:
                tab_object['omnidatabase_debug'].v_connection.Close()
            except Exception:
                None
        elif tab_object['type'] == 'terminal':
            if tab_object['thread']!=None:
                tab_object['thread'].stop()
            if tab_object['terminal_type'] == 'local':
                tab_object['terminal_object'].terminate()
            else:
                tab_object['terminal_object'].close()
                tab_object['terminal_ssh_client'].close()

    except Exception as exc:
        None

def clear_client_object(
    p_client_id = None
):
    try:
        client_object = global_object[p_client_id]

        for tab_id in list(client_object['tab_list']):
            global_object[p_client_id]['tab_list'][tab_id]['to_be_removed'] = True

        try:
            client_object['polling_lock'].release()
        except:
            None
        try:
            client_object['returning_data_lock'].release()
        except:
            None
    except Exception as exc:
        print(str(exc))
        None

def create_tab_object(
    p_session,
    p_tab_id,
    p_object
):
    v_object = p_object
    v_object['last_update'] = datetime.now()
    v_object['to_be_removed'] = False
    global_object[p_session.session_key]['tab_list'][p_tab_id] = v_object
    return v_object


def get_client_object(p_client_id):
    #get client attribute in global object or create if it doesn't exist
    try:
        client_object = global_object[p_client_id]
    except Exception as exc:
        client_object = {
            'id': p_client_id,
            'polling_lock': threading.Lock(),
            'returning_data_lock': threading.Lock(),
            'returning_data': [],
            'tab_list': {},
            'last_update': datetime.now()
        }
        global_object[p_client_id] = client_object

    return client_object

def get_database_object(
    p_session = None,
    p_tab_id = None,
    p_attempt_to_open_connection = False
):
    v_session = p_session.get('omnidb_session')
    v_client_id = p_session.session_key
    v_client_object = get_client_object(v_client_id)

    # Retrieving tab object
    try:
        v_tab_object = v_client_object['tab_list'][p_tab_id]
    except Exception as exc:
        # Create global lock object
        v_tab_object = create_tab_object(
            p_session,
            p_tab_id,
            {
                'omnidatabase': None,
                'type': 'connection'
            }
        )

    return get_database_tab_object(
        v_session,
        v_client_object,
        v_tab_object,
        p_tab_id,
        p_attempt_to_open_connection,
        True
    )

def get_database_tab_object(
    p_session = None,
    p_client_object = None,
    p_tab_object = None,
    p_con_tab_id = None,
    p_attempt_to_open_connection = False,
    p_use_lock = False
):
    v_new_database_object = p_session.v_tab_connections[p_con_tab_id]

    # Updating time
    p_tab_object['last_update'] = datetime.now()

    if p_tab_object['omnidatabase'] == None:
        p_tab_object['omnidatabase'] = v_new_database_object
        if p_use_lock:
            v_new_database_object.v_lock = threading.Lock()

    # Check if database attributes changed and create a new database object if it did
    if (v_new_database_object.v_db_type!=p_tab_object['omnidatabase'].v_db_type or
        v_new_database_object.v_connection.v_host!=p_tab_object['omnidatabase'].v_connection.v_host or
        str(v_new_database_object.v_connection.v_port)!=str(p_tab_object['omnidatabase'].v_connection.v_port) or
        v_new_database_object.v_active_service!=p_tab_object['omnidatabase'].v_active_service or
        v_new_database_object.v_user!=p_tab_object['omnidatabase'].v_user or
        v_new_database_object.v_connection.v_password!=p_tab_object['omnidatabase'].v_connection.v_password):

        v_database_new = OmniDatabase.Generic.InstantiateDatabase(
            v_new_database_object.v_db_type,
            v_new_database_object.v_connection.v_host,
            str(v_new_database_object.v_connection.v_port),
            v_new_database_object.v_active_service,
            v_new_database_object.v_active_user,
            v_new_database_object.v_connection.v_password,
            v_new_database_object.v_conn_id,
            v_new_database_object.v_alias,
            p_conn_string = v_new_database_object.v_conn_string,
            p_parse_conn_string = False
        )
        if p_use_lock:
            v_database_new.v_lock = threading.Lock()

        # Instead of waiting for garbage collector to clear existing connection,
        # put it in the list of to be removed connections and let the cleaning
        # thread close it
        to_be_removed.append(p_tab_object['omnidatabase'])

        p_tab_object['omnidatabase'] = v_database_new

    # Try to open connection if not opened yet
    if p_attempt_to_open_connection and not p_tab_object['omnidatabase'].v_connection.v_con or p_tab_object['omnidatabase'].v_connection.GetConStatus() == 0:
        p_tab_object['omnidatabase'].v_connection.Open()

    return p_tab_object['omnidatabase']
