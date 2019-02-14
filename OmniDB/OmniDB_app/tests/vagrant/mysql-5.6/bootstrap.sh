#!/bin/sh -e

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=omnidb
APP_DB_PASS=omnidb

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=omnidb_tests

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

# Installing dependencies
apt-get -y install software-properties-common dirmngr

REPO_APT_SOURCE=/etc/apt/sources.list.d/mysql.list
if [ ! -f "$REPO_APT_SOURCE" ]
then
  # Add MySQL apt repo:
  echo "deb http://repo.mysql.com/apt/debian/ jessie mysql-5.6" >> "$REPO_APT_SOURCE"

  # Add MySQL repo key:
  #apt-key adv --no-tty --keyserver pgp.mit.edu --recv-keys 5072E1F5
  apt-key adv --no-tty --recv-keys 5072E1F5
fi

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

apt-get -y install mysql-server --allow-unauthenticated

sed -i -e '/bind-address/s/^/#/g' /etc/mysql/mysql.conf.d/mysqld.cnf

systemctl restart mysql

mysql -e "create database ${APP_DB_NAME};"
mysql -e "create user ${APP_DB_USER} identified by '${APP_DB_PASS}';"
mysql -e "grant all privileges on ${APP_DB_NAME}.* to ${APP_DB_USER};"
mysql -e "flush privileges;"

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created MySQL dev virtual machine."
echo ""
