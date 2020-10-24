#!/bin/bash

if [ $1 = "gtm" ]
then

  # Initializing GTM
  su - postgres -c "/usr/local/pgsql/bin/initgtm -Z gtm -D /usr/local/pgsql/data"

else

  # Initializing node
  su - postgres -c "/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data --nodename $(hostname)"

  PG_CONF="/usr/local/pgsql/data/postgresql.conf"
  PG_HBA="/usr/local/pgsql/data/pg_hba.conf"
  PG_DIR="/usr/local/pgsql/data"

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
  echo "pooler_port = $2" >> "$PG_CONF"
  echo "gtm_host = '$3'" >> "$PG_CONF"
  echo "gtm_port = 6666" >> "$PG_CONF"

  # XL specific authentication
  echo "local   all           postgres                          trust" >> "$PG_HBA"
  echo "host    all           postgres     127.0.0.1/32         trust" >> "$PG_HBA"
  echo "host    all           postgres     ::1/128              trust" >> "$PG_HBA"
  echo "host    all           postgres     $4         trust" >> "$PG_HBA"

  # Append to pg_hba.conf to add password auth:
  echo "host    all           all          all                  md5" >> "$PG_HBA"

fi
