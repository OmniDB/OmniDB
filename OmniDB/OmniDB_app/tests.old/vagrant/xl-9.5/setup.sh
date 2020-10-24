#!/bin/bash

if [ $(hostname) = "xlcoord" ]
then

  echo "ALTER NODE xlcoord WITH (TYPE = 'coordinator', HOST = 'localhost', PORT = 5432);" > /tmp/script.sql
  echo "CREATE NODE xldata1 WITH (TYPE = 'datanode', HOST = '$2', PORT = 5432);" >> /tmp/script.sql
  echo "CREATE NODE xldata2 WITH (TYPE = 'datanode', HOST = '$3', PORT = 5432);" >> /tmp/script.sql
  echo "SELECT pgxc_pool_reload();" >> /tmp/script.sql

else
  if [ $(hostname) = "xldata1" ]
  then

    echo "ALTER NODE xldata1 WITH (TYPE = 'datanode', HOST = 'localhost', PORT = 5432);" > /tmp/script.sql
    echo "CREATE NODE xlcoord WITH (TYPE = 'coordinator', HOST = '$1', PORT = 5432);" >> /tmp/script.sql
    echo "CREATE NODE xldata2 WITH (TYPE = 'datanode', HOST = '$3', PORT = 5432);" >> /tmp/script.sql
    echo "SELECT pgxc_pool_reload();" >> /tmp/script.sql

  else

    echo "ALTER NODE xldata2 WITH (TYPE = 'datanode', HOST = 'localhost', PORT = 5432);" > /tmp/script.sql
    echo "CREATE NODE xlcoord WITH (TYPE = 'coordinator', HOST = '$1', PORT = 5432);" >> /tmp/script.sql
    echo "CREATE NODE xldata1 WITH (TYPE = 'datanode', HOST = '$2', PORT = 5432);" >> /tmp/script.sql
    echo "SELECT pgxc_pool_reload();" >> /tmp/script.sql

  fi
fi

chmod 777 /tmp/script.sql
sudo su - postgres -c "/usr/local/pgsql/bin/psql -f /tmp/script.sql"
