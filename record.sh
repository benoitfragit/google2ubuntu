#!/bin/sh
PID=$1
killall rec 2>/dev/null
( 
rec -r 16000 -d /tmp/voix_$PID.flac ) & pid=$!
( sleep 5s && kill -HUP $pid ) 2>/dev/null & watcher=$!
wait $pid 2>/dev/null && pkill -HUP -P $watcher

rate=$(sox --i /tmp/voix_$PID.flac | grep "Sample Rate" | awk '{print $4}')
if [ $rate != 16000 ]; then
	sox /tmp/voix_$PID.flac -r 16000 /tmp/voix_$PID.flac 2>/dev/null
fi
exit 0;
