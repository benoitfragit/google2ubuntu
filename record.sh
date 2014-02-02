#!/bin/sh
PID=$1
killall rec 2>/dev/null
( rec -r 16000 -d /tmp/voix_$PID.flac ) & pid=$!
( sleep 5s && kill -HUP $pid ) 2>/dev/null & watcher=$!
wait $pid 2>/dev/null && pkill -HUP -P $watcher
exit 0;
