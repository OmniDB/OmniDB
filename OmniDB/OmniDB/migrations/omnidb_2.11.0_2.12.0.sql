DROP TABLE command_list;--omnidb--

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

CREATE TABLE users_bak AS
SELECT *
FROM users;--omnidb--

DROP TABLE users;--omnidb--

CREATE TABLE users (
    user_id integer not null,
    user_name varchar(30),
    password varchar(100),
    theme_id integer,
    editor_font_size varchar(10),
    chat_enabled integer,
    super_user integer,
    csv_encoding varchar(20),
    csv_delimiter varchar(10),
    constraint pk_users primary key (user_id),
    constraint users_fk_0 foreign key (theme_id) references themes (theme_id)  on update NO ACTION  on delete NO ACTION,
    constraint uq_users_0 unique (user_name)
);--omnidb--

INSERT INTO users (
    user_id,
    user_name,
    password,
    theme_id,
    editor_font_size,
    chat_enabled,
    super_user,
    csv_encoding,
    csv_delimiter
)
SELECT user_id,
       user_name,
       password,
       theme_id,
       editor_font_size,
       chat_enabled,
       super_user,
       'utf-8' AS csv_encoding,
       ';' AS csv_delimiter
FROM users_bak;--omnidb--

DROP TABLE users_bak;--omnidb--

ALTER TABLE tabs ADD COLUMN title text;--omnidb--

INSERT INTO shortcuts VALUES(NULL,'shortcut_autocomplete',1,0,0,0,'SPACE');--omnidb--

UPDATE version SET ver_id = '2.12.0';--omnidb--
