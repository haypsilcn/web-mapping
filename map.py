import folium
import pandas

data = pandas.read_csv("data/Volcanoes.txt")
latitudes = list(data["LAT"])
longitudes = list(data["LON"])
elevs = list(data["ELEV"])
names = list(data["NAME"])

map_ = folium.Map(location=[40, -108], zoom_start=5, tiles="Stamen Terrain")

html = """
<a href = "https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s meters
"""


def color_marker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


featureGroupVolcanoes = folium.FeatureGroup(name="Volcanoes")
featureGroupPopulation = folium.FeatureGroup(name="Population")

for latitude, longitude, elev, name in zip(latitudes, longitudes, elevs, names):
    iframe = folium.IFrame(html=html % (name, name, elev), width=200, height=100)
    featureGroupVolcanoes.add_child(
        folium.CircleMarker(location=(latitude, longitude), radius=6, popup=folium.Popup(iframe),
                            fill_color=color_marker(elev), color=color_marker(elev), fill=True, fill_ocpacity=1))

featureGroupPopulation.add_child(folium.GeoJson(data=open("data/world.json", "r", encoding="utf-8-sig").read(),
                                                style_function=lambda x: {'fillColor': 'yellow'
                                                if x['properties']['POP2005'] < 1000000
                                                else 'orange'
                                                if 1000000 <= x['properties']['POP2005'] < 2000000
                                                else 'red'}))
map_.add_child(featureGroupVolcanoes)
map_.add_child(featureGroupPopulation)
map_.add_child(folium.LayerControl())
map_.save("Map.html")
