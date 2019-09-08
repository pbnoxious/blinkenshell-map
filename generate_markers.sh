#!/bin/bash

coordfile='coordinates'
markerfile='markers.js'
#rm -f $markerfile

awk '{print "L.marker(["$2"], title: "$1").addTo(mymap).bindPopup(\""$1"\")"}' $coordfile > $markerfile
