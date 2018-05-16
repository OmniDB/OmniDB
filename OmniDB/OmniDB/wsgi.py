"""
WSGI config for OmniDB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from . import startup, ws_core, monitoring_core

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OmniDB.settings")

application = get_wsgi_application()

# Startup Procedure
#startup.startup_procedure()

#Monitoring Core
#monitoring_core.start_monitoring_thread()

#Websocket Core
ws_core.start_wsserver_thread()
