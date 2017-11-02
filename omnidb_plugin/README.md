# Summary

- 1. Installing from DEB/RPM packages
- 2. Compiling the extension from source
- 3. Notes

# 1. Installing from DEB/RPM packages

## 1.1. Install the package

```bash
# For example, Debian-like 64 bits:
sudo dpkg -i omnidb-plugin_2.3.0-debian-amd64.deb

# For example, for CentOS-like 64 bits:
sudo rpm -ivU omnidb-plugin_2.3.0-centos-amd64.rpm
```

## 1.2. Create a symlink

```bash
# Find the PostgreSQL version and path for $libdir. For example:
sudo ln -s /opt/omnidb-plugin/omnidb_plugin_96.so /usr/lib/postgresql/9.6/lib/omnidb_plugin.so
```

## 1.3. Set shared_preload_libraries

```bash
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

sudo systemctl restart postgresql
```

## 1.4. Post-installation steps

## 1.4.1. Create omnidb schema in your database (should be done by a superuser)

```bash
psql -d <database> -f debugger_schema.sql
```

## 1.4.2. Create sample functions (optional)

```bash
psql -d <database> -f debugger_schema.sql
```

# 2. Compiling the extension from source

## 2.1. Install headers for PostgreSQL and libpq

```bash
sudo apt install postgresql-server-dev-X.Y libpq-dev
```

## 2.2. Compile omnidb_plugin

```bash
make
```

## 2.3. Install omnidb_plugin

```bash
sudo make install
```

## 2.4. Set shared_preload_libraries

```bash
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

sudo systemctl restart postgresql
```

## 2.5. Post-installation steps

## 2.5.1. Create omnidb_plugin extension (should be done by a superuser)

```bash
psql -d <database> -c 'CREATE EXTENSION omnidb_plugin'
```

## 2.2.2. Create sample functions (optional)

```bash
psql -d <database> -f debugger_schema.sql
```

# 3. Notes

- omnidb_plugin only works in Linux at the moment. OmniDB server can still be
hosted in Windows and MacOSX, but for the debugger to work properly, it needs to
connect to omnidb_plugin in PostgreSQL in Linux.

- The omnidb_plugin extension can only be created if you compile the plugin
yourself following step 2 above.

- If you use OmniDB to connect to PostgreSQL using .pgpass file, you should
create a corresponding .pgpass file inside the home of the postgres user.
