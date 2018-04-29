from . import user_database
from . import settings
import os
import time
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

def clean_temp_folder(p_all_files = False):
    v_temp_folder = settings.TEMP_DIR
    current_time = time.time()
    for f in os.listdir(v_temp_folder):
        try:
            v_file = os.path.join(v_temp_folder,f)
            if f !='.gitkeep':
                creation_time = os.path.getctime(v_file)
                if ((current_time - creation_time) // (24 * 3600) >= 1) or p_all_files:
                    os.remove(v_file)
        except Exception as exc:
            pass

def startup_procedure():
    user_database.work()
    clean_temp_folder(True)

    #removing existing sessions
    database_sessions = OmniDatabase.Generic.InstantiateDatabase(
        'sqlite','','',settings.SESSION_DATABASE,'','','0',''
    )
    try:
        database_sessions.v_connection.Execute('''
            delete
            from django_session
        ''')
    except Exception as exc:
        print('Error:')
        print(exc)
