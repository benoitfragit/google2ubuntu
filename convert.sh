#!/bin/sh
PID=$1

rate=$(sox --i /tmp/voix_$PID.flac | grep "Sample Rate" | awk '{print $4}')
if [ $rate != 16000 ]; then
	sox /tmp/voix_$PID.flac -r 16000 /tmp/voix_$PID.flac 2>/dev/null
fi

exit 0
