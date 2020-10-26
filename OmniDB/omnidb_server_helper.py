import sys
import OmniDB_app.include.OmniDatabase as OmniDatabase
import OmniDB_app.include.Spartacus.Utils as Utils

from django.contrib.auth.models import User
from OmniDB_app.models.main import *

from datetime import datetime
from django.utils.timezone import make_aware

import django.db.transaction as transaction
from django.utils import timezone

def log_message(p_logger, p_type, p_message):
    print(p_message,flush=True)
    if p_type=='error':
        p_logger.error(p_message)
    else:
        p_logger.info(p_message)


def migration_main(p_old_db_file, p_interactive, p_logger):
    config_object = Config.objects.all()[0]

    perform_migration = False
    if not config_object.mig_2_to_3_done:
        perform_migration = True
    elif p_interactive:
        value = input('Target database already migrated from OmniDB 2, continue anyway? (y/n) ')
        if value.lower()=='y':
            perform_migration = True

    if perform_migration:
        log_message(p_logger,'info','Attempting to migrate users, connections and monitoring units and snippets from OmniDB 2 to 3...')

        database = OmniDatabase.Generic.InstantiateDatabase(
            'sqlite','','',p_old_db_file,'','','0',''
        )

        # Check that OmniDB 2 required tables exist
        migration_enabled = True
        try:
            database.v_connection.Query('''
                select count(1)
                from users
            ''')
        except:
            migration_enabled = False
        try:
            database.v_connection.Query('''
                select count(1)
                from connections
            ''')
        except:
            migration_enabled = False

        if not migration_enabled:
            log_message(p_logger,'info','Source database file does not contain the required tables, skipping...')
            config_object.mig_2_to_3_done = True
            config_object.save()
        else:

            try:
                transaction.set_autocommit(False)

                cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')
                v_users = database.v_connection.Query('''
                    select user_id as userid,
                           user_name as username,
                           super_user as superuser
                    from users
                    order by user_id
                ''')
                for user in v_users.Rows:
                    # Try to get existing user
                    try:
                        log_message(p_logger,'info',"Creating user '{0}'...".format(user['username']))
                        user_object=User.objects.get(username=user['username'])
                        log_message(p_logger,'info',"User '{0}' already exists.".format(user['username']))
                    except:
                        # Creating the user
                        user_object = User.objects.create_user(username=user['username'],
                                                 password='changeme',
                                                 email='',
                                                 last_login=timezone.now(),
                                                 is_superuser=user['superuser']==1,
                                                 first_name='',
                                                 last_name='',
                                                 is_staff=False,
                                                 is_active=True,
                                                 date_joined=timezone.now())
                        log_message(p_logger,'info',"User '{0}' created.".format(user['username']))


                    # User connections
                    v_connections = database.v_connection.Query('''
                        select coalesce(dbt_st_name,'') as dbt_st_name,
                                coalesce(server,'') as server,
                                coalesce(port,'') as port,
                                coalesce(service,'') as service,
                                coalesce(user,'') as user,
                                coalesce(alias,'') as alias,
                                coalesce(ssh_server,'') as ssh_server,
                                coalesce(ssh_port,'') as ssh_port,
                                coalesce(ssh_user,'') as ssh_user,
                                coalesce(ssh_password,'') as ssh_password,
                                coalesce(ssh_key,'') as ssh_key,
                                coalesce(use_tunnel,0) as use_tunnel,
                                coalesce(conn_string,'') as conn_string
                        from connections
                        where user_id = {0}
                        order by dbt_st_name,
                                 conn_id
                    '''.format(user['userid']))

                    if len(v_connections.Rows) == 0:
                        log_message(p_logger,'info',"User '{0}' does not contain connections in the source database.".format(user['username']))
                    else:
                        log_message(p_logger,'info',"Attempting to create connections of user '{0}'...".format(user['username']))

                        for r in v_connections.Rows:
                            try:
                                v_server = cryptor.Decrypt(r["server"])
                            except Exception as exc:
                                v_server = r["server"]
                            try:
                                v_port = cryptor.Decrypt(r["port"])
                            except Exception as exc:
                                v_port = r["port"]
                            try:
                                v_service = cryptor.Decrypt(r["service"])
                            except Exception as exc:
                                v_service = r["service"]
                            try:
                                v_user = cryptor.Decrypt(r["user"])
                            except Exception as exc:
                                v_user = r["user"]
                            try:
                                v_alias = cryptor.Decrypt(r["alias"])
                            except Exception as exc:
                                v_alias = r["alias"]
                            try:
                                v_conn_string = cryptor.Decrypt(r["conn_string"])
                            except Exception as exc:
                                v_conn_string = r["conn_string"]

                            #SSH Tunnel information
                            try:
                                v_ssh_server = cryptor.Decrypt(r["ssh_server"])
                            except Exception as exc:
                                v_ssh_server = r["ssh_server"]
                            try:
                                v_ssh_port = cryptor.Decrypt(r["ssh_port"])
                            except Exception as exc:
                                v_ssh_port = r["ssh_port"]
                            try:
                                v_ssh_user = cryptor.Decrypt(r["ssh_user"])
                            except Exception as exc:
                                v_ssh_user = r["ssh_user"]
                            try:
                                v_ssh_password = cryptor.Decrypt(r["ssh_password"])
                            except Exception as exc:
                                v_ssh_password = r["ssh_password"]
                            try:
                                v_ssh_key = cryptor.Decrypt(r["ssh_key"])
                            except Exception as exc:
                                v_ssh_key = r["ssh_key"]
                            try:
                                v_use_tunnel = cryptor.Decrypt(r["use_tunnel"])
                            except Exception as exc:
                                v_use_tunnel = r["use_tunnel"]

                            # Check if connection already exists before creating it
                            conn = Connection.objects.filter(
                                user=user_object,
                                technology=Technology.objects.get(name=r["dbt_st_name"]),
                                server=v_server,
                                port=v_port,
                                database=v_service,
                                username=v_user,
                                password='',
                                alias=v_alias,
                                ssh_server=v_ssh_server,
                                ssh_port=v_ssh_port,
                                ssh_user=v_ssh_user,
                                ssh_password=v_ssh_password,
                                ssh_key=v_ssh_key,
                                use_tunnel=v_use_tunnel==1,
                                conn_string=v_conn_string,
                            )

                            if len(conn)>0:
                                log_message(p_logger,'info',"Skipping creation of connection with alias '{0}' because an identical connection already exists.".format(v_alias))
                            else:
                                log_message(p_logger,'info',"Creating connection with alias '{0}'...".format(v_alias))

                                connection = Connection(
                                    user=user_object,
                                    technology=Technology.objects.get(name=r["dbt_st_name"]),
                                    server=v_server,
                                    port=v_port,
                                    database=v_service,
                                    username=v_user,
                                    password='',
                                    alias=v_alias,
                                    ssh_server=v_ssh_server,
                                    ssh_port=v_ssh_port,
                                    ssh_user=v_ssh_user,
                                    ssh_password=v_ssh_password,
                                    ssh_key=v_ssh_key,
                                    use_tunnel=v_use_tunnel==1,
                                    conn_string=v_conn_string,
                                )
                                connection.save()
                                log_message(p_logger,'info',"Connection with alias '{0}' created.".format(v_alias))

                    # User snippets
                    log_message(p_logger,'info',"Attempting to create snippets of user '{0}'...".format(user['username']))

                    v_folders = database.v_connection.Query('''
                        select sn_id, sn_name, sn_id_parent
                        from snippets_nodes
                        where user_id = {0}
                    '''.format(user['userid']))

                    #Child texts
                    v_files = database.v_connection.Query('''
                        select st_id, st_name, sn_id_parent, st_text
                        from snippets_texts
                        where user_id = {0}
                    '''.format(user['userid']))

                    v_root = {
                        'id': None,
                        'object': None
                    }

                    migration_build_snippets_object_recursive(v_folders,v_files,v_root, user_object, p_logger)

                    # User monitoring units
                    log_message(p_logger,'info',"Attempting to create monitoring units of user '{0}'...".format(user['username']))

                    v_units = database.v_connection.Query('''
                        select title,
                        case type
                          when 'chart' then 'chart'
                          when 'chart_append' then 'timeseries'
                          when 'grid' then 'grid'
                          when 'graph' then 'graph'
                        end type,
                        interval,
                        dbt_st_name,
                        script_chart,
                        script_data
                        from mon_units
                        where user_id = {0}
                    '''.format(user['userid']))

                    for unit in v_units.Rows:
                        unit_object = MonUnits(
                            user=user_object,
                            technology=Technology.objects.get(name=unit['dbt_st_name']),
                            script_chart=unit['script_chart'],
                            script_data=unit['script_data'],
                            type=unit['type'],
                            title=unit['title'],
                            is_default=False,
                            interval=unit['interval']
                        )
                        unit_object.save()

                        log_message(p_logger,'info',"Monitoring unit '{0}' created.".format(unit['title']))

                config_object.mig_2_to_3_done = True
                config_object.save()
                log_message(p_logger,'info','Database migration finished.')

            except Exception as exc:
                log_message(p_logger,'error','Failed to complete migration, rolled back. Error: {0}'.format(str(exc)))
                sys.exit()

            transaction.set_autocommit(True)

def migration_build_snippets_object_recursive(p_folders,p_files,p_current_object, p_user, p_logger):
    # Adding files
    for file in p_files.Rows:
        # Match
        if ((file['sn_id_parent'] == None and p_current_object['id'] == None) or (file['sn_id_parent']!=None and file['sn_id_parent'] == p_current_object['id'])):
            new_date = make_aware(datetime.now())
            file_object = SnippetFile(
                user=p_user,
                parent=p_current_object['object'],
                name=file['st_name'],
                create_date=new_date,
                modify_date=new_date,
                text=file['st_text']
            )
            file_object.save()
            log_message(p_logger,'info',"Snippet '{0}' created.".format(file['st_name']))
    # Adding folders
    for folder in p_folders.Rows:
        # Match
        if ((folder['sn_id_parent'] == None and p_current_object['id'] == None) or (folder['sn_id_parent']!=None and folder['sn_id_parent'] == p_current_object['id'])):
            folder_object = SnippetFolder(
                user=p_user,
                parent=p_current_object['object'],
                name=folder['sn_name'],
                create_date=new_date,
                modify_date=new_date
            )

            folder_object.save()
            log_message(p_logger,'info',"Folder '{0}' created.".format(folder['sn_name']))
            v_folder = {
                'id': folder['sn_id'],
                'object': folder_object
            }

            migration_build_snippets_object_recursive(p_folders,p_files,v_folder, p_user, p_logger)
