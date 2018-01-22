#!/usr/bin/env python
import sys, uuid
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB import settings

import optparse

database = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','',settings.OMNIDB_DATABASE,'','','0',''
)
database_sessions = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','',settings.SESSION_DATABASE,'','','0',''
)

def create_superuser(p_user, p_pwd):
    try:
        print('Creating superuser...')
        v_cryptor = Utils.Cryptor("omnidb")
        database.v_connection.Execute('''
            insert into users values (
            (select coalesce(max(user_id), 0) + 1 from users),'{0}','{1}',1,'14',1,1,'{2}', 1, 0)
        '''.format(p_user,v_cryptor.Encrypt(p_pwd),str(uuid.uuid4())))
        print('Superuser created.')
        database.v_connection.Execute('''
            insert into users_channels (
                use_in_code,
                cha_in_code,
                usc_bo_silenced
            ) values (
                1,
                1,
                0
            )
            '''
        )
    except Exception as exc:
        print('Error:')
        print(exc)

def clean_users():
    try:
        print('Cleaning users...')
        database.v_connection.Execute('''
            delete
            from users
        ''')
        print ('Done.')
    except Exception as exc:
        print('Error:')
        print(exc)

def clean_chat():
    try:
        print('Cleaning chat...')
        database.v_connection.Execute('''
            delete
            from messages_groups
        ''')
        database.v_connection.Execute('''
            delete
            from messages_channels
        ''')
        database.v_connection.Execute('''
            delete
            from messages
        ''')
        database.v_connection.Execute('''
            delete
            from users_groups
        ''')
        database.v_connection.Execute('''
            delete
            from users_channels
        ''')
        database.v_connection.Execute('''
            delete
            from groups
        ''')
        database.v_connection.Execute('''
            delete
            from channels
        ''')
        database.v_connection.Execute('''
            insert into channels (
                cha_in_code,
                cha_st_name,
                cha_bo_private
            )
            values (
                1,
                'General',
                0
            )
        ''')
        print ('Done.')
    except Exception as exc:
        print('Error:')
        print(exc)

def clean_sessions():
    try:
        print('Cleaning sessions...')
        database_sessions.v_connection.Execute('''
            delete
            from django_session
        ''')
        print ('Done.')
    except Exception as exc:
        print('Error:')
        print(exc)

def vacuum():
    try:
        print('Vacuuming OmniDB database...')
        database.v_connection.Execute('vacuum')
        print ('Done.')
        print('Vacuuming Sessions database...')
        database_sessions.v_connection.Execute('vacuum')
        print ('Done.')
    except Exception as exc:
        print('Error:')
        print(exc)


if __name__ == "__main__":

    parser = optparse.OptionParser(version=settings.OMNIDB_VERSION)
    parser.add_option("-c", "--createsuperuser", dest="createsuperuser",
                      nargs=2,metavar="username password",
                      help="create super user: -c username password")
    parser.add_option("-a", "--vacuum", dest="vacuum",
                      default=False, action="store_true",
                      help="databases maintenance")
    parser.add_option("-r", "--resetdatabase", dest="reset",
                      default=False,action="store_true",
                      help="reset user and Django databases")
    (options, args) = parser.parse_args()

    if len(sys.argv[1:])==0:
        parser.print_help()
        sys.exit(0)

    if options.reset:
        print('*** ATENTION *** ALL USERS DATA WILL BE LOST')
        try:
            value = input('Would you like to continue? (y/n) ')
            if value.lower()=='y':
                clean_users()
                clean_chat()
                clean_sessions()
                vacuum()
                create_superuser('admin', 'admin')
        except Exception as exc:
            print('Error:')
            print(exc)

    if options.vacuum:
        vacuum()

    if options.createsuperuser:
        create_superuser(options.createsuperuser[0], options.createsuperuser[1])
