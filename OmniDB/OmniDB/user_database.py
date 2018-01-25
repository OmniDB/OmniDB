from . import settings
import os
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

migrations = {
    '0.0.0': ('2.4.1', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_0.0.0_2.4.1.sql')),
    '2.4.0': ('2.4.1', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.4.0_2.4.1.sql')),
    '2.4.1': ('2.5.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.4.1_2.5.0.sql')),
}

def get_current_version(p_database):
    try:
        return p_database.v_connection.ExecuteScalar('select ver_id from version')
    except:
        return '0.0.0'

def migrate(p_database, p_current_version):
    if p_current_version in migrations:
        next_version = migrations[p_current_version][0]
        sql_file = migrations[p_current_version][1]
        try:
            print('Starting migration of user database from version {0} to version {1}...'.format(p_current_version, next_version))
            with open(sql_file, 'r') as f:
                p_database.v_connection.Open()
                for sql in f.read().split('--omnidb--'):
                    p_database.v_connection.Execute(sql)
                p_database.v_connection.Close()
            print('OmniDB successfully migrated user database from version {0} to version {1}'.format(p_current_version, next_version))
            return True
        except Exception as exc:
            print('OmniDB migration error: Error migrating from version {0} to version {1}: {2}'.format(p_current_version, next_version, str(exc)))
            return False
    else:
        print('OmniDB migration error: There is no migration from version {0}'.format(p_current_version))
        return False

def work():
    database = OmniDatabase.Generic.InstantiateDatabase('sqlite','','',settings.OMNIDB_DATABASE,'','','0','')
    current_version = get_current_version(database)
    if current_version != settings.OMNIDB_SHORT_VERSION:
        if int(current_version.replace('.', '')) < int(settings.OMNIDB_SHORT_VERSION.replace('.', '')):
            while int(current_version.replace('.', '')) < int(settings.OMNIDB_SHORT_VERSION.replace('.', '')):
                if not migrate(database, current_version):
                    break
                current_version = get_current_version(database)
        else:
            print('OmniDB migration error: User database version {0} is ahead of server version {1}'.format(current_version, settings.OMNIDB_SHORT_VERSION))
    else:
        print('User database version {0} is already matching server version.'.format(current_version))
