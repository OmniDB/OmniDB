import os

# OmniDB settings
OMNIDB_VERSION = 'OmniDB 3.0.0'
OMNIDB_SHORT_VERSION = '3.0.0'
OMNIDB_ADDRESS = '127.0.0.1'
DEV_MODE = True
DESKTOP_MODE = False
APP_TOKEN = None
PWD_TIMEOUT_TOTAL = 1800
THREAD_POOL_MAX_WORKERS = 2
PATH = ''
HOME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Django settings
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = []
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_NAME = 'omnidb_sessionid'
CSRF_COOKIE_NAME = 'omnidb_csrftoken'

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HOME_DIR, 'omnidb.db')
    }
}

#DATABASE = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'omnidb',
#        'USER': 'postgres',
#        'PASSWORD': '',
#        'HOST': '10.33.2.114',
#        'PORT': '5432',
#    }
#}
