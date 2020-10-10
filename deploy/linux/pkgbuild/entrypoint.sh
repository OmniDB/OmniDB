#!/bin/bash

# Checking environment
echo "VERSION=$VERSION"


#######################################
# Preparing directory for omnidb-server
#######################################

# Extracting tar.gz
cd $HOME
cp /tmp/omnidb-server_$VERSION.tar.gz .
tar -xzvf omnidb-server_$VERSION.tar.gz
cp omnidb-server_$VERSION/omnidb-server .
rm -rf omnidb-server_$VERSION/ omnidb-server_$VERSION.tar.gz

# Creating directory structure
mkdir omnidb-server_$VERSION
cd omnidb-server_$VERSION/
mkdir -p opt/omnidb-server
mv $HOME/omnidb-server opt/omnidb-server/
mkdir -p usr/bin
cat > usr/bin/omnidb-server <<EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-server/ /opt/omnidb-server/omnidb-server \$@
EOF
chmod 755 usr/bin/omnidb-server
mkdir -p etc/systemd/system
cat > etc/systemd/system/omnidb.service << EOF
[Unit]
Description=OmniDB server daemon
After=network.target

[Service]
Type=forking
ExecStart=/bin/bash -c "/opt/omnidb-server/omnidb-server &"
RemainAfterExit=yes
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF
chmod 644 etc/systemd/system/omnidb.service
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
Description: OmniDB is a very flexible, secure and work-effective environment for multiple DBMS.
 Server package includes web server and requires a web browser to be used. Ideal for network and server usage.
 App package includes everything, even a simple web browser.
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
cd ..


####################################
# Preparing directory for omnidb-app
####################################

# Extracting tar.gz
cd $HOME
cp /tmp/omnidb-app_$VERSION.tar.gz .
tar -xzvf omnidb-app_$VERSION.tar.gz
mv omnidb-app_$VERSION omnidb-app
rm -rf omnidb-app_$VERSION.tar.gz

# Creating directory structure
mkdir omnidb-app_$VERSION
cd omnidb-app_$VERSION/
mkdir opt
mv $HOME/omnidb-app opt/
mkdir -p usr/bin
cat > usr/bin/omnidb-app <<EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-app/ /opt/omnidb-app/omnidb-app \$@
EOF
chmod 755 usr/bin/omnidb-app
mkdir -p usr/share
cd usr/share/
cp $HOME/icons.tar.gz .
tar -xzvf icons.tar.gz
rm icons.tar.gz
cd ../..
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
cat > DEBIAN/control << EOF
Package: omnidb-app
Version: $VERSION
Section: base
Priority: optional
Architecture: amd64
Installed-Size: $(du -s)
Maintainer: The OmniDB Team
Homepage: http://omnidb.org
Description: OmniDB is a very flexible, secure and work-effective environment for multiple DBMS.
 Server package includes web server and requires a web browser to be used. Ideal for network and server usage.
 App package includes everything, even a simple web browser.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cd ..


#########################
# Generating deb packages
#########################

dpkg -b omnidb-server_$VERSION
dpkg -b omnidb-app_$VERSION
mv omnidb*.deb /tmp/


#########################
# Generating rpm packages
#########################

fpm -s deb -t rpm omnidb-server_$VERSION.deb
fpm -s deb -t rpm omnidb-app_$VERSION.deb
mv omnidb*.rpm /tmp/
