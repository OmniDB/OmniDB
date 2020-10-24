#!/bin/bash

cd tarbuild
docker build -t omnidb/tarbuild .
cd ..

cd pkgbuild
docker build -t omnidb/pkgbuild .
cd ..
