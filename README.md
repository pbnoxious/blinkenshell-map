# blinkenshell-map

A map to see where your fellow blinkenshellers are!

The current URL is <http://pbnoxious.blinkenshell.org/map/map.html>

## How does it work?

Every blinkenshell user that has a "coordinates" file in their public_html will automatically be added to the map.
A small python script parses these from time to time (currently once per day) and converts them into GeoJSON markers.
These GeoJSON objects are then added as a Leaflet layer to an OpenStreetMap background with tiles from Mapbox.

## Structure of the coordinates file
In principle, just adding the Lat/Lon coordinates is sufficient but there are additional options.
The file will be correctly parsed if it is structured as follows:
```
lat_coordinate,lon_coordinate
(optional popup text)
(optional color as #hex)
```

## Built With
* [Leaflet](https://leafletjs.com/) - The library to add the Marker layer
* [OpenStreetMap](https://openstreetmap.org) - Base data for the map
* [Mapbox](https://www.mapbox.com/) - Map tile provider

## Author

* [pbnoxious](https://github.com/pbnoxious)
