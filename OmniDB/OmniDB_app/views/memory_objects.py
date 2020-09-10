import os
import json
import threading

global_object = {}
global_lock = threading.Lock()

def get_client_object(p_client_id):
    #get client attribute in global object or create if it doesn't exist
    try:
        global_lock.acquire()
        client_object = global_object[p_client_id]
    except Exception as exc:
        client_object = {
            'id': p_client_id,
            'polling_lock': threading.Lock(),
            'returning_data': [],
            'tab_list': {}
        }
        global_object[p_client_id] = client_object
    global_lock.release()

    return client_object

def get_database_object(
    p_session = None,
    p_client_id = None,
    p_tab_id = None,
    p_attempt_to_open_connection = False,
    p_check_database_timeout = False
):
    #print(p_client_id)
    #print(p_tab_id)

    v_client_object = get_client_object(p_client_id)

    v_database_object = p_session.v_tab_connections[p_tab_id]

    print(v_client_object)
    print('--------------------------')
    print(v_database_object)

    # Retrieving tab object
    try:
        tab_object = v_client_object['tab_list'][p_tab_id]
    except Exception as exc:
        print('Object does not exist yet')
        tab_object =  {
            'omnidatabase': v_database_object
        }
        v_client_object['tab_list'][p_tab_id] = tab_object

    # Try to open connection if not opened yet
    if p_attempt_to_open_connection and not tab_object['omnidatabase'].v_connection.v_con or tab_object['omnidatabase'].v_connection.GetConStatus() == 0:
        tab_object['omnidatabase'].v_connection.Open()
        print('OPENING NOW')



    return tab_object['omnidatabase']
