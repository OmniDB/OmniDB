# 1. If you installed omnidb-plugin DEB/RPM packages

## 1.1. Set shared_preload_libraries
```bash
nano /etc/postgresql/X.Y/main/postgresql.conf
    shared_preload_libraries = '/opt/omnidb-plugin/omnidb_plugin_XY'

sudo systemctl restart postgresql
```

## 1.2. Post-installation steps

### 1.2.1. Create omnidb schema in your database (should be done by a superuser)
```bash
psql -d <database> -f debugger_schema.sql
```

### 1.2.2. Create sample functions (optional)
```bash
psql -d <database> -f debugger_schema.sql
```

# 2. If you are compiling the extension from source

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

### 2.5.1. Create omnidb_plugin extension (should be done by a superuser)
```bash
psql -d <database> -c 'CREATE EXTENSION omnidb_plugin'
```

### 2.2.2. Create sample functions (optional)
```bash
psql -d <database> -f debugger_schema.sql
```
