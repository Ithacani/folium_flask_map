""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template_string
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import geocoder


app = Flask(__name__)


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    # get location information for a pre-set address
    address = geocoder.osm('Victoria St, London SW1E 5ND')
    
    # Extract the lat long and store as a variable
    address_latlng = [address.lat, address.lng]
    
    # Now turn the map on using address_latlng as starting focus
    map = folium.Map(location=(address_latlng), zoom_start=14)

    # add a buffer variable as a child to the map.  Radius = 500 meters
    buffer = folium.Circle([address.lat, address.lng], radius=500)
    map.add_child(buffer)
    
    # add the pre-set marker to map
    marker = folium.Marker(address_latlng, popup='London', tooltip='click', icon=folium.Icon(color='orange',icon_color='white',prefix='fa', icon='magnifying-glass'))
    map.add_child(marker)

    # add minimap to map
    minimap = plugins.MiniMap(toggle_display=True)
    map.add_child(minimap)

    # make Marker Cluster Group layer
    mcg = folium.plugins.MarkerCluster(control=False)
    mcg.add_to(map)

    # adds search bar 
    plugins.Geocoder(
        collapsed=False, 
        position='topleft', 
        add_marker=True,
        layer='osm'
    ).add_to(map)

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

    # add route plotting
    route_lats_longs = [[51.4957, -0.1448], #London Victoria
                        [51.5020, -0.1401], #Buckingham Palace
                        [51.5074, -0.1276], #Trafalgar Square
                        [51.5010, -0.1262], #Parliament Square
                        [51.4977, -0.1347], #Part way back (for road bend)
                        [51.4957, -0.1448],] #Back to London Victoria

    plugins.AntPath(route_lats_longs).add_to(map)

    # add layer control to show different map types - do this last
    folium.LayerControl().add_to(map)

    return map.get_root().render()


@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map()

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


@app.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=800,
        height=600,
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using components</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )

@app.route("/example")
def exampleroute():
    # get location information for address
    address = geocoder.osm('Victoria St, London SW1E 5ND')
    
    # store the address latitude and longitude in a variable
    address_latlng = [address.lat, address.lng]

    # turn the map on and focus in on the stored address variable at zoom level 14
    map = folium.Map(location=(address_latlng), zoom_start=14)

    # add marker to map
    marker = folium.Marker(address_latlng, popup='London Victoria', tooltip='click me', icon=folium.Icon(color='blue', icon_color='black', prefix='fa', icon='magnifying-glass'))
    marker.add_to(map)

    # return
    return map.get_root().render()



if __name__ == "__main__":
    app.run(debug=True)