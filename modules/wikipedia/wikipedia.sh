#!/bin/bash
CONTENU="$1"
CONTENU=$(echo $CONTENU | sed "s/ /+/g")
xdg-open http://en.wikipedia.org/w/index.php?search="$CONTENU" &

exit 0
