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

def index(request):
    #Invalid session
    if not request.session.get('omnidb_session'):
        request.session ["omnidb_alert_message"] = "Session object was destroyed, please sign in again."
        return redirect('login')

    v_session = request.session.get('omnidb_session')

    if len(v_session.v_databases)==0:
        request.session ["omnidb_alert_message"] = "Create at least one connection."
        return redirect('connections')

    if settings.IS_SSL:
        v_is_secure = 'true'
    else:
        v_is_secure = 'false'

    if request.session.get('selected_connection')!=None:
        v_connection = request.session.get('selected_connection')
        request.session['selected_connection'] = None
    else:
        v_connection = -1

    context = {
        'session' : v_session,
        'desktop_mode': settings.DESKTOP_MODE,
        'omnidb_version': settings.OMNIDB_VERSION,
        'menu_item': 'workspace',
        'query_port': settings.WS_QUERY_PORT,
        'is_secure' : v_is_secure,
        'execute': settings.BINDKEY_EXECUTE,
        'execute_mac': settings.BINDKEY_EXECUTE_MAC,
        'replace': settings.BINDKEY_REPLACE,
        'replace_mac': settings.BINDKEY_REPLACE_MAC,
        'selected_connection': v_connection
    }

    template = loader.get_template('OmniDB_app/workspace.html')
    return HttpResponse(template.render(context, request))

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
    v_cryptor = request.session.get('cryptor')

    json_object = json.loads(request.POST.get('data', None))
    p_font_size = json_object['p_font_size']
    p_theme = json_object['p_theme']
    p_pwd = json_object['p_pwd']
    p_chat_enabled = json_object['p_chat_enabled']

    v_session.v_theme_id = p_theme
    v_session.v_editor_font_size = p_font_size
    v_session.v_enable_omnichat = p_chat_enabled

    v_enc_pwd = v_cryptor.Encrypt(p_pwd)

    v_update_command = ""
    v_query_theme_name = "select theme_name, theme_type from themes where theme_id = " + p_theme

    if p_pwd!="":
        v_update_command = '''
            update users
            set theme_id = {0},
            editor_font_size = '{1}',
            password = '{2}',
            chat_enabled = {3}
            where user_id = {4}
        '''.format(p_theme,p_font_size,v_enc_pwd,p_chat_enabled,v_session.v_user_id)
    else:
        v_update_command = '''
            update users
            set theme_id = {0},
            editor_font_size = '{1}',
            chat_enabled = {2}
            where user_id = {3}
        '''.format(p_theme,p_font_size,p_chat_enabled,v_session.v_user_id)

    try:
        v_session.v_omnidb_database.v_connection.Execute(v_update_command)
        v_theme_details = v_session.v_omnidb_database.v_connection.Query(v_query_theme_name)

        v_session.v_editor_theme = v_theme_details.Rows[0]["theme_name"]
        v_session.v_theme_type = v_theme_details.Rows[0]["theme_type"]

        v_details = {
            'v_theme_name': v_theme_details.Rows[0]["theme_name"],
            'v_theme_type': v_theme_details.Rows[0]["theme_type"]
        }

        v_return['v_data'] = v_details

    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True

    request.session['omnidb_session'] = v_session

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
    v_options = ''

    #Connection list
    v_index = 0
    for v_database_object in v_session.v_databases:
        v_database = v_database_object['database']
        v_database_data = {
            'v_db_type': v_database.v_db_type,
            'v_alias': v_database.v_alias,
        }

        v_databases.append(v_database_data)

        v_alias = '({0}) '.format(v_database.v_alias)

        v_options = v_options + '<option data-image="/static/OmniDB_app/images/{0}_medium.png\" value="{1}" data-description="{2}">{3}{4}</option>'.format(v_database.v_db_type,v_index,v_database.PrintDatabaseDetails(),v_alias,v_database.PrintDatabaseInfo())
        v_index = v_index + 1

    v_html = '<select style="width: 100%; font-weight: bold;" onchange="changeDatabase(this.value);">{0}</select>'.format(v_options)

    #retrieving saved tabs
    try:
        v_existing_tabs = []
        v_tabs = v_session.v_omnidb_database.v_connection.Query('''
            select conn_id,snippet, tab_id
            from tabs
            where user_id = {0}
            order by conn_id, tab_id
        '''.format(v_session.v_user_id))
        for v_tab in v_tabs.Rows:
            #retrieving index from conn_id
            v_index = 0
            for v_database_object in v_session.v_databases:
                if v_tab['conn_id'] == v_database_object['database'].v_conn_id:
                    v_existing_tabs.append({'index': v_index, 'snippet': v_tab['snippet'], 'tab_db_id': v_tab['tab_id']})
                    break
                v_index = v_index + 1

    except Exception as exc:
        print(exc)
        None

    v_return['v_data'] = {
        'v_select_html': v_html,
        'v_connections': v_databases,
        'v_id': v_session.v_database_index,
        'v_existing_tabs': v_existing_tabs
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
    v_complete = json_object['p_complete']
    v_schema = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

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
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)


    v_return['v_data'] = {
        'v_nodes': v_nodes,
        'v_edges': v_edges
    }

    return JsonResponse(v_return)

def alter_table_data(request):

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
    v_table_name     = json_object['p_table']
    v_schema_name    = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    #Retrieving data types
    v_data_types_table = v_session.v_omnidb_database.v_connection.Query('''
        select dt_type, dt_in_sufix
        from data_types
        where dbt_st_name = '{0}'
    '''.format(v_database.v_db_type))

    v_data_types = []

    for v_data_type in v_data_types_table.Rows:
        if v_data_type["dt_in_sufix"]==0:
            v_data_types.append(v_data_type["dt_type"])
        elif v_data_type["dt_in_sufix"]==1:
            v_data_types.append(v_data_type["dt_type"] + "(#)")
        elif v_data_type["dt_in_sufix"]==2:
            v_data_types.append(v_data_type["dt_type"] + "(#,#)")

    #Retrieving tables list
    v_tables_table = v_database.QueryTables(True)

    v_tables = []

    if v_database.v_has_schema:
        for v_table in v_tables_table.Rows:
            v_tables.append(v_table["table_schema"] + "." + v_table["table_name"])
    else:
        for v_table in v_tables_table.Rows:
            v_tables.append(v_table["table_name"])

    if v_table_name:

        #Retrieving columns
        if v_schema_name:
            v_columns_table = v_database.QueryTablesFields(v_table_name, False, v_schema_name)
        else:
            v_columns_table = v_database.QueryTablesFields(v_table_name)

        v_table_columns = []

        for v_column in v_columns_table.Rows:

            try:
                v_data_sufix = v_session.v_omnidb_database.v_connection.ExecuteScalar('''
                    select dt_in_sufix
                    from data_types
                    where dbt_st_name = '{0}'
                    and dt_type = '{1}'
                '''.format(v_database.v_db_type,str.lower(v_column["data_type"])))
            except Exception:
                v_data_sufix = ''

            v_row_data = []

            v_row_data.append(v_column["column_name"])

            if v_data_sufix==2:
                if v_column["data_precision"]!="" and v_column["data_scale"]!="":
                	v_row_data.append(v_column["data_type"]+ "(" + str(v_column["data_precision"]) + "," + str(v_column["data_scale"]) + ")")
                elif v_column["data_scale"]!="":
                	v_row_data.append(v_column["data_type"] + "(" + str(v_column["data_scale"]) + ")")
                else:
                	v_row_data.append(v_column["data_type"])
            elif v_data_sufix==1:
                if v_column["data_length"]!="":
                	v_row_data.append(v_column["data_type"] + "(" + str(v_column["data_length"]) + ")")
                else:
                	v_row_data.append(v_column["data_type"])
            else:
                v_row_data.append(v_column["data_type"])


            v_row_data.append(v_column["nullable"])

            v_row_data.append("");

            v_table_columns.append(v_row_data)

        v_table_constraints = []

        #Retrieving primary key
        if v_schema_name:
            v_pk_table = v_database.QueryTablesPrimaryKeys(v_table_name, False, v_schema_name)
        else:
            v_pk_table = v_database.QueryTablesPrimaryKeys(v_table_name)

        if v_pk_table != None and len(v_pk_table.Rows)>0:

            v_column_list = ''
            v_first = True

            for v_column in v_pk_table.Rows:
            	if not v_first:
            		v_column_list += ", "

            	v_column_list += v_column["column_name"]
            	v_first = False

            v_row_data = []

            v_row_data.append(v_pk_table.Rows[0]["constraint_name"])
            v_row_data.append("Primary Key")
            v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list)
            v_row_data.append("")
            v_row_data.append("")
            v_row_data.append("")
            v_row_data.append("")

            if v_database.v_can_drop_constraint:
            	v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>")
            else:
            	v_row_data.append("")

            v_table_constraints.append(v_row_data)

        #Retrieving foreign keys
        if v_schema_name:
            v_fks_table = v_database.QueryTablesForeignKeys(v_table_name, False, v_schema_name)
        else:
            v_fks_table = v_database.QueryTablesForeignKeys(v_table_name)

        if v_fks_table != None and len(v_fks_table.Rows)>0:

            v_column_list = ""
            v_referenced_column_list = ""
            v_constraint_name = v_fks_table.Rows[0]["constraint_name"]
            v_update_rule = v_fks_table.Rows[0]["update_rule"]
            v_delete_rule = v_fks_table.Rows[0]["delete_rule"]
            v_r_table_name = ""

            if v_database.v_has_schema:
                v_r_table_name = v_fks_table.Rows[0]["r_table_schema"] + "." + v_fks_table.Rows[0]["r_table_name"]
            else:
                v_r_table_name = v_fks_table.Rows[0]["r_table_name"]

            v_first = True

            for v_column in v_fks_table.Rows:

                if v_column["constraint_name"]!=v_constraint_name:
                	v_row_data = []

                	v_row_data.append(v_constraint_name)
                	v_row_data.append("Foreign Key")
                	v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list)
                	v_row_data.append(v_r_table_name)
                	v_row_data.append(v_referenced_column_list)
                	v_row_data.append(v_delete_rule)
                	v_row_data.append(v_update_rule)

                	if v_database.v_can_drop_constraint:
                		v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>")
                	else:
                		v_row_data.append("")

                	v_table_constraints.append(v_row_data)

                	v_constraint_name = v_column["constraint_name"]
                	v_update_rule = v_column["update_rule"]
                	v_delete_rule = v_column["delete_rule"]

                	v_column_list = ""
                	v_referenced_column_list = ""
                	v_first = True

                if v_database.v_has_schema:
                	v_r_table_name = v_column["r_table_schema"] + "." + v_column["r_table_name"]
                else:
                	v_r_table_name = v_column["r_table_name"]


                if not v_first:
                	v_column_list += ", "
                	v_referenced_column_list += ", "

                v_column_list += v_column["column_name"]
                v_referenced_column_list += v_column["r_column_name"]
                v_first = False

            if v_column_list!="":
                v_row_data = []

                v_row_data.append(v_constraint_name)
                v_row_data.append("Foreign Key")
                v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list)
                v_row_data.append(v_r_table_name)
                v_row_data.append(v_referenced_column_list)
                v_row_data.append(v_delete_rule)
                v_row_data.append(v_update_rule)

                if v_database.v_can_drop_constraint:
                	v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>")
                else:
                	v_row_data.append("")

                v_table_constraints.append(v_row_data)

        #Retrieving uniques
        if v_schema_name:
            v_uniques_table = v_database.QueryTablesUniques(v_table_name, False, v_schema_name)
        else:
            v_uniques_table = v_database.QueryTablesUniques(v_table_name)

        if v_uniques_table != None and len(v_uniques_table.Rows)>0:
            v_column_list = ""
            v_constraint_name = v_uniques_table.Rows[0]["constraint_name"]
            v_first = True

            for v_column in v_uniques_table.Rows:

            	if v_column["constraint_name"]!=v_constraint_name:
            		v_row_data = []

            		v_row_data.append(v_constraint_name)
            		v_row_data.append("Unique");
            		v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list)
            		v_row_data.append("")
            		v_row_data.append("")
            		v_row_data.append("")
            		v_row_data.append("")

            		if v_database.v_can_drop_constraint:
            			v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>")
            		else:
            			v_row_data.append("")

            		v_table_constraints.append(v_row_data)

            		v_constraint_name = v_column["constraint_name"]
            		v_column_list = ""
            		v_first = True


            	if not v_first:
            		v_column_list += ", "

            	v_column_list += v_column["column_name"]
            	v_first = False

            if v_column_list!="":
            	v_row_data = []

            	v_row_data.append(v_constraint_name)
            	v_row_data.append("Unique")
            	v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list)
            	v_row_data.append("")
            	v_row_data.append("")
            	v_row_data.append("")
            	v_row_data.append("")

            	if v_database.v_can_drop_constraint:
            		v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>")
            	else:
            		v_row_data.append("")

            	v_table_constraints.append(v_row_data)

        v_table_indexes = []

        #Retrieving indexes
        if v_schema_name:
            v_indexes_table = v_database.QueryTablesIndexes(v_table_name, False, v_schema_name)
        else:
            v_indexes_table = v_database.QueryTablesIndexes(v_table_name)

        if v_indexes_table != None and len(v_indexes_table.Rows)>0:

        	v_column_list = ""
        	v_index_name = v_indexes_table.Rows[0]["index_name"]
        	v_uniqueness = v_indexes_table.Rows[0]["uniqueness"]
        	v_first = True

        	for v_column in v_indexes_table.Rows:

        		if v_column["index_name"]!=v_index_name:
        			v_row_data = []

        			v_row_data.append(v_index_name)
        			v_row_data.append(v_uniqueness)
        			v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_list)
        			v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropIndexAlterTable()'/>")

        			v_table_indexes.append(v_row_data)

        			v_index_name = v_column["index_name"]
        			v_uniqueness = v_column["uniqueness"]
        			v_column_list = ""
        			v_first = True

        		if not v_first:
        			v_column_list += ", "

        		v_column_list += v_column["column_name"]
        		v_first = False

        	if v_column_list!="":
        		v_row_data = []

        		v_row_data.append(v_index_name)
        		v_row_data.append(v_uniqueness)
        		v_row_data.append("<img src='/static/OmniDB_app/images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_list)
        		v_row_data.append("<img src='/static/OmniDB_app/images/tab_close.png' class='img_ht' onclick='dropIndexAlterTable()'/>")

        		v_table_indexes.append(v_row_data)

        v_return['v_data'] = {
            'v_can_rename_table': v_database.v_can_rename_table,
        	'v_data_columns': v_table_columns,
        	'v_data_constraints': v_table_constraints,
        	'v_data_indexes': v_table_indexes,
        	'v_data_types': v_data_types,
        	'v_tables': v_tables,
        	'v_can_rename_column': v_database.v_can_rename_column,
        	'v_can_alter_type': v_database.v_can_alter_type,
        	'v_can_alter_nullable': v_database.v_can_alter_nullable,
        	'v_can_drop_column': v_database.v_can_drop_column,
        	'v_can_add_constraint': v_database.v_can_add_constraint,
        	'v_can_drop_constraint': v_database.v_can_drop_constraint,
        	'v_has_update_rule': v_database.v_has_update_rule,
        	'v_update_rules': v_database.v_update_rules,
        	'v_delete_rules': v_database.v_delete_rules
        }
    else:
        v_return['v_data'] = {
            'v_can_rename_table': v_database.v_can_rename_table,
        	'v_data_columns': [],
        	'v_data_constraints': [],
        	'v_data_indexes': [],
        	'v_data_types': v_data_types,
        	'v_tables': v_tables,
        	'v_can_rename_column': v_database.v_can_rename_column,
        	'v_can_alter_type': v_database.v_can_alter_type,
        	'v_can_alter_nullable': v_database.v_can_alter_nullable,
        	'v_can_drop_column': v_database.v_can_drop_column,
        	'v_can_add_constraint': v_database.v_can_add_constraint,
        	'v_can_drop_constraint': v_database.v_can_drop_constraint,
        	'v_has_update_rule': v_database.v_has_update_rule,
        	'v_update_rules': v_database.v_update_rules,
        	'v_delete_rules': v_database.v_delete_rules
        }

    return JsonResponse(v_return)

def save_alter_table(request):

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
    p_schema_name = json_object['p_schema_name']
    p_original_table_name = json_object['p_original_table_name']
    p_new_table_name = json_object['p_new_table_name']
    p_mode = json_object['p_mode']
    p_data_columns = json_object['p_data_columns']
    p_row_columns_info = json_object['p_row_columns_info']
    p_data_constraints = json_object['p_data_constraints']
    p_row_constraints_info = json_object['p_row_constraints_info']
    p_data_indexes = json_object['p_data_indexes']
    p_row_indexes_info = json_object['p_row_indexes_info']

    v_database = v_session.v_databases[p_database_index]['database']

    v_return['v_data'] = {
        'v_columns_simple_commands_return': [],
        'v_columns_group_commands_return': [],
        'v_constraints_commands_return': [],
        'v_indexes_commands_return': [],
        'v_create_table_command': None,
        'v_rename_table_command': None
    }

    i = 0

    if p_mode == "alter":

        v_table_name = ""

        if v_database.v_has_schema:
        	v_table_name = p_schema_name + "." + p_original_table_name
        else:
        	v_table_name = p_original_table_name

        #Columns
        for v_row in p_row_columns_info:
        	#Adding new column
            if v_row['mode'] == 2:
                v_command = v_database.v_add_column_command
                v_command = v_command.replace ("#p_table_name#", v_table_name)
                v_command = v_command.replace ("#p_column_name#", p_data_columns [i] [0])
                v_command = v_command.replace ("#p_data_type#", p_data_columns [i] [1])

                if p_data_columns [i] [2] == "YES":
                    v_command = v_command.replace ("#p_nullable#", "")
                else:
                    v_command = v_command.replace ("#p_nullable#", "not null")

                v_info_return = {
                    'error': False,
                    'v_command': v_command,
                    'v_message': '',
                    'mode': 2,
                    'index': p_row_columns_info[i]['index']
                }

                try:
                    v_database.v_connection.Execute(v_command)
                    v_info_return['v_message'] = "Success."
                except Exception as exc:
                    v_info_return['v_message'] = str(exc)
                    v_info_return['error'] = True

                v_return['v_data']['v_columns_simple_commands_return'].append(v_info_return)

            #Dropping existing column
            elif v_row['mode'] == -1:
                v_command = v_database.v_drop_column_command
                v_command = v_command.replace ("#p_table_name#", v_table_name)
                v_command = v_command.replace ("#p_column_name#", v_row['originalColName'])

                v_info_return = {
                    'error': False,
                    'v_command': v_command,
                    'v_message': '',
                    'mode': -1,
                    'index': p_row_columns_info[i]['index']
                }

                try:
                    v_database.v_connection.Execute(v_command)
                    v_info_return['v_message'] = "Success."
                except Exception as exc:
                    v_info_return['v_message'] = str(exc)
                    v_info_return['error'] = True

                v_return['v_data']['v_columns_simple_commands_return'].append(v_info_return)

        	#Changing existing column
            elif v_row['mode'] == 1:

                v_info_return = {
                    'alter_datatype': None,
                    'alter_nullable': None,
                    'alter_colname': None,
                    'mode': 1,
                    'index': p_row_columns_info[i]['index']
                }

                #Changing column type
                v_info_return1 = {
                    'error': False,
                    'v_command': None,
                    'v_message': 'Success.',
                    'mode': 1,
                    'index': p_row_columns_info[i]['index']
                }

                if v_row['originalDataType'] != p_data_columns [i] [1]:

                    v_command = v_database.v_alter_type_command
                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_column_name#", v_row['originalColName'])
                    v_command = v_command.replace ("#p_new_data_type#", p_data_columns [i] [1])

                    v_info_return1['v_command'] = v_command

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return1['v_message'] = str(exc)
                        v_info_return1['error'] = True


                v_info_return['alter_datatype'] = v_info_return1

        		#Changing column nullable
                v_info_return1 = {
                    'error': False,
                    'v_command': None,
                    'v_message': 'Success.',
                    'mode': 1,
                    'index': p_row_columns_info[i]['index']
                }

                if v_row['originalNullable'] != p_data_columns [i] [2]:

                    v_command;

                    if p_data_columns [i] [2] == "YES":
                        v_command = v_database.v_set_nullable_command
                    else:
                        v_command = v_database.v_drop_nullable_command

                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_column_name#", v_row['originalColName'])
                    v_command = v_command.replace ("#p_new_data_type#", p_data_columns [i] [1])

                    v_info_return1['v_command'] = v_command

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return1['v_message'] = str(exc)
                        v_info_return1['error'] = True

                v_info_return['alter_nullable'] = v_info_return1

        		#Changing column name
                v_info_return1 = {
                    'error': False,
                    'v_command': None,
                    'v_message': 'Success.',
                    'mode': 1,
                    'index': p_row_columns_info[i]['index']
                }

                if v_row['originalColName'] != p_data_columns [i] [0]:

                    v_command = v_database.v_rename_column_command
                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_column_name#", v_row['originalColName'])
                    v_command = v_command.replace ("#p_new_column_name#", p_data_columns [i] [0])
                    v_command = v_command.replace ("#p_new_data_type#", p_data_columns [i] [1])
                    if p_data_columns [i] [2]=="YES":
                        v_command = v_command.replace ("#p_new_nullable#", "")
                    else:
                        v_command = v_command.replace ("#p_new_nullable#", "not null")

                    v_info_return1['v_command'] = v_command

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return1['v_message'] = str(exc)
                        v_info_return1['error'] = True

                v_info_return['alter_colname'] = v_info_return1

                v_return['v_data']['v_columns_group_commands_return'].append(v_info_return)

            i = i+1

        #Constraints
        for v_row in p_row_constraints_info:

            #Adding new constraint
            if v_row['mode'] == 2:

                #Adding PK
                if p_data_constraints[i][1] == "Primary Key":

                    v_command = v_database.v_add_pk_command
                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0])
                    v_command = v_command.replace ("#p_columns#", p_data_constraints [i] [2])

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': 2,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

        		#Adding FK
                elif p_data_constraints [i] [1] == "Foreign Key":

                    v_command = v_database.v_add_fk_command
                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0])
                    v_command = v_command.replace ("#p_columns#", p_data_constraints [i] [2])
                    v_command = v_command.replace ("#p_r_table_name#", p_data_constraints [i] [3])
                    v_command = v_command.replace ("#p_r_columns#", p_data_constraints [i] [4])
                    v_command = v_command.replace ("#p_delete_update_rules#", v_database.HandleUpdateDeleteRules(p_data_constraints [i] [6], p_data_constraints [i] [5]))

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': 2,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

                #Adding Unique
                elif p_data_constraints [i] [1] == "Unique":

                    v_command = v_database.v_add_unique_command
                    v_command = v_command.replace ("#p_table_name#", v_table_name)
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0])
                    v_command = v_command.replace ("#p_columns#", p_data_constraints [i] [2])

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': 2,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

        	#Dropping existing constraint
            elif v_row['mode'] == -1:

                #Dropping PK
                if p_data_constraints [i] [1] == "Primary Key":

                    v_command = v_database.v_drop_pk_command;
                    v_command = v_command.replace ("#p_table_name#", v_table_name);
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0]);

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': -1,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

        		#Dropping FK
                elif p_data_constraints [i] [1] == "Foreign Key":

                    v_command = v_database.v_drop_fk_command;
                    v_command = v_command.replace ("#p_table_name#", v_table_name);
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0]);

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': -1,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

        		#Dropping Unique
                elif p_data_constraints [i] [1] == "Unique":

                    v_command = v_database.v_drop_unique_command;
                    v_command = v_command.replace ("#p_table_name#", v_table_name);
                    v_command = v_command.replace ("#p_constraint_name#", p_data_constraints [i] [0]);

                    v_info_return = {
                        'error': False,
                        'v_command': v_command,
                        'v_message': 'Success.',
                        'mode': -1,
                        'index': p_row_constraints_info[i]['index']
                    }

                    try:
                        v_database.v_connection.Execute(v_command)
                    except Exception as exc:
                        v_info_return['v_message'] = str(exc)
                        v_info_return['error'] = True

                    v_return['v_data']['v_constraints_commands_return'].append(v_info_return)

            i = i + 1

        i = 0;

        #Indexes
        for v_row in p_row_indexes_info:

        	#Adding new index
            if v_row['mode'] == 2:

                v_command = "";

                if p_data_indexes [i] [1] == "Unique":
                	v_command = v_database.v_create_unique_index_command
                else:
                	v_command = v_database.v_create_index_command

                v_command = v_command.replace ("#p_table_name#", v_table_name)
                v_command = v_command.replace ("#p_index_name#", p_data_indexes [i] [0])
                v_command = v_command.replace ("#p_columns#", p_data_indexes [i] [2])

                v_info_return = {
                    'error': False,
                    'v_command': v_command,
                    'v_message': 'Success.',
                    'mode': 2,
                    'index': p_row_indexes_info[i]['index']
                }

                try:
                    v_database.v_connection.Execute(v_command)
                except Exception as exc:
                    v_info_return['v_message'] = str(exc)
                    v_info_return['error'] = True

                v_return['v_data']['v_indexes_commands_return'].append(v_info_return)

        	#Dropping existing index
            elif v_row['mode'] == -1:

                v_command = v_database.v_drop_index_command
                v_command = v_command.replace ("#p_table_name#", v_table_name)
                v_command = v_command.replace ("#p_index_name#", p_data_indexes [i] [0])
                v_command = v_command.replace ("#p_schema_name#", p_schema_name)

                v_info_return = {
                    'error': False,
                    'v_command': v_command,
                    'v_message': 'Success.',
                    'mode': -1,
                    'index': p_row_indexes_info[i]['index']
                }

                try:
                    v_database.v_connection.Execute(v_command)
                except Exception as exc:
                    v_info_return['v_message'] = str(exc)
                    v_info_return['error'] = True

                v_return['v_data']['v_indexes_commands_return'].append(v_info_return)

            i = i+1

        if p_original_table_name != p_new_table_name:

            v_command = v_database.v_rename_table_command
            v_command = v_command.replace ("#p_table_name#", v_table_name)
            v_command = v_command.replace ("#p_new_table_name#", p_new_table_name)

            v_info_return = {
                'error': False,
                'v_command': v_command,
                'v_message': 'Success.',
                'mode': 0,
                'index': 0
            }

            try:
                v_database.v_connection.Execute(v_command)
            except Exception as exc:
                v_info_return['v_message'] = str(exc)
                v_info_return['error'] = True

            v_return['v_data']['v_rename_table_command'] = v_info_return

    #Creating new table
    else:

        v_table_name = ""

        if v_database.v_has_schema:
        	v_table_name = p_schema_name + "." + p_new_table_name
        else:
        	v_table_name = p_new_table_name

        v_command = "create table " + v_table_name + " ("

        v_first = True

        for v_row in p_row_columns_info:

        	if not v_first:
        		v_command += ","

        	v_command += p_data_columns [i] [0] + " " + p_data_columns [i] [1]
        	if p_data_columns [i] [2] == "NO":
        		v_command += " not null"

        	i = i + 1

        	v_first = False

        i = 0

        for v_row in p_row_constraints_info:

            if not v_first:
            	v_command += ","

            v_first = False

            if p_data_constraints [i] [1] == "Primary Key":

            	v_command_constraint = v_database.v_create_pk_command
            	v_command_constraint = v_command_constraint.replace ("#p_constraint_name#", p_data_constraints [i] [0])
            	v_command_constraint = v_command_constraint.replace ("#p_columns#", p_data_constraints [i] [2])

            	v_command += v_command_constraint

            elif p_data_constraints [i] [1] == "Foreign Key":

            	v_command_constraint = v_database.v_create_fk_command
            	v_command_constraint = v_command_constraint.replace ("#p_constraint_name#", p_data_constraints [i] [0])
            	v_command_constraint = v_command_constraint.replace ("#p_columns#", p_data_constraints [i] [2])
            	v_command_constraint = v_command_constraint.replace ("#p_r_table_name#", p_data_constraints [i] [3])
            	v_command_constraint = v_command_constraint.replace ("#p_r_columns#", p_data_constraints [i] [4])
            	v_command_constraint = v_command_constraint.replace ("#p_delete_update_rules#", v_database.HandleUpdateDeleteRules(p_data_constraints [i] [6], p_data_constraints [i] [5]))

            	v_command += v_command_constraint

            elif p_data_constraints [i] [1] == "Unique":

            	v_command_constraint = v_database.v_create_unique_command
            	v_command_constraint = v_command_constraint.replace ("#p_constraint_name#", p_data_constraints [i] [0])
            	v_command_constraint = v_command_constraint.replace ("#p_columns#", p_data_constraints [i] [2])

            	v_command += v_command_constraint

            i = i + 1

        v_command += ")"

        v_info_return = {
            'error': False,
            'v_command': v_command,
            'v_message': 'Success.',
            'mode': 0,
            'index': 0
        }

        try:
            v_database.v_connection.Execute(v_command)
        except Exception as exc:
            v_info_return['v_message'] = str(exc)
            v_info_return['error'] = True

        v_return['v_data']['v_create_table_command'] = v_info_return


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
    v_table          = json_object['p_table']
    v_schema         = json_object['p_schema']

    v_database = v_session.v_databases[v_database_index]['database']

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
        v_data1 = v_database.QueryDataLimited('select * from ' + v_table_name, 0)
        v_query_column_classes = ''
        v_first = True

        for v_column in v_columns.Rows:
            if not v_first:
                v_query_column_classes = v_query_column_classes + 'union '
            v_first = False

            v_query_column_classes = v_query_column_classes + '''
            select '{0}' as column,
                   dc.cat_st_class as cat_st_class,
                   dt.dt_type as dt_type,
                   dt.dt_st_readformat as dt_st_readformat,
                   dt.dt_st_compareformat as dt_st_compareformat,
                   dt.dt_st_writeformat as dt_st_writeformat
            from data_types dt,
                 data_categories dc
            where dt.dbt_st_name = '{1}'
              and dt.dt_type = '{2}'
              and dt.cat_st_name = dc.cat_st_name
            union
            select '{0}' as column,
                   'text' as cat_st_class,
                   '{2}' as dt_type,
                   '#' as dt_st_readformat,
                   '#' as dt_st_compareformat,
                   '#' as dt_st_writeformat
            where '{2}' not in (
                select dt_type from data_types where dbt_st_name='{1}'
            )'''.format(
                v_column['column_name'],
                v_database.v_db_type,
                v_column['data_type'].lower()
            )

        v_column_classes = v_session.v_omnidb_database.v_connection.Query(v_query_column_classes)

        for v_column in v_data1.Columns:
            v_col = {}
            for v_column_class in v_column_classes.Rows:
                if v_column == v_column_class['column'].replace('"',''):
                    v_col['v_class'] = v_column_class['cat_st_class']
                    v_col['v_type'] = v_column_class['dt_type']
                    v_col['v_column'] = v_column_class['column']
                    v_col['v_readformat'] = v_column_class['dt_st_readformat']
                    v_col['v_writeformat'] = v_column_class['dt_st_writeformat']
                    v_col['v_compareformat'] = v_column_class['dt_st_compareformat']
                    v_col['v_is_pk'] = False
                    break
            v_return['v_data']['v_cols'].append(v_col)

        if v_pk != None:
            if len(v_pk.Rows) > 0:
                v_return['v_data']['v_ini_orderby'] = 'order by '
            v_first = True
            v_index = 0
            for k in range(0, len(v_return['v_data']['v_cols'])):
                for v_pk_col in v_pk.Rows:
                    if v_pk_col['column_name'].lower() == v_return['v_data']['v_cols'][k]['v_column'].lower():
                        v_return['v_data']['v_cols'][k]['v_is_pk'] = True

                        if not v_first:
                            v_return['v_data']['v_ini_orderby'] = v_return['v_data']['v_ini_orderby'] + ', '
                        v_first = False

                        v_return['v_data']['v_ini_orderby'] = v_return['v_data']['v_ini_orderby'] + 't.' + v_pk_col['column_name']

                        v_pk_info = {}
                        v_pk_info['v_column'] = v_pk_col['column_name']
                        v_pk_info['v_index'] = v_index
                        v_pk_info['v_class'] = v_return['v_data']['v_cols'][k]['v_class']
                        v_pk_info['v_compareformat'] = v_return['v_data']['v_cols'][k]['v_compareformat']

                        v_return['v_data']['v_pk'].append(v_pk_info)
                        break
                v_index = v_index + 1

    except Exception as exc:
        v_return['v_data'] = str(exc)
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
    p_prefix = json_object['p_prefix']
    p_sql = json_object['p_sql']
    p_prefix_pos = json_object['p_prefix_pos']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_database = v_session.v_databases[p_database_index]['database']

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
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True

        return JsonResponse(v_return)

    v_score = 100

    v_list.append ({'value': p_prefix + ".", 'score': v_score, 'meta': ""})

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
    p_table = json_object['p_table']
    p_schema = json_object['p_schema']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_database = v_session.v_databases[p_database_index]['database']

    if v_database.v_has_schema:
        v_table_name = p_schema + "." + p_table
    else:
        v_table_name = p_table

    v_list = []

    try:
    	v_data1 = v_database.v_connection.GetFields ("select x.* from " + v_table_name + " x where 1 = 0")
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True

        return JsonResponse(v_return)

    v_score = 100

    v_list.append ({'value': "t.", 'score': v_score, 'meta': ""})

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

    v_session = request.session.get('omnidb_session')


    try:
        v_count = v_session.v_omnidb_database.v_connection.ExecuteScalar ('''
            select count(*)
            from command_list
            where user_id = {0}
        '''.format(str(v_session.v_user_id)))

        v_commands = v_session.v_omnidb_database.v_connection.Query ('''
            select cl_st_start,
                   cl_st_end,
                   cl_st_duration,
                   cl_st_mode,
                   cl_st_status,
                   cl_st_command
            from command_list
            where user_id = {0}
            order by cl_in_codigo desc
            limit {1},{2}
        '''.format(str(v_session.v_user_id),str((v_current_page-1)*settings.CH_CMDS_PER_PAGE),settings.CH_CMDS_PER_PAGE),True)
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    v_command_list = []

    index = 0

    for v_command in v_commands.Rows:
        v_command_data_list = []
        v_command_data_list.append(v_command["cl_st_start"])
        v_command_data_list.append(v_command["cl_st_end"])
        v_command_data_list.append(v_command["cl_st_duration"])
        v_command_data_list.append(v_command["cl_st_mode"])
        if v_command["cl_st_status"]=='success':
            v_command_data_list.append('<img src="/static/OmniDB_app/images/status/status_F.png" title="Success"/>')
        else:
            v_command_data_list.append('<img src="/static/OmniDB_app/images/status/status_X.png" title="Error"/>')
        v_command_data_list.append(v_command["cl_st_command"])
        v_command_data_list.append('<img src="/static/OmniDB_app/images/trigger.png" class="img_ht" title="Open command in new tab" onclick="commandHistoryOpenCmd({0})"/>'.format(index))
        v_command_list.append(v_command_data_list)
        index = index + 1

    v_page = ceil(v_count/settings.CH_CMDS_PER_PAGE)
    if v_page==0:
        v_page=1

    v_return['v_data'] = { 'command_list': v_command_list,
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

    v_session = request.session.get('omnidb_session')


    try:
        v_session.v_omnidb_database.v_connection.Execute ("delete from command_list where user_id={0}".format(v_session.v_user_id))
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
    v_sql            = json_object['p_query']

    v_database = v_session.v_databases[v_database_index]['database']

    #Check database prompt timeout
    v_timeout = v_session.DatabaseReachPasswordTimeout(int(v_database_index))
    if v_timeout['timeout']:
        v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    try:
        v_data = v_database.v_connection.Query(v_sql,True)
        v_return['v_data'] = {
            'v_col_names' : v_data.Columns,
            'v_data' : v_data.Rows,
            'v_query_info' : "Number of records: {0}".format(len(v_data.Rows))
        }
    except Exception as exc:
        v_return['v_data'] = str(exc)
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
