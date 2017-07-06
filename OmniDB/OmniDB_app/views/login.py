from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from OmniDB import ws_core
from OmniDB import settings
import json

import sys
sys.path.append("OmniDB_app/include")

import Spartacus.Database, Spartacus.Utils
import OmniDatabase
from Session import Session
from OmniDB import ws_core
from OmniDB import settings

def index(request):
    context = {
    }

    template = loader.get_template('OmniDB_app/login.html')
    return HttpResponse(template.render(context, request))

def logout(request):

    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was already destroyed."
        return redirect('login')

    v_session = request.session.get('omnidb_session')

    #removing from session list
    ws_core.omnidb_sessions.pop(v_session.v_user_key,None)

    request.session['omnidb_session'] = None

    return redirect('login')

def check_session_message(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    if request.session.get('omnidb_alert_message'):
        v_return['v_data'] = request.session.get('omnidb_alert_message')
        request.session['omnidb_alert_message'] = ''

    return JsonResponse(v_return)

def sign_in(request):

    v_return = {}
    v_return['v_data'] = False
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    if not request.session.get('cryptor'):
        request.session['cryptor'] = Spartacus.Utils.Cryptor("omnidb")

    json_object = json.loads(request.POST.get('data', None))
    username = json_object['p_username']
    pwd = json_object['p_pwd']

    database = OmniDatabase.Generic.InstantiateDatabase(
        'sqlite',
        '',
        '',
        settings.OMNIDB_DATABASE,
        '',
        '',
        '0',
        ''
    )

    table = database.v_connection.Query('''
        select u.user_id,
               u.password,
               t.theme_id,
               t.theme_name,
               t.theme_type,
               u.editor_font_size,
               (case when u.chat_enabled is null then 1 else u.chat_enabled end) as chat_enabled,
               (case when u.super_user is null then 0 else u.super_user end) as super_user,
               u.user_key
        from users u,
             themes t
         where u.theme_id = t.theme_id
        and u.user_name = '{0}'
    '''.format(username))

    if len(table.Rows) > 0:
        cryptor = request.session.get('cryptor')
        pwd_decrypted = cryptor.Decrypt(table.Rows[0]['password'])
        if pwd_decrypted == pwd:
            v_session = Session(
                table.Rows[0]["user_id"],
                username,
                database,
                table.Rows[0]["theme_name"],
                table.Rows[0]["theme_type"],
                table.Rows[0]["theme_id"],
                table.Rows[0]["editor_font_size"],
                int(table.Rows[0]["chat_enabled"]),
                int(table.Rows[0]["super_user"]),
                cryptor,
                table.Rows[0]["user_key"]
            )
            request.session['omnidb_session'] = v_session
            v_return['v_data'] = True
            ws_core.omnidb_sessions[v_session.v_user_key] = v_session

    return JsonResponse(v_return)
