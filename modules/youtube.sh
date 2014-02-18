#!/bin/bash
CONTENU="$1"
CONTENU=$(echo $CONTENU | sed "s/ /+/g")
echo $CONTENU
xdg-open http://www.youtube.com/results?search_query="$CONTENU" &

exit 0
