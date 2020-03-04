#!/bin/sh -e

VERSION=2.17.0
ARCH=centos-amd64

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
cp /usr/lib64/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
chmod 755 deploy/packages/omnidb-app/libgconf-2.so.4
echo "Done."

echo -n "Copying libXss... "
cp deploy/lib/libXss.so.1 deploy/packages/omnidb-app/libXss.so.1
chmod 755 deploy/packages/omnidb-app/libXss.so.1
echo "Done."

echo -n "Copying libnss3... "
cp deploy/lib/libnss3.so deploy/packages/omnidb-app/libnss3.so
chmod 755 deploy/packages/omnidb-app/libnss3.so
echo "Done."

echo -n "Copying libXtst... "
cp /usr/lib64/libXtst.so.6 deploy/packages/omnidb-app/libXtst.so.6
chmod 755 deploy/packages/omnidb-app/libXtst.so.6
echo "Done."

echo -n "Renaming bundles... "
mv deploy/packages/omnidb-app deploy/packages/omnidb-app_$VERSION-$ARCH
echo "Done."

echo "Generating tar.gz packages... "
cd deploy/packages
tar -czvf omnidb-app_$VERSION-$ARCH.tar.gz omnidb-app_$VERSION-$ARCH
echo "Done"

echo "Generating rpm packages..."
mkdir omnidb-app
cd omnidb-app
mkdir -p BUILD RPMS SOURCES SPECS
cp ../omnidb-app_$VERSION-$ARCH.tar.gz SOURCES/
cp -r ../../icons SOURCES/
cat > SOURCES/omnidb-app.desktop <<EOF
[Desktop Entry]
Name=OmniDB
Comment=OmniDB
Exec="/usr/bin/omnidb-app"
Terminal=false
Type=Application
Icon=omnidb
Categories=Development;
EOF
cat > SOURCES/omnidb-app.sh <<EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-app/ /opt/omnidb-app/omnidb-app \$@
EOF

cat > SPECS/omnidb-app.spec <<EOF
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define _unpackaged_files_terminate_build 0
%define _topdir /root/OmniDB/OmniDB/deploy/packages/omnidb-app
%define _datadir /usr/share
%define _bindir /usr/bin
%define name omnidb-app
%define version $VERSION
%define arch $ARCH
%define longname %{name}_%{version}-%{arch}
%define configname omnidb-config-app
%define buildroot %{_topdir}/%{longname}-root

BuildRoot: %{buildroot}
BuildArch: x86_64
Summary: Application to manage multiple databases
License: MIT
Name: %{name}
Version: %{version}
Release: 0
Source: %{longname}.tar.gz
Prefix: /opt
Group: Development/Tools
Vendor: The OmniDB Team
AutoReqProv: no

%description
OmniDB is a web tool that simplifies database management focusing on interactivity, designed to be powerful and lightweight. OmniDB is supported by 2ndQuadrant (https://www.2ndquadrant.com)

%prep
%setup -n %{longname}

%build

%install
mkdir -p %{buildroot}/opt/%{name}
chmod 777 %{buildroot}/opt/%{name}
cp -r ./* %{buildroot}/opt/%{name}
mkdir -p %{buildroot}/%{_datadir}/applications
cp -r ../../SOURCES/icons %{buildroot}/%{_datadir}/
desktop-file-install --dir=%{buildroot}/%{_datadir}/applications ../../SOURCES/%{name}.desktop
mkdir -p %{buildroot}/%{_bindir}
cp ../../SOURCES/%{name}.sh %{buildroot}/%{_bindir}/%{name}
chmod 777 %{buildroot}/%{_bindir}/%{name}
ln -s /opt/%{name}/%{configname} %{buildroot}/%{_bindir}/%{configname}

%post
update-desktop-database

%files
%defattr(0777,root,root,0777)
/opt/%{name}
/opt/%{name}/*
%{_datadir}/icons/hicolor/128x128/apps/omnidb.png
%{_datadir}/icons/hicolor/16x16/apps/omnidb.png
%{_datadir}/icons/hicolor/24x24/apps/omnidb.png
%{_datadir}/icons/hicolor/256x256/apps/omnidb.png
%{_datadir}/icons/hicolor/32x32/apps/omnidb.png
%{_datadir}/icons/hicolor/48x48/apps/omnidb.png
%{_datadir}/icons/hicolor/512x512/apps/omnidb.png
%{_datadir}/icons/hicolor/64x64/apps/omnidb.png
%{_datadir}/icons/hicolor/96x96/apps/omnidb.png
%{_datadir}/applications/%{name}.desktop
%{_bindir}/%{name}
%{_bindir}/%{configname}
EOF

rpmbuild -v -bb --clean SPECS/omnidb-app.spec
cp RPMS/x86_64/omnidb-app-$VERSION-0.x86_64.rpm ../omnidb-app_$VERSION-$ARCH.rpm
cd ..
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-app_$VERSION-$ARCH omnidb-app
echo "Done"

cd ../..
echo "All Linux app packages for OmniDB version $VERSION architecture $ARCH were successfully created."
