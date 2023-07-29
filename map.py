import folium
from folium import plugins
import ipywidgets
import geocoder
import geopy
import numpy as np
import pandas as pd
from vega_datasets import data as vds
from IPython import display

# geocode address, place marker on map, add a minimap, bring in layer control

# get location information for address
address = geocoder.osm('Victoria St, London SW1E 5ND')

# address latitude and longitude
address_latlng = [address.lat, address.lng]

# map
map = folium.Map(location=(address_latlng), zoom_start=14)

# add marker to map
folium.Marker(address_latlng, popup='Home!', tooltip='click').add_to(map)

minimap = plugins.MiniMap(toggle_display=True)

# add minimap to map
map.add_child(minimap)

# add full screen button to map
plugins.Fullscreen(position='topright').add_to(map)

folium.raster_layers.TileLayer('Open Street Map').add_to(map)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
# folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map)
# folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
# folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)

# add scroll zoom toggler to map
# plugins.ScrollZoomToggler().add_to(map)

# # add layer control to show different maps
folium.LayerControl().add_to(map)

# # display map
map

# save display map
map.save("map.html")