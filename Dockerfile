FROM debian:stable-slim

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN wget https://omnidb.org/dist/2.5.0/omnidb-server_2.5.0-debian-amd64.deb

RUN dpkg -i /app/omnidb-server_2.5.0-debian-amd64.deb

EXPOSE 8000

CMD ["omnidb-server"]
