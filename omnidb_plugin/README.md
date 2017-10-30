# 1. If you installed omnidb-plugin DEB/RPM packages

## 1.1. Set shared_preload_libraries
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = '/opt/omnidb-plugin/omnidb_plugin_XY'

# 2. If you are compiling from source

## 2.1. Install headers for PostgreSQL
sudo apt install postgresql-server-dev-X.Y libpq-dev

## 2.2. Compile omnidb_plugin
./compile.sh

## 2.3. Copy to PostgreSQL $libdir
sudo cp omnidb_plugin.so /usr/lib/postgresql/X.Y/lib/

## 2.4. Set shared_preload_libraries
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

## 2.5. Post-installation steps

## 2.5.1. Create omnidb schema in your database (should be done by a superuser)
psql -d <database> -f debugger_schema.sql

## 2.5.2. Create sample functions (optional)
psql -d <database> -f debugger_schema.sql

# 3. If you want the extension

## 3.1. Install headers for PostgreSQL
sudo apt install postgresql-server-dev-X.Y libpq-dev

## 3.2. Compile omnidb_plugin
make

## 3.3. Install omnidb_plugin
sudo make install

## 3.4. Set shared_preload_libraries
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

## 3.5. Post-installation steps

## 3.5.1. Create omnidb_plugin extension (should be done by a superuser)
psql -d <database> -c 'CREATE EXTENSION omnidb_plugin'
