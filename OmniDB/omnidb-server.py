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
from OmniDB import user_database, ws_core

import logging
import logging.config
import optparse
import time

from django.contrib.sessions.backends.db import SessionStore

import socket
import random

import configparser

logger = logging.getLogger('OmniDB_app.Init')

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

            v_cherrypy_config = {
                'server.socket_host': parameters['listening_address'],
                'server.socket_port': port,
                'engine.autoreload_on': False,
                'log.screen': False,
                'log.access_file': '',
                'log.error_file': ''
            }

            if parameters['is_ssl']:
                v_cherrypy_config['server.ssl_module'] = 'builtin'
                v_cherrypy_config['server.ssl_certificate'] = parameters['ssl_certificate_file']
                v_cherrypy_config['server.ssl_private_key'] = parameters['ssl_key_file']

            cherrypy.config.update(v_cherrypy_config)

            print ("Starting server {0} at {1}:{2}.".format(OmniDB.settings.OMNIDB_VERSION,parameters['listening_address'],str(port)))
            logger.info("Starting server {0} at {1}:{2}.".format(OmniDB.settings.OMNIDB_VERSION,parameters['listening_address'],str(port)))
            cherrypy.engine.start()

            print ("Open OmniDB in your favorite browser")
            print ("Press Ctrl+C to exit")

            cherrypy.engine.block()
        else:
            print('Tried 20 different ports without success, closing...')
            logger.info('Tried 20 different ports without success, closing...')

if __name__ == "__main__":

    parser = optparse.OptionParser(version=OmniDB.settings.OMNIDB_VERSION)
    parser.add_option("-p", "--port", dest="port",
                      default=None, type=int,
                      help="listening port")

    parser.add_option("-w", "--wsport", dest="wsport",
                      default=None, type=int,
                      help="websocket port")

    parser.add_option("-H", "--host", dest="host",
                      default=None, type=str,
                      help="listening address")

    parser.add_option("-c", "--configfile", dest="conf",
                      default=OmniDB.settings.CONFFILE, type=str,
                      help="configuration file")

    (options, args) = parser.parse_args()

    #Parsing config file
    Config = configparser.ConfigParser()
    Config.read(options.conf)
    if not os.path.exists(options.conf):
        print("Config file not found, using default settings.")

    if options.host!=None:
        listening_address = options.host
    else:
        try:
            listening_address = Config.get('webserver', 'listening_address')
        except:
            listening_address = '0.0.0.0'
    if options.port!=None:
        listening_port = options.port
    else:
        try:
            listening_port = Config.getint('webserver', 'listening_port')
        except:
            listening_port = OmniDB.settings.OMNIDB_DEFAULT_SERVER_PORT
    if options.wsport!=None:
        ws_port = options.wsport
    else:
        try:
            ws_port = Config.getint('webserver', 'websocket_port')
        except:
            ws_port = OmniDB.settings.WS_QUERY_PORT
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

    #Choosing empty port
    port = ws_port
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
        OmniDB.settings.WS_QUERY_PORT   = port
        OmniDB.settings.IS_SSL          = is_ssl
        OmniDB.settings.SSL_CERTIFICATE = ssl_certificate_file
        OmniDB.settings.SSL_KEY         = ssl_key_file

        print ("Starting websocket server at port {0}.".format(str(port)))
        logger.info("Starting websocket server at port {0}.".format(str(port)))

        #Removing Expired Sessions
        SessionStore.clear_expired()

        # User Database
        user_database.work()

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
        print('Tried 20 different ports without success, closing...')
        logger.info('Tried 20 different ports without success, closing...')
