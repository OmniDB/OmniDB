import os
import sys
import shutil
import random
import string
import getpass
from . import custom_settings
import config

# Development Mode
DEBUG = custom_settings.DEV_MODE
DESKTOP_MODE = custom_settings.DESKTOP_MODE
BASE_DIR = custom_settings.BASE_DIR
HOME_DIR = custom_settings.HOME_DIR
SESSION_COOKIE_SECURE = custom_settings.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = custom_settings.CSRF_COOKIE_SECURE
CSRF_TRUSTED_ORIGINS = custom_settings.CSRF_TRUSTED_ORIGINS
SESSION_COOKIE_NAME = custom_settings.SESSION_COOKIE_NAME
CSRF_COOKIE_NAME = custom_settings.CSRF_COOKIE_NAME
ALLOWED_HOSTS = custom_settings.ALLOWED_HOSTS

TEMP_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','temp')
PLUGINS_DIR = os.path.join(BASE_DIR,'OmniDB_app','plugins')
PLUGINS_STATIC_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','plugins')
APP_DIR = os.path.join(BASE_DIR,'OmniDB_app')

if DEBUG:
    SECRET_KEY = 'ijbq-+%n_(_^ct+qnqp%ir8fzu3n#q^i71j4&y#-6#qe(dx!h3'
else:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(50))


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'



INSTALLED_APPS = [
    'OmniDB_app.apps.OmnidbAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OmniDB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OmniDB.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GITHUB_KEY = 'Iv1.b66f09dc30df16f3'
SOCIAL_AUTH_GITHUB_SECRET = '3403a3cc31a991d48ef72fbd73fa45e3af5b62ba'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HOME_DIR, 'omnidb.db')
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'omnidb',
#        'USER': 'postgres',
#        'PASSWORD': '',
#        'HOST': '10.33.2.114',
#        'PORT': '5432',
#    }
#}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PATH = custom_settings.PATH
# Processing PATH
if PATH == '/':
    PATH = ''
elif PATH != '':
    if PATH[0] != '/':
        PATH = '/' + PATH
    if PATH[len(PATH)-1] == '/':
        PATH = PATH[:-1]

STATIC_URL = PATH + '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "OmniDB_app/static")

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#OMNIDB LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%m/%d/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile_omnidb': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(HOME_DIR, 'omnidb.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'logfile_django': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(HOME_DIR, 'omnidb.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
            'level':'ERROR',
        },
        'console_django':{
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console_omnidb_app':{
            'class':'logging.StreamHandler',
            'formatter': 'standard',
            'level':'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile_django','console_django'],
            'propagate': False,
        },
        'OmniDB_app': {
            'handlers': ['logfile_omnidb','console_omnidb_app'],
            'propagate': False,
            'level':'INFO',
        },
        'cherrypy.error': {
            'handlers': ['logfile_django','console_omnidb_app'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

#OMNIDB PARAMETERS
OMNIDB_VERSION                 = custom_settings.OMNIDB_VERSION
OMNIDB_SHORT_VERSION           = custom_settings.OMNIDB_SHORT_VERSION
CH_CMDS_PER_PAGE               = 20
PWD_TIMEOUT_TOTAL              = custom_settings.PWD_TIMEOUT_TOTAL
PWD_TIMEOUT_REFRESH            = 300
THREAD_POOL_MAX_WORKERS        = custom_settings.THREAD_POOL_MAX_WORKERS
