v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')

p_database.v_connection.Open()
p_database.v_connection.Execute('BEGIN TRANSACTION;')

v_table = p_database.v_connection.Query('SELECT user_id, password FROM users;')
for v_row in v_table.Rows:
    v_hashed_pwd = v_cryptor.Hash(v_row['password'])
    p_database.v_connection.Execute("UPDATE users SET password = '{0}' WHERE user_id = {1};".format(v_hashed_pwd, v_row['user_id']))

p_database.v_connection.Execute('''
    CREATE TABLE connections_bak AS
    SELECT *
    FROM connections;
''')

p_database.v_connection.Execute('DROP TABLE connections;')

p_database.v_connection.Execute('''
    CREATE TABLE connections (
        conn_id integer,
        user_id integer,
        dbt_st_name varchar(40),
        server varchar(500),
        port varchar(20),
        service varchar(500),
        user varchar(100),
        alias varchar(100),
        ssh_server varchar(500),
        ssh_port varchar(20),
        ssh_user varchar(100),
        ssh_password varchar(100),
        ssh_key text,
        use_tunnel integer,
        constraint pk_connections primary key (conn_id),
        constraint connections_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
        constraint connections_fk_1 foreign key (dbt_st_name) references db_type (dbt_st_name)  on update CASCADE  on delete CASCADE
    );
''')

p_database.v_connection.Execute('''
    INSERT INTO connections (
        conn_id,
        user_id,
        dbt_st_name,
        server,
        port,
        service,
        user,
        alias,
        ssh_server,
        ssh_port,
        ssh_user,
        ssh_password,
        ssh_key,
        use_tunnel
    )
    SELECT conn_id,
           user_id,
           dbt_st_name,
           server,
           port,
           service,
           user,
           alias,
           ssh_server,
           ssh_port,
           ssh_user,
           ssh_password,
           ssh_key,
           use_tunnel
    FROM connections_bak;
''')

p_database.v_connection.Execute('DROP TABLE connections_bak;')

p_database.v_connection.Execute('''
    CREATE TABLE cgroups (
      cgroup_id integer primary key,
      user_id integer references users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
      cgroup_name text
    );
''')

p_database.v_connection.Execute('''
    CREATE TABLE cgroups_connections (
        cgroup_id integer references cgroups (cgroup_id) ON UPDATE CASCADE ON DELETE CASCADE,
        conn_id integer references connections (conn_id) ON UPDATE CASCADE ON DELETE CASCADE,
        primary key (cgroup_id, conn_id)
    );
''')

p_database.v_connection.Execute("UPDATE version SET ver_id = '2.13.0';")

p_database.v_connection.Execute('COMMIT;')
p_database.v_connection.Close()
p_database.v_connection.Execute('VACUUM;')
