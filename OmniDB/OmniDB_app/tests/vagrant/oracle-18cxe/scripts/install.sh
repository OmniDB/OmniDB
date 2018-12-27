#!/bin/bash
#
# LICENSE UPL 1.0
#
# Copyright (c) 1982-2018 Oracle and/or its affiliates. All rights reserved.
#
# Since: July, 2018
# Author: gerald.venzl@oracle.com
# Description: Installs Oracle database software
#
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
#

echo 'INSTALLER: Started up'

# get up to date
yum upgrade -y

echo 'INSTALLER: System updated'

# fix locale warning
yum reinstall -y glibc-common
echo LANG=en_US.utf-8 >> /etc/environment
echo LC_ALL=en_US.utf-8 >> /etc/environment

echo 'INSTALLER: Locale set'

# Install Oracle Database prereq and openssl packages
# (preinstall is pulled automatically with 18c XE rpm, but it
#  doesn't create /home/oracle unless it's installed separately)
yum install -y oracle-database-preinstall-18c openssl

echo 'INSTALLER: Oracle preinstall and openssl complete'

# set environment variables
echo "export ORACLE_BASE=/opt/oracle" >> /home/oracle/.bashrc && \
echo "export ORACLE_HOME=/opt/oracle/product/18c/dbhomeXE" >> /home/oracle/.bashrc && \
echo "export ORACLE_SID=XE" >> /home/oracle/.bashrc && \
echo "export PATH=\$PATH:\$ORACLE_HOME/bin" >> /home/oracle/.bashrc

echo 'INSTALLER: Environment variables set'

# Install Oracle
yum -y localinstall /vagrant/oracle-database-xe-18c-*.x86_64.rpm

echo 'INSTALLER: Oracle software installed'

# Auto generate ORACLE PWD if not passed on
export ORACLE_PWD=${ORACLE_PWD:-"`openssl rand -base64 8`1"}

# Create database
mv /etc/sysconfig/oracle-xe-18c.conf /etc/sysconfig/oracle-xe-18c.conf.original && \
cp /vagrant/ora-response/oracle-xe-18c.conf.tmpl /etc/sysconfig/oracle-xe-18c.conf && \
chmod g+w /etc/sysconfig/oracle-xe-18c.conf && \
sed -i -e "s|###ORACLE_CHARACTERSET###|$ORACLE_CHARACTERSET|g" /etc/sysconfig/oracle-xe-18c.conf && \
sed -i -e "s|###ORACLE_PWD###|$ORACLE_PWD|g" /etc/sysconfig/oracle-xe-18c.conf
su -l -c '/etc/init.d/oracle-xe-18c configure'

echo 'INSTALLER: Database created'

# enable global port for EM Express
su -l oracle -c 'sqlplus / as sysdba <<EOF
   EXEC DBMS_XDB_CONFIG.SETGLOBALPORTENABLED (TRUE);
   exit
EOF'

echo 'INSTALLER: Global EM Express port enabled'

# configure systemd to start oracle instance on startup
sudo systemctl daemon-reload
sudo systemctl enable oracle-xe-18c
sudo systemctl start oracle-xe-18c
echo "INSTALLER: Created and enabled oracle-xe-18c systemd's service"

sudo cp /vagrant/scripts/setPassword.sh /home/oracle/ && \
sudo chown oracle:oinstall /home/oracle/setPassword.sh && \
sudo chmod u+x /home/oracle/setPassword.sh

echo "INSTALLER: setPassword.sh file setup";

echo "ORACLE PASSWORD FOR SYS, SYSTEM AND PDBADMIN: $ORACLE_PWD";

echo "INSTALLER: Installation complete, database ready to use!";
