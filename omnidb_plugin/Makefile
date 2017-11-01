EXTENSION = omnidb_plugin
DATA = omnidb_plugin--0.0.1.sql
MODULES = omnidb_plugin

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
INCLUDEDIR := $(shell $(PG_CONFIG) --includedir)
INCLUDEDIR-SERVER := $(shell $(PG_CONFIG) --includedir-server)
include $(PGXS)

omnidb_plugin.so: omnidb_plugin.c
	gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I $(INCLUDEDIR) -I $(INCLUDEDIR-SERVER)
	gcc -fPIC -o omnidb_plugin.so omnidb_plugin.o -lpq -shared
