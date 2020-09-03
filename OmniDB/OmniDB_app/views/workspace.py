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
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    v_session = request.session.get('omnidb_session')

    v_session.RefreshDatabaseList();

    if settings.IS_SSL:
        v_is_secure = 'true'
    else:
        v_is_secure = 'false'

    if settings.DEV_MODE:
        v_dev_mode = 'true'
    else:
        v_dev_mode = 'false'

    #Shortcuts
    default_shortcuts = []
    user_shortcuts = []

    shortcut_object = {}

    try:
        user_shortcuts = Shortcut.objects.filter(user=request.user)
    except Exception as exc:
        None

    try:
        for default_shortcut in Shortcut.objects.filter(user=None):
            # Search if there is a corresponding user shortcut
            found = False
            for user_shortcut in user_shortcuts:
                if user_shortcut.code == default_shortcut.code:
                    found = True
                    current_shortcut = user_shortcut
            if not found:
                current_shortcut = default_shortcut
            # Adding the selected shortctur
            shortcut_object[current_shortcut.code] = {
                'ctrl_pressed': 1 if current_shortcut.ctrl_pressed else 0,
                'shift_pressed': 1 if current_shortcut.shift_pressed else 0,
                'alt_pressed': 1 if current_shortcut.alt_pressed else 0,
                'meta_pressed': 1 if current_shortcut.meta_pressed else 0,
                'shortcut_key': current_shortcut.key,
                'shortcut_code': current_shortcut.code
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
        'delimiter': user_details.csv_delimiter,
        'desktop_mode': settings.DESKTOP_MODE,
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION,
        'menu_item': 'workspace',
        'is_secure' : v_is_secure,
        'dev_mode': v_dev_mode,
        'autocomplete': settings.BINDKEY_AUTOCOMPLETE,
        'autocomplete_mac': settings.BINDKEY_AUTOCOMPLETE_MAC,
        'shortcuts': shortcut_object,
        'tab_token': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(20)),
        'show_terminal_option': v_show_terminal_option,
        'url_folder': settings.PATH
    }

    #wiping tab connection list
    v_session.v_tab_connections = dict([])
    request.session['omnidb_session'] = v_session

    template = loader.get_template('OmniDB_app/new.html')
    return HttpResponse(template.render(context, request))

def old(request):
    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    v_session = request.session.get('omnidb_session')

    if settings.IS_SSL:
        v_is_secure = 'true'
    else:
        v_is_secure = 'false'

    if settings.DEV_MODE:
        v_dev_mode = 'true'
    else:
        v_dev_mode = 'false'


    v_shortcuts = v_session.v_omnidb_database.v_connection.Query('''
        select default_shortcut_code as shortcut_code,
               case when user_defined_shortcut_code is null then default_ctrl_pressed else user_defined_ctrl_pressed end as ctrl_pressed,
               case when user_defined_shortcut_code is null then default_shift_pressed else user_defined_shift_pressed end as shift_pressed,
               case when user_defined_shortcut_code is null then default_alt_pressed else user_defined_alt_pressed end as alt_pressed,
               case when user_defined_shortcut_code is null then default_meta_pressed else user_defined_meta_pressed end as meta_pressed,
               case when user_defined_shortcut_code is null then default_shortcut_key else user_defined_shortcut_key end as shortcut_key
        from
        (select defaults.shortcut_code as default_shortcut_code,
               defaults.ctrl_pressed as default_ctrl_pressed,
               defaults.shift_pressed as default_shift_pressed,
               defaults.alt_pressed as default_alt_pressed,
               defaults.meta_pressed as default_meta_pressed,
               defaults.shortcut_key as default_shortcut_key,
               user_defined.shortcut_code as user_defined_shortcut_code,
               user_defined.ctrl_pressed as user_defined_ctrl_pressed,
               user_defined.shift_pressed as user_defined_shift_pressed,
               user_defined.alt_pressed as user_defined_alt_pressed,
               user_defined.meta_pressed as user_defined_meta_pressed,
               user_defined.shortcut_key as user_defined_shortcut_key
        from shortcuts defaults
        left join shortcuts user_defined on (defaults.shortcut_code = user_defined.shortcut_code and user_defined.user_id = {0})
        where defaults.user_id is null) subquery
    '''.format(v_session.v_user_id))

    v_welcome_closed = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
        select welcome_closed from users where user_id = {0}
    '''.format(v_session.v_user_id))

    shortcut_object = {}

    for v_shortcut in v_shortcuts.Rows:
        shortcut_object[v_shortcut['shortcut_code']] = {
            'ctrl_pressed': v_shortcut['ctrl_pressed'],
            'shift_pressed': v_shortcut['shift_pressed'],
            'alt_pressed': v_shortcut['alt_pressed'],
            'meta_pressed': v_shortcut['meta_pressed'],
            'shortcut_key': v_shortcut['shortcut_key'],
            'shortcut_code': v_shortcut['shortcut_code']
        }



    #if not v_session.v_super_user or platform.system()=='Windows':
    #    v_show_terminal_option = 'false'
    #else:
    #    v_show_terminal_option = 'true'
    v_show_terminal_option = 'false'
    context = {
        'session' : None,
        'editor_theme': v_session.v_editor_theme,
        'theme_type': v_session.v_theme_type,
        'theme_id': v_session.v_theme_id,
        'editor_font_size': v_session.v_editor_font_size,
        'interface_font_size': v_session.v_interface_font_size,
        'user_id': v_session.v_user_id,
        'user_key': v_session.v_user_key,
        'user_name': v_session.v_user_name,
        'super_user': v_session.v_super_user,
        'welcome_closed': v_welcome_closed,
        'enable_omnichat': v_session.v_enable_omnichat,
        'csv_encoding': v_session.v_csv_encoding,
        'delimiter': v_session.v_csv_delimiter,
        'desktop_mode': settings.DESKTOP_MODE,
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION,
        'menu_item': 'workspace',
        'is_secure' : v_is_secure,
        'dev_mode': v_dev_mode,
        'autocomplete': settings.BINDKEY_AUTOCOMPLETE,
        'autocomplete_mac': settings.BINDKEY_AUTOCOMPLETE_MAC,
        'shortcuts': shortcut_object,
        'tab_token': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(20)),
        'show_terminal_option': v_show_terminal_option,
        'url_folder': settings.PATH
    }

    #wiping tab connection list
    v_session.v_tab_connections = dict([])
    request.session['omnidb_session'] = v_session

    template = loader.get_template('OmniDB_app/workspace.html')
    return HttpResponse(template.render(context, request))

def welcome(request):

    context = {
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION
    }

    template = loader.get_template('OmniDB_app/welcome.html')
    return HttpResponse(template.render(context, request))

def shortcuts(request):

    context = {
        'omnidb_version': settings.OMNIDB_VERSION,
        'omnidb_short_version': settings.OMNIDB_SHORT_VERSION
    }

    template = loader.get_template('OmniDB_app/shortcuts.html')
    return HttpResponse(template.render(context, request))

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

    try:
        #Delete existing user shortcuts
        Shortcut.objects.filter(user=request.user).delete()

        #Adding new user shortcuts
        for v_shortcut in v_shortcuts:
            shortcut_object = Shortcut(
                user=request.user,
                code=v_shortcut['shortcut_code'],
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

def get_database_list(request):

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
    v_session.RefreshDatabaseList();
    for key,v_database_object in v_session.v_databases.items():
        if v_database_object['tunnel']['enabled'] or v_database_object['technology']=='terminal':
            if v_database_object['alias']!='':
                v_alias = v_database_object['alias']
            else:
                v_alias = v_database_object['tunnel']['user'] + '@' + v_database_object['tunnel']['server'] + ':' + v_database_object['tunnel']['port']
            v_terminal_object = {
                'v_conn_id': key,
                'v_alias': v_alias
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
                'v_details1': '{0}{1}'.format(v_alias,v_database.PrintDatabaseInfo()),
                'v_details2': v_details
            }

            v_databases.append(v_database_data)

    #retrieving saved tabs
    try:
        v_existing_tabs = []
        for tab in Tab.objects.filter(user=request.user).order_by('connection'):
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
    v_data = json_object['p_database']

    v_database = v_session.v_databases[v_database_index]['database']

    v_database_new = OmniDatabase.Generic.InstantiateDatabase(
        v_database.v_db_type,
        v_database.v_connection.v_host,
        str(v_database.v_connection.v_port),
        v_database.v_active_service,
        v_database.v_active_user,
        v_database.v_connection.v_password,
        v_database.v_conn_id,
        v_database.v_alias,
        p_conn_string = v_database.v_conn_string,
        p_parse_conn_string = False
    )

    v_database_new.v_active_service = v_data;
    v_database_new.v_connection.v_service = v_data;

    v_session.v_tab_connections[v_tab_id] = v_database_new

    request.session['omnidb_session'] = v_session

    v_return['v_data'] = {
    }

    return JsonResponse(v_return)

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
        #changing password of tab connection
        try:
            v_tab_connection = v_session.v_tab_connections[v_tab_id]
            v_tab_connection.v_connection.v_password = v_password
            v_session.v_tab_connections[v_tab_id] = v_tab_connection
        except Exception:
            None
    else:
        v_return['v_error'] = True
        v_return['v_data'] = v_test

    request.session['omnidb_session'] = v_session

    return JsonResponse(v_return)

def draw_graph(request):

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
    v_complete = json_object['p_complete']
    v_schema = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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

    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)


    v_return['v_data'] = {
        'v_nodes': v_nodes,
        'v_edges': v_edges
    }

    return JsonResponse(v_return)

def start_edit_data(request):

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
    v_table          = json_object['p_table']
    v_schema         = json_object['p_schema']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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

def get_completions(request):

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
    p_database_index = json_object['p_database_index']
    p_tab_id = json_object['p_tab_id']
    p_prefix = json_object['p_prefix']
    p_sql = json_object['p_sql']
    p_prefix_pos = json_object['p_prefix_pos']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_database = v_session.v_tab_connections[p_tab_id]

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

    #v_list.append ({'value': p_prefix + ".", 'score': v_score, 'meta': ""})

    v_score -= 100

    for v_type in v_data1:
        v_list.append ({'value': p_prefix + "." + v_type.v_truename, 'score': v_score, 'meta': v_type.v_dbtype});
        v_score -= 100;

    v_return['v_data'] = v_list

    return JsonResponse(v_return)

def get_completions_table(request):

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
    p_database_index = json_object['p_database_index']
    p_tab_id = json_object['p_tab_id']
    p_table = json_object['p_table']
    p_schema = json_object['p_schema']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_database = v_session.v_tab_connections[p_tab_id]

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

def get_command_list(request):

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
    v_current_page = json_object['p_current_page']
    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_command_contains']
    v_command_from = json_object['p_command_from']
    v_command_to = json_object['p_command_to']

    v_session = request.session.get('omnidb_session')

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        conn = Connection.objects.get(id=v_database.v_conn_id)

        v_filter = '''\
            where user_id = {0}
              and conn_id = {1}
        '''.format(
            str(v_session.v_user_id),
            str(v_database.v_conn_id)
        )

        if v_command_contains is not None and v_command_contains != '':
            v_filter = '''\
                {0}
                  and cl_st_command like '%{1}%'
            '''.format(
                v_filter,
                v_command_contains
            )

        if v_command_from is not None and v_command_from != '':
            v_filter = '''\
                {0}
                  and date(cl_st_start) >= date('{1}')
            '''.format(
                v_filter,
                v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_filter = '''\
                {0}
                  and date(cl_st_start) <= date('{1}')
            '''.format(
                v_filter,
                v_command_to
            )

        v_query = QueryHistory.objects.filter(
            user=request.user,
            connection=conn
        )

        if v_command_from is not None and v_command_from != '':
            v_query = v_query.filter(
                start_time__gte=v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_query = v_query.filter(
                end_time__lte=v_command_to
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

def clear_command_list(request):

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

    v_database_index = json_object['p_database_index']
    v_command_contains = json_object['p_command_contains']
    v_command_from = json_object['p_command_from']
    v_command_to = json_object['p_command_to']

    v_session = request.session.get('omnidb_session')

    v_database = v_session.v_databases[v_database_index]['database']

    try:
        v_filter = '''\
            where user_id = {0}
              and conn_id = {1}
        '''.format(
            str(v_session.v_user_id),
            str(v_database.v_conn_id)
        )

        if v_command_contains is not None and v_command_contains != '':
            v_filter = '''\
                {0}
                  and cl_st_command like '%{1}%'
            '''.format(
                v_filter,
                v_command_contains
            )

        if v_command_from is not None and v_command_from != '':
            v_filter = '''\
                {0}
                  and date(cl_st_start) >= date('{1}')
            '''.format(
                v_filter,
                v_command_from
            )

        if v_command_to is not None and v_command_to != '':
            v_filter = '''\
                {0}
                  and date(cl_st_start) <= date('{1}')
            '''.format(
                v_filter,
                v_command_to
            )

        v_session.v_omnidb_database.v_connection.Execute('''
                delete from command_list
                {0}
            '''.format(v_filter)
        )
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

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

def refresh_monitoring(request):

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
    v_sql            = json_object['p_query']

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_data = v_database.v_connection.Query(v_sql,True,True)
        v_return['v_data'] = {
            'v_col_names' : v_data.Columns,
            'v_data' : v_data.Rows,
            'v_query_info' : "Number of records: {0}".format(len(v_data.Rows))
        }
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

import time

def test_ws(request):

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
    time.sleep(10)

    return JsonResponse(v_return)

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

    # v_session = request.session.get('omnidb_session')

    json_object = json.loads(request.POST.get('data', None))
    v_database_index = json_object['p_database_index']
    v_tab_id = json_object['p_tab_id']

    v_database = v_session.v_tab_connections[v_tab_id]

    v_query = '''
        select command_text,
               command_date
        from console_history
        where user_id = {0}
          and conn_id = {1}
        order by command_date desc
    '''.format(v_session.v_user_id,v_database_index)


    v_return['v_data'] = []
    v_data = []
    v_data_clean = []

    try:
        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:
            v_actions = "<i title='Select' class='fas fa-check-circle action-grid action-check' onclick='consoleHistorySelectCommand()'></i>"

            v_data.append([v_actions,v_unit['command_date'],v_unit['command_text']])
            v_data_clean.append(v_unit['command_text'])
        v_return['v_data'] = { 'data': v_data, 'data_clean': v_data_clean }

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)

def get_console_history_clean(request):

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

    v_query = '''
        select command_text,
               command_date
        from console_history
        where user_id = {0}
          and conn_id = {1}
        order by command_date desc
    '''.format(v_session.v_user_id,v_database_index)


    v_return['v_data'] = []
    v_data_clean = []

    try:
        v_units = v_session.v_omnidb_database.v_connection.Query(v_query)
        for v_unit in v_units.Rows:
            v_data_clean.append(v_unit['command_text'])
        v_return['v_data'] = v_data_clean

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


def get_autocomplete_results(request):

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
    v_sql = json_object['p_sql']
    v_value = json_object['p_value']
    v_pos = json_object['p_pos']
    v_num_dots = v_value.count('.')

    v_database = v_session.v_tab_connections[v_tab_id]

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

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

    #get reserved words list if there are no dots
    #if v_num_dots == 0:
    #    v_reserved_words_list = v_database.v_reserved_words
    #    v_value_upper = v_value.upper()
    #    v_filtered_words_list = [k for k in v_reserved_words_list if k.startswith(v_value_upper)]
    #    v_current_group = { 'type': 'keyword', 'elements': [] }
    #    for v_filtered_word in v_filtered_words_list:
    #        v_current_group['elements'].append({ 'value': v_filtered_word, 'select_value': v_filtered_word, 'complement': ''})
    #    if len(v_current_group['elements']) > 0:
    #        v_result.append(v_current_group)

    v_return['v_data'] = {
                            'data': v_result,
                            'max_result_word': max_result_word,
                            'max_complement_word': max_complement_word
                        }

    return JsonResponse(v_return)
