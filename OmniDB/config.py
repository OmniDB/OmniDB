# What address the webserver listens to, 0.0.0.0 listens to all addresses bound to the machine
listening_address    = '127.0.0.1'

# Webserver port, if port is in use another random port will be selected
listening_port       = 8000

# Security parameters
# is_ssl = True requires ssl_certificate_file and ssl_key_file parameters
# This is highly recommended to protect information
is_ssl               = False
ssl_certificate_file = '/path/to/cert_file'
ssl_key_file         = '/path/to/key_file'

# Trusted origins, use this parameter if OmniDB is configured with SSL and is being accessed by another domain
csrf_trusted_origins = []

# Url path to access OmniDB, default is empty
path = ''

# Max number of threads that can used by each advanced object search request
thread_pool_max_workers = 2

# Number of seconds between each prompt password request. Default: 30 minutes
pwd_timeout_total = 1800

# List of domains that OmniDB can serve. '*' serves all domains
allowed_hosts = ['*']

# Session cookie name
session_cookie_name = 'omnidb_sessionid'

# CSRF cookie name
csrf_cookie_name = 'omnidb_csrftoken'
<<<<<<< HEAD

# OmniDB database settings

#database = {
#    'TECHNOLOGY': 'sqlite'
#}

database = {
    'TECHNOLOGY': 'postgresql',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': '',
    'HOST': '192.168.100.22',
    'PORT': '5432',
}
=======
>>>>>>> 98cf54b085c130c7b916e0f76a49d102d154ee0a
