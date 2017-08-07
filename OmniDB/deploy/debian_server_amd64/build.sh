#!/bin/bash

VERSION=2.0.3
ARCH=debian-amd64

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
echo "Done"

echo "Generating deb packages... "
mv omnidb-server_$VERSION-$ARCH omnidb-server
mkdir -p omnidb-server_$VERSION-$ARCH
cd omnidb-server_$VERSION-$ARCH
mkdir opt
mv ../omnidb-server opt/
mkdir -p usr/bin
cd usr/bin
ln -s /opt/omnidb-server/omnidb-server .
ln -s /opt/omnidb-server/omnidb-config-server .
cd ../..
mkdir DEBIAN
cat > DEBIAN/control <<EOF
Package: omnidb-server
Version: $VERSION
Section: base
Priority: optional
Architecture: amd64
Installed-Size: $(du -s)
Maintainer: The OmniDB Team
Homepage: http://omnidb.org
Description: OmniDB is a web tool that simplifies database management focusing on interactivity, designed to be powerful and lightweight.
 Server package includes web server and requires a web browser to be used. Ideal for network and server usage.
 App package includes everything, even a simple web browser.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cd ..
dpkg -b omnidb-server_$VERSION-$ARCH
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
