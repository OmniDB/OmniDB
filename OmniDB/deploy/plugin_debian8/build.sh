#!/bin/bash

VERSION=2.17.0
ARCH=debian-amd64

cd ~/OmniDB/omnidb_plugin

echo -n "Cleaning... "
rm -f *.o
echo "Done."

echo "Compiling for 9.4... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/9.4/server
gcc -fPIC -o omnidb_plugin_94.so omnidb_plugin.o -lpq -shared
echo "Done."

echo "Compiling for 9.5... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/9.5/server
gcc -fPIC -o omnidb_plugin_95.so omnidb_plugin.o -lpq -shared
echo "Done."

echo "Compiling for 9.6... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/9.6/server
gcc -fPIC -o omnidb_plugin_96.so omnidb_plugin.o -lpq -shared
echo "Done."

echo "Compiling for 10... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/10/server
gcc -fPIC -o omnidb_plugin_10.so omnidb_plugin.o -lpq -shared
echo "Done."

echo "Compiling for 11... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/11/server
gcc -fPIC -o omnidb_plugin_11.so omnidb_plugin.o -lpq -shared
echo "Done."

echo "Compiling for 12... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/12/server
gcc -fPIC -o omnidb_plugin_12.so omnidb_plugin.o -lpq -shared
echo "Done."

echo -n "Cleaning... "
rm -f *.o
echo "Done."

echo -n "Organizing bundle..."
cd ~/OmniDB/OmniDB
mkdir deploy/packages
cp -r ~/OmniDB/omnidb_plugin deploy/packages/
echo "Done."

echo -n "Renaming bundle... "
mv deploy/packages/omnidb_plugin deploy/packages/omnidb-plugin_$VERSION-$ARCH
echo "Done."

echo "Generating tar.gz package... "
cd deploy/packages
tar -czvf omnidb-plugin_$VERSION-$ARCH.tar.gz omnidb-plugin_$VERSION-$ARCH
echo "Done"

echo "Generating deb package... "
mv omnidb-plugin_$VERSION-$ARCH omnidb-plugin
mkdir -p omnidb-plugin_$VERSION-$ARCH
cd omnidb-plugin_$VERSION-$ARCH
mkdir opt
mv ../omnidb-plugin opt/
mkdir DEBIAN
cat > DEBIAN/control <<EOF
Package: omnidb-plugin
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
 Plugin package includes a PostgreSQL plugin to enable PLpgSQL function debugger.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cd ..
dpkg -b omnidb-plugin_$VERSION-$ARCH
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-plugin_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
