#!/bin/sh

HOME_DIR=/OmniDB/OmniDB
PID=$(/bin/ps -ef|grep omnidb-server|grep -v 'grep'| awk '{print $2}')
ERROR=$(grep HTTPServer.tick $HOME_DIR/nohup.out| head -1|wc -l)

if [ "$ERROR" -eq 1 ]
then
	echo "Reload OmniDB Server"
	/bin/kill $PID
	cd $HOME_DIR
	nohup python omnidb-server.py -c omnidb.conf &
	exit 0
else
	echo "Clear omnidb log"
	echo '' > $HOME_DIR/nohup.out
	exit 0
fi
done
