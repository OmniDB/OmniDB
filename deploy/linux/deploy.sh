#!/bin/bash

docker run -e REPO="git://github.com/OmniDB/OmniDB" -e VERSION="3.0.1" -v $PWD:/tmp --rm omnidb/tarbuild
docker run -e VERSION="3.0.1" -v $PWD:/tmp --rm omnidb/pkgbuild

sudo chown $USER:$USER *.tar.gz
sudo chown $USER:$USER *.deb
sudo chown $USER:$USER *.rpm
