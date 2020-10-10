#!/bin/bash

cd tarbuild
docker build -t omnidb/tarbuild .
cd ..

cd debbuild
docker build -t omnidb/debbuild .
cd ..
