#!/bin/sh
PID=$1
rate=$(sox --i /tmp/voix_$PID.flac | grep "Sample Rate" | awk '{print $4}')
if [ $rate != "16000" ]; then
	sox /tmp/voix_"$PID".flac /tmp/voix_"$PID"_.flac rate 16k
	mv /tmp/voix_"$PID"_.flac /tmp/voix_"$PID".flac
fi

exit 0
