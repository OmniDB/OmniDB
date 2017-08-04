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
from OmniDB import ws_core

import logging
import logging.config
import optparse
import time

from django.contrib.sessions.backends.db import SessionStore

logger = logging.getLogger()

server_port=None

class DjangoApplication(object):
    HOST = "0.0.0.0"

    def mount_static(self, url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def run(self):

        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': server_port,
            'engine.autoreload_on': False,
            'log.screen': False,
            'log.access_file': '',
            'log.error_file': ''
        })
        #cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
        logging.config.dictConfig(OmniDB.settings.LOGGING)
        cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False
        self.mount_static(OmniDB.settings.STATIC_URL, OmniDB.settings.STATIC_ROOT)

        cherrypy.tree.graft(WSGIHandler())
        print ("Starting {0} at http://localhost:{1}".format(OmniDB.settings.OMNIDB_VERSION,str(server_port)))
        cherrypy.engine.start()

        print ("Open OmniDB in your favorite browser")
        print ("Press Ctrl+C to exit")
        cherrypy.engine.block()

if __name__ == "__main__":
    #default port

    parser = optparse.OptionParser(version=OmniDB.settings.OMNIDB_VERSION)
    parser.add_option("-p", "--port", dest="port",
                      default=OmniDB.settings.OMNIDB_DEFAULT_SERVER_PORT, type=int,
                      help="listening port")
    (options, args) = parser.parse_args()

    #Removing Expired Sessions
    SessionStore.clear_expired()

    #Websocket Core
    ws_core.start_wsserver_thread()
    server_port = options.port
    DjangoApplication().run()
