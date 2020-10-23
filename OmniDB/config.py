# What address the webserver listens to, 0.0.0.0 listens to all addresses bound to the machine
LISTENING_ADDRESS    = '127.0.0.1'

# Webserver port, if port is in use another random port will be selected
LISTENING_PORT       = 8000

# Url path to access OmniDB, default is empty
CUSTOM_PATH = ''

# Number of seconds between each prompt password request. Default: 30 minutes
PWD_TIMEOUT_TOTAL = 1800

# Security parameters
# is_ssl = True requires ssl_certificate_file and ssl_key_file parameters
# This is highly recommended to protect information
IS_SSL                 = False
SSL_CERTIFICATE_FILE   = '/path/to/cert_file'
SSL_KEY_FILE           = '/path/to/key_file'
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE    = True

# Trusted origins, use this parameter if OmniDB is configured with SSL and is being accessed by another domain
CSRF_TRUSTED_ORIGINS = []

# Max number of threads that can used by each advanced object search request
THREAD_POOL_MAX_WORKERS = 2

# List of domains that OmniDB can serve. '*' serves all domains
ALLOWED_HOSTS = ['*']

# Session cookie name
SESSION_COOKIE_NAME = 'omnidb_sessionid'

# CSRF cookie name
CSRF_COOKIE_NAME = 'omnidb_csrftoken'

### PostgreSQL Database Backend ################################################

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'dbname',
#        'USER': 'postgres',
#        'PASSWORD': '',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}

### LDAP Authentication ########################################################

#import ldap
#import django_auth_ldap.config
#from django_auth_ldap.config import LDAPSearch

#AUTH_LDAP_SERVER_URI = 'SERVER'
#AUTH_LDAP_BIND_DN = "uid=example,dc=example,dc=com"
#AUTH_LDAP_BIND_PASSWORD = "password"
#AUTH_LDAP_USER_SEARCH = django_auth_ldap.config.LDAPSearch(
#            "uid=example,dc=example,dc=com", ldap.SCOPE_SUBTREE, "uid=%(user)s"
#            )

#AUTHENTICATION_BACKENDS = [
#    'django_auth_ldap.backend.LDAPBackend',
#    'django.contrib.auth.backends.ModelBackend'
#]
