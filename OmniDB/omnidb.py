#!/usr/bin/env python
import sys, uuid
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase
from OmniDB import settings

database = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','',settings.OMNIDB_DATABASE,'','','0',''
)
database_sessions = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','','db.sqlite3','','','0',''
)

def print_help():
    print('OmniDB console:')
    print('- create_superuser USERNAME PASSWORD')
    print('- clean sessions')
    print('- clean command_history')
    print('- clean all')
    print('- vacuum')

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

def create_superuser(p_user,p_pwd):
    try:
        print('Creating superuser...')
        v_cryptor = Utils.Cryptor("omnidb")
        database.v_connection.Execute('''
            insert into users values (
            (select coalesce(max(user_id), 0) + 1 from users),'{0}','{1}',1,'14',1,1,'{2}')
        '''.format(p_user,v_cryptor.Encrypt(p_pwd),str(uuid.uuid4())))
        print('Superuser created.')
    except Exception as exc:
        print('Error:')
        print(exc)

def clean_all():
    print('*** ATENTION *** ALL USERS DATA WILL BE LOST')
    try:
        value = input('Would you like to continue? (y/n) ')
        if value.lower()=='y':
            clean_users();
            clean_sessions();
            vacuum();
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

def clean_command_history():
    try:
        print('Cleaning command history...')
        database.v_connection.Execute('''
            delete
            from command_list
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
    if len(sys.argv)==1:
        print_help()
    elif sys.argv[1]=='create_superuser':
        if len(sys.argv)!=4:
            print('Wrong number of arguments:')
            print('createsuperuser USERNAME PASSWORD')
        else:
            create_superuser(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='clean':
        if len(sys.argv)!=3:
            print('Wrong number of arguments:')
            print('clean sessions')
            print('clean command_history')
            print('clean all')
        else:
            if sys.argv[2]=='sessions':
                clean_sessions()
            elif sys.argv[2]=='command_history':
                clean_command_history()
            elif sys.argv[2]=='all':
                clean_all()
            else:
                print('Command not found.')
                print_help()
    elif sys.argv[1]=='vacuum':
        vacuum()
    else:
            print('Command not found.')
            print_help()
