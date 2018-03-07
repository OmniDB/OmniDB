UPDATE data_categories SET cat_st_class = 'other' WHERE cat_st_name = 'boolean';--omnidb--

CREATE TABLE shortcuts (
    user_id integer,
    shortcut_code text,
    ctrl_pressed integer,
    shift_pressed integer,
    alt_pressed integer,
    meta_pressed integer,
    shortcut_key text,
    constraint pk_shortcuts primary key (user_id, shortcut_code),
    constraint fk_shortcuts_users foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE
);--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_analyze',0,0,1,0,'S');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_explain',0,0,1,0,'A');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_indent',0,0,1,0,'D');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_left_inner_tab',1,0,0,0,',');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_left_outer_tab',0,0,1,0,',');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_new_inner_tab',1,0,0,0,'INSERT');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_new_outer_tab',0,0,1,0,'INSERT');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_remove_inner_tab',1,0,0,0,'END');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_remove_outer_tab',0,0,1,0,'END');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_right_inner_tab',1,0,0,0,'.');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_run_query',0,0,1,0,'Q');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_right_outer_tab',0,0,1,0,'.');--omnidb--

UPDATE version SET ver_id = '2.6.0';--omnidb--
