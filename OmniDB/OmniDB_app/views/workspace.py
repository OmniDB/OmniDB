from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from datetime import datetime
from math import ceil
import json

import sys

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB import settings
from OmniDB_app.include.Session import Session

from django.contrib.sessions.backends.db import SessionStore
import sqlparse
import random
import string
import platform

from OmniDB_app.models.main import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from OmniDB_app.views.memory_objects import *

@login_required
def index(request):
    try:
        user_details = UserDetails.objects.get(user=request.user)
    #user details does not exist, create it.
    except Exception:
        user_details = UserDetails(user=request.user)
        user_details.save()

    #Invalid session
    if not request.session.get('omnidb_session'):
        #request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('/')

    v_session = request.session.get('omnidb_session')

    v_session.RefreshDatabaseList();

    #Shortcuts
    default_shortcuts = []
    user_shortcuts = []

    shortcut_object = {}

    try:
        user_shortcuts = Shortcut.objects.filter(user=request.user)
        for shortcut in user_shortcuts:
            shortcut_object[shortcut.code] = {
                'ctrl_pressed': 1 if shortcut.ctrl_pressed else 0,
                'shift_pressed': 1 if shortcut.shift_pressed else 0,
                'alt_pressed': 1 if shortcut.alt_pressed else 0,
                'meta_pressed': 1 if shortcut.meta_pressed else 0,
                'shortcut_key': shortcut.key,
                'os': shortcut.os,
                'shortcut_code': shortcut.code
            }
    except Exception as exc:
        None

    v_show_terminal_option = 'false'

    if user_details.welcome_closed:
        welcome_closed = 1
    else:
        welcome_closed = 0

    if request.user.is_superuser:
        superuser = 1
    else:
        superuser = 0

    if user_details.theme=='light':
        theme = 'omnidb'
    else:
        theme = 'omnidb_dark'

    context = {
        'session' : None,
        'editor_theme': theme,
        'theme': user_details.theme,
        'font_size': user_details.font_size,
        'user_id': request.user.id,
        'user_key': request.session.session_key,
        'user_name': request.user.username,
        'super_user': superuser,
        'welcome_closed': 1 if user_details.welcome_closed else 0,
        'enable_omnichat': 0,
        'csv_encoding': user_details.csv_encoding,
        'csv_delimiter': user_details.csv_delimiter,
        'desktop_mode': settings.DESKTOP_MODE,
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION,
        'menu_item': 'workspace',
        'shortcuts': shortcut_object,
        'tab_token': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(20)),
        'show_terminal_option': v_show_terminal_option,
        'url_folder': settings.PATH,
        'csrf_cookie_name': settings.CSRF_COOKIE_NAME
    }

    #wiping saved tabs databases list
    v_session.v_tabs_databases = dict([])
    request.session['omnidb_session'] = v_session

    clear_client_object(
        p_client_id = request.session.session_key
    )

    template = loader.get_template('OmniDB_app/new.html')
    return HttpResponse(template.render(context, request))

@user_authenticated
def welcome(request):

    context = {
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION
    }

    template = loader.get_template('OmniDB_app/welcome.html')
    return HttpResponse(template.render(context, request))

@user_authenticated
def shortcuts(request):

    context = {
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION
    }

    template = loader.get_template('OmniDB_app/shortcuts.html')
    return HttpResponse(template.render(context, request))

@user_authenticated
def close_welcome(request):

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

    try:
        user_details = UserDetails.objects.get(user=request.user)
        user_details.welcome_closed = True
        user_details.save()
    except Exception:
        None

    return JsonResponse(v_return)

@user_authenticated
def save_config_user(request):

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
    p_font_size = json_object['p_font_size']
    p_theme = json_object['p_theme']
    p_pwd = json_object['p_pwd']
    p_csv_encoding = json_object['p_csv_encoding']
    p_csv_delimiter = json_object['p_csv_delimiter']

    v_session.v_theme_id = p_theme
    v_session.v_font_size = p_font_size
    v_session.v_csv_encoding = p_csv_encoding
    v_session.v_csv_delimiter = p_csv_delimiter

    if p_pwd!="":
        request.user.set_password(p_pwd)

    user_details = UserDetails.objects.get(user=request.user)
    user_details.theme = p_theme
    user_details.font_size = p_font_size
    user_details.csv_encoding = p_csv_encoding
    user_details.csv_delimiter = p_csv_delimiter
    user_details.save()

    request.session['omnidb_session'] = v_session

    return JsonResponse(v_return)

@user_authenticated
def save_shortcuts(request):

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
    v_shortcuts = json_object['p_shortcuts']
    v_current_os = json_object['p_current_os']

    try:
        #Delete existing user shortcuts
        Shortcut.objects.filter(user=request.user).delete()

        #Adding new user shortcuts
        for v_shortcut in v_shortcuts:
            shortcut_object = Shortcut(
                user=request.user,
                code=v_shortcut['shortcut_code'],
                os=v_current_os,
                ctrl_pressed= True if v_shortcut['ctrl_pressed']==1 else False,
                shift_pressed= True if v_shortcut['shift_pressed']==1 else False,
                alt_pressed= True if v_shortcut['alt_pressed']==1 else False,
                meta_pressed= True if v_shortcut['meta_pressed']==1 else False,
                key=v_shortcut['shortcut_key']
            )
            shortcut_object.save()
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
def get_database_list(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    v_session = request.session.get('omnidb_session')
    v_cryptor = request.session.get('cryptor')

    v_databases = []
    v_groups = []
    v_remote_terminals = []
    v_options = ''

    #Global group
    v_current_group_data = {
        'v_group_id': 0,
        'v_name': 'All connections',
        'conn_list': []
    }
    v_groups.append(v_current_group_data)

    try:
        for group in Group.objects.filter(user=request.user):
            v_current_group_data = {
                'v_group_id': group.id,
                'v_name':  group.name,
                'conn_list': []
            }
            for group_conn in GroupConnection.objects.filter(group=group):
                v_current_group_data['conn_list'].append(group_conn.connection.id)

            v_groups.append(v_current_group_data)

    # No group connections
    except Exception as exc:
        None

    v_options = ''

    #Connection list
    v_index = 0
    for key,v_database_object in v_session.v_databases.items():
        if v_database_object['tunnel']['enabled'] or v_database_object['technology']=='terminal':
            v_alias = ''
            if v_database_object['alias']!='':
                v_alias = v_database_object['alias']
            v_details = v_database_object['tunnel']['user'] + '@' + v_database_object['tunnel']['server'] + ':' + v_database_object['tunnel']['port']
            v_terminal_object = {
                'v_conn_id': key,
                'v_alias': v_alias,
                'v_details': v_details,
                'v_public': v_database_object['public']
            }
            v_remote_terminals.append(v_terminal_object)

        if v_database_object['database']!=None:
            v_database = v_database_object['database']

            if v_database.v_alias=='':
                v_alias = ''
            else:
                v_alias = '({0}) '.format(v_database.v_alias)
            if not v_database_object['tunnel']['enabled']:
                v_details = v_database.PrintDatabaseDetails()
            else:
                v_details = v_database.PrintDatabaseDetails() + ' <b>(' + v_database_object['tunnel']['server'] + ':' + v_database_object['tunnel']['port'] + ')</b>'

            v_database_data = {
                'v_db_type': v_database.v_db_type,
                'v_alias': v_database.v_alias,
                'v_conn_id': v_database.v_conn_id,
                'v_console_help': v_database.v_console_help,
                'v_database': v_database.v_active_service,
                'v_conn_string': v_database.v_conn_string,
                'v_details1': v_database.PrintDatabaseInfo(),
                'v_details2': v_details,
                'v_public': v_database_object['public']
            }

            v_databases.append(v_database_data)

    #retrieving saved tabs
    try:
        v_existing_tabs = []
        for tab in Tab.objects.filter(user=request.user).order_by('connection'):
            if (tab.connection.public or tab.connection.user.id == request.user.id):
                v_existing_tabs.append({'index': tab.connection.id, 'snippet': tab.snippet, 'title': tab.title, 'tab_db_id': tab.id})

    except Exception as exc:
        None

    request.session['omnidb_session'] = v_session

    v_return['v_data'] = {
        'v_select_html': None,
        'v_select_group_html': None,
        'v_connections': v_databases,
        'v_groups': v_groups,
        'v_remote_terminals': v_remote_terminals,
        'v_id': v_session.v_database_index,
        'v_existing_tabs': v_existing_tabs
    }

    return JsonResponse(v_return)

@user_authenticated
def change_active_database(request):

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
    v_new_database = json_object['p_database']

    v_session.v_tabs_databases[v_tab_id] = v_new_database

    request.session['omnidb_session'] = v_session

    v_return['v_data'] = {
    }

    return JsonResponse(v_return)

@user_authenticated
def renew_password(request):

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
    v_password = json_object['p_password']

    v_database_object = v_session.v_databases[v_database_index]
    v_database_object['database'].v_connection.v_password = v_password

    v_test = v_database_object['database'].TestConnection()

    if v_test=='Connection successful.':
        v_database_object['prompt_timeout'] = datetime.now()
    else:
        v_return['v_error'] = True
        v_return['v_data'] = v_test

    request.session['omnidb_session'] = v_session

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def draw_graph(request, v_database):

    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_complete = json_object['p_complete']
    v_schema = json_object['p_schema']

    v_nodes = []
    v_edges = []

    try:
        v_tables = v_database.QueryTables(False,v_schema)
        for v_table in v_tables.Rows:
            v_node_data = {
                'id': v_table['table_name'],
                'label': v_table['table_name'],
                'group': 1
            }

            if v_complete:
                v_node_data['label'] += "\n"
                v_columns = v_database.QueryTablesFields(v_table['table_name'],False,v_schema)
                for v_column in v_columns.Rows:
                    v_node_data['label'] += v_column['column_name'] + ' : ' + v_column['data_type'] + "\n"

            v_nodes.append(v_node_data)

        v_data = v_database.QueryTablesForeignKeys(None,False,v_schema)

        v_curr_constraint = ""
        v_curr_from = ""
        v_curr_to = ""
        v_curr_to_schema = ""

        for v_fk in v_data.Rows:
            if v_curr_constraint!="" and v_curr_constraint!=v_fk["constraint_name"]:
                v_edge = {
                    'from' : v_curr_from,
                    'to' : v_curr_to,
                    'label': '',
                    'arrows': 'to'
                }

                #FK referencing other schema, create a new node if it isn't in v_nodes list.
                if v_database.v_schema != v_curr_to_schema:
                    v_found = False
                    for k in range (len(v_nodes) - 1,0):
                        if v_nodes[k]['label'] == v_curr_to:
                            v_found = True
                            break

                    if not v_found:
                        v_node = {
                            'id' : v_curr_to,
                            'label': v_curr_to,
                            'group': 0
                        }
                        v_nodes.append(v_node)

                v_edges.append (v_edge)
                v_curr_constraint = ""

            v_curr_from = v_fk["table_name"]
            v_curr_to = v_fk["r_table_name"]
            v_curr_constraint = v_fk["constraint_name"]
            v_curr_to_schema = v_fk["r_table_schema"]

        if v_curr_constraint!="":
            v_edge = {
                'from' : v_curr_from,
                'to' : v_curr_to,
                'label': '',
                'arrows': 'to'
            }

            v_edges.append (v_edge)

            #FK referencing other schema, create a new node if it isn't in v_nodes list.
            if v_database.v_schema != v_curr_to_schema:
                v_found = False

                for k in range (len(v_nodes) - 1,0):
                    if v_nodes[k]['label'] == v_curr_to:
                        v_found = True
                        break

                if not v_found:
                    v_node = {
                        'id' : v_curr_to,
                        'label': v_curr_to,
                        'group': 0
                    }

                    v_nodes.append(v_node)

        v_return['v_data'] = {
            'v_nodes': v_nodes,
            'v_edges': v_edges
        }

    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def start_edit_data(request, v_database):

    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_table          = json_object['p_table']
    v_schema         = json_object['p_schema']

    v_return['v_data'] = {
        'v_pk' : [],
        'v_cols' : [],
        'v_ini_orderby' : ''
    }

    try:
        v_pk = v_database.QueryTablesPrimaryKeys (v_table,False,v_schema)
        if v_database.v_has_schema:
            v_table_name = v_schema + '.' + v_table
        else:
            v_table_name = v_table
        v_columns = v_database.QueryTablesFields(v_table,False,v_schema)

        v_pk_cols = None
        if v_pk != None and len(v_pk.Rows) > 0:
            v_pk_cols = v_database.QueryTablesPrimaryKeysColumns(v_pk.Rows[0]['constraint_name'], v_table, False, v_schema)
            v_return['v_data']['v_ini_orderby'] = 'ORDER BY '
            v_first = True
            for v_pk_col in v_pk_cols.Rows:
                if not v_first:
                    v_return['v_data']['v_ini_orderby'] = v_return['v_data']['v_ini_orderby'] + ', '
                v_first = False
                v_return['v_data']['v_ini_orderby'] = v_return['v_data']['v_ini_orderby'] + 't.' + v_pk_col['column_name']
        v_index = 0
        for v_column in v_columns.Rows:
            v_col = {}
            v_col['v_type'] = v_column['data_type']
            v_col['v_column'] = v_column['column_name']
            v_col['v_is_pk'] = False
            # Finding corresponding PK column
            if v_pk_cols != None:
                for v_pk_col in v_pk_cols.Rows:
                    if v_pk_col['column_name'].lower() == v_column['column_name'].lower():
                        v_col['v_is_pk'] = True
                        v_pk_info = {}
                        v_pk_info['v_column'] = v_pk_col['column_name']
                        v_pk_info['v_index'] = v_index
                        v_pk_info['v_type'] = v_column['data_type']
                        v_return['v_data']['v_pk'].append(v_pk_info)
                        break
            v_return['v_data']['v_cols'].append(v_col)
            v_index = v_index + 1

    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True

    return JsonResponse(v_return)

def get_positions(p_source, p_search_string):
    ret = []
    v_len = len(p_search_string)
    start = -v_len
    while True:
        try:
            start = p_source.index(p_search_string, start + v_len)
            ret.append(start)
        except ValueError:
            break
    return ret

def is_reference(p_sql, p_prefix, p_occurence_index,p_cursor_index):
    v_length = len(p_prefix)

    v_next_index = p_occurence_index + v_length

    #If prefix and occurence are the same
    if v_next_index == p_cursor_index:
        return False

    #prefix is at the end of the string
    if p_occurence_index + v_length >= len(p_sql):
        if p_occurence_index == 0:
            return False
        elif p_sql [p_occurence_index - 1] == ' ':
            return True
        else:
            return False

    next_char = p_sql [v_next_index]

    if next_char=='.':
        return False

    if next_char == ',' or next_char == '\n' or next_char == ' ' or next_char == ')':
        if p_occurence_index == 0:
            return False
        elif p_sql [p_occurence_index - 1] == ' ':
            return True
        else:
            return False

    return False

@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def get_completions(request, v_database):

    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_tab_id = json_object['p_tab_id']
    p_prefix = json_object['p_prefix']
    p_sql = json_object['p_sql']
    p_prefix_pos = json_object['p_prefix_pos']

    v_list = []

    v_found = False

    inst = get_positions (p_sql, p_prefix)

    index = 0

    for v_index in inst:
        v_found = is_reference(p_sql, p_prefix, v_index, p_prefix_pos)
        if v_found:
            index = v_index
            break

    if not v_found:
        v_return['v_data'] = v_list
        return JsonResponse(v_return)

    v_table = ""

    while index > 0 and p_sql[index - 1] == ' ':
        index = index - 1

    v_last_pos = index

    if p_sql [v_last_pos - 1] == ')':
        v_level = 0

        while index > 0:
            if p_sql [index - 1] == ')':
                v_level = v_level - 1
            elif p_sql [index - 1] == '(':
                v_level = v_level + 1

            if p_sql [index - 1] == '(' and v_level == 0:
                break

            index = index - 1

        v_table = p_sql[index - 1:v_last_pos]


    else:
        v_quoted = False
        if p_sql [index - 1]=='"':
            v_quoted = True
        while index > 0 and (p_sql [index - 1] != ' ' or v_quoted) and (p_sql [index - 1] != ',' or v_quoted):
            index = index - 1
            if p_sql [index - 2] == '"':
                if v_quoted:
                    v_quoted = False
                else:
                    v_quoted = True

        v_first_pos = index
        v_table = p_sql[v_first_pos:v_last_pos]
    try:
        v_data1 = v_database.v_connection.GetFields ("select x.* from " + v_table + " x where 1 = 0")
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_score = 100

    v_score -= 100

    for v_type in v_data1:
        v_list.append ({'value': p_prefix + "." + v_type.v_truename, 'score': v_score, 'meta': v_type.v_dbtype});
        v_score -= 100;

    v_return['v_data'] = v_list

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def get_completions_table(request, v_database):

    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    p_database_index = json_object['p_database_index']
    p_tab_id = json_object['p_tab_id']
    p_table = json_object['p_table']
    p_schema = json_object['p_schema']

    if v_database.v_has_schema:
        v_table_name = p_schema + "." + p_table
    else:
        v_table_name = p_table

    v_list = []

    try:
        v_data1 = v_database.v_connection.GetFields ("select x.* from " + v_table_name + " x where 1 = 0")
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_score = 100

    #v_list.append ({'value': "t.", 'score': v_score, 'meta': ""})

    v_score -= 100

    for v_type in v_data1:
        v_list.append ({'value': "t." + v_type.v_truename, 'score': v_score, 'meta': v_type.v_dbtype});
        v_score -= 100;

    v_return['v_data'] = v_list

    return JsonResponse(v_return)

@user_authenticated
def indent_sql(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    #Invalid session
    if not request.session.get('omnidb_session'):
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    v_sql = json_object['p_sql']

    v_session = request.session.get('omnidb_session')

    v_return['v_data'] = v_sql


    try:
        v_return['v_data'] = sqlparse.format(v_sql, reindent=True)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def refresh_monitoring(request, v_database):
    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    v_tab_id = json_object['p_tab_id']
    v_sql = json_object['p_query']

    try:
        v_data = v_database.Query(v_sql,True,True)
        v_return['v_data'] = {
            'v_col_names' : v_data.Columns,
            'v_data' : v_data.Rows,
            'v_query_info' : "Number of records: {0}".format(len(v_data.Rows))
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True

    return JsonResponse(v_return)

@user_authenticated
def get_command_list(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))
    v_current_page = json_object['p_current_page']
    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_command_contains']
    v_command_from = json_object['p_command_from']
    v_command_to = json_object['p_command_to']

    v_session = request.session.get('omnidb_session')

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        conn = Connection.objects.get(id=v_database.v_conn_id)

        v_query = QueryHistory.objects.filter(
            user=request.user,
            connection=conn,
            snippet__icontains=v_command_contains
        ).order_by('-start_time')

        if v_command_from is not None and v_command_from != '':
            v_query = v_query.filter(
                start_time__gte=v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_query = v_query.filter(
                start_time__lte=v_command_to
            )

        v_count = v_query.count()

        offset = ((v_current_page-1) * settings.CH_CMDS_PER_PAGE)

        v_commands = v_query[offset:offset+settings.CH_CMDS_PER_PAGE]

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_command_list = []

    index = 0

    for v_command in v_commands:
        v_command_data_list = []

        v_command_data_list.append(v_command.start_time)
        v_command_data_list.append(v_command.end_time)
        v_command_data_list.append(v_command.duration)

        if v_command.status=='success':
            v_command_data_list.append("<div class='text-center'><i title='Success' class='fas fa-check text-success action-grid action-status-ok'></i></div>")
        else:
            v_command_data_list.append("<div class='text-center'><i title='Error' class='fas fa-exclamation-circle text-danger action-grid action-status-error'></i></div>")

        # v_command_data_list.append("<div class='text-center'><button type='button' class='btn btn-sm btn-secondary my-1'><i title='Open command in the current tab' class='fas fa-bolt action-grid action-bolt' onclick='commandHistoryOpenCmd({0})'></i></button></div>".format(index))
        v_command_data_list.append(v_command.snippet)

        v_command_list.append(v_command_data_list)

        index = index + 1

    v_page = ceil(v_count/settings.CH_CMDS_PER_PAGE)
    if v_page==0:
        v_page=1

    v_return['v_data'] = {
        'commandList': v_command_list,
        'pages': v_page
    }

    return JsonResponse(v_return)

@user_authenticated
def clear_command_list(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))

    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_command_contains']
    v_command_from = json_object['p_command_from']
    v_command_to = json_object['p_command_to']

    v_session = request.session.get('omnidb_session')

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        conn = Connection.objects.get(id=v_database.v_conn_id)

        v_query = QueryHistory.objects.filter(
            user=request.user,
            connection=conn,
            snippet__icontains=v_command_contains
        ).order_by('-start_time')

        if v_command_from is not None and v_command_from != '':
            v_query = v_query.filter(
                start_time__gte=v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_query = v_query.filter(
                start_time__lte=v_command_to
            )

        v_query.delete()
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

@user_authenticated
def get_console_history(request):

    #User not authenticated
    if not request.user.is_authenticated:
        v_return['v_error'] = True
        v_return['v_error_id'] = 1
        return JsonResponse(v_return)

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_current_page = json_object['p_current_page']
    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_command_contains']
    v_command_from = json_object['p_command_from']
    v_command_to = json_object['p_command_to']

    v_return['v_data'] = []
    v_data = []
    v_data_clean = []

    try:
        conn = Connection.objects.get(id=v_database_index)

        v_filter = '''\
            where user_id = {0}
              and conn_id = {1}
        '''.format(
            str(v_session.v_user_id),
            str(v_database_index)
        )

        v_query = ConsoleHistory.objects.filter(
            user=request.user,
            connection=conn,
            snippet__icontains=v_command_contains
        ).order_by('-start_time')

        if v_command_from is not None and v_command_from != '':
            v_query = v_query.filter(
                start_time__gte=v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_query = v_query.filter(
                start_time__lte=v_command_to
            )

        v_count = v_query.count()

        offset = ((v_current_page-1) * settings.CH_CMDS_PER_PAGE)

        v_commands = v_query[offset:offset+settings.CH_CMDS_PER_PAGE]

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_command_list = []

    for v_command in v_commands:
        v_command_data_list = []

        v_command_data_list.append(v_command.start_time)
        v_command_data_list.append(v_command.snippet)

        v_command_list.append(v_command_data_list)


    v_page = ceil(v_count/settings.CH_CMDS_PER_PAGE)
    if v_page==0:
        v_page=1

    v_return['v_data'] = {
        'commandList': v_command_list,
        'pages': v_page
    }

    return JsonResponse(v_return)

@user_authenticated
def clear_console_list(request):

    v_return = {}
    v_return['v_data'] = ''
    v_return['v_error'] = False
    v_return['v_error_id'] = -1

    json_object = json.loads(request.POST.get('data', None))

    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_console_contains']
    v_command_from = json_object['p_console_from']
    v_command_to = json_object['p_console_to']

    v_session = request.session.get('omnidb_session')

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        conn = Connection.objects.get(id=v_database.v_conn_id)

        v_query = ConsoleHistory.objects.filter(
            user=request.user,
            connection=conn,
            snippet__icontains=v_command_contains
        ).order_by('-start_time')

        if v_command_from is not None and v_command_from != '':
            v_query = v_query.filter(
                start_time__gte=v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_query = v_query.filter(
                start_time__lte=v_command_to
            )

        v_query.delete()
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_alias(p_sql,p_pos,p_val):
    try:
        s = sqlparse.parse(p_sql)
        v_alias = p_val[:-1]
        for stmt in s:
            for item in stmt.tokens:
                if item.ttype==None:
                    try:
                        v_cur_alias = item.get_alias()
                        if v_cur_alias==None:
                            if item.value == v_alias:
                                return item.value
                        elif v_cur_alias == v_alias:
                            #check if there is punctuation
                            if str(item.tokens[1].ttype)!='Token.Punctuation':
                                return item.get_real_name()
                            else:
                                return item.tokens[0].value + '.' + item.tokens[2].value
                    except:
                        None

    except Exception as exc:
        return None
    return None


@user_authenticated
@database_required(p_check_timeout = True, p_open_connection = True)
def get_autocomplete_results(request, v_database):

    v_return = {
        'v_data': '',
        'v_error': False,
        'v_error_id': -1
    }

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']
    v_sql = json_object['p_sql']
    v_value = json_object['p_value']
    v_pos = json_object['p_pos']
    v_num_dots = v_value.count('.')

    v_result = []
    max_result_word = ''
    max_complement_word = ''

    v_alias = None
    if v_value!='' and v_value[len(v_value)-1]=='.':
        v_alias = get_alias(v_sql,v_pos,v_value)
        if v_alias:
            try:
                v_data1 = v_database.v_connection.GetFields ("select x.* from " + v_alias + " x where 1 = 0")
                v_current_group = { 'type': 'column', 'elements': [] }
                max_result_length = 0
                max_complement_length = 0
                for v_type in v_data1:
                    curr_result_length = len(v_value + v_type.v_truename)
                    curr_complement_length = len(v_type.v_dbtype)
                    curr_result_word = v_value + v_type.v_truename
                    curr_complement_word = v_type.v_dbtype

                    if curr_result_length > max_result_length:
                        max_result_length = curr_result_length
                        max_result_word = curr_result_word
                    if curr_complement_length > max_complement_length:
                        max_complement_length = curr_complement_length
                        max_complement_word = curr_complement_word

                    v_current_group['elements'].append({ 'value': v_value + v_type.v_truename, 'select_value': v_value + v_type.v_truename, 'complement': v_type.v_dbtype})
                if len(v_current_group['elements']) > 0:
                    v_result.append(v_current_group)
            except Exception as exc:
                None

    if not v_alias:
        v_filter = '''where search.result like '{0}%' '''.format(v_value)
        v_query_columns = 'type,sequence,result,select_value,complement'
        if v_num_dots > 0:
            v_filter = '''where search.result_complete like '{0}%' and search.num_dots <= {1}'''.format(v_value,v_num_dots)
            v_query_columns = 'type,sequence,result_complete as result,select_value,complement_complete as complement'
        elif v_value=='':
            v_filter = '''where search.num_dots = 0 '''

        try:
            max_result_length = 0
            max_complement_length = 0

            v_search = v_database.GetAutocompleteValues(v_query_columns,v_filter)

            if v_search!=None:
                v_current_group = { 'type': '', 'elements': [] }
                if len(v_search.Rows) > 0:
                    v_current_group['type'] = v_search.Rows[0]['type']
                for v_search_row in v_search.Rows:

                    if v_current_group['type'] != v_search_row['type']:
                        v_result.append(v_current_group)
                        v_current_group = { 'type': v_search_row['type'], 'elements': [] }

                    curr_result_length = len(v_search_row['result'])
                    curr_complement_length = len(v_search_row['complement'])
                    curr_result_word = v_search_row['result']
                    curr_complement_word = v_search_row['complement']
                    v_current_group['elements'].append({ 'value': v_search_row['result'], 'select_value': v_search_row['select_value'],'complement': v_search_row['complement']})

                    if curr_result_length > max_result_length:
                        max_result_length = curr_result_length
                        max_result_word = curr_result_word
                    if curr_complement_length > max_complement_length:
                        max_complement_length = curr_complement_length
                        max_complement_word = curr_complement_word

                if len(v_current_group['elements']) > 0:
                    v_result.append(v_current_group)

        except Exception as exc:
            v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
            v_return['v_error'] = True
            return JsonResponse(v_return)

    v_return['v_data'] = {
        'data': v_result,
        'max_result_word': max_result_word,
        'max_complement_word': max_complement_word
    }

    return JsonResponse(v_return)
