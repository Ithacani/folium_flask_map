# using ipywidgets
# plot location with marker

import folium
import geocoder
import ipywidgets
from IPython import display

# text widget
address_text_box = ipywidgets.Text(value='', placeholder='type here', description='address:')

# widget function
def plot_locations(address):
    # location address
    location = geocoder.osm(address)
    
    # latitude and longitude of location
    latlng = [location.lat, location.lng]
    
    # create map
    plot_locations_map = folium.Map(location=[40, -100], zoom_start=4)
    
    # marker
    folium.Marker(latlng, popup=str(address), tooltip='click').add_to(plot_locations_map)
    
    # display map
    display(plot_locations_map)
    
# interaction between widget and function    
ipywidgets.interact_manual(plot_locations, address=address_text_box)

'''
test addresses
4790 W 16th St, Indianapolis, IN 46222 (Indy 500 Track)
2920 Zoo Dr, San Diego, CA 92101 (San Diego Zoo)
1 Infinite Loop, Cupertino, CA 95014 (Apple)
'''