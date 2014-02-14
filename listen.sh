#!/bin/sh
# Okay Google hotword activation script
# Josh Chen, 14 Feb 2014
# Feel free to modify as you need
# configuration file
CONFIGURATION="$HOME/.config/google2ubuntu/google2ubuntu.conf"
BASEDIR=$(dirname $0)
cd $BASEDIR

# default recording time
threshold=5

> "/tmp/hotword"
while [ -f "/tmp/hotword" ]; do	
	# load the config every time, let the user setup the treshold and the hotword
	if [ -f "$CONFIGURATION" ]; 
	then
	{
		# load the configuration
		. "$CONFIGURATION"

		# small security test
		if [ "$threshold" = "" ];
		then
			threshold=5
		fi
	}
	fi
    
    # Initialize
    killall rec 2>/dev/null
    rm /tmp/pingvox.flac 2>/dev/null
    touch /tmp/pingvox.flac
    
    # If voice detected, record for 2.5s interval
    # Listen and record only when sound levels are over 17% (on razor optimal alsamixer settings seem to be 100 Internal mic, 28 Internal mic B)
    
    # >> MIC CONFIGURATION HERE <<
    ( rec /tmp/pingvox.flac rate 16000 silence 1 0.1 "$threshold"% ) & pid=$!
    
    while [ "$(stat -c%s /tmp/pingvox.flac)" == "0" ]; do
        if [ ! -f "/tmp/hotword" ]; then
        {
			killall rec
			exit 0
		}
		fi
    done
    ( sleep 2s && kill -HUP $pid ) 2>/dev/null & watcher=$!
    wait $pid 2>/dev/null && pkill -HUP -P $watcher
    
    echo
    echo 'Voice detected, launching listener.py'
    
    # Call script that checks for hotword
    python listener.py
    wait
    
done

exit 0;
