#!/bin/sh
PID=$1
( rec -r 16000 -d /tmp/voix_$PID.flac ) & pid=$!
( sleep 5s && kill -HUP $pid ) 2>/dev/null & watcher=$!
wait $pid 2>/dev/null && pkill -HUP -P $watcher
exit 0;
