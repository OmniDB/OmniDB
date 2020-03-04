#!/bin/bash

VERSION=2.17.0
ARCH=debian-amd64

echo "Installing OmniDB dependencies..."
pip install pip --upgrade
pip install setuptools --upgrade
pip install -r ~/OmniDB/requirements.txt --upgrade
pip uninstall paramiko -y
pip install -r ~/OmniDB/OmniDB/deploy/requirements_for_deploy_app.txt --upgrade
echo "Done."

echo "Installing NodeJS modules..."
cd ~/OmniDB/omnidb_app
npm install --unsafe-perm
echo "Done."

echo "Installing electron-packager..."
npm install electron-packager -g
echo "Done."

cd ~/OmniDB/OmniDB

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf deploy/packages
echo "Done."

echo -n "Switching to Release Mode..."
sed -i -e 's/DEV_MODE = True/DEV_MODE = False/g' OmniDB/custom_settings.py
echo "Done."

echo -n "Switching to Desktop Mode... "
sed -i -e 's/DESKTOP_MODE = False/DESKTOP_MODE = True/g' OmniDB/custom_settings.py
echo "Done."

echo "Generating server bundles... "
pyinstaller OmniDB-lin.spec
echo "Done."

echo -n "Organizing server bundles..."
rm -rf build
mkdir deploy/packages
cp dist/omnidb-config/omnidb-config dist/omnidb-server/omnidb-config-server
chmod 777 dist/omnidb-server/OmniDB_app/static/temp/
chmod 777 dist/omnidb-server/OmniDB_app/static/plugins/
chmod 777 dist/omnidb-server/OmniDB_app/plugins/
chmod 777 dist/omnidb-server/OmniDB_app/plugins/temp_loaded/
rm -rf ~/OmniDB/omnidb_app/omnidb-server
mv dist/omnidb-server ~/OmniDB/omnidb_app
rm -rf dist
echo "Done."

echo "Generating GUI bundles..."
cd ~/OmniDB/omnidb_app
./buildgui.sh
cd omnidb-app-linux-x64
rm LICENSE* version
echo "Done."

echo -n "Organizing GUI bundles..."
cd ~/OmniDB/OmniDB
mv ~/OmniDB/omnidb_app/omnidb-app-linux-x64 deploy/packages/omnidb-app
echo "Done."

echo -n "Copying libgconf... "
cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
chmod 755 deploy/packages/omnidb-app/libgconf-2.so.4
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
cat > omnidb-app <<EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-app/ /opt/omnidb-app/omnidb-app \$@
EOF
chmod 777 omnidb-app
ln -s /opt/omnidb-app/omnidb-config-app .
cd ../..
mkdir -p usr/share
cp -r ../../icons usr/share/
mkdir -p usr/share/applications/
cat > usr/share/applications/omnidb-app.desktop <<EOF
[Desktop Entry]
Name=OmniDB
Comment=OmniDB
Exec="/usr/bin/omnidb-app"
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
 Server package includes web server and requires a web browser to be used. Ideal for network and server usage.
 App package includes everything, even a simple web browser.
 Plugin package includes a PostgreSQL plugin to enable PLpgSQL function debugger.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cat > DEBIAN/postinst << EOF
#!/bin/bash
chmod 777 /opt/omnidb-app/resources/app/omnidb-server/OmniDB_app/static/temp/
chmod 777 /opt/omnidb-app/resources/app/omnidb-server/OmniDB_app/static/plugins/
chmod 777 /opt/omnidb-app/resources/app/omnidb-server/OmniDB_app/plugins/
chmod 777 /opt/omnidb-app/resources/app/omnidb-server/OmniDB_app/plugins/temp_loaded/
EOF
chmod 755 DEBIAN/postinst
cd ..
dpkg -b omnidb-app_$VERSION-$ARCH
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-app_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux app packages for OmniDB version $VERSION architecture $ARCH were successfully created."
