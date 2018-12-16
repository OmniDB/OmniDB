CREATE TABLE cgroups (
  cgroup_id integer primary key,
  user_id integer references users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  cgroup_name text
)

CREATE TABLE cgroups_connections (
cgroup_id integer references cgroups (cgroup_id) ON UPDATE CASCADE ON DELETE CASCADE,
conn_id integer references connections (conn_id) ON UPDATE CASCADE ON DELETE CASCADE,
primary key (cgroup_id, conn_id)
)

UPDATE version SET ver_id = '2.13.0';--omnidb--
