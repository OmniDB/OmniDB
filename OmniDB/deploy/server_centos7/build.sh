#!/bin/sh -e

VERSION=2.17.0
ARCH=centos-amd64

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

echo "Generating rpm packages..."
mkdir omnidb-server
cd omnidb-server
mkdir -p BUILD RPMS SOURCES SPECS
cp ../omnidb-server_$VERSION-$ARCH.tar.gz SOURCES/
cp ../omnidb-server_$VERSION-$ARCH/omnidb.conf SOURCES/
cat > SOURCES/omnidb-server.sh << EOF
#!/bin/bash
LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:.:/opt/omnidb-server/ /opt/omnidb-server/omnidb-server \$@
EOF
cat > SOURCES/omnidb.service << EOF
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

cat > SPECS/omnidb-server.spec << EOF
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define _unpackaged_files_terminate_build 0
%define _topdir /root/OmniDB/OmniDB/deploy/packages/omnidb-server
%define _bindir /usr/bin
%define _etcdir /etc
%define _systemddir /etc/systemd/system
%define _servicename omnidb
%define name omnidb-server
%define version $VERSION
%define arch $ARCH
%define longname %{name}_%{version}-%{arch}
%define configname omnidb-config-server
%define buildroot %{_topdir}/%{longname}-root

BuildRoot: %{buildroot}
BuildArch: x86_64
Summary: Server to manage multiple databases
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
mkdir -p %{buildroot}/%{_bindir}
cp ../../SOURCES/%{name}.sh %{buildroot}/%{_bindir}/%{name}
chmod 777 %{buildroot}/%{_bindir}/%{name}
ln -s /opt/%{name}/%{configname} %{buildroot}/%{_bindir}/%{configname}
mkdir -p %{buildroot}/%{_systemddir}
cp ../../SOURCES/%{_servicename}.service %{buildroot}/%{_systemddir}
chmod 644 %{buildroot}/%{_systemddir}/%{_servicename}.service
cp ../../SOURCES/%{_servicename}.conf %{buildroot}/%{_etcdir}
chmod 644 %{buildroot}/%{_etcdir}/%{_servicename}.conf

%files
%defattr(0777,root,root,0777)
/opt/%{name}
/opt/%{name}/*
%{_bindir}/%{name}
%{_bindir}/%{configname}
%{_systemddir}/%{_servicename}.service
%{_etcdir}/%{_servicename}.conf

%config(noreplace) %{_etcdir}/%{_servicename}.conf
EOF

rpmbuild -v -bb --clean SPECS/omnidb-server.spec
cp RPMS/x86_64/omnidb-server-$VERSION-0.x86_64.rpm ../omnidb-server_$VERSION-centos7-amd64.rpm
cd ..
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-server_$VERSION-$ARCH omnidb-server
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
