#!/bin/sh -e

# Edit the following to change the version of PostgreSQL that is installed
PG_VERSION=9.5

# Edit the following to change the local port PostgreSQL port 5432 will be mapped to
PG_LOCAL_PORT=5407

###########################################################
# Changes below this line are probably not necessary
###########################################################
print_db_usage () {
  echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: $PG_LOCAL_PORT)"
  echo ""
  echo "Admin access to postgres user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo ""
  echo "psql access to app database user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo "  psql -h localhost"
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

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

# Installing dependencies
apt-get -y install build-essential git bison flex libreadline-dev zlib1g-dev

# Cloning Postgres-XL repo
cd
git clone git://git.postgresql.org/git/postgres-xl.git
cd postgres-xl
git checkout XL9_5_STABLE

# Compiling and installing
./configure
make
make install
cd contrib
make
make install

# Adding postgres user
echo "PATH=/usr/local/pgsql/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games" > /etc/environment
useradd -m -s /bin/bash -U postgres

# Creating folder datanode
mkdir /usr/local/pgsql/data_datanode_2
chown postgres /usr/local/pgsql/data_datanode_2

# Initializing datanode
su - postgres -c "/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data_datanode_2 --nodename datanode_2"

PG_CONF="/usr/local/pgsql/data_datanode_2/postgresql.conf"
PG_HBA="/usr/local/pgsql/data_datanode_2/pg_hba.conf"
PG_DIR="/usr/local/pgsql/data_datanode_2"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Other XL specific settings
echo "log_destination = 'stderr'" >> "$PG_CONF"
echo "logging_collector = on" >> "$PG_CONF"
echo "log_directory = 'pg_log'" >> "$PG_CONF"
echo "max_connections = 100" >> "$PG_CONF"
echo "hot_standby = off" >> "$PG_CONF"
echo "pooler_port = 40102" >> "$PG_CONF"

# XL specific authentication
echo "local   all           postgres                          trust" >> "$PG_HBA"
echo "host    all           postgres     127.0.0.1/32         trust" >> "$PG_HBA"
echo "host    all           postgres     ::1/128              trust" >> "$PG_HBA"
echo "host    all           postgres     192.168.56.105/32    trust" >> "$PG_HBA"
echo "host    all           postgres     192.168.56.106/32    trust" >> "$PG_HBA"

# Append to pg_hba.conf to add password auth:
echo "host    all           all          all                  md5" >> "$PG_HBA"

# Starting coordinator
su - postgres -c "/usr/local/pgsql/bin/postgres --datanode -D /usr/local/pgsql/data_datanode_2 >logfile 2>&1 &"
sleep 30

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created PostgreSQL dev virtual machine."
echo ""
print_db_usage
