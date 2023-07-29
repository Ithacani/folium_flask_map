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
from folium.plugins import Search, MarkerCluster
import geocoder

app = Flask(__name__)


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    # get location information for address
    address = geocoder.osm('Victoria St, London SW1E 5ND')
    
    # address latitude and longitude
    address_latlng = [address.lat, address.lng]
    
    map = folium.Map(location=(address_latlng), zoom_start=14)
    
    # add marker to map
    folium.Marker(address_latlng, popup='London', tooltip='click').add_to(map)

    minimap = plugins.MiniMap(toggle_display=True)

    # add minimap to map
    map.add_child(minimap)

    # make Marker Cluster Group layer
    mcg = folium.plugins.MarkerCluster(control=False)
    map.add_child(mcg)

    # add search bar
    servicesearch = Search(
        position='topright',
        layer=mcg,
        geom_type='Point',
        placeholder='Search for a location',
        collapsed=False,
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

    # add layer control to show different maps
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


if __name__ == "__main__":
    app.run(debug=True)