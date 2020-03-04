#!/bin/bash

VERSION=2.17.0
ARCH=debian-amd64

echo "Installing OmniDB dependencies..."
pip install pip --upgrade
pip install setuptools --upgrade
pip install -r ~/OmniDB/requirements.txt --upgrade
pip uninstall paramiko -y
pip install -r ~/OmniDB/OmniDB/deploy/requirements_for_deploy_server.txt --upgrade
echo "Done"

cd ~/OmniDB/OmniDB

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf deploy/packages
echo "Done."

echo -n "Switching to Release Mode..."
sed -i -e 's/DEV_MODE = True/DEV_MODE = False/g' OmniDB/custom_settings.py
echo "Done."

echo -n "Replacing line-end char for SQLite backward compatibility..."
sed -i -e 's/char(10)/x\x270a\x27/g' OmniDB/migrations/*.sql
echo "Done"

echo "Generating bundles... "
pyinstaller OmniDB-lin.spec
echo "Done."

echo -n "Organizing bundles..."
rm -rf build
mkdir deploy/packages
cp dist/omnidb-config/omnidb-config dist/omnidb-server/omnidb-config-server
mv dist/omnidb-server deploy/packages
chmod 777 deploy/packages/omnidb-server/OmniDB_app/static/temp/
chmod 777 deploy/packages/omnidb-server/OmniDB_app/static/plugins/
chmod 777 deploy/packages/omnidb-server/OmniDB_app/plugins/
chmod 777 deploy/packages/omnidb-server/OmniDB_app/plugins/temp_loaded/
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
cat > omnidb-server <<EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-server/ /opt/omnidb-server/omnidb-server \$@
EOF
chmod 777 omnidb-server
ln -s /opt/omnidb-server/omnidb-config-server .
cd ../..
mkdir -p etc
cp opt/omnidb-server/omnidb.conf etc/
mkdir -p etc/systemd/system
cd etc/systemd/system
cat > omnidb.service << EOF
[Unit]
Description=OmniDB server daemon
After=network.target

[Service]
Type=forking
ExecStart=/bin/bash -c "/opt/omnidb-server/omnidb-server -c /etc/omnidb.conf &"
RemainAfterExit=yes
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF
chmod 644 omnidb.service
cd ../../..
mkdir DEBIAN
cat > DEBIAN/control << EOF
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
 Plugin package includes a PostgreSQL plugin to enable PLpgSQL function debugger.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cat > DEBIAN/preinst << EOF
#!/bin/bash
if [ -f /etc/systemd/system/omnidb.service ]; then
  systemctl is-active --quiet omnidb
  if [ $? -eq 0 ]; then
    systemctl stop omnidb
  fi
fi
EOF
chmod 755 DEBIAN/preinst
cat > DEBIAN/postinst << EOF
#!/bin/bash
chmod 777 /opt/omnidb-server/OmniDB_app/static/temp/
chmod 777 /opt/omnidb-server/OmniDB_app/static/plugins/
chmod 777 /opt/omnidb-server/OmniDB_app/plugins/
chmod 777 /opt/omnidb-server/OmniDB_app/plugins/temp_loaded/
systemctl daemon-reload
systemctl enable omnidb
systemctl start omnidb
EOF
chmod 755 DEBIAN/postinst
cat > DEBIAN/prerm << EOF
#!/bin/bash
systemctl is-active --quiet omnidb
if [ $? -eq 0 ]; then
  systemctl stop omnidb
fi
systemctl is-enabled --quiet omnidb
if [ $? -eq 0 ]; then
  systemctl disable omnidb
fi
EOF
chmod 755 DEBIAN/prerm
cat > DEBIAN/postrm << EOF
#!/bin/bash
systemctl daemon-reload
systemctl reset-failed
EOF
chmod 755 DEBIAN/postrm
cat > DEBIAN/conffiles << EOF
/etc/omnidb.conf
EOF
chmod 755 DEBIAN/conffiles
cd ..
dpkg -b omnidb-server_$VERSION-$ARCH
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
