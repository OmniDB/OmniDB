CREATE TABLE units_users_connections (
    uuc_id integer not null,
    unit_id integer not null,
    user_id integer not null,
    conn_id integer not null,
    interval integer not null,
    constraint pk_units_users_connections primary key (uuc_id),
    constraint units_users_connections_fk_0 foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE,
    constraint units_users_connections_fk_1 foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE,
    constraint units_users_connections_fk_2 foreign key (unit_id) references mon_units (unit_id) on update CASCADE on delete CASCADE
);--omnidb--

UPDATE version SET ver_id = '2.10.0';--omnidb--
