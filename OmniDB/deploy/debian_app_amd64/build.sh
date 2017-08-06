#!/bin/bash

VERSION=2.0.2
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
cp dist/omnidb-config/omnidb-config dist/omnidb-server/omnidb-config-app
mv dist/omnidb-app deploy/packages
rm -rf dist
echo "Done."

echo -n "Copying cefpython files... "
cp -r "$HOME/.pyenv/versions/3.5.2/lib/python3.5/site-packages/cefpython3" deploy/packages/omnidb-app
echo "Done."

echo -n "Copying libgconf... "
if [ $ARCH == "debian-amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
else
	cp /usr/lib/i386-linux-gnu/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib/i386-linux-gnu/libgconf-2.so.4 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
fi
chmod 755 deploy/packages/omnidb-app/libgconf-2.so.4
chmod 755 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
echo "Done."

echo -n "Copying libxcb... "
if [ $ARCH == "debian-amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libxcb.so.1 deploy/packages/omnidb-app/libxcb.so.1
	cp /usr/lib/x86_64-linux-gnu/libxcb.so.1 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
else
	cp /usr/lib/i386-linux-gnu/libxcb.so.1 deploy/packages/omnidb-app/libxcb.so.1
	cp /usr/lib/i386-linux-gnu/libxcb.so.1 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
fi
chmod 755 deploy/packages/omnidb-app/libxcb.so.1
chmod 755 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
echo "Done."

echo -n "Copying libXss... "
if [ $ARCH == "debian-amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libXss.so.1 deploy/packages/omnidb-app/libXss.so.1
	cp /usr/lib/x86_64-linux-gnu/libXss.so.1 deploy/packages/omnidb-app/cefpython3/libXss.so.1
else
	cp /usr/lib/i386-linux-gnu/libXss.so.1 deploy/packages/omnidb-app/libXss.so.1
	cp /usr/lib/i386-linux-gnu/libXss.so.1 deploy/packages/omnidb-app/cefpython3/libXss.so.1
fi
chmod 755 deploy/packages/omnidb-app/libXss.so.1
chmod 755 deploy/packages/omnidb-app/cefpython3/libXss.so.1
echo "Done."

echo -n "Renaming bundles... "
mv deploy/packages/omnidb-app deploy/packages/omnidb-app_$VERSION-$ARCH
echo "Done."

echo "Generating tar.gz packages... "
cd deploy/packages
tar -czvf omnidb-app_$VERSION-$ARCH.tar.gz omnidb-app_$VERSION-$ARCH
echo "Done"

echo "Generating deb packages... "
mv omnidb-app_$VERSION-$ARCH omnidb-app
mkdir -p omnidb-app_$VERSION-$ARCH
cd omnidb-app_$VERSION-$ARCH
mkdir opt
mv ../omnidb-app opt/
mkdir -p usr/bin
cd usr/bin
ln -s /opt/omnidb-app/omnidb-app .
ln -s /opt/omnidb-app/omnidb-config-app .
cd ../..
mkdir -p usr/share
cp -r ../../icons usr/share/
mkdir -p usr/share/applications/
cat > usr/share/applications/omnidb-app.desktop <<EOF
[Desktop Entry]
Name=OmniDB
Comment=OmniDB
Exec="/opt/omnidb-app/omnidb-app"
Terminal=false
Type=Application
Icon=omnidb
Categories=Development
EOF
mkdir DEBIAN
cat > DEBIAN/control <<EOF
Package: omnidb-app
Version: $VERSION
Section: base
Priority: optional
Architecture: amd64
Installed-Size: $(du -s)
Maintainer: The OmniDB Team
Homepage: http://omnidb.org
Description: OmniDB is a web tool that simplifies database management focusing on interactivity, designed to be powerful and lightweight.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cd ..
dpkg -b omnidb-app_$VERSION-$ARCH
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux app packages for OmniDB version $VERSION architecture $ARCH were successfully created."
