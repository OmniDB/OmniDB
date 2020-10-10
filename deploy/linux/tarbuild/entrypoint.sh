#!/bin/bash

# Cloning repo
git clone $REPO --depth 1 -b $BRANCH OmniDB

# Installing dependencies
cd OmniDB
pip install -r requirements.txt

# Building server
cd OmniDB/OmniDB
pyinstaller OmniDB-lin.spec
mv dist/omnidb-server $HOME
rm -rf build dist
cd $HOME
mkdir omnidb-server_$VERSION
cp omnidb-server omnidb-server_$VERSION/
tar -czvf omnidb-server_$VERSION.tar.gz omnidb-server_$VERSION/
mv omnidb-server_$VERSION.tar.gz /tmp/

# Building app
cd $HOME
curl -LO https://dl.nwjs.io/v0.38.4/nwjs-v0.38.4-linux-x64.tar.gz
tar -xzvf nwjs-v0.38.4-linux-x64.tar.gz
mv nwjs-v0.38.4-linux-x64 omnidb-app_$VERSION
cd omnidb-app_$VERSION
mkdir omnidb-server
cp $HOME/omnidb-server ./omnidb-server/
cp $HOME/OmniDB/deploy/app/* .
mv nw omnidb-app
cd $HOME
tar -czvf omnidb-app_$VERSION.tar.gz omnidb-app_$VERSION/
mv omnidb-app_$VERSION.tar.gz /tmp/
