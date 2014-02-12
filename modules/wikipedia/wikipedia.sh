#!/bin/bash
CONTENU="$1"
CONTENU=$(echo $CONTENU | sed "s/ /+/g")
xdg-open http://fr.wikipedia.org/wiki/"$CONTENU" & 

exit 0
