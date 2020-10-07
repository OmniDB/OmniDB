FROM oraclelinux:7
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

COPY oracle-database-xe-18c-*.x86_64.rpm $HOME/
COPY oracle-xe-18c.conf.tmpl $HOME/
COPY listener.ora $HOME/
COPY tnsnames.ora $HOME/

ENV ORACLE_DOCKER_INSTALL=true
ENV ORACLE_CHARACTERSET="AL32UTF8"
ENV ORACLE_PASSWORD="omnidb"

RUN yum upgrade -y \
 && yum reinstall -y glibc-common \
 && echo "LANG=en_US.utf-8" >> /etc/environment \
 && echo "LC_ALL=en_US.utf-8" >> /etc/environment \
 && yum install -y oracle-database-preinstall-18c openssl \
 && echo "export ORACLE_BASE=/opt/oracle" >> /home/oracle/.bashrc \
 && echo "export ORACLE_HOME=/opt/oracle/product/18c/dbhomeXE" >> /home/oracle/.bashrc \
 && echo "export ORACLE_SID=XE" >> /home/oracle/.bashrc \
 && echo "export PATH=\$PATH:\$ORACLE_HOME/bin" >> /home/oracle/.bashrc \
 && yum -y localinstall oracle-database-xe-18c-*.x86_64.rpm \
 && export ORACLE_PWD=$ORACLE_PASSWORD \
 && mv /etc/sysconfig/oracle-xe-18c.conf /etc/sysconfig/oracle-xe-18c.conf.original \
 && cp oracle-xe-18c.conf.tmpl /etc/sysconfig/oracle-xe-18c.conf \
 && chmod g+w /etc/sysconfig/oracle-xe-18c.conf \
 && sed -i -e "s|###ORACLE_CHARACTERSET###|$ORACLE_CHARACTERSET|g" /etc/sysconfig/oracle-xe-18c.conf \
 && sed -i -e "s|###ORACLE_PWD###|$ORACLE_PWD|g" /etc/sysconfig/oracle-xe-18c.conf \
 && su -l -c '/etc/init.d/oracle-xe-18c configure' \
 && cp -f listener.ora tnsnames.ora /opt/oracle/product/18c/dbhomeXE/network/admin/ \
 && chmod o+r /opt/oracle/product/18c/dbhomeXE/network/admin/listener.ora /opt/oracle/product/18c/dbhomeXE/network/admin/tnsnames.ora \
 && rm -f oracle-database-xe-18c-*.x86_64.rpm oracle-xe-18c.conf.tmpl listener.ora tnsnames.ora
