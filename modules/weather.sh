#!/bin/bash

xdg-open "https://www.google.com/#q=weather+$1&hl=${LANG%%.*}&safe=off" &

exit 0
