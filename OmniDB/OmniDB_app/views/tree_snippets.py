from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
import json

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
from OmniDB_app.include.Session import Session

def get_node_children(request):

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
    v_sn_id_parent = json_object['p_sn_id_parent']

    if not v_sn_id_parent:
        v_filter = ' is null'
    else:
        v_filter = ' = {0}'.format(v_sn_id_parent)

    v_return['v_data'] = {
        'v_list_nodes': [],
        'v_list_texts': []
    }

    try:
        #Child nodes
        v_child_nodes = v_session.v_omnidb_database.v_connection.Query('''
            select sn_id, sn_name
            from snippets_nodes
            where user_id = {0}
              and sn_id_parent {1}
        '''.format(v_session.v_user_id,v_filter))
        for v_node in v_child_nodes.Rows:
            v_node_data = {
                'v_id': v_node['sn_id'],
                'v_name': v_node['sn_name']
            }
            v_return['v_data']['v_list_nodes'].append(v_node_data)

        #Child texts
        v_child_texts = v_session.v_omnidb_database.v_connection.Query('''
            select st_id, st_name
            from snippets_texts
            where user_id = {0}
              and sn_id_parent {1}
        '''.format(v_session.v_user_id,v_filter))
        for v_text in v_child_texts.Rows:
            v_text_data = {
                'v_id': v_text['st_id'],
                'v_name': v_text['st_name']
            }
            v_return['v_data']['v_list_texts'].append(v_text_data)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_snippet_text(request):

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
    v_st_id = json_object['p_st_id']

    try:
        v_return['v_data'] = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
            select st_text
            from snippets_texts
            where st_id = {0}
        '''.format(v_st_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def new_node_snippet(request):

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
    v_sn_id_parent = json_object['p_sn_id_parent']
    v_mode = json_object['p_mode']
    v_name = json_object['p_name']

    if not v_sn_id_parent:
        v_sn_id_parent = 'null'

    try:
        if v_mode == 'node':
            v_session.v_omnidb_database.v_connection.Execute('''
                insert into snippets_nodes values (
                (select coalesce(max(sn_id), 0) + 1 from snippets_nodes),'{0}',{1},'','',{2})
            '''.format(v_name,v_session.v_user_id,v_sn_id_parent))
        else:
            v_session.v_omnidb_database.v_connection.Execute('''
                insert into snippets_texts values (
                (select coalesce(max(st_id), 0) + 1 from snippets_texts),'{0}','','','',{1},{2})
            '''.format(v_name,v_sn_id_parent,v_session.v_user_id))
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

        v_return['v_data'] = ''

    return JsonResponse(v_return)

def delete_node_snippet(request):

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
    v_id = json_object['p_id']
    v_mode = json_object['p_mode']

    try:
        if v_mode == 'node':
            v_session.v_omnidb_database.v_connection.Execute('''
                delete
                from snippets_nodes
                where sn_id = {0}
            '''.format(v_id))
        else:
            v_session.v_omnidb_database.v_connection.Execute('''
                delete
                from snippets_texts
                where st_id = {0}
            '''.format(v_id))

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)


        v_return['v_data'] = ''

    return JsonResponse(v_return)

def save_snippet_text(request):

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
    v_id = json_object['p_id']
    v_name = json_object['p_name']
    v_text = json_object['p_text']

    try:
        #new snippet
        if not v_id:
            v_session.v_omnidb_database.v_connection.Execute('''
                insert into snippets_texts values (
                (select coalesce(max(st_id), 0) + 1 from snippets_texts),'{0}','{1}','','',null,{2})
            '''.format(v_name,v_text.replace("'", "''"),v_session.v_user_id))
        #existing snippet
        else:
            v_session.v_omnidb_database.v_connection.Execute('''
                update snippets_texts
                set st_text = '{0}'
                where st_id = {1}
            '''.format(v_text.replace("'", "''"),v_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

        v_return['v_data'] = ''

    return JsonResponse(v_return)


def rename_node_snippet(request):

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
    v_id = json_object['p_id']
    v_name = json_object['p_name']
    v_mode = json_object['p_mode']

    try:
        #node
        if v_mode=='node':
            v_session.v_omnidb_database.v_connection.Execute('''
                update snippets_nodes
                set sn_name = '{0}'
                where sn_id = {1}
            '''.format(v_name,v_id))
        #snippet
        else:
            v_session.v_omnidb_database.v_connection.Execute('''
                update snippets_texts
                set st_name = '{0}'
                where st_id = {1}
            '''.format(v_name,v_id))


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

        v_return['v_data'] = ''

    return JsonResponse(v_return)
