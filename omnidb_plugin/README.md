# Summary

- [1- Linux Installation](#1-linux-installation)
- [2- Windows Installation](#2-windows-installation)
- [3- FreeBSD Installation](#3-freebsd-installation)
- [4- MacOSX Installation](#4-macosx-installation)
- [5- Post-installation steps ** **REQUIRED** **](#5-post-installation-steps--required-)


# 1. Linux Installation

You can install from packages or compile from source.

- 1.1. Installing from DEB/RPM packages
- 1.2. Compiling the extension from source

## 1.1. Installing from DEB/RPM packages

### 1.1.1. Install the package

```bash
# For example, Debian-like 64 bits:
sudo dpkg -i omnidb-plugin_2.16.0-debian-amd64.deb

# For example, for CentOS-like 64 bits:
sudo rpm -ivU omnidb-plugin_2.16.0-centos-amd64.rpm
```

### 1.1.2. Create a symlink

```bash
# Find the PostgreSQL version and path for $libdir and create a link to the specific library. For example:
sudo ln -s /opt/omnidb-plugin/omnidb_plugin_96.so /usr/lib/postgresql/9.6/lib/omnidb_plugin.so
```

### 1.1.3. Set shared_preload_libraries

```bash
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

sudo systemctl restart postgresql
```

### 1.1.4. Post-installation steps

#### 1.1.4.1. Create omnidb schema in your database (should be done by a superuser)

```bash
psql -d <database> -f debugger_schema.sql
```

#### 1.1.4.2. Create sample functions (optional)

```bash
psql -d <database> -f sample_functions.sql
```

#### 1.1.4.3. Next steps

Follow [Post-installation steps](#5-post-installation-steps--required-) in
section 5.

## 1.2. Compiling the extension from source

### 1.2.1. Install headers for PostgreSQL and libpq

```bash
sudo apt install postgresql-server-dev-X.Y libpq-dev
```

### 1.2.2. Compile omnidb_plugin

```bash
make
```

### 1.2.3. Install omnidb_plugin

```bash
sudo make install
```

### 1.2.4. Set shared_preload_libraries

```bash
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

sudo systemctl restart postgresql
```

### 1.2.5. Post-installation steps

#### 1.2.5.1. Create omnidb_plugin extension (should be done by a superuser)

```bash
psql -d <database> -c 'CREATE EXTENSION omnidb_plugin'
```

#### 1.2.5.2. Create sample functions (optional)

```bash
psql -d <database> -f sample_functions.sql
```

#### 1.2.5.3. Next steps

Follow [Post-installation steps](#5-post-installation-steps--required-) in
section 5.


# 2. Windows Installation

## 2.1. Downloading the plugin

Download the zip corresponding to your architecture from the website.

## 2.2. Installing the plugin

Move the omnidb_plugin.dll corresponding to your PostgreSQL version to the
folder *lib*, which is inside the folder where PostgreSQL was installed.

## 2.3. Set shared_preload_libraries

Change the file *PostgreSQL_directory/data/postgresql.conf*, including the
following line:

```bash
shared_preload_libraries = 'omnidb_plugin'
```

Then restart PostgreSQL.

## 2.4. Post-installation steps

### 2.4.1. Create omnidb schema in your database (should be done by a superuser)

```bash
psql -d <database> -f debugger_schema.sql
```

### 2.4.2. Create sample functions (optional)

```bash
psql -d <database> -f sample_functions.sql
```

### 2.4.3. Next steps

Follow [Post-installation steps](#5-post-installation-steps--required-) in
section 5.


# 3. FreeBSD Installation

## 3.1. Downloading the plugin

Download the tar.gz corresponding to your architecture from the website.

```bash
wget --no-check-certificate https://omnidb.org/dist/2.16.0/omnidb-plugin_2.16.0-freebsd.tar.gz
```

## 3.1. Installing the plugin

Move the omnidb_plugin.so corresponding to your PostgreSQL version to the folder
*lib*, which is inside the folder where PostgreSQL was installed.

```bash
tar -xzvf omnidb-plugin_2.16.0-freebsd.tar.gz
cp omnidb-plugin_2.16.0-freebsd/omnidb_plugin_10.so /usr/local/lib/postgresql/omnidb_plugin.so
```

## 3.3. Set shared_preload_libraries

Change the file *PostgreSQL_directory/data/postgresql.conf*, including the
following line:

```bash
shared_preload_libraries = 'omnidb_plugin'
```

Then restart PostgreSQL.

## 3.4. Post-installation steps

### 3.4.1. Create omnidb schema in your database (should be done by a superuser)

```bash
psql -d <database> -f debugger_schema.sql
```

### 3.4.2. Create sample functions (optional)

```bash
psql -d <database> -f sample_functions.sql
```

### 3.4.3. Next steps

Follow [Post-installation steps](#5-post-installation-steps--required-) in
section 5.


# 4. MacOSX Installation

## 4.1. Limitations

If you have PostgreSQL installed in your Mac and want to also install OmniDB
debugger, please be aware that currently we don't offer any packages for the
debugger for Mac OS X. Your only option is to compile and install from sources.
It is not that hard, as you can see below.

## 4.2. Compiling the extension from source

### 4.2.1. Install SDK headers for Mac OS

```bash
sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
```

### 4.2.2. If not installed, install PostgreSQL from Homebrew

This will also install PostgreSQL headers and libpq.

If brew is not installed yet, you can install it like this:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then:

```bash
brew install postgresql
```

### 4.2.3. Compile omnidb_plugin

```bash
make
```

### 4.2.4. Install omnidb_plugin

```bash
sudo make install
```

### 4.2.5. Set shared_preload_libraries

```bash
vim /usr/local/var/postgres/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

brew services restart postgresql
```

### 4.2.6. Post-installation steps

#### 4.2.6.1. Create omnidb_plugin extension (should be done by a superuser)

```bash
psql -d <database> -c 'CREATE EXTENSION omnidb_plugin'
```

#### 4.2.6.2. Create sample functions (optional)

```bash
psql -d <database> -f sample_functions.sql
```

#### 4.2.6.3. Next steps

Follow [Post-installation steps](#5-post-installation-steps--required-) in
section 5.


# 5. Post-installation steps ** **REQUIRED** **

## 5.1. Grant privileges to each database user that will debug functions (should be done by a superuser)

Every database user that uses the debugger needs access to the debugger control
tables.

```bash
psql -d <database> -c 'GRANT ALL ON SCHEMA omnidb TO <user>; GRANT ALL ON ALL TABLES IN SCHEMA omnidb TO <user>;'
```

## 5.2. Enable passwordless access to each database user that will debug functions

Every database user that uses the debugger needs local passwordless access to
the target database. This is because the database will create an additional
local connection to perform debugging operations.

We need to add a rule to *pg_hba.conf* of type `host`, matching the PostgreSQL
user and database OmniDB is connected to. The method can be either `trust`,
which is insecure and not recommended, or `md5`.

#### trust

- Add a rule similar to:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    <database>      <user>          127.0.0.1/32            trust
host    <database>      <user>          ::1/128                 trust
```

#### md5

- Add rules similar to:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    <database>      <user>          127.0.0.1/32            md5
host    <database>      <user>          ::1/128                 md5
```

- Create a `.pgpass` file with a similar content:

```bash
localhost:<port>:<database>:<username>:<password>
```

More information about how `.pgpass` works can be found here: https://www.postgresql.org/docs/11/static/libpq-pgpass.html
