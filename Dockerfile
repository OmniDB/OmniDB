FROM debian:stable-slim

ENV OMNIDB_VERSION=2.14.0
ENV SERVICE_USER=omnidb

WORKDIR /${SERVICE_USER}

RUN  adduser --system --home /${SERVICE_USER} --no-create-home ${SERVICE_USER} \
  && mkdir -p /${SERVICE_USER} \
  && chown -R ${SERVICE_USER}.root /${SERVICE_USER} \
  && chmod -R g+w /${SERVICE_USER} \
  && apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y wget dumb-init \
  && if [ ! -e '/bin/systemctl' ]; then ln -s /bin/echo /bin/systemctl; fi \
  && rm -rf /var/lib/apt/lists/*

RUN wget -q https://omnidb.org/dist/${OMNIDB_VERSION}/omnidb-server_${OMNIDB_VERSION}-debian-amd64.deb \
  && dpkg -i omnidb-server_${OMNIDB_VERSION}-debian-amd64.deb \
  && rm -rf omnidb-server_${OMNIDB_VERSION}-debian-amd64.deb

USER ${SERVICE_USER}
  
EXPOSE 8000
EXPOSE 25482

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
CMD ["omnidb-server", "-H", "0.0.0.0"]
