#!/bin/sh -e

VERSION=2.5.0
ARCH=fedora-amd64

echo "Installing OmniDB dependencies..."
pip install pip --upgrade
pip install -r ~/OmniDB/requirements.txt --upgrade
pip install -r ~/OmniDB/OmniDB/deploy/requirements_for_deploy_app.txt --upgrade
echo "Done"

cd ~/OmniDB/OmniDB

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf deploy/packages
echo "Done."

echo -n "Switching to Release Mode..."
sed -i -e 's/DEV_MODE = True/DEV_MODE = False/g' OmniDB/settings.py
echo "Done."

echo -n "Switching to Desktop Mode... "
sed -i -e 's/DESKTOP_MODE = False/DESKTOP_MODE = True/g' OmniDB/settings.py
echo "Done."

echo "Generating bundles... "
pyinstaller OmniDB-lin.spec
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
if [ $ARCH == "fedora-amd64" ]
then
	cp /usr/lib64/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib64/libgconf-2.so.4 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
else
	cp /usr/lib/libgconf-2.so.4 deploy/packages/omnidb-app/libgconf-2.so.4
	cp /usr/lib/libgconf-2.so.4 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
fi
chmod 755 deploy/packages/omnidb-app/libgconf-2.so.4
chmod 755 deploy/packages/omnidb-app/cefpython3/libgconf-2.so.4
echo "Done."

echo -n "Copying libxcb... "
if [ $ARCH == "fedora-amd64" ]
then
	cp /usr/lib64/libxcb.so.1 deploy/packages/omnidb-app/libxcb.so.1
	cp /usr/lib64/libxcb.so.1 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
    cp /usr/lib64/libxcb-dri3.so.0 deploy/packages/omnidb-app/libxcb-dri3.so.0
    cp /usr/lib64/libxcb-dri3.so.0 deploy/packages/omnidb-app/cefpython3/libxcb-dri3.so.0
    cp /usr/lib64/libxcb-shm.so.0 deploy/packages/omnidb-app/libxcb-shm.so.0
    cp /usr/lib64/libxcb-shm.so.0 deploy/packages/omnidb-app/cefpython3/libxcb-shm.so.0
else
	cp /usr/lib/libxcb.so.1 deploy/packages/omnidb-app/libxcb.so.1
	cp /usr/lib/libxcb.so.1 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
    cp /usr/lib/libxcb-dri3.so.0 deploy/packages/omnidb-app/libxcb-dri3.so.0
    cp /usr/lib/libxcb-dri3.so.0 deploy/packages/omnidb-app/cefpython3/libxcb-dri3.so.0
fi
chmod 755 deploy/packages/omnidb-app/libxcb.so.1
chmod 755 deploy/packages/omnidb-app/cefpython3/libxcb.so.1
chmod 755 deploy/packages/omnidb-app/libxcb-dri3.so.0
chmod 755 deploy/packages/omnidb-app/cefpython3/libxcb-dri3.so.0
chmod 755 deploy/packages/omnidb-app/libxcb-shm.so.0
chmod 755 deploy/packages/omnidb-app/cefpython3/libxcb-shm.so.0
echo "Done."

echo -n "Copying libXss... "
cp deploy/lib/libXss.so.1 deploy/packages/omnidb-app/libXss.so.1
cp deploy/lib/libXss.so.1 deploy/packages/omnidb-app/cefpython3/libXss.so.1
chmod 755 deploy/packages/omnidb-app/libXss.so.1
chmod 755 deploy/packages/omnidb-app/cefpython3/libXss.so.1
echo "Done."

echo -n "Copying libnss3... "
cp deploy/lib/libnss3.so deploy/packages/omnidb-app/libnss3.so
cp deploy/lib/libnss3.so deploy/packages/omnidb-app/cefpython3/libnss3.so
chmod 755 deploy/packages/omnidb-app/libnss3.so
chmod 755 deploy/packages/omnidb-app/cefpython3/libnss3.so
echo "Done."

echo -n "Copying libXtst... "
if [ $ARCH == "fedora-amd64" ]
then
        cp /usr/lib64/libXtst.so.6 deploy/packages/omnidb-app/libXtst.so.6
        cp /usr/lib64/libXtst.so.6 deploy/packages/omnidb-app/cefpython3/libXtst.so.6
else
        cp /usr/lib/libXtst.so.6 deploy/packages/omnidb-app/libXtst.so.6
        cp /usr/lib/libXtst.so.6 deploy/packages/omnidb-app/cefpython3/libXtst.so.6
fi
chmod 755 deploy/packages/omnidb-app/libXtst.so.6
chmod 755 deploy/packages/omnidb-app/cefpython3/libXtst.so.6
echo "Done."

echo -n "Renaming bundles... "
mv deploy/packages/omnidb-app deploy/packages/omnidb-app_$VERSION-$ARCH
echo "Done."

echo "Including OIC... "
cd deploy/packages/omnidb-app_$VERSION-$ARCH
cp ~/linux_x64/* .
ln -s libclntsh.so.11.1 libclntsh.so
ln -s libocci.so.11.1 libocci.so
cd ..
echo "Done"

echo "Generating tar.gz packages... "
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
Exec="/opt/omnidb-app/omnidb-app"
Terminal=false
Type=Application
Icon=omnidb
Categories=Development;
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
ln -s /opt/%{name}/%{name} %{buildroot}/%{_bindir}/%{name}
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
