#!/bin/sh
( rec -r 16000 -d voix.flac ) & pid=$!
( sleep 5s && kill -HUP $pid ) 2>/dev/null & watcher=$!
wait $pid 2>/dev/null && pkill -HUP -P $watcher
exit 0;
