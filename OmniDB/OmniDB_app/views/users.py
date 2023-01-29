from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
import uuid
import json

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB_app.include.Session import Session
from OmniDB import settings
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User

from OmniDB_app.views.memory_objects import user_authenticated

@user_authenticated
def get_users(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    v_session = request.session.get('omnidb_session')

    v_user_list = []
    v_user_id_list = []

    if not v_session.v_super_user:
        v_return['v_data'] = 'You must be superuser to manage users.'
        v_return['v_error'] = True
        return JsonResponse(v_return)
    try:
        for user in User.objects.all():
            v_user_data_list = []
            v_user_data_list.append(user.username)
            v_user_data_list.append('')
            v_user_data_list.append(1 if user.is_superuser else 0)
            v_user_data_list.append('''<i title="Remove User" class='fas fa-times action-grid action-close' onclick='removeUser("{0}")'></i>'''.format(user.id))

            v_user_list.append(v_user_data_list)
            v_user_id_list.append(user.id)
    except Exception as exc:
        None



    v_return['v_data'] = {
        'v_data': v_user_list,
        'v_user_ids': v_user_id_list
    }

    return JsonResponse(v_return)

@user_authenticated
def new_user(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    v_session = request.session.get('omnidb_session')

    if not v_session.v_super_user:
        v_return['v_data'] = 'You must be superuser to manage users.'
        v_return['v_error'] = True
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    v_data = json_object['p_data']

    try:
        for user in v_data:
            new_user = User.objects.create_user(
                username=user[0],
                password=user[1],
                email='',
                last_login=timezone.now(),
                is_superuser=False,
                first_name='',
                last_name='',
                is_staff=False,
                is_active=True,
                date_joined=timezone.now())
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
def remove_user(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    v_session = request.session.get('omnidb_session')

    if not v_session.v_super_user:
        v_return['v_data'] = 'You must be superuser to manage users.'
        v_return['v_error'] = True
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    v_id = json_object['p_id']

    try:
        user = User.objects.get(id=v_id)
        user.delete()
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
def save_users(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1


    v_session = request.session.get('omnidb_session')

    if not v_session.v_super_user:
        v_return['v_data'] = 'You must be superuser to manage users.'
        v_return['v_error'] = True
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))

    try:
        v_data = json_object['p_data']

        # Creating new users.
        v_data_new = v_data['new']
        for user_item in v_data_new:
            new_user = User.objects.create_user(
                username=user_item[0],
                password=user_item[1],
                email='',
                last_login=timezone.now(),
                is_superuser=False,
                first_name='',
                last_name='',
                is_staff=False,
                is_active=True,
                date_joined=timezone.now())

        # Editting users.
        v_data_edited = v_data['edited']
        v_user_id_list = json_object['p_user_id_list']
        v_index = 0
        for r in v_data_edited:
            user = User.objects.get(id=v_user_id_list[v_index])
            user.username = r[0]
            if r[1]!="":
                user.set_password(r[1])
            user.is_superuser = True if r[2]==1 else False
            user.save()
            v_index = v_index + 1

            if request.user == user and r[1]!="":
                update_session_auth_hash(request,user)

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
