FROM python:latest

LABEL maintainer="OmniDB team"

ENV SERVICE_USER=omnidb

WORKDIR /${SERVICE_USER}

ADD ./OmniDB /${SERVICE_USER}
ADD requirements.txt /tmp
ADD entrypoint.sh /entrypoint.sh

RUN  adduser --system --home /${SERVICE_USER} --no-create-home ${SERVICE_USER} --uid 110 \
  && mkdir -p /${SERVICE_USER} \
  && chown -R ${SERVICE_USER}.root /${SERVICE_USER} \
  && chmod -R g+w /${SERVICE_USER} \
  && apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y python3-pip libldap2-dev libsasl2-dev \
  && pip3 install -r /tmp/requirements.txt \
  && apt remove -y libldap2-dev libsasl2-dev \
  && rm -rf /var/lib/apt/lists/*

USER ${SERVICE_USER}
  
EXPOSE 8080
EXPOSE 25482

ENTRYPOINT [ "/entrypoint.sh"]
CMD ["python3", "omnidb-server.py"]
