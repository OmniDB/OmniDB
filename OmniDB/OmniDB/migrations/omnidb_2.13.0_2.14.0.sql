UPDATE connections SET ssh_server = '' WHERE ssh_server IS NULL;--omnidb--
UPDATE connections SET ssh_port = '22' WHERE ssh_port IS NULL;--omnidb--
UPDATE connections SET ssh_user = '' WHERE ssh_user IS NULL;--omnidb--
UPDATE connections SET ssh_password = '' WHERE ssh_password IS NULL;--omnidb--
UPDATE connections SET ssh_key = '' WHERE ssh_key IS NULL;--omnidb--
UPDATE connections SET use_tunnel = 0 WHERE use_tunnel IS NULL;--omnidb--
ALTER TABLE connections ADD COLUMN conn_string TEXT;--omnidb--
UPDATE connections SET conn_string = '';--omnidb--

CREATE TABLE units_users_connections_temp (
    uuc_id integer not null,
    unit_id integer not null,
    user_id integer not null,
    conn_id integer not null,
    interval integer not null,
    plugin_name text,
    constraint pk_units_users_connections primary key (uuc_id),
    constraint units_users_connections_fk_0 foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE,
    constraint units_users_connections_fk_1 foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE
);--omnidb--
INSERT INTO units_users_connections_temp
SELECT uuc_id,
       unit_id,
       user_id,
       conn_id,
       interval,
       ''
FROM units_users_connections;--omnidb--
DROP TABLE units_users_connections;--omnidb--
ALTER TABLE units_users_connections_temp RENAME TO units_users_connections;--omnidb--

ALTER TABLE users ADD COLUMN interface_font_size TEXT;--omnidb--
UPDATE users SET interface_font_size = '11';--omnidb--

UPDATE version SET ver_id = '2.14.0';--omnidb--
