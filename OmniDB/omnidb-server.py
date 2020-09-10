#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import platform
import random
import string
import importlib

#Parameters
import optparse
import configparser
import OmniDB.custom_settings
OmniDB.custom_settings.DEV_MODE = False
OmniDB.custom_settings.DESKTOP_MODE = False

parser = optparse.OptionParser(version=OmniDB.custom_settings.OMNIDB_VERSION)

group = optparse.OptionGroup(parser, "General Options")

group.add_option("-d", "--homedir", dest="homedir",
                  default='', type=str,
                  help="home directory containing local databases config and log files")

group.add_option("-C", "--configfile", dest="conf",
                  default='', type=str,
                  help="configuration file")

parser.add_option_group(group)

group = optparse.OptionGroup(parser, "Webserver Options")

group.add_option("-H", "--host", dest="host",
                  default=None, type=str,
                  help="listening address")

group.add_option("-p", "--port", dest="port",
                  default=None, type=int,
                  help="listening port")


group.add_option("-A", "--app", dest="app",
                  action="store_true",
                  default=False,
                  help=optparse.SUPPRESS_HELP)

group.add_option("-P", "--path", dest="path",
                  default='', type=str,
                  help="path to access the application, other than /")

parser.add_option_group(group)

group = optparse.OptionGroup(parser, "Management Options",
                             "Options to list, create and drop users and connections.")
group.add_option("-r", "--resetdatabase", dest="reset",
                  default=False, action="store_true",
                  help="reset user and session databases")
group.add_option("-t", "--deletetemp", dest="deletetemp",
                  default=False, action="store_true",
                  help="delete temporary files")
group.add_option("-j", "--jsonoutput", dest="jsonoutput",
                  default=False, action="store_true",
                  help="format list output as json")
group.add_option("-l", "--listusers", dest="listusers",
                  default=False, action="store_true",
                  help="list users")
group.add_option("-u", "--createuser", dest="createuser",
                  nargs=2,metavar="username password",
                  help="create user: -u username password")
group.add_option("-s", "--createsuperuser", dest="createsuperuser",
                  nargs=2,metavar="username password",
                  help="create super user: -s username password")
group.add_option("-x", "--dropuser", dest="dropuser",
                  nargs=1,metavar="username",
                  help="drop user: -x username")
group.add_option("-m", "--listconnections", dest="listconnections",
                  nargs=1,metavar="username",
                  help="list connections: -m username")
group.add_option("-c", "--createconnection", dest="createconnection",
                  nargs=6,metavar="username technology host port database dbuser",
                  help="create connection: -c username technology host port database dbuser")
group.add_option("-z", "--dropconnection", dest="dropconnection",
                  nargs=1,metavar="connid",
                  help="drop connection: -z connid")
parser.add_option_group(group)

(options, args) = parser.parse_args()

#Generate random token if in app mode
if options.app:
    OmniDB.custom_settings.DESKTOP_MODE = True
    OmniDB.custom_settings.APP_TOKEN = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(50))
    app_version = True
else:
    app_version = False

if options.homedir!='':
    if not os.path.exists(options.homedir):
        print("Home directory does not exist. Please specify a directory that exists.",flush=True)
        sys.exit()
    else:
        OmniDB.custom_settings.HOME_DIR = options.homedir
else:
    if OmniDB.custom_settings.DESKTOP_MODE:
        OmniDB.custom_settings.HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-app')
    else:
        OmniDB.custom_settings.HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-server')

    if not os.path.exists(OmniDB.custom_settings.HOME_DIR):
        os.makedirs(OmniDB.custom_settings.HOME_DIR)


if options.conf!='':
    if not os.path.exists(options.conf):
        print("Config file not found. Please specify a file that exists.",flush=True)
        sys.exit()
    else:
        config_file = options.conf
else:
    config_file = os.path.join(OmniDB.custom_settings.HOME_DIR, 'config.py')
    if not os.path.exists(config_file):
        shutil.copyfile(os.path.join(OmniDB.custom_settings.BASE_DIR, 'config.py'), config_file)

# Loading config file
spec = importlib.util.spec_from_file_location("omnidb_settings", config_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
omnidb_settings = module

maintenance_action = False

if options.reset:
    maintenance_action = True
    print('*** ATENTION *** ALL USERS DATA WILL BE LOST')
    try:
        value = input('Would you like to continue? (y/n) ')
        if value.lower()=='y':
            #clean_chat()
            clean_users()
            clean_sessions()
            vacuum()
            clean_temp()
            create_superuser('admin', 'admin')
    except Exception as exc:
        print('Error:')
        print(exc)

if options.deletetemp:
    maintenance_action = True
    clean_temp()

if options.listusers:
    maintenance_action = True
    list_users()

if options.createuser:
    maintenance_action = True
    create_user(options.createuser[0], options.createuser[1])

if options.createsuperuser:
    maintenance_action = True
    create_superuser(options.createsuperuser[0], options.createsuperuser[1])

if options.dropuser:
    maintenance_action = True
    drop_user(options.dropuser)

if options.listconnections:
    maintenance_action = True
    list_connections(options.listconnections)

if options.createconnection:
    maintenance_action = True
    create_connection(options.createconnection[0], options.createconnection[1], options.createconnection[2], options.createconnection[3], options.createconnection[4], options.createconnection[5])

if options.dropconnection:
    maintenance_action = True
    drop_connection(options.dropconnection)

# Maintenance performed, exit before starting webserver
if maintenance_action == True:
    sys.exit()

if options.host!=None:
    listening_address = options.host
else:
    if hasattr(omnidb_settings,'listening_address'):
        listening_address = omnidb_settings.listening_address
    else:
        listening_address = OmniDB.custom_settings.OMNIDB_ADDRESS

if options.port!=None:
    listening_port = options.port
else:
    if hasattr(omnidb_settings,'listening_port'):
        listening_port = omnidb_settings.listening_port
    else:
        listening_port = 8000

if options.path!='':
    OmniDB.custom_settings.PATH = options.path
else:
    if hasattr(omnidb_settings,'path'):
        OmniDB.custom_settings.PATH = omnidb_settings.path

if hasattr(omnidb_settings,'is_ssl'):
    is_ssl = omnidb_settings.is_ssl
    if is_ssl:
        OmniDB.custom_settings.SESSION_COOKIE_SECURE = True
        OmniDB.custom_settings.CSRF_COOKIE_SECURE = True
else:
    is_ssl = False

if hasattr(omnidb_settings,'ssl_certificate_file'):
    ssl_certificate_file = omnidb_settings.ssl_certificate_file

    if is_ssl and not os.path.exists(ssl_certificate_file):
        print("Certificate file not found. Please specify a file that exists.",flush=True)
        logger.info("Certificate file not found. Please specify a file that exists.")
        sys.exit()
else:
    ssl_certificate_file = ''

if hasattr(omnidb_settings,'ssl_key_file'):
    ssl_key_file = omnidb_settings.ssl_key_file

    if is_ssl and not os.path.exists(ssl_key_file):
        print("Key file not found. Please specify a file that exists.",flush=True)
        logger.info("Key file not found. Please specify a file that exists.")
        sys.exit()
else:
    ssl_key_file = ''

if hasattr(omnidb_settings,'allowed_hosts'):
    OmniDB.custom_settings.ALLOWED_HOSTS = omnidb_settings.allowed_hosts

if hasattr(omnidb_settings,'session_cookie_name'):
    OmniDB.custom_settings.SESSION_COOKIE_NAME = omnidb_settings.session_cookie_name

if hasattr(omnidb_settings,'csrf_cookie_name'):
    OmniDB.custom_settings.CSRF_COOKIE_NAME = omnidb_settings.csrf_cookie_name

if hasattr(omnidb_settings,'csrf_trusted_origins'):
    OmniDB.custom_settings.CSRF_TRUSTED_ORIGINS = omnidb_settings.csrf_trusted_origins

if hasattr(omnidb_settings,'thread_pool_max_workers'):
    OmniDB.custom_settings.THREAD_POOL_MAX_WORKERS = omnidb_settings.thread_pool_max_workers

if hasattr(omnidb_settings,'pwd_timeout_total'):
    OmniDB.custom_settings.PWD_TIMEOUT_TOTAL = omnidb_settings.pwd_timeout_total

#importing settings after setting HOME_DIR and other required parameters
import OmniDB.settings

import logging
import logging.config

logger = logging.getLogger('OmniDB_app.Init')

import OmniDB
import OmniDB_app
import OmniDB_app.apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'OmniDB.settings'
import django
from django.core.management import call_command
django.setup()
import html.parser
import http.cookies

import django.template.defaulttags
import django.template.loader_tags
import django.contrib.staticfiles
import django.contrib.staticfiles.apps
import django.contrib.admin.apps
import django.contrib.auth.apps
import django.contrib.contenttypes.apps
import django.contrib.sessions.apps
import django.contrib.messages.apps
import OmniDB_app.urls
import django.contrib.messages.middleware
import django.contrib.auth.middleware
import django.contrib.sessions.middleware
import django.contrib.sessions.serializers
import django.template.loaders
import django.contrib.auth.context_processors
import django.contrib.messages.context_processors
import django.views.defaults
import django.contrib.auth.password_validation

from django.core.handlers.wsgi import WSGIHandler
from OmniDB import startup

import time
import cherrypy

from django.contrib.sessions.backends.db import SessionStore

import socket
import random
import urllib.request

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        print(str(e))
        return False
    s.close()
    return True

class DjangoApplication(object):

    def mount_static(self, url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def run(self,parameters):
        #cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

        logging.config.dictConfig(OmniDB.settings.LOGGING)
        #cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False
        self.mount_static(OmniDB.settings.STATIC_URL, OmniDB.settings.STATIC_ROOT)

        cherrypy.tree.graft(WSGIHandler())

        port = parameters['listening_port']
        num_attempts = 0

        print('''Starting OmniDB server...''',flush=True)
        logger.info('''Starting OmniDB server...''')
        print('''Checking port availability...''',flush=True)
        logger.info('''Checking port availability...''')

        while not check_port(port):
            print("Port {0} is busy, trying another port...".format(port),flush=True)
            logger.info("Port {0} is busy, trying another port...".format(port))
            port = random.randint(1025,32676)
            num_attempts = num_attempts + 1

            if num_attempts == 20:
                break

        if num_attempts < 20:

            v_cherrypy_config = {
                'server.socket_host': parameters['listening_address'],
                'server.socket_port': port,
                'engine.autoreload_on': False,
                'log.screen': False,
                'log.access_file': '',
                'log.error_file': ''
            }

            if parameters['is_ssl']:
                import ssl
                ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_ctx.options |= ssl.OP_NO_TLSv1
                ssl_ctx.options |= ssl.OP_NO_TLSv1_1
                ssl_ctx.load_cert_chain(parameters['ssl_certificate_file'],
                                       parameters['ssl_key_file'])
                v_cherrypy_config['server.ssl_module'] = 'builtin'
                v_cherrypy_config['server.ssl_certificate'] = parameters['ssl_certificate_file']
                v_cherrypy_config['server.ssl_private_key'] = parameters['ssl_key_file']
                v_cherrypy_config['server.ssl_context'] = ssl_ctx

            cherrypy.config.update(v_cherrypy_config)

            print ("Starting server {0} at {1}:{2}{3}.".format(OmniDB.settings.OMNIDB_VERSION,parameters['listening_address'],str(port),OmniDB.settings.PATH),flush=True)
            logger.info("Starting server {0} at {1}:{2}.".format(OmniDB.settings.OMNIDB_VERSION,parameters['listening_address'],str(port)))

            # Startup
            startup.startup_procedure()

            cherrypy.engine.start()

            if not app_version:
                print ("Open OmniDB in your favorite browser",flush=True)
                if platform.system() != 'Windows':
                    print ("Press Ctrl+C to exit",flush=True)
            else:
                #Sending response to electron app
                print ("http://localhost:{0}/login/?user=admin&pwd=admin&token={1}".format(str(port),OmniDB.custom_settings.APP_TOKEN),flush=True)


            cherrypy.engine.block()
            cherrypy.engine.exit()
        else:
            print('Tried 20 different ports without success, closing...',flush=True)
            logger.info('Tried 20 different ports without success, closing...')

# OmniDB config actions

call_command("migrate", interactive=False)
call_command("clearsessions")

#Removing Expired Sessions
SessionStore.clear_expired()

DjangoApplication().run(
    {
        'listening_address'   : listening_address,
        'listening_port'      : listening_port,
        'is_ssl'              : is_ssl,
        'ssl_certificate_file': ssl_certificate_file,
        'ssl_key_file'        : ssl_key_file
    }
)
