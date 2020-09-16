import os
import json
import threading
from django.http import JsonResponse

global_object = {}
global_lock = threading.Lock()

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

def clear_client_object(
    p_client_id = None
):
    print(global_object)
    try:
        del global_object[p_client_id]
    except Exception as exc:
        None

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
            'tab_list': {}
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
    v_tab_global_database_object = v_session.v_tab_connections[p_tab_id]

    # Retrieving tab object
    try:
        tab_object = v_client_object['tab_list'][p_tab_id]
    except Exception as exc:
        tab_object =  {
            'omnidatabase': v_tab_global_database_object,
            'database_object_lock': threading.Lock()
        }
        v_client_object['tab_list'][p_tab_id] = tab_object

    #tab_object['database_object_lock'].acquire()

    # Try to open connection if not opened yet
    if p_attempt_to_open_connection and not tab_object['omnidatabase'].v_connection.v_con or tab_object['omnidatabase'].v_connection.GetConStatus() == 0:
        tab_object['omnidatabase'].v_connection.Open()

    return tab_object['omnidatabase']

def release_database_object(
    p_client_id = None,
    p_tab_id = None
):
    v_client_object = get_client_object(p_client_id)

    # Retrieving tab object
    try:
        tab_object = v_client_object['tab_list'][p_tab_id]
        tab_object['database_object_lock'].release()
    except Exception as exc:
        None
