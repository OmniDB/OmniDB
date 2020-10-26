FROM centos:7
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

RUN yum -y update \
 && yum -y install epel-release \
 && yum -y install gcc gcc-c++ make git patch rpm-build \
 && rpm -ivh https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
 && yum -y install postgresql94 postgresql94-server postgresql94-libs postgresql94-contrib postgresql94-devel \
 && yum -y install postgresql95 postgresql95-server postgresql95-libs postgresql95-contrib postgresql95-devel \
 && yum -y install postgresql96 postgresql96-server postgresql96-libs postgresql96-contrib postgresql96-devel \
 && yum -y install postgresql10 postgresql10-server postgresql10-libs postgresql10-contrib postgresql10-devel \
 && yum -y install postgresql11 postgresql11-server postgresql11-libs postgresql11-contrib postgresql11-devel \
 && yum -y install postgresql12 postgresql12-server postgresql12-libs postgresql12-contrib postgresql12-devel

COPY clone.sh $HOME/
