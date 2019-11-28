FROM debian:stable-slim
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

RUN apt-get update \
 && apt-get -y install wget gnupg2 \
 && echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > "/etc/apt/sources.list.d/pgdg.list" \
 && wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add - \
 && apt-get update

ENV PG_VERSION=9.4
ENV PG_PORT=5494
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

ENV PG_VERSION=9.5
ENV PG_PORT=5495
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

ENV PG_VERSION=9.6
ENV PG_PORT=5496
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

ENV PG_VERSION=10
ENV PG_PORT=5410
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

ENV PG_VERSION=11
ENV PG_PORT=5411
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

ENV PG_VERSION=12
ENV PG_PORT=5412
ENV PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
ENV PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
ENV PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

RUN apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" \
 && sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF" \
 && sed -i "s/port = 5432/port = $PG_PORT/" "$PG_CONF" \
 && echo "host all all all md5" >> "$PG_HBA" \
 && echo "client_encoding = utf8" >> "$PG_CONF" \
 && echo "max_replication_slots = 10" >> "$PG_CONF" \
 && echo "wal_level = logical" >> "$PG_CONF"

USER postgres
ENV HOME /var/lib/postgresql
WORKDIR /var/lib/postgresql
SHELL ["/bin/bash", "-c"]

COPY dellstore2-normal-1.0.tar.gz $HOME/
COPY restore.sh $HOME/
