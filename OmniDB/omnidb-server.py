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

from django.core.handlers.wsgi import WSGIHandler
from OmniDB import user_database, ws_core, ws_chat

import logging
import logging.config
import optparse
import time

from django.contrib.sessions.backends.db import SessionStore

import socket
import random

import configparser

logger = logging.getLogger('OmniDB_app.Init')

import signal

def signal_handler(signal, frame):
        print('Terminating OmniDB...')
        sys.exit(0)

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        return False
    s.close()
    return True

if __name__ == "__main__":

    parser = optparse.OptionParser(version=OmniDB.settings.OMNIDB_VERSION)
    parser.add_option("-p", "--port", dest="port",
                      default=None, type=int,
                      help="listening port")

    parser.add_option("-H", "--host", dest="host",
                      default=None, type=str,
                      help="listening address")

    parser.add_option("-c", "--configfile", dest="conf",
                      default=OmniDB.settings.CONFFILE, type=str,
                      help="configuration file")

    parser.add_option("-w", "--wschatport", dest="chatport",
                      default=None, type=int,
                      help="chat port")

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
    if options.chatport!=None:
        chat_port = options.chatport
    else:
        try:
            chat_port = Config.getint('webserver', 'chat_port')
        except:
            chat_port = OmniDB.settings.WS_CHAT_PORT
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
    port = chat_port
    num_attempts = 0

    print('''Starting chat websocket...''')
    logger.info('''Starting chat websocket...''')
    print('''Checking port availability...''')
    logger.info('''Checking port availability...''')

    while not check_port(port) or num_attempts >= 20:
        print("Port {0} is busy, trying another port...".format(port))
        logger.info("Port {0} is busy, trying another port...".format(port))
        port = random.randint(1025,32676)
        num_attempts = num_attempts + 1

    if num_attempts < 20:
        OmniDB.settings.WS_CHAT_PORT   = port
        OmniDB.settings.IS_SSL          = is_ssl
        OmniDB.settings.SSL_CERTIFICATE = ssl_certificate_file
        OmniDB.settings.SSL_KEY         = ssl_key_file

        print ("Starting chat websocket server at port {0}.".format(str(port)))
        logger.info("Starting chat websocket server at port {0}.".format(str(port)))

        #Websocket Chat
        ws_chat.start_wsserver_thread()
    else:
        print('Tried 20 different ports without success, closing...')
        logger.info('Tried 20 different ports without success, closing...')

    #Choosing empty port
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
        OmniDB.settings.OMNIDB_PORT          = port
        OmniDB.settings.IS_SSL               = is_ssl
        OmniDB.settings.SSL_CERTIFICATE      = ssl_certificate_file
        OmniDB.settings.SSL_KEY              = ssl_key_file

        print ("Starting server at port {0}.".format(str(port)))
        logger.info("Starting server at port {0}.".format(str(port)))

        #Removing Expired Sessions
        SessionStore.clear_expired()

        # User Database
        user_database.work()

        #Websocket Core
        ws_core.start_wsserver_thread()

        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to exit.')
        signal.pause()
    else:
        print('Tried 20 different ports without success, closing...')
        logger.info('Tried 20 different ports without success, closing...')
