#!/bin/sh
# configuration file
CONFIGURATION="$HOME/.config/google2ubuntu/google2ubuntu.conf"

# default recording time
recording=5
if [ -f "$CONFIGURATION" ]; 
then
{
	# load the configuration
	. "$CONFIGURATION"

	# small security test
	if [ "$recording" = "" ];
	then
		recording=5
	fi
}
fi

# get the pid 
PID=$1
# kill the previous instance of rec to cascade commands
killall rec 2>/dev/null

# record during fixed seconds
( rec -r 16000 -d /tmp/voix_$PID.flac ) & pid=$!
( sleep "$recording"s && kill -HUP $pid ) 2>/dev/null & watcher=$!
wait $pid 2>/dev/null && pkill -HUP -P $watcher

exit 0;
