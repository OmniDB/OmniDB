#!/usr/bin/env python
import sys, uuid, os
import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

import OmniDB.custom_settings

import optparse

parser = optparse.OptionParser(version=OmniDB.custom_settings.OMNIDB_VERSION)

group = optparse.OptionGroup(parser, "General Options",
                             "Options to manage and perform maintenance on the OmniDB user database.")
group.add_option("-d", "--homedir", dest="homedir",
                  default='', type=str,
                  help="home directory containing local databases config and log files")
group.add_option("-a", "--vacuum", dest="vacuum",
                  default=False, action="store_true",
                  help="databases maintenance")
group.add_option("-r", "--resetdatabase", dest="reset",
                  default=False,action="store_true",
                  help="reset user and session databases")
group.add_option("-t", "--deletetemp", dest="deletetemp",
                  default=False,action="store_true",
                  help="delete temporary files")
parser.add_option_group(group)

group = optparse.OptionGroup(parser, "User Management Options",
                             "Options to list, create and drop users and superusers.")
group.add_option("-l", "--listusers", dest="listusers",
                  default=False, action="store_true",
                  help="list users")
group.add_option("-u", "--createuser", dest="createuser",
                  nargs=2,metavar="username password",
                  help="create user: -u username password")
group.add_option("-s", "--createsuperuser", dest="createsuperuser",
                  nargs=2,metavar="username password",
                  help="create super user: -s username password")
group.add_option("-x", "--dropuser", dest="dropuser",
                  nargs=1,metavar="username",
                  help="drop user: -x username")
parser.add_option_group(group)

group = optparse.OptionGroup(parser, "Connection Management Options",
                    "Options to list, create and drop connections.")
group.add_option("-m", "--listconnections", dest="listconnections",
                  nargs=1,metavar="username",
                  help="list connections: -m username")
group.add_option("-c", "--createconnection", dest="createconnection",
                  nargs=6,metavar="username technology host port database dbuser",
                  help="create connection: -c username technology host port database dbuser")
group.add_option("-z", "--dropconnection", dest="dropconnection",
                  nargs=1,metavar="connid",
                  help="drop connection: -z connid")
parser.add_option_group(group)

(options, args) = parser.parse_args()

if options.homedir!='':
    if not os.path.exists(options.homedir):
        print("Home directory does not exist. Please specify a directory that exists.")
        sys.exit()
    else:
        OmniDB.custom_settings.HOME_DIR = options.homedir

#importing settings after setting HOME_DIR
import OmniDB.settings
from OmniDB.startup import clean_temp_folder

database = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','',OmniDB.settings.OMNIDB_DATABASE,'','','0',''
)
database_sessions = OmniDatabase.Generic.InstantiateDatabase(
    'sqlite','','',OmniDB.settings.SESSION_DATABASE,'','','0',''
)

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

def clean_temp():
    try:
        print('Cleaning temp folder...')
        clean_temp_folder(True)
        print ('Done.')
    except Exception as exc:
        print('Error:')
        print(exc)

def list_users():
    try:
        v_table = database.v_connection.Query('''
            select user_id as userid,
                   user_name as username,
                   super_user as superuser
            from users
            order by user_id
        ''')
        print(v_table.Pretty())
    except Exception as exc:
        print('Error:')
        print(exc)

def create_user(p_user, p_pwd):
    try:
        print('Creating user...')
        v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')
        database.v_connection.Execute('''
            insert into users values (
            (select coalesce(max(user_id), 0) + 1 from users),'{0}','{1}',1,'14',1,0,'utf-8',';','11')
        '''.format(p_user,v_cryptor.Hash(v_cryptor.Encrypt(p_pwd))))
        print('User created.')
        #database.v_connection.Execute('''
        #    insert into users_channels (
        #        use_in_code,
        #        cha_in_code,
        #        usc_bo_silenced
        #    ) values (
        #        1,
        #        1,
        #        0
        #    )
        #    '''
        #)
    except Exception as exc:
        print('Error:')
        print(exc)

def create_superuser(p_user, p_pwd):
    try:
        print('Creating superuser...')
        v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')
        database.v_connection.Execute('''
            insert into users values (
            (select coalesce(max(user_id), 0) + 1 from users),'{0}','{1}',1,'14',1,1,'utf-8',';','11')
        '''.format(p_user,v_cryptor.Hash(v_cryptor.Encrypt(p_pwd))))
        print('Superuser created.')
        #database.v_connection.Execute('''
        #    insert into users_channels (
        #        use_in_code,
        #        cha_in_code,
        #        usc_bo_silenced
        #    ) values (
        #        1,
        #        1,
        #        0
        #    )
        #    '''
        #)
    except Exception as exc:
        print('Error:')
        print(exc)

def drop_user(p_user):
    try:
        v_table = database.v_connection.Query('''
            select *
            from users
            where user_name = '{0}'
        '''.format(p_user))
        if len(v_table.Rows) > 0:
            print('Dropping user {0}...'.format(p_user))
            database.v_connection.Execute('''
                delete
                from users
                where user_name = '{0}'
            '''.format(p_user))
            print('User {0} dropped.'.format(p_user))
        else:
            print('User {0} does not exist.'.format(p_user))
    except Exception as exc:
        print('Error:')
        print(exc)

def list_connections(p_user):
    try:
        v_table = database.v_connection.Query('''
            select c.conn_id as connid,
                   c.dbt_st_name as technology,
                   c.server as host,
                   c.port as port,
                   c.service as database,
                   c.user as dbuser
            from users u
            inner join connections c
            on c.user_id = u.user_id
            where u.user_name = '{0}'
            order by conn_id
        '''.format(p_user))
        v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')
        for v_row in v_table.Rows:
            v_row['host'] = v_cryptor.Decrypt(v_row['host'])
            v_row['port'] = v_cryptor.Decrypt(v_row['port'])
            v_row['database'] = v_cryptor.Decrypt(v_row['database'])
            v_row['dbuser'] = v_cryptor.Decrypt(v_row['dbuser'])
        print(v_table.Pretty())
    except Exception as exc:
        print('Error:')
        print(exc)

def create_connection(p_username, p_technology, p_host, p_port, p_database, p_dbuser):
    try:
        v_users = database.v_connection.Query('''
            select *
            from users
            where user_name = '{0}'
        '''.format(p_username))
        if len(v_users.Rows) > 0:
            v_technologies = database.v_connection.Query('''
                select *
                from db_type
                where dbt_in_enabled = 1
                  and dbt_st_name = '{0}'
            '''.format(p_technology))
            if len(v_technologies.Rows) > 0:
                print('Creating connection...')
                v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')
                database.v_connection.Execute('''
                    insert into connections values (
                        (select coalesce(max(conn_id), 0) + 1 from connections),
                        {0}, '{1}', '{2}', '{3}', '{4}', '{5}',
                        '', '', '', '', '', '', 0
                    )
                '''.format(
                    v_users.Rows[0]['user_id'],
                    p_technology,
                    v_cryptor.Encrypt(p_host),
                    v_cryptor.Encrypt(p_port),
                    v_cryptor.Encrypt(p_database),
                    v_cryptor.Encrypt(p_dbuser),
                ))
                print('Connection created.')
            else:
                print('Technology {0} does not exist.'.format(p_technology))
        else:
            print('User {0} does not exist.'.format(p_user))
    except Exception as exc:
        print('Error:')
        print(exc)

def drop_connection(p_connid):
    try:
        v_table = database.v_connection.Query('''
            select *
            from connections
            where conn_id = {0}
        '''.format(p_connid))
        if len(v_table.Rows) > 0:
            print('Dropping connection...'.format(p_connid))
            database.v_connection.Execute('''
                delete
                from connections
                where conn_id = {0}
            '''.format(p_connid))
            print('Connection dropped.')
        else:
            print('Connection {0} does not exist.'.format(p_connid))
    except Exception as exc:
        print('Error:')
        print(exc)

if __name__ == "__main__":

    if len(sys.argv[1:])==0:
        parser.print_help()
        sys.exit(0)

    if options.reset:
        print('*** ATENTION *** ALL USERS DATA WILL BE LOST')
        try:
            value = input('Would you like to continue? (y/n) ')
            if value.lower()=='y':
                #clean_chat()
                clean_users()
                clean_sessions()
                vacuum()
                clean_temp()
                create_superuser('admin', 'admin')
        except Exception as exc:
            print('Error:')
            print(exc)

    if options.vacuum:
        vacuum()

    if options.deletetemp:
        clean_temp()

    if options.listusers:
        list_users()

    if options.createuser:
        create_user(options.createuser[0], options.createuser[1])

    if options.createsuperuser:
        create_superuser(options.createsuperuser[0], options.createsuperuser[1])

    if options.dropuser:
        drop_user(options.dropuser)

    if options.listconnections:
        list_connections(options.listconnections)

    if options.createconnection:
        create_connection(options.createconnection[0], options.createconnection[1], options.createconnection[2], options.createconnection[3], options.createconnection[4], options.createconnection[5])

    if options.dropconnection:
        drop_connection(options.dropconnection)
