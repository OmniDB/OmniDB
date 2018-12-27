from . import settings
import os
import shutil
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

migrations = {
    '0.0.0': ('2.14.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_0.0.0_2.14.0.sql')),
    '2.4.0': ('2.4.1', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.4.0_2.4.1.sql')),
    '2.4.1': ('2.5.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.4.1_2.5.0.sql')),
    '2.5.0': ('2.6.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.5.0_2.6.0.sql')),
    '2.6.0': ('2.7.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.6.0_2.7.0.sql')),
    '2.7.0': ('2.8.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.7.0_2.8.0.sql')),
    '2.8.0': ('2.9.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.8.0_2.9.0.sql')),
    '2.9.0': ('2.10.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.9.0_2.10.0.sql')),
    '2.10.0': ('2.11.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.10.0_2.11.0.sql')),
    '2.11.0': ('2.12.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.11.0_2.12.0.sql')),
    '2.12.0': ('2.13.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.12.0_2.13.0.py')),
    '2.13.0': ('2.14.0', os.path.join(settings.BASE_DIR, 'OmniDB/migrations/omnidb_2.13.0_2.14.0.sql')),
}

def get_current_version(p_database):
    try:
        return p_database.v_connection.ExecuteScalar('select ver_id from version')
    except:
        return '0.0.0'

def migrate(p_database, p_current_version):
    if p_current_version in migrations:
        try:
            next_version = migrations[p_current_version][0]
            print('Starting migration of user database from version {0} to version {1}...'.format(p_current_version, next_version))
            file = migrations[p_current_version][1]
            tmp = file.split('.')
            ext = tmp[len(tmp)-1]
            if ext == 'sql':
                with open(file, 'r') as f:
                    p_database.v_connection.Open()
                    p_database.v_connection.Execute('BEGIN TRANSACTION;')
                    for sql in f.read().split('--omnidb--'):
                        p_database.v_connection.Execute(sql)
                    p_database.v_connection.Execute('COMMIT;')
                    p_database.v_connection.Close()
                    p_database.v_connection.Execute('VACUUM;')
            elif ext == 'py':
                with open(file, 'r') as f:
                    exec(f.read())
            else:
                raise Exception('Unsupported migration file format: {0}'.format(file))
            print('OmniDB successfully migrated user database from version {0} to version {1}'.format(p_current_version, next_version))
            return True
        except Exception as exc:
            print('OmniDB migration error: Error migrating from version {0} to version {1}: {2}'.format(p_current_version, next_version, str(exc)))
            return False
    else:
        print('OmniDB migration error: There is no migration from version {0}'.format(p_current_version))
        return False

def work():
    database = OmniDatabase.Generic.InstantiateDatabase('sqlite','','',settings.OMNIDB_DATABASE,'','','0','',p_foreignkeys=False)
    current_version = get_current_version(database)
    if current_version != settings.OMNIDB_SHORT_VERSION:
        if int(current_version.replace('.', '')) < int(settings.OMNIDB_SHORT_VERSION.replace('.', '')):
            if os.path.exists(settings.OMNIDB_DATABASE):
                shutil.copyfile(settings.OMNIDB_DATABASE, '{0}.bak_{1}'.format(settings.OMNIDB_DATABASE, settings.OMNIDB_SHORT_VERSION))
            while int(current_version.replace('.', '')) < int(settings.OMNIDB_SHORT_VERSION.replace('.', '')):
                if not migrate(database, current_version):
                    break
                current_version = get_current_version(database)
        else:
            print('OmniDB migration error: User database version {0} is ahead of server version {1}'.format(current_version, settings.OMNIDB_SHORT_VERSION))
    else:
        print('User database version {0} is already matching server version.'.format(current_version))
