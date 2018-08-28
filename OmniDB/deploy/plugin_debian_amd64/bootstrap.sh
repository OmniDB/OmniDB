#!/bin/bash

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  exit
fi

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > "$PG_REPO_APT_SOURCE"

  # Add PGDG repo key:
  wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

apt-get -y install build-essential git postgresql-server-dev-9.3 postgresql-server-dev-9.4 postgresql-server-dev-9.5 postgresql-server-dev-9.6 postgresql-server-dev-10 libpq-dev

# POSTGRESQL TESTING

PG_REPO_APT_SOURCE_TESTING=/etc/apt/sources.list.d/pgdg_testing.list
if [ ! -f "$PG_REPO_APT_SOURCE_TESTING" ]
then
  # Add PG apt repo testing:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg-testing main 11" > "$PG_REPO_APT_SOURCE_TESTING"
fi

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

apt-get -y install postgresql-server-dev-11 libpq-dev=11~beta3-1.pgdg80+1 libpq5=11~beta3-1.pgdg80+1

echo "Cloning OmniDB repo..."
rm -rf ~/OmniDB
git clone --depth 1 --branch dev https://github.com/OmniDB/OmniDB ~/OmniDB
echo "Done"

echo "Building..."
cd ~/OmniDB/OmniDB/deploy/plugin_debian_amd64/
./build.sh
echo "Done"
