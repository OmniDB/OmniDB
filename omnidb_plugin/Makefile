EXTENSION = omnidb_plugin
DATA = omnidb_plugin--0.0.1.sql
OBJS = omnidb_plugin.o
MODULE_big = omnidb_plugin

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
override CPPFLAGS := $(CPPFLAGS) -I$(shell $(PG_CONFIG) --includedir)
SHLIB_LINK = -lpq
include $(PGXS)
