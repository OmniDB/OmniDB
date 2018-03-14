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
OmniDB.custom_settings.DESKTOP_MODE = True
OmniDB.custom_settings.APP_TOKEN = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(50))

parser = optparse.OptionParser(version=OmniDB.custom_settings.OMNIDB_VERSION)

parser.add_option("-p", "--port", dest="port",
                  default=None, type=int,
                  help="listening port")

parser.add_option("-w", "--wsport", dest="wsport",
                  default=None, type=int,
                  help="websocket port")

parser.add_option("-d", "--homedir", dest="homedir",
                  default='', type=str,
                  help="home directory containing local databases config and log files")

parser.add_option("-c", "--configfile", dest="conf",
                  default='', type=str,
                  help="configuration file")

(options, args) = parser.parse_args()

if options.homedir!='':
    if not os.path.exists(options.homedir):
        print("Home directory does not exist. Please specify a directory that exists.")
        sys.exit()
    else:
        OmniDB.custom_settings.HOME_DIR = options.homedir

#importing settings after setting HOME_DIR
import OmniDB.settings

if options.conf!='':
    if not os.path.exists(options.conf):
        print("Config file not found, using default settings.")
        config_file = OmniDB.settings.CONFFILE
    else:
        config_file = options.conf
else:
    config_file = OmniDB.settings.CONFFILE

#Parsing config file
Config = configparser.ConfigParser()
Config.read(config_file)

if options.port!=None:
    listening_port = options.port
else:
    try:
        listening_port = Config.getint('webserver', 'listening_port')
    except:
        listening_port = 25480

if options.wsport!=None:
    ws_port = options.wsport
else:
    try:
        ws_port = Config.getint('webserver', 'websocket_port')
    except:
        ws_port = OmniDB.settings.OMNIDB_WEBSOCKET_PORT



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
import psycopg2

from django.core.handlers.wsgi import WSGIHandler
from OmniDB import startup, ws_core

import logging
import logging.config
import time
import cherrypy

from django.contrib.sessions.backends.db import SessionStore

from cefpython3 import cefpython as cef

import socket
import urllib.request

logger = logging.getLogger('OmniDB_app.Init')

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        return False
    s.close()
    return True

def init_browser(server_port):
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="http://localhost:{0}?user=admin&pwd=admin&token={1}".format(str(server_port),OmniDB.custom_settings.APP_TOKEN),window_title="OmniDB")
    cef.MessageLoop()
    cef.Shutdown()

class DjangoApplication(object):
    HOST = "127.0.0.1"

    def mount_static(self, url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def run(self):
        #cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

        logging.config.dictConfig(OmniDB.settings.LOGGING)
        #cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False
        self.mount_static(OmniDB.settings.STATIC_URL, OmniDB.settings.STATIC_ROOT)

        cherrypy.tree.graft(WSGIHandler())

        port = listening_port
        num_attempts = 0

        print('''Starting OmniDB server...''')
        logger.info('''Starting OmniDB server...''')
        print('''Checking port availability...''')
        logger.info('''Checking port availability...''')

        while not check_port(port) or num_attempts >= 20:
            print("Port {0} is busy, trying another port...".format(port))
            logger.info("Port {0} is busy, trying another port...".format(port))
            port = random.randint(1025,32676)
            num_attempts = num_attempts + 1

        if num_attempts < 20:
            cherrypy.config.update({
                'server.socket_host': self.HOST,
                'server.socket_port': port,
                'engine.autoreload_on': False,
                'log.screen': False,
                'log.access_file': '',
                'log.error_file': ''
            })

            print ("Starting server {0} at http://127.0.0.1:{1}.".format(OmniDB.settings.OMNIDB_VERSION,str(port)))
            logger.info("Starting server {0} at http://127.0.0.1:{1}.".format(OmniDB.settings.OMNIDB_VERSION,str(port)))
            cherrypy.engine.start()

            init_browser(port)
            cherrypy.engine.exit()
        else:
            print('Tried 20 different ports without success, closing...')
            logger.info('Tried 20 different ports without success, closing...')

if __name__ == "__main__":

    #Choosing empty port
    port = ws_port
    num_attempts_port = 0

    print('''Starting OmniDB websocket...''')
    logger.info('''Starting OmniDB websocket...''')
    print('''Checking port availability...''')
    logger.info('''Checking port availability...''')

    while not check_port(port) or num_attempts_port >= 20:
        print("Port {0} is busy, trying another port...".format(port))
        logger.info("Port {0} is busy, trying another port...".format(port))
        port = random.randint(1025,32676)
        num_attempts_port = num_attempts_port + 1

    if num_attempts_port < 20:
        OmniDB.settings.OMNIDB_WEBSOCKET_PORT          = port
        OmniDB.settings.OMNIDB_EXTERNAL_WEBSOCKET_PORT = port
        OmniDB.settings.OMNIDB_ADDRESS                 = '127.0.0.1'

        print ("Starting websocket server at port {0}.".format(str(port)))
        logger.info("Starting websocket server at port {0}.".format(str(port)))

        #Removing Expired Sessions
        SessionStore.clear_expired()

        # Startup
        startup.startup_procedure()

        #Websocket Core
        ws_core.start_wsserver_thread()
        DjangoApplication().run()


    else:
        print('Tried 20 different ports without success, closing...')
        logger.info('Tried 20 different ports without success, closing...')
