import os
import sys
import shutil
import random
import string
import getpass
from . import custom_settings

#import ldap
#import django_auth_ldap
#import django_auth_ldap.config

# Development Mode
DEBUG = custom_settings.DEV_MODE
DESKTOP_MODE = custom_settings.DESKTOP_MODE
BASE_DIR = custom_settings.BASE_DIR
HOME_DIR = custom_settings.HOME_DIR
OMNIDB_LOG_LEVEL = custom_settings.OMNIDB_LOG_LEVEL
TEMP_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','temp')
PLUGINS_DIR = os.path.join(BASE_DIR,'OmniDB_app','plugins')
PLUGINS_STATIC_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','plugins')
APP_DIR = os.path.join(BASE_DIR,'OmniDB_app')

SESSION_COOKIE_SECURE = custom_settings.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = custom_settings.CSRF_COOKIE_SECURE
CSRF_TRUSTED_ORIGINS = []
SESSION_COOKIE_NAME = 'omnidb_sessionid'
CSRF_COOKIE_NAME = 'omnidb_csrftoken'
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HOME_DIR, 'omnidb.db')
    }
}

if DEBUG:
    SECRET_KEY = 'ijbq-+%n_(_^ct+qnqp%ir8fzu3n#q^i71j4&y#-6#qe(dx!h3'
else:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(50))

INSTALLED_APPS = [
    'OmniDB_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_sass'
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

#import ldap
#import django_auth_ldap.config
#from django_auth_ldap.config import LDAPSearch

#AUTH_LDAP_SERVER_URI = 'SERVER'
#AUTH_LDAP_BIND_DN = "uid=example,dc=example,dc=com"
#AUTH_LDAP_BIND_PASSWORD = "password"
#AUTH_LDAP_USER_SEARCH = django_auth_ldap.config.LDAPSearch(
#            "uid=example,dc=example,dc=com", ldap.SCOPE_SUBTREE, "uid=%(user)s"
#            )
#AUTH_LDAP_USER_ATTR_MAP = {
#            "username": "sAMAccountName",
#                "first_name": "givenName",
#                    "last_name": "sn",
#                        "email": "mail",
#}
#from django_auth_ldap.config import ActiveDirectoryGroupType
#AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#            "dc=tech,dc=local", ldap.SCOPE_SUBTREE, "(objectCategory=Group)"
#            )
#AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#            "is_superuser": "CN=django-admins,CN=Users,DC=TECH,DC=LOCAL",
#            "is_staff": "CN=django-admins,CN=Users,DC=TECH,DC=LOCAL",
#            }
#AUTH_LDAP_FIND_GROUP_PERMS = True
#AUTH_LDAP_CACHE_GROUPS = True
#AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1  # 1 hour cache

AUTHENTICATION_BACKENDS = [
    #'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GITHUB_KEY = 'Iv1.b66f09dc30df16f3'
SOCIAL_AUTH_GITHUB_SECRET = '3403a3cc31a991d48ef72fbd73fa45e3af5b62ba'

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


LOGIN_URL = PATH + '/omnidb_login'
LOGIN_REDIRECT_URL = PATH + '/'

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
            'formatter': 'standard'
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
            'level': OMNIDB_LOG_LEVEL,
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
PWD_TIMEOUT_TOTAL              = 1800
PWD_TIMEOUT_REFRESH            = 300
THREAD_POOL_MAX_WORKERS        = 2
