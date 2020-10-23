#!/bin/bash

if [ $1 = "gtm" ]
then
  su - postgres -c "/usr/local/pgsql/bin/gtm -D /usr/local/pgsql/data >logfile 2>&1 &"
else
  su - postgres -c "/usr/local/pgsql/bin/postgres --$1 -D /usr/local/pgsql/data >logfile 2>&1 &"
fi
