FROM debian:jessie-slim
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
 && apt install -y wget \
 && echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
 && wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add - \
 && apt-get update -y \
 && apt-get -y install build-essential git postgresql-server-dev-9.4 postgresql-server-dev-9.5 postgresql-server-dev-9.6 postgresql-server-dev-10 postgresql-server-dev-11 postgresql-server-dev-12 libpq-dev

COPY clone.sh $HOME/
