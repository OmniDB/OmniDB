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

from django.contrib.auth.models import User
from OmniDB_app.models.main import SnippetFile, SnippetFolder

from datetime import datetime
from django.utils.timezone import make_aware

def get_all_snippets(request):
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

    v_folders = SnippetFolder.objects.filter(user=request.user)
    v_files = SnippetFile.objects.filter(user=request.user)

    v_root = {
        'id': None,
        'files': [],
        'folders': []
    }

    build_snippets_object_recursive(v_folders,v_files,v_root)

    return JsonResponse(v_root)

def build_snippets_object_recursive(p_folders,p_files,p_current_object):
    # Adding files
    for file in p_files:
        # Match
        if ((file.parent is None and p_current_object['id'] is None) or (file.parent is not None and file.parent.id == p_current_object['id'])):
            p_current_object['files'].append(
                {
                    'id': file.id,
                    'name': file.name
                }
            )
    # Adding folders
    for folder in p_folders:
        # Match
        if ((folder.parent is None and p_current_object['id'] is None) or (folder.parent is not None and folder.parent.id == p_current_object['id'])):
            v_folder = {
                'id': folder.id,
                'name': folder.name,
                'files': [],
                'folders': []
            }

            build_snippets_object_recursive(p_folders,p_files,v_folder)

            p_current_object['folders'].append(v_folder)


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

    v_return['v_data'] = {
        'v_list_nodes': [],
        'v_list_texts': []
    }

    try:
        for folder in SnippetFolder.objects.filter(user=request.user,parent=v_sn_id_parent):
            v_node_data = {
                'v_id': folder.id,
                'v_name': folder.name
            }
            v_return['v_data']['v_list_nodes'].append(v_node_data)
    except Exception as exc:
        None

    try:
        for file in SnippetFile.objects.filter(user=request.user,parent=v_sn_id_parent):
            v_node_data = {
                'v_id': file.id,
                'v_name': file.name
            }
            v_return['v_data']['v_list_texts'].append(v_node_data)
    except Exception as exc:
        None

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
        v_return['v_data'] = SnippetFile.objects.get(id=v_st_id).text
    except Exception as exc:
        None

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

    if v_sn_id_parent:
        v_parent = SnippetFolder.objects.get(id=v_sn_id_parent)
    else:
        v_parent = None

    try:
        new_date = make_aware(datetime.now())
        if v_mode == 'node':
            folder = SnippetFolder(
                user=request.user,
                parent=v_parent,
                name=v_name,
                create_date=new_date,
                modify_date=new_date
            )
            folder.save()
        else:
            file = SnippetFile(
                user=request.user,
                parent=v_parent,
                name=v_name,
                create_date=new_date,
                modify_date=new_date,
                text=''
            )
            file.save()
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
            folder = SnippetFolder.objects.get(id=v_id)
            folder.delete()
        else:
            file = SnippetFile.objects.get(id=v_id)
            file.delete()

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
    v_parent_id = json_object['p_parent']
    v_text = json_object['p_text']

    if v_parent_id:
        v_parent = SnippetFolder.objects.get(id=v_parent_id)
    else:
        v_parent = None

    try:
        #new snippet
        new_date = make_aware(datetime.now())
        if not v_id:
            file = SnippetFile(
                user=request.user,
                parent=v_parent,
                name=v_name,
                create_date=new_date,
                modify_date=new_date,
                text=v_text
            )
            file.save()
        #existing snippet
        else:
            file = SnippetFile.objects.get(id=v_id)
            file.text = v_text.replace("'", "''")
            file.modify_date=new_date
            file.save()

        v_return['v_data'] = {
            'type': 'snippet',
            'id': file.id,
            'parent': v_parent_id,
            'name': file.name
        }


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

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
            folder = SnippetFolder.objects.get(id=v_id)
            folder.name = v_name.replace("'", "''")
            folder.modify_date=make_aware(datetime.now())
            folder.save()
        #snippet
        else:
            file = SnippetFile.objects.get(id=v_id)
            file.name = v_name.replace("'", "''")
            file.modify_date=make_aware(datetime.now())
            file.save()


    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

        v_return['v_data'] = ''

    return JsonResponse(v_return)
