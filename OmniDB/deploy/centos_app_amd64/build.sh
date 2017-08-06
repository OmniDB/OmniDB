#!/bin/sh -e

VERSION=2.0.3
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
cp dist/omnidb-config/omnidb-config dist/omnidb-app/omnidb-config-app
mv dist/omnidb-app deploy/packages
rm -rf dist
echo "Done."

echo -n "Copying cefpython files... "
cp -r "$HOME/.pyenv/versions/3.5.2/lib/python3.5/site-packages/cefpython3" deploy/packages/omnidb-app
echo "Done."

echo -n "Copying libgconf... "
if [ $ARCH == "centos-amd64" ]
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
if [ $ARCH == "centos-amd64" ]
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
if [ $ARCH == "centos-amd64" ]
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

echo -n "Cleaning... "
rm -rf omnidb-app_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux app packages for OmniDB version $VERSION architecture $ARCH were successfully created."
