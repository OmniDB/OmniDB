DROP TABLE command_list;--omnidb

CREATE TABLE command_list (
    user_id integer not null,
    cl_in_codigo integer not null,
    cl_st_command text,
    cl_st_start text,
    cl_st_end text,
    cl_st_status text,
    cl_st_duration text,
    conn_id integer not null,
    constraint pk_command_list primary key (cl_in_codigo),
    constraint command_list_fk_0 foreign key (user_id) references users (user_id)  on update CASCADE  on delete CASCADE,
    constraint command_list_fk_1 foreign key (conn_id) references connections (conn_id)  on update CASCADE  on delete CASCADE
);--omnidb--

UPDATE version SET ver_id = '2.12.0';--omnidb--
