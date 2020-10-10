FROM pyappbuild

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

ARG REPO="git://github.com/OmniDB/OmniDB"
ARG BRANCH="dev"
ARG VERSION="3.0.0"

ENV REPO=$REPO
ENV BRANCH=$BRANCH
ENV VERSION=$VERSION

COPY entrypoint.sh $HOME

ENTRYPOINT ["/root/entrypoint.sh"]
