#!/bin/bash

# Initialize data folder
[ -d ~/.omnidb/omnidb-server/ ] ||mkdir -p ~/.omnidb/omnidb-server/

# Initialize configuration file
if [ ! -f ~/.omnidb/omnidb-server/config.py ]; then  
    # Global configuration
    cat << EOF > ~/.omnidb/omnidb-server/config.py
LISTENING_ADDRESS    = '0.0.0.0'
LISTENING_PORT       = 8080
CUSTOM_PATH = ''
PWD_TIMEOUT_TOTAL = 1800
IS_SSL                 = False
SSL_CERTIFICATE_FILE   = '/path/to/cert_file'
SSL_KEY_FILE           = '/path/to/key_file'
CSRF_TRUSTED_ORIGINS = []
THREAD_POOL_MAX_WORKERS = 2
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_NAME = 'omnidb_sessionid'
CSRF_COOKIE_NAME = 'omnidb_csrftoken'
EOF

    # LDAP specific config - direct bind
    if [ ! -z "$AUTH_LDAP_SERVER_URI" ] && [ ! -z "$AUTH_LDAP_USER_DN_TEMPLATE" ]; then
        cat << EOF >> ~/.omnidb/omnidb-server/config.py
import ldap
import django_auth_ldap.config
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI='${AUTH_LDAP_SERVER_URI}'
AUTH_LDAP_USER_DN_TEMPLATE='${AUTH_LDAP_USER_DN_TEMPLATE}'
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
]
EOF
    fi

    # LDAP specific config - search/bin
    if [ ! -z "$AUTH_LDAP_SERVER_URI" ] && [ ! -z "$AUTH_LDAP_BIND_DN" ] && [ ! -z "$AUTH_LDAP_BIND_PASSWORD" ] && [ ! -z "$AUTH_LDAP_USER_SEARCH" ] && [ ! -z "$AUTH_LDAP_USER_SEARCH_ITEM" ]; then
        cat << EOF >> ~/.omnidb/omnidb-server/config.py
import ldap
import django_auth_ldap.config
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI='${AUTH_LDAP_SERVER_URI}'
AUTH_LDAP_BIND_DN = "${AUTH_LDAP_BIND_DN}"
AUTH_LDAP_BIND_PASSWORD = "${AUTH_LDAP_BIND_PASSWORD}"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "${AUTH_LDAP_USER_SEARCH}", ldap.SCOPE_SUBTREE, "${AUTH_LDAP_USER_SEARCH_ITEM}"
)

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
]
EOF
    fi

    # SQL 
    # TODO
fi

# Call everything from CMD
exec $@