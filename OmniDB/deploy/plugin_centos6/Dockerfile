FROM centos:6
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

RUN yum -y update \
 && yum -y install epel-release \
 && yum install -y gcc gcc-c++ make git patch rpm-build \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-3.noarch.rpm \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-3.noarch.rpm \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-6-x86_64/pgdg-centos95-9.5-3.noarch.rpm \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-6-x86_64/pgdg-centos96-9.6-3.noarch.rpm \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-6-x86_64/pgdg-centos10-10-2.noarch.rpm \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-6-x86_64/pgdg-redhat11-11-2.noarch.rpm \
 && yum -y check-update \
 && yum -y install postgresql93 postgresql93-server postgresql93-libs postgresql93-contrib postgresql93-devel \
 && yum -y install postgresql94 postgresql94-server postgresql94-libs postgresql94-contrib postgresql94-devel \
 && yum -y install postgresql95 postgresql95-server postgresql95-libs postgresql95-contrib postgresql95-devel \
 && yum -y install postgresql96 postgresql96-server postgresql96-libs postgresql96-contrib postgresql96-devel \
 && yum -y install postgresql10 postgresql10-server postgresql10-libs postgresql10-contrib postgresql10-devel \
 && yum -y install postgresql11 postgresql11-server postgresql11-libs postgresql11-contrib postgresql11-devel

COPY clone.sh $HOME/
