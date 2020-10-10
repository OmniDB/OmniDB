#!/bin/bash

docker run -e REPO="git://github.com/rafaelthca/OmniDB" -v $PWD:/tmp --rm omnidb/tarbuild
