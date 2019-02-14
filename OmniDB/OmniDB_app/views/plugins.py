from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from datetime import datetime
from math import ceil
import json
from os import listdir, makedirs, remove
from os.path import isfile, join, isdir
from OmniDB import settings
import importlib
from configparser import ConfigParser
from itertools import chain
import time
import shutil
import os

import OmniDB_app.include.OmniDatabase as OmniDatabase

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

#loading python plugins
plugins = {}
failed_plugins = {}
monitoring_units = []
omnidb_database = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite',
    '',
    '',
    settings.OMNIDB_DATABASE,
    '',
    '',
    '0',
    '',
    True
)

def load_plugin(plugin_folder, p_load):
    plugin_name = ''
    plugin_version = ''
    enabled_message = ''
    py_loaded = False
    if plugin_folder[0]=='.':
        return
    if isfile(join(settings.PLUGINS_DIR,plugin_folder,'plugin.conf')):
        conf_exists = True
    else:
        failed_plugins[plugin_folder] = {
            'module'         : None,
            'folder'         : plugin_folder,
            'name'           : '',
            'version'        : '',
            'conf_exists'    : False,
            'js_exists'      : False,
            'py_exists'      : False,
            'py_loaded'      : False,
            'css_exists'     : False,
            'message': 'Missing plugin.conf file.',
            'javascript_file': '',
            'css_file'       : '',
            'plugin_folder'  : ''
        }
        print('Missing plugin.conf file.')
        return
    if isfile(join(settings.PLUGINS_STATIC_DIR,plugin_folder,'plugin.js')):
        js_exists = True
    else:
        js_exists = False
    if isfile(join(settings.PLUGINS_DIR,plugin_folder,'plugin.py')):
        py_exists = True
    else:
        py_exists = False
    if isfile(join(settings.PLUGINS_STATIC_DIR,plugin_folder,'plugin.css')):
        css_exists = True
    else:
        css_exists = False

    module = None
    #if is directory, try to import plugin.py inside it
    if isdir(join(settings.PLUGINS_DIR,plugin_folder)):
        try:
            parser = ConfigParser()
            with open(join(settings.PLUGINS_DIR,plugin_folder,'plugin.conf')) as lines:
                lines = chain(("[top]",), lines)
                parser.read_file(lines)
                plugin_name = parser.get('top', 'name')
                plugin_version = parser.get('top', 'version')
                conf_parsed = True
        except Exception as exc:
            enabled = False
            enabled_message = 'Failed to parse plugin configuration file.'
            print('Failed to parse plugin configuration file.')
            failed_plugins[plugin_folder] = {
                'module'         : None,
                'folder'         : plugin_folder,
                'name'           : '',
                'version'        : '',
                'conf_exists'    : conf_exists,
                'js_exists'      : js_exists,
                'py_exists'      : py_exists,
                'py_loaded'      : False,
                'css_exists'     : css_exists,
                'message': 'Failed to parse plugin configuration file.',
                'javascript_file': '/static/plugins/{0}/plugin.js'.format(plugin_folder),
                'css_file'       : '/static/plugins/{0}/plugin.css'.format(plugin_folder) if css_exists else '',
                'plugin_folder'  : '/static/plugins/{0}/'.format(plugin_folder)
            }
            return

        #check that the plugin name wasn't loaded yet
        try:
            plugin_object = plugins[plugin_name]
            #didn't raise exception, so plugin was already loaded. Exit
            return
        except:
            None

        if p_load and py_exists:
            try:
                loaded_folder_name = '{0}_{1}'.format(plugin_name,str(time.time()).replace('.','_'))
                loaded_folder_complete_name = join(settings.PLUGINS_DIR,'temp_loaded',loaded_folder_name)
                os.mkdir(loaded_folder_complete_name)
                shutil.copytree(join(settings.PLUGINS_DIR,plugin_folder),join(loaded_folder_complete_name,plugin_name))
                module = importlib.import_module('OmniDB_app.plugins.temp_loaded.{0}.{1}.plugin'.format(loaded_folder_name,plugin_name))
                try:
                    mon_units = getattr(module, 'monitoring_units')
                    for mon_unit in mon_units:
                        mon_unit['plugin_name'] = plugin_name
                        monitoring_units.append(mon_unit)

                except Exception as exc:
                    None
                print('Loaded plugin {0}.'.format(plugin_name),flush=True)
                py_loaded = True
            except Exception as exc:
                print('Failed to load plugin {0}: {1}.'.format(plugin_name, str(exc)),flush=True)
                plugins[plugin_name] = {
                    'module'         : None,
                    'folder'         : plugin_folder,
                    'name'           : plugin_name,
                    'version'        : plugin_version,
                    'conf_exists'    : conf_exists,
                    'js_exists'      : js_exists,
                    'py_exists'      : py_exists,
                    'py_loaded'      : False,
                    'css_exists'     : css_exists,
                    'message': str(exc),
                    'javascript_file': '/static/plugins/{0}/plugin.js'.format(plugin_folder),
                    'css_file'       : '/static/plugins/{0}/plugin.css'.format(plugin_folder) if css_exists else '',
                    'plugin_folder'  : '/static/plugins/{0}/'.format(plugin_folder)
                }
                return
        elif py_exists:
            enabled_message = 'OmniDB needs to be restarted to load plugin python file.'

    plugins[plugin_name] = {
        'module'         : module,
        'folder'         : plugin_folder,
        'name'           : plugin_name,
        'version'        : plugin_version,
        'conf_exists'    : conf_exists,
        'js_exists'      : js_exists,
        'py_exists'      : py_exists,
        'py_loaded'      : py_loaded,
        'css_exists'     : css_exists,
        'message'        : enabled_message,
        'javascript_file': '/static/plugins/{0}/plugin.js'.format(plugin_folder),
        'css_file'       : '/static/plugins/{0}/plugin.css'.format(plugin_folder) if css_exists else '',
        'plugin_folder'  : '/static/plugins/{0}/'.format(plugin_folder)
    }
    return

#loading javascript plugins
def list_plugins(request):

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
    plugin_list = []
    plugin_message_list = []

    for key, plugin in failed_plugins.items():
        if plugin['conf_exists']:
            conf_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            conf_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['js_exists']:
            js_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            js_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['py_exists']:
            py_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            py_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['css_exists']:
            css_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            css_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['message'] == '':
            plugin_enabled = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            plugin_enabled = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'

        plugin_list.append([plugin['folder'],plugin['name'],plugin['version'],conf_html,js_html,py_html,css_html,plugin_enabled,'''<i title='Delete Plugin' class='fas fa-times action-grid action-close' onclick='deletePlugin("{0}","{1}")'></i>'''.format(plugin['name'],plugin['folder'])])
        plugin_message_list.append(plugin['message'])

    for key, plugin in plugins.items():
        if plugin['conf_exists']:
            conf_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            conf_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['js_exists']:
            js_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            js_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['py_exists']:
            py_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            py_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['css_exists']:
            css_html = '<i class="fas fa-check-circle action-grid action-check"></i>'
        else:
            css_html = '<i class="fas fa-exclamation-triangle action-grid action-close"></i>'
        if plugin['message'] == '':
            plugin_enabled = '<i class="fas fa-check-circle action-grid action-check" onclick="getPluginMessage()"></i>'
        else:
            plugin_enabled = '<i class="fas fa-exclamation-triangle action-grid action-close" onclick="getPluginMessage()"></i>'

        plugin_list.append([plugin['folder'],plugin['name'],plugin['version'],conf_html,js_html,py_html,css_html,plugin_enabled,'''<i title='Delete Plugin' class='fas fa-times action-grid action-close' onclick='deletePlugin("{0}","{1}")'></i>'''.format(plugin['name'],plugin['folder'])])
        plugin_message_list.append(plugin['message'])
    v_return['v_data'] = {
        'list': plugin_list,
        'message': plugin_message_list
    }

    return JsonResponse(v_return)

#loading javascript plugins
def get_plugins(request):

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
    plugin_list = []
    for key, plugin in plugins.items():
        if plugin['message']=='' and plugin['js_exists']:
            plugin_list.append({ 'name': plugin['name'], 'file': plugin['javascript_file'], 'cssfile': plugin['css_file'], 'folder': plugin['plugin_folder']})

    v_return['v_data'] = plugin_list

    return JsonResponse(v_return)

def load_plugins():
    #delete temp loaded python files
    plugin_temp_files = listdir(join(settings.PLUGINS_DIR,'temp_loaded'))
    for plugin_temp_file in plugin_temp_files:
        try:
            if plugin_temp_file!='.gitkeep':
                item_name = join(settings.PLUGINS_DIR,'temp_loaded',plugin_temp_file)
                if isfile(item_name):
                    os.remove(item_name)
                else:
                    shutil.rmtree(item_name)

        except Exception as exc:
            None

    plugins_folders = listdir(settings.PLUGINS_DIR)
    for plugin_folder in plugins_folders:
        if plugin_folder != 'temp_loaded':
            load_plugin(plugin_folder,True)
    #delete existing monitoring units from plugins that don't exist anymore
    plugin_string = ''
    first = True
    for key, plugin in plugins.items():
        if not first:
            plugin_string = plugin_string + ','
        first = False
        plugin_string = plugin_string + "'" + plugin['name'] + "'"
    try:
        omnidb_database.v_connection.Execute('''
            delete
            from units_users_connections
            where plugin_name <> ''
              and plugin_name not in ({0})
        '''.format(plugin_string))
    except Exception as exc:
        None

load_plugins()


#upload plugin
def upload_view(request):
    return_object = {
        'v_error': False
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #Invalid session
            if not request.session.get('omnidb_session'):
                return_object = {
                    'v_error': True,
                    'v_message': 'Session object was destroyed, click <a href="Login.aspx">here</a> to be redirected to login screen or finish what you were doing and reload the page.'
                }
                return JsonResponse(return_object)

            v_session = request.session.get('omnidb_session')

            if not v_session.v_super_user:
                return_object = {
                    'v_error': True,
                    'v_message': 'You must be superuser to delete a plugin.'
                }
                return JsonResponse(return_object)

            try:
                return_object = handle_uploaded_file(request.FILES['file'])
            except Exception as exc:
                return_object = {
                    'v_error': True,
                    'v_message': str(exc)
                }
    else:
        form = UploadFileForm()
    return JsonResponse(return_object)

#upload plugin helper
def handle_uploaded_file(f):
    v_dir_name = join(settings.TEMP_DIR,'{0}'.format(str(time.time()).replace('.','_')))

    makedirs(v_dir_name)

    v_file = join(v_dir_name,f.name)

    with open(v_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #extracting
    shutil.unpack_archive(v_file,v_dir_name)

    #remove uploaded file
    remove(v_file)

    v_has_plugins_folder = isdir(join(v_dir_name,'plugins'))
    v_has_static_folder = isdir(join(v_dir_name,'static','plugins'))

    v_plugin_folder_name = ''

    if not v_has_plugins_folder:
        shutil.rmtree(v_dir_name)
        return {
            'v_error': True,
            'v_message': '''Package doesn't have the plugins directory.'''
        }
    elif not v_has_static_folder:
        shutil.rmtree(v_dir_name)
        return {
            'v_error': True,
            'v_message': '''Package doesn't have the static/plugins directory.'''
        }
    else:
        try:
            files = listdir(join(v_dir_name,'plugins'))
            if len(files)==0:
                shutil.rmtree(v_dir_name)
                return {
                    'v_error': True,
                    'v_message': '''plugins directory is empty.'''
                }
            elif len(files)>1:
                shutil.rmtree(v_dir_name)
                return {
                    'v_error': True,
                    'v_message': '''plugins directory contains more than one directory.'''
                }
            plugin_dir_name = files[0]
            v_plugin_folder_name = plugin_dir_name
            shutil.move(join(v_dir_name,'plugins',plugin_dir_name), settings.PLUGINS_DIR)
        except Exception as exc:
            None

        try:
            files = listdir(join(v_dir_name,'static','plugins'))
            dir_name = files[0]
            if len(files)==0:
                shutil.rmtree(v_dir_name)
                return {
                    'v_error': True,
                    'v_message': '''static/plugins directory is empty.'''
                }
            elif len(files)>1:
                shutil.rmtree(v_dir_name)
                return {
                    'v_error': True,
                    'v_message': '''static/plugins directory contains more than one directory.'''
                }
            elif dir_name!=plugin_dir_name:
                shutil.rmtree(v_dir_name)
                return {
                    'v_error': True,
                    'v_message': '''Folders plugins and static/plugins contain directories with different names.'''
                }
            else:
                shutil.move(join(v_dir_name,'static','plugins',dir_name), settings.PLUGINS_STATIC_DIR)
        except Exception as exc:
            None

        shutil.rmtree(v_dir_name)
        if v_plugin_folder_name!='':
            try:
                load_plugin(v_plugin_folder_name,False)
            except Exception as exc:
                return {
                    'v_error': True,
                    'v_message': str(exc)
                }
        return {
            'v_error': False
        }


#reloading plugins
def reload_plugins(request):

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

    load_plugins()

    v_return['v_data'] = True

    return JsonResponse(v_return)

def delete_plugin(request):

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
    if not v_session.v_super_user:
        v_return['v_error'] = True
        v_return['v_data'] = 'You must be superuser to delete a plugin.'
        return JsonResponse(v_return)

    json_object = json.loads(request.POST.get('data', None))
    p_plugin_name = json_object['p_plugin_name']
    p_plugin_folder = json_object['p_plugin_folder']

    try:
        plugin = plugins[p_plugin_name]
        try:
            shutil.rmtree(join(settings.PLUGINS_STATIC_DIR,plugin['folder']))
        except:
            None
        try:
            shutil.rmtree(join(settings.PLUGINS_DIR,plugin['folder']))
        except:
            None
        del plugins[p_plugin_name]
    except:
        None

    try:
        plugin = failed_plugins[p_plugin_folder]
        try:
            shutil.rmtree(join(settings.PLUGINS_STATIC_DIR,plugin['folder']))
        except:
            None
        try:
            shutil.rmtree(join(settings.PLUGINS_DIR,plugin['folder']))
        except:
            None
        del plugins[p_plugin_name]
    except:
        None

    v_return['v_data'] = 'Please restart OmniDB to unload plugin libraries.'

    return JsonResponse(v_return)

def exec_plugin_function(request):

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
    p_plugin_name = json_object['p_plugin_name']
    p_function_name = json_object['p_function_name']
    p_data = json_object['p_data']
    p_check_database_connection = json_object['p_check_database_connection']
    p_database_index = json_object['p_database_index']
    p_tab_id = json_object['p_tab_id']

    try:
        v_database_orig = v_session.v_tab_connections[p_tab_id]

        v_database = OmniDatabase.Generic.InstantiateDatabase(
            v_database_orig.v_db_type,
            v_database_orig.v_connection.v_host,
            str(v_database_orig.v_connection.v_port),
            v_database_orig.v_active_service,
            v_database_orig.v_active_user,
            v_database_orig.v_connection.v_password,
            v_database_orig.v_conn_id,
            v_database_orig.v_alias,
            'OmniDB / {0}'.format(p_plugin_name),
            p_conn_string = v_database_orig.v_conn_string,
            p_parse_conn_string = False
        )
    except:
        v_database = None

    #Check database prompt timeout
    if p_check_database_connection and p_database_index:
        v_timeout = v_session.DatabaseReachPasswordTimeout(int(p_database_index))
        if v_timeout['timeout']:
            v_return['v_data'] = {'password_timeout': True, 'message': v_timeout['message'] }
            v_return['v_error'] = True
            return JsonResponse(v_return)

    try:
        print(plugins[p_plugin_name]['module'])
        v_return['v_data'] = getattr(plugins[p_plugin_name]['module'], p_function_name)(v_database,p_data)
    except Exception as exc:
        v_return['v_data'] = {'password_timeout': True, 'message': str(exc) }
        v_return['v_error'] = True
        return JsonResponse(v_return)

    return JsonResponse(v_return)
