#!/bin/bash

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

# Installing dependencies
apt-get -y install build-essential git bison flex libreadline-dev zlib1g-dev

# Cloning Postgres-XL repo
cd
git clone git://git.postgresql.org/git/postgres-xl.git
cd postgres-xl
git checkout XL_10_STABLE

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

# Creating data folder
mkdir /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
