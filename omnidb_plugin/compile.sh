#!/bin/bash

PGVERSION=11

rm -f *.o *.so
gcc -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/$PGVERSION/server
gcc -fPIC -o omnidb_plugin.so omnidb_plugin.o -lpq -shared

# debug mode
#rm -f *.o *.so
#gcc -D DEBUG -fPIC -c -o omnidb_plugin.o omnidb_plugin.c -lpq -I /usr/include/postgresql -I /usr/include/postgresql/$PGVERSION/server
#gcc -D DEBUG -fPIC -o omnidb_plugin.so omnidb_plugin.o -lpq -shared
