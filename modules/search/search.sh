#!/bin/bash
CONTENU="$2 $3 $4"
case $1 in
	"Wikipédia" )
		xdg-open http://fr.wikipedia.org/wiki/"$CONTENU" &;;
	"YouTube" ) 
		xdg-open http://www.youtube.com/results?search_query="$CONTENU"&sm=3 & ;;
	"Google" ) 
		xdg-open http://www.google.com/search?q="$CONTENU" & ;;
esac 

exit 0
