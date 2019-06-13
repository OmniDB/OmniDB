import os, shutil
from . import custom_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if custom_settings.DEV_MODE:
    HOME_DIR = BASE_DIR
elif custom_settings.HOME_DIR:
    HOME_DIR = custom_settings.HOME_DIR
else:
    if custom_settings.DESKTOP_MODE:
        HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-app')
    else:
        HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-server')
if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)

CONFFILE = os.path.join(HOME_DIR, 'omnidb.conf')
if not custom_settings.DEV_MODE and not os.path.exists(CONFFILE):
    shutil.copyfile(os.path.join(BASE_DIR, 'omnidb.conf'), CONFFILE)
