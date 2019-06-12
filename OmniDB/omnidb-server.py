#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import random
import string

#Parameters
import optparse
import configparser
import OmniDB.custom_settings
OmniDB.custom_settings.DEV_MODE = False
OmniDB.custom_settings.DESKTOP_MODE = False

parser = optparse.OptionParser(version=OmniDB.custom_settings.OMNIDB_VERSION)
parser.add_option("-H", "--host", dest="host",
                  default=None, type=str,
                  help="listening address")

parser.add_option("-p", "--port", dest="port",
                  default=None, type=int,
                  help="listening port")

parser.add_option("-w", "--wsport", dest="wsport",
                  default=None, type=int,
                  help="websocket port")

parser.add_option("-e", "--ewsport", dest="ewsport",
                  default=None, type=int,
                  help="external websocket port")

parser.add_option("-d", "--homedir", dest="homedir",
                  default='', type=str,
                  help="home directory containing local databases config and log files")

parser.add_option("-c", "--configfile", dest="conf",
                  default='', type=str,
                  help="configuration file")

parser.add_option("-A", "--app", dest="app",
                  action="store_true",
                  default=False,
                  help=optparse.SUPPRESS_HELP)

parser.add_option("-P", "--path", dest="path",
                  default='', type=str,
                  help="path to access the application, other than /")

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


#importing runtime settings after setting HOME_DIR and other required parameters
import OmniDB.runtime_settings

if options.conf!='':
    if not os.path.exists(options.conf):
        print("Config file not found, using default settings.",flush=True)
        config_file = OmniDB.runtime_settings.CONFFILE
    else:
        config_file = options.conf
else:
    config_file = OmniDB.runtime_settings.CONFFILE

#Parsing config file
Config = configparser.ConfigParser()
Config.read(config_file)

if options.host!=None:
    listening_address = options.host
else:
    try:
        listening_address = Config.get('webserver', 'listening_address')
    except:
        listening_address = OmniDB.custom_settings.OMNIDB_ADDRESS

if options.port!=None:
    listening_port = options.port
else:
    try:
        listening_port = Config.getint('webserver', 'listening_port')
    except:
        listening_port = 8000

if options.wsport!=None:
    ws_port = options.wsport
else:
    try:
        ws_port = Config.getint('webserver', 'websocket_port')
    except:
        ws_port = OmniDB.custom_settings.OMNIDB_WEBSOCKET_PORT

if options.ewsport!=None:
    ews_port = options.ewsport
else:
    try:
        ews_port = Config.getint('webserver', 'external_websocket_port')
    except:
        ews_port = None

if options.path!='':
    OmniDB.custom_settings.PATH = options.path
else:
    try:
        OmniDB.custom_settings.PATH = Config.get('webserver', 'path')
    except:
        OmniDB.custom_settings.PATH = ''

try:
    is_ssl = Config.getboolean('webserver', 'is_ssl')
except:
    is_ssl = False
try:
    ssl_certificate_file = Config.get('webserver', 'ssl_certificate_file')
except:
    ssl_certificate_file = ''
try:
    ssl_key_file = Config.get('webserver', 'ssl_key_file')
except:
    ssl_key_file = ''
try:
    csrf_trusted_origins = Config.get('webserver', 'csrf_trusted_origins')
except:
    csrf_trusted_origins = ''

try:
    OmniDB.custom_settings.THREAD_POOL_MAX_WORKERS = Config.getint('queryserver', 'thread_pool_max_workers')
except:
    pass

try:
    OmniDB.custom_settings.PWD_TIMEOUT_TOTAL = Config.getint('queryserver', 'pwd_timeout_total')
except:
    pass

#importing settings after setting HOME_DIR and other required parameters
import OmniDB.settings

import logging
import logging.config

logger = logging.getLogger('OmniDB_app.Init')

#Configuring Django settings before loading them
OmniDB.settings.DEBUG = False
if is_ssl:
    OmniDB.settings.SESSION_COOKIE_SECURE = True
    OmniDB.settings.CSRF_COOKIE_SECURE = True
    csrf_trusted_origins_list = csrf_trusted_origins.split(',')
    if len(csrf_trusted_origins_list)>0:
        OmniDB.settings.CSRF_TRUSTED_ORIGINS = csrf_trusted_origins_list

    if not os.path.exists(ssl_certificate_file):
        print("Certificate file not found. Please specify a file that exists.",flush=True)
        logger.info("Certificate file not found. Please specify a file that exists.")
        sys.exit()
    if not os.path.exists(ssl_key_file):
        print("Key file not found. Please specify a file that exists.",flush=True)
        logger.info("Key file not found. Please specify a file that exists.")
        sys.exit()

import OmniDB
import OmniDB_app
import OmniDB_app.apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'OmniDB.settings'
import django
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
from OmniDB import startup, ws_core

import time
import cherrypy

from django.contrib.sessions.backends.db import SessionStore

import socket
import random
import urllib.request

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
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

        while not check_port(port) or num_attempts >= 20:
            print("Port {0} is busy, trying another port...".format(port),flush=True)
            logger.info("Port {0} is busy, trying another port...".format(port))
            port = random.randint(1025,32676)
            num_attempts = num_attempts + 1

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

if __name__ == "__main__":

    #Choosing empty port
    port = ws_port
    num_attempts_port = 0

    print('''Starting OmniDB websocket...''',flush=True)
    logger.info('''Starting OmniDB websocket...''')
    print('''Checking port availability...''',flush=True)
    logger.info('''Checking port availability...''')

    while not check_port(port) or num_attempts_port >= 20:
        print("Port {0} is busy, trying another port...".format(port),flush=True)
        logger.info("Port {0} is busy, trying another port...".format(port))
        port = random.randint(1025,32676)
        num_attempts_port = num_attempts_port + 1

    if num_attempts_port < 20:
        OmniDB.settings.OMNIDB_WEBSOCKET_PORT          = port
        if ews_port==None:
            OmniDB.settings.OMNIDB_EXTERNAL_WEBSOCKET_PORT = port
        else:
            OmniDB.settings.OMNIDB_EXTERNAL_WEBSOCKET_PORT = ews_port
        OmniDB.settings.OMNIDB_ADDRESS                 = listening_address
        OmniDB.settings.IS_SSL                         = is_ssl
        OmniDB.settings.SSL_CERTIFICATE                = ssl_certificate_file
        OmniDB.settings.SSL_KEY                        = ssl_key_file
        OmniDB.settings.SESSION_COOKIE_SECURE          = True
        OmniDB.settings.CSRF_COOKIE_SECURE             = True

        print ("Starting websocket server at port {0}.".format(str(port)),flush=True)
        logger.info("Starting websocket server at port {0}.".format(str(port)))

        #Removing Expired Sessions
        SessionStore.clear_expired()

        #Websocket Core
        ws_core.start_wsserver_thread()
        DjangoApplication().run(
            {
                'listening_address'   : listening_address,
                'listening_port'      : listening_port,
                'is_ssl'              : is_ssl,
                'ssl_certificate_file': ssl_certificate_file,
                'ssl_key_file'        : ssl_key_file
            }
        )


    else:
        print('Tried 20 different ports without success, closing...',flush=True)
        logger.info('Tried 20 different ports without success, closing...')
