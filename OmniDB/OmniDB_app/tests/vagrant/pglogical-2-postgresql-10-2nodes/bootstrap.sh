#!/bin/sh -e

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=omnidb
APP_DB_PASS=omnidb

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=omnidb_tests

# Edit the following to change the version of PostgreSQL that is installed
PG_VERSION=10

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

#!/bin/bash

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'yum update'"
  exit
fi

# Update package list and upgrade all packages
yum -y update

# Install EPEL repo
yum -y install epel-release

# Install dependencies
yum -y install libicu libxslt

# Install PostgreSQL
rpm -ivh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/postgresql10-libs-10.4-1PGDG.rhel7.x86_64.rpm
rpm -ivh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/postgresql10-10.4-1PGDG.rhel7.x86_64.rpm
rpm -ivh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/postgresql10-server-10.4-1PGDG.rhel7.x86_64.rpm
rpm -ivh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/postgresql10-contrib-10.4-1PGDG.rhel7.x86_64.rpm

# Install PGDG repo
rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm

# Install pglogical repo
rpm -ivh http://packages.2ndquadrant.com/pglogical/yum-repo-rpms/pglogical-rhel-1.0-3.noarch.rpm

# Install pglogical
yum -y install postgresql10-pglogical

# Initialize PostgreSQL database
/usr/pgsql-10/bin/postgresql-10-setup initdb

# Enable PostgreSQL service
systemctl enable postgresql-10

# Start PostgreSQL service
systemctl start postgresql-10

PG_CONF="/var/lib/pgsql/$PG_VERSION/data/postgresql.conf"
PG_HBA="/var/lib/pgsql/$PG_VERSION/data/pg_hba.conf"
PG_DIR="/var/lib/pgsql/$PG_VERSION/data"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Other pglogical specific settings
echo "wal_level = 'logical'" >> "$PG_CONF"
echo "track_commit_timestamp = on" >> "$PG_CONF"
echo "max_connections = 100" >> "$PG_CONF"
echo "max_wal_senders = 10" >> "$PG_CONF"
echo "max_replication_slots = 10" >> "$PG_CONF"
echo "max_worker_processes = 10" >> "$PG_CONF"
echo "shared_preload_libraries = 'pglogical'" >> "$PG_CONF"

# pglogical specific authentication
echo "local   all           omnidb                            trust" >> "$PG_HBA"
echo "host    all           omnidb       127.0.0.1/32         trust" >> "$PG_HBA"
echo "host    all           omnidb       ::1/128              trust" >> "$PG_HBA"
echo "local   replication   omnidb                            trust" >> "$PG_HBA"
echo "host    replication   omnidb       127.0.0.1/32         trust" >> "$PG_HBA"
echo "host    replication   omnidb       ::1/128              trust" >> "$PG_HBA"
echo "host    all           omnidb       10.33.3.114/32       trust" >> "$PG_HBA"
echo "host    replication   omnidb       10.33.3.114/32       trust" >> "$PG_HBA"
echo "host    all           omnidb       10.33.3.115/32       trust" >> "$PG_HBA"
echo "host    replication   omnidb       10.33.3.115/32       trust" >> "$PG_HBA"

# Append to pg_hba.conf to add password auth:
echo "host    all           all          all                  md5" >> "$PG_HBA"

# Restart so that all new config is loaded:
systemctl restart postgresql-10

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS' SUPERUSER;

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
