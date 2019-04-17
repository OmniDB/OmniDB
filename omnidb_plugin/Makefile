EXTENSION = omnidb_plugin
DATA = omnidb_plugin--0.0.1.sql
MODULES = omnidb_plugin

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
override CPPFLAGS := $(CPPFLAGS) -I$(shell $(PG_CONFIG) --includedir)
override LDFLAGS := $(LDFLAGS) -lpq
include $(PGXS)
