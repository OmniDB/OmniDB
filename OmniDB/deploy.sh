VERSION=2.0.2

# amd64 or i386
ARCH=$1

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf packages
echo "Done."

echo "Generating bundles... "
pyinstaller OmniDB.spec
echo "Done."

echo -n "Organizing bundles..."
rm -rf build
mkdir packages
cp dist/omnidb-config/omnidb-config dist/omnidb-server/omnidb-config-server
cp dist/omnidb-config/omnidb-config dist/omnidb-app/omnidb-config-app
mv dist/omnidb-server packages
mv dist/omnidb-app packages
rm -rf dist
echo "Done."

echo -n "Copying cefpython files... "
cp -r "/usr/local/lib/python$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1).$(python3 --version | cut -d' ' -f2 | cut -d'.' -f2)/dist-packages/cefpython3" packages/omnidb-app/
echo "Done."

echo -n "Copying libgconf... "
if [ $ARCH == "amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 packages/omnidb-app/cefpython3/libgconf-2.so.4
else
	cp /usr/lib/i386-linux-gnu/libgconf-2.so.4 packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib/i386-linux-gnu/libgconf-2.so.4 packages/omnidb-app/cefpython3/libgconf-2.so.4
fi
chmod 755 packages/omnidb-app/libgconf-2.so.4
chmod 755 packages/omnidb-app/cefpython3/libgconf-2.so.4
echo "Done."

echo -n "Copying libxcb... "
if [ $ARCH == "amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libxcb.so.1 packages/omnidb-app/libxcb.so.1
	cp /usr/lib/x86_64-linux-gnu/libxcb.so.1 packages/omnidb-app/cefpython3/libxcb.so.1
else
	cp /usr/lib/i386-linux-gnu/libxcb.so.1 packages/omnidb-app/libxcb.so.1
	cp /usr/lib/i386-linux-gnu/libxcb.so.1 packages/omnidb-app/cefpython3/libxcb.so.1
fi
chmod 755 packages/omnidb-app/libxcb.so.1
chmod 755 packages/omnidb-app/cefpython3/libxcb.so.1
echo "Done."

echo -n "Copying libXss... "
if [ $ARCH == "amd64" ]
then
	cp /usr/lib/x86_64-linux-gnu/libXss.so.1 packages/omnidb-app/libXss.so.1
	cp /usr/lib/x86_64-linux-gnu/libXss.so.1 packages/omnidb-app/cefpython3/libXss.so.1
else
	cp /usr/lib/i386-linux-gnu/libXss.so.1 packages/omnidb-app/libXss.so.1
	cp /usr/lib/i386-linux-gnu/libXss.so.1 packages/omnidb-app/cefpython3/libXss.so.1
fi
chmod 755 packages/omnidb-app/libXss.so.1
chmod 755 packages/omnidb-app/cefpython3/libXss.so.1
echo "Done."

echo -n "Renaming bundles... "
mv packages/omnidb-server packages/omnidb-server_$VERSION-$ARCH
mv packages/omnidb-app packages/omnidb-app_$VERSION-$ARCH
echo "Done."

echo "Generating tar.gz packages... "
cd packages
tar -czvf omnidb-server_$VERSION-$ARCH.tar.gz omnidb-server_$VERSION-$ARCH
tar -czvf omnidb-app_$VERSION-$ARCH.tar.gz omnidb-app_$VERSION-$ARCH
cd ..
echo "Done"

echo "Generating deb packages... "
cd packages
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
Architecture: $ARCH
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
Architecture: $ARCH
Installed-Size: $(du -s)
Maintainer: The OmniDB Team
Homepage: http://omnidb.org
Description: OmniDB is a web tool that simplifies database management focusing on interactivity, designed to be powerful and lightweight.
 OmniDB is supported by 2ndQuadrant (http://www.2ndquadrant.com)
EOF
cd ..
dpkg -b omnidb-app_$VERSION-$ARCH
echo "Done"

#echo "Generating rpm packages..."
#alien -r omnidb-server_$VERSION-$ARCH.deb
#alien -r omnidb-app_$VERSION-$ARCH.deb
#echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH
rm -rf omnidb-app_$VERSION-$ARCH
echo "Done"

cd ..
echo "All Linux packages for OmniDB version $VERSION architecture $ARCH were successfully created."

