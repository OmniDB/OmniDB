#!/bin/bash

VERSION=2.17.0
ARCH=centos-amd64

cd ~/OmniDB/omnidb_plugin

echo -n "Cleaning... "
rm -f *.o
echo "Done."

echo "Compiling for 9.4... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-9.4/lib -lpq -I /usr/pgsql-9.4/include -I /usr/pgsql-9.4/include/server
gcc -fPIC -o omnidb_plugin_94.so omnidb_plugin.o -L /usr/pgsql-9.4/lib -lpq -shared
echo "Done."

echo "Compiling for 9.5... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-9.5/lib -lpq -I /usr/pgsql-9.5/include -I /usr/pgsql-9.5/include/server
gcc -fPIC -o omnidb_plugin_95.so omnidb_plugin.o -L /usr/pgsql-9.5/lib -lpq -shared
echo "Done."

echo "Compiling for 9.6... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-9.6/lib -lpq -I /usr/pgsql-9.6/include -I /usr/pgsql-9.6/include/server
gcc -fPIC -o omnidb_plugin_96.so omnidb_plugin.o -L /usr/pgsql-9.6/lib -lpq -shared
echo "Done."

echo "Compiling for 10... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-10/lib -lpq -I /usr/pgsql-10/include -I /usr/pgsql-10/include/server
gcc -fPIC -o omnidb_plugin_10.so omnidb_plugin.o -L /usr/pgsql-10/lib -lpq -shared
echo "Done."

echo "Compiling for 11... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-11/lib -lpq -I /usr/pgsql-11/include -I /usr/pgsql-11/include/server
gcc -fPIC -o omnidb_plugin_11.so omnidb_plugin.o -L /usr/pgsql-11/lib -lpq -shared
echo "Done."

echo "Compiling for 12... "
rm -f *.o
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -L /usr/pgsql-12/lib -lpq -I /usr/pgsql-12/include -I /usr/pgsql-12/include/server
gcc -fPIC -o omnidb_plugin_12.so omnidb_plugin.o -L /usr/pgsql-12/lib -lpq -shared
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

echo "Generating rpm packages..."
mkdir omnidb-plugin
cd omnidb-plugin
mkdir -p BUILD RPMS SOURCES SPECS
cp ../omnidb-plugin_$VERSION-$ARCH.tar.gz SOURCES/

cat > SPECS/omnidb-plugin.spec <<EOF
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define _unpackaged_files_terminate_build 0
%define _topdir /root/OmniDB/OmniDB/deploy/packages/omnidb-plugin
%define name omnidb-plugin
%define version $VERSION
%define arch $ARCH
%define longname %{name}_%{version}-%{arch}
%define buildroot %{_topdir}/%{longname}-root

BuildRoot: %{buildroot}
BuildArch: x86_64
Summary: PostgreSQL plugin to allow OmniDB to debug PLpgSQL functions
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

%files
%defattr(0777,root,root,0777)
/opt/%{name}
/opt/%{name}/*
EOF

rpmbuild -v -bb --clean SPECS/omnidb-plugin.spec
cp RPMS/x86_64/omnidb-plugin-$VERSION-0.x86_64.rpm ../omnidb-plugin_$VERSION-centos7-amd64.rpm
cd ..
echo "Done"

echo -n "Cleaning... "
rm -rf omnidb-plugin_$VERSION-$ARCH
echo "Done"

cd ../..
echo "All Linux server packages for OmniDB version $VERSION architecture $ARCH were successfully created."
