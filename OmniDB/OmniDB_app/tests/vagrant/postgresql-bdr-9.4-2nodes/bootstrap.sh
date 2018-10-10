#!/bin/sh -e

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=omnidb
APP_DB_PASS=omnidb

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=omnidb_tests

# Edit the following to change the version of PostgreSQL that is installed
PG_VERSION=9.4

# Edit the following to change the local port PostgreSQL port 5432 will be mapped to
PG_LOCAL_PORT=5432

###########################################################
# Changes below this line are probably not necessary
###########################################################
print_db_usage () {
  echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: $PG_LOCAL_PORT)"
  echo "  Host: localhost"
  echo "  Port: $PG_LOCAL_PORT"
  echo "  Database: $APP_DB_NAME"
  echo "  Username: $APP_DB_USER"
  echo "  Password: $APP_DB_PASS"
  echo ""
  echo "Admin access to postgres user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo ""
  echo "psql access to app database user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost $APP_DB_NAME"
  echo ""
  echo "Env variable for application development:"
  echo "  DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:$PG_LOCAL_PORT/$APP_DB_NAME"
  echo ""
  echo "Local command to access the database via psql:"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost -p $PG_LOCAL_PORT $APP_DB_NAME"
}

export DEBIAN_FRONTEND=noninteractive

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  echo ""
  print_db_usage
  exit
fi

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > "$PG_REPO_APT_SOURCE"

  # Add PGDG repo key:
  wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

apt-get -y install apt-transport-https curl ca-certificates

SQ_REPO_APT_SOURCE=/etc/apt/sources.list.d/2ndquadrant.list
if [ ! -f "$SQ_REPO_APT_SOURCE" ]
then
  # Add 2ndQ apt repo:
  echo "deb https://apt.2ndquadrant.com/ stretch-2ndquadrant main" > "$SQ_REPO_APT_SOURCE"

  # Add 2ndQ repo key:
  curl https://apt.2ndquadrant.com/site/keys/9904CD4BD6BAF0C3.asc | sudo apt-key add -
fi

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

apt-get -y install postgresql-bdr-9.4 postgresql-bdr-9.4-bdr-plugin

PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Other BDR specific settings
echo "shared_preload_libraries = 'bdr'" >> "$PG_CONF"
echo "wal_level = 'logical'" >> "$PG_CONF"
echo "track_commit_timestamp = on" >> "$PG_CONF"
echo "max_connections = 100" >> "$PG_CONF"
echo "max_wal_senders = 10" >> "$PG_CONF"
echo "max_replication_slots = 10" >> "$PG_CONF"
echo "# Make sure there are enough background worker slots for BDR to run" >> "$PG_CONF"
echo "max_worker_processes = 10" >> "$PG_CONF"
echo "# These aren't required, but are useful for diagnosing problems" >> "$PG_CONF"
echo "#log_error_verbosity = verbose" >> "$PG_CONF"
echo "#log_min_messages = debug1" >> "$PG_CONF"
echo "#log_line_prefix = 'd=%d p=%p a=%a%q '" >> "$PG_CONF"
echo "# Useful options for playing with conflicts" >> "$PG_CONF"
echo "#bdr.default_apply_delay=2000   # milliseconds" >> "$PG_CONF"
echo "#bdr.log_conflicts_to_table=on" >> "$PG_CONF"

# BDR specific authentication
echo "local   all           omnidb                            trust" >> "$PG_HBA"
echo "host    all           omnidb       127.0.0.1/32         trust" >> "$PG_HBA"
echo "host    all           omnidb       ::1/128              trust" >> "$PG_HBA"
echo "local   replication   omnidb                            trust" >> "$PG_HBA"
echo "host    replication   omnidb       127.0.0.1/32         trust" >> "$PG_HBA"
echo "host    replication   omnidb       ::1/128              trust" >> "$PG_HBA"
echo "host    all           omnidb       10.33.4.114/32       trust" >> "$PG_HBA"
echo "host    replication   omnidb       10.33.4.114/32       trust" >> "$PG_HBA"
echo "host    all           omnidb       10.33.4.115/32       trust" >> "$PG_HBA"
echo "host    replication   omnidb       10.33.4.115/32       trust" >> "$PG_HBA"

# Append to pg_hba.conf to add password auth:
echo "host    all           all          all                  md5" >> "$PG_HBA"

# Restart so that all new config is loaded:
systemctl restart postgresql

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS' SUPERUSER REPLICATION;

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created PostgreSQL dev virtual machine."
echo ""
print_db_usage
