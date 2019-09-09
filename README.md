# blinkenshell-map

A map to see where your fellow blinkenshellers are!

## How does it work?

Every blinkenshell user that has a "coordinates" file in their public_html will automatically be added to the map.
A small python script parses these from time to time and converts them into GeoJSON markers.
This GeoJSON layer is then added as a Leaflet layer to an OpenStreetMap based rendering done by Mapbox.

## Structure of the coordinates file
In principle just adding the Lat/Lon coordinates is sufficients, but there are additional options.
The file will be correctly parsed if it is structured as follows:
```
lat.coordinates,lon.coordinates
(optional popup text)
(optional color as #hex)
```

## Built With
* [Leaflet](https://leafletjs.com/) - The library to add the Marker layer
* [OpenStreetMap](https://openstreetmap.org) - Base data for the map
* [Mapbox](https://www.mapbox.com/) - Map tile provider

## Author

* [pbnoxious](https://github.com/pbnoxious)
