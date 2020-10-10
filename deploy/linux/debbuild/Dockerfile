FROM debian:jessie-slim

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

ARG VERSION="3.0.0"

ENV VERSION=$VERSION

COPY entrypoint.sh $HOME

ENTRYPOINT ["/root/entrypoint.sh"]
