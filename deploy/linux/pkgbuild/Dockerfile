FROM debian:jessie-slim

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update \
 && apt-get -y install rubygems ruby-dev build-essential rpm \
 && gem install fpm

ARG VERSION="3.0.0"

ENV VERSION=$VERSION

COPY icons.tar.gz $HOME
COPY entrypoint.sh $HOME

ENTRYPOINT ["/root/entrypoint.sh"]
