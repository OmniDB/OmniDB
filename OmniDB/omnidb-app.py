#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'OmniDB.settings'
import django
django.setup()
import sys
import html.parser
import http.cookies
import OmniDB
import OmniDB.settings
import django.template.defaulttags
import django.template.loader_tags
import OmniDB_app
import OmniDB_app.apps
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

import cherrypy
from django.core.handlers.wsgi import WSGIHandler
from OmniDB import home, ws_core

import logging
import logging.config
import optparse
import time

from django.contrib.sessions.backends.db import SessionStore

from cefpython3 import cefpython as cef

import socket
import random

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
    cef.CreateBrowserSync(url="http://localhost:{0}?user=admin&pwd=admin".format(str(server_port)),window_title="OmniDB")
    cef.MessageLoop()
    cef.Shutdown()
    cherrypy.engine.exit()

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

    def run(self,server_port):
        #cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

        logging.config.dictConfig(OmniDB.settings.LOGGING)
        #cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False
        self.mount_static(OmniDB.settings.STATIC_URL, OmniDB.settings.STATIC_ROOT)

        cherrypy.tree.graft(WSGIHandler())

        port = server_port
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

            print ("Starting server {0} at http://localhost:{1}.".format(OmniDB.settings.OMNIDB_VERSION,str(port)))
            logger.info("Starting server {0} at http://localhost:{1}.".format(OmniDB.settings.OMNIDB_VERSION,str(port)))
            cherrypy.engine.start()

            init_browser(port)
            cherrypy.engine.block()
        else:
            print('Tried 20 different ports without success, closing...')
            logger.info('Tried 20 different ports without success, closing...')

if __name__ == "__main__":
    #default port

    parser = optparse.OptionParser(version=OmniDB.settings.OMNIDB_VERSION)
    parser.add_option("-p", "--port", dest="port",
                      default=OmniDB.settings.OMNIDB_DEFAULT_APP_PORT, type=int,
                      help="listening port")

    parser.add_option("-w", "--wsport", dest="wsport",
                      default=OmniDB.settings.WS_QUERY_PORT, type=int,
                      help="websocket port")
    (options, args) = parser.parse_args()

    #Choosing empty port
    port = options.wsport
    num_attempts = 0

    print('''Starting OmniDB websocket...''')
    logger.info('''Starting OmniDB websocket...''')
    print('''Checking port availability...''')
    logger.info('''Checking port availability...''')

    while not check_port(port) or num_attempts >= 20:
        print("Port {0} is busy, trying another port...".format(port))
        logger.info("Port {0} is busy, trying another port...".format(port))
        port = random.randint(1025,32676)
        num_attempts = num_attempts + 1

    if num_attempts < 20:
        OmniDB.settings.WS_QUERY_PORT = port

        print ("Starting websocket server at port {0}.".format(str(port)))
        logger.info("Starting websocket server at port {0}.".format(str(port)))

        #Removing Expired Sessions
        SessionStore.clear_expired()

        # Home folder and files
        home.work()

        #Websocket Core
        ws_core.start_wsserver_thread()
        DjangoApplication().run(options.port)
    else:
        print('Tried 20 different ports without success, closing...')
        logger.info('Tried 20 different ports without success, closing...')
