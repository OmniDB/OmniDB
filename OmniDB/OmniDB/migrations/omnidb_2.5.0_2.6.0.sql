UPDATE data_categories SET cat_st_class = 'other' WHERE cat_st_name = 'boolean';--omnidb--

UPDATE mon_units SET script_chart = replace('total_size = connection.ExecuteScalar(''''''\n    SELECT round(sum(pg_catalog.pg_database_size(datname)/1048576.0),2)\n    FROM pg_catalog.pg_database\n    WHERE NOT datistemplate\n'''''')\n\nresult = {\n    "type": "line",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Database Size (Total: " + str(total_size) + " MB)"\n        },\n        "tooltips": {\n            "mode": "index",\n            "intersect": False\n        },\n        "hover": {\n            "mode": "nearest",\n            "intersect": True\n        },\n        "scales": {\n            "xAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Time"\n                }\n            }],\n            "yAxes": [{\n                "display": True,\n                "scaleLabel": {\n                    "display": True,\n                    "labelString": "Size (MB)"\n                }\n            }]\n        }\n    }\n}\n','\n',char(10))
WHERE unit_id = 2;--omnidb--
UPDATE mon_units SET script_chart = replace('total_size = connection.ExecuteScalar(''''''\n    SELECT round(sum(pg_catalog.pg_database_size(datname)/1048576.0),2)\n    FROM pg_catalog.pg_database\n    WHERE NOT datistemplate\n'''''')\n\nresult = {\n    "type": "pie",\n    "data": None,\n    "options": {\n        "responsive": True,\n        "title":{\n            "display":True,\n            "text":"Database Size (Total: " + str(total_size) + " MB)"\n        }\n    }\n}\n','\n',char(10))
WHERE unit_id = 10;--omnidb--

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
INSERT INTO shortcuts VALUES(NULL,'shortcut_cancel_query',0,0,1,0,'C');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_next_console_command',1,0,0,0,'ARROWDOWN');--omnidb--
INSERT INTO shortcuts VALUES(NULL,'shortcut_previous_console_command',1,0,0,0,'ARROWUP');--omnidb--

CREATE TABLE console_history (
    user_id integer,
    conn_id integer,
    command_text text,
    command_date text,
    constraint fk_ch_users foreign key (user_id) references users (user_id) on update CASCADE on delete CASCADE,
    constraint fk_ch_conn foreign key (conn_id) references connections (conn_id) on update CASCADE on delete CASCADE
);--omnidb--

UPDATE version SET ver_id = '2.6.0';--omnidb--
