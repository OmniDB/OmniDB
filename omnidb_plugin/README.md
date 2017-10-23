# Install headers for PostgreSQL
sudo apt install postgresql-server-dev-9.6 libpq-dev

# Compile omnidb_plugin
./compile.sh

# Copy to PostgreSQL $libdir
sudo cp omnidb_plugin.so /usr/lib/postgresql/9.6/lib/

# Set shared_preload_libraries
nano /etc/postgresql/9.6/main/postgresql.conf
    shared_preload_libraries = 'omnidb_plugin'

# Create omnidb schema in your database
psql -d <database> -f debugger_schema.sql

# Create sample functions (optional)
psql -d <database> -f debugger_schema.sql
