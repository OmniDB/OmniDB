FROM debian:stable-slim

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN wget -q https://omnidb.org/dist/2.14.0/omnidb-server_2.14.0-debian-amd64.deb \
 && dpkg -i /app/omnidb-server_2.14.0-debian-amd64.deb \
 && rm -rf omnidb-server_2.14.0-debian-amd64.deb

EXPOSE 8000
EXPOSE 25482

CMD ["omnidb-server"]
