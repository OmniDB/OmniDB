FROM centos:7
MAINTAINER William Ivanski <william.ivanski@gmail.com>

USER root
ENV HOME /root
WORKDIR /root
SHELL ["/bin/bash", "-c"]

ENV PYTHON_VERSION=3.6.5

RUN yum install -y gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel rpm-build wget \
 && git clone --depth 1 https://github.com/pyenv/pyenv.git ~/.pyenv \
 && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
 && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
 && echo 'eval "$(pyenv init -)"' >> ~/.bashrc \
 && source ~/.bashrc \
 && env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install $PYTHON_VERSION \
 && pyenv global $PYTHON_VERSION

COPY clone.sh $HOME/
