sudo apt install postgresql-server-dev-9.6

./compile.sh

sudo cp omnidb_plugin.so /usr/lib/postgresql/9.6/lib/

nano /etc/postgresql/9.6/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'


create schema omnidb;

create table omnidb.contexts
(
  pid integer not null primary key,
  function text,
  hook text,
  lineno integer,
  stmttype text,
  breakpoint integer not null
);

create table omnidb.variables
(
  pid integer not null,
  name text,
  attribute text,
  vartype text,
  value text
);

alter table omnidb.variables add constraint omnidb_variables_contexts_fk
foreign key (pid) references omnidb.contexts (pid) on delete cascade;

create table omnidb.statistics
(
  pid integer not null,
  lineno integer,
  step integer,
  tstart timestamp without time zone,
  tend timestamp without time zone
);

alter table omnidb.statistics add constraint omnidb_statistics_contexts_fk
foreign key (pid) references omnidb.contexts (pid) on delete cascade;
