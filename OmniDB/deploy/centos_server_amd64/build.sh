#!/bin/sh -e

VERSION=2.0.2
ARCH=centos-amd64

cd ~/OmniDB/OmniDB

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf deploy/packages
echo "Done."

echo "Generating bundles... "
pyinstaller OmniDB.spec
echo "Done."

echo -n "Organizing bundles..."
rm -rf build
mkdir deploy/packages
cp dist/omnidb-config/omnidb-config dist/omnidb-server/omnidb-config-server
mv dist/omnidb-server deploy/packages
rm -rf dist
echo "Done."

echo -n "Renaming bundles... "
mv deploy/packages/omnidb-server deploy/packages/omnidb-server_$VERSION-$ARCH
echo "Done."

echo "Generating tar.gz packages... "
cd deploy/packages
tar -czvf omnidb-server_$VERSION-$ARCH.tar.gz omnidb-server_$VERSION-$ARCH
cd ..
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
