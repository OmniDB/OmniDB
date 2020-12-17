FROM python:latest

LABEL maintainer="OmniDB team"

ARG OMNIDB_VERSION=3.0.3b

SHELL ["/bin/bash", "-c"]

USER root

RUN addgroup --system omnidb \
    && adduser --system omnidb --ingroup omnidb \
    && apt-get update \
    && apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev vim -y

USER omnidb:omnidb
ENV HOME /home/omnidb
WORKDIR ${HOME}

RUN wget https://github.com/OmniDB/OmniDB/archive/${OMNIDB_VERSION}.tar.gz \
    && tar -xvzf ${OMNIDB_VERSION}.tar.gz \
    && mv OmniDB-${OMNIDB_VERSION} OmniDB

WORKDIR ${HOME}/OmniDB

RUN pip install -r requirements.txt

WORKDIR ${HOME}/OmniDB/OmniDB

RUN sed -i "s/LISTENING_ADDRESS    = '127.0.0.1'/LISTENING_ADDRESS    = '0.0.0.0'/g" config.py \
    && python omnidb-server.py --init \
    && python omnidb-server.py --dropuser=admin

EXPOSE 8000

CMD python omnidb-server.py
