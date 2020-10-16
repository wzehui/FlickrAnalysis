import folium
import pandas as pd

sheet = pd.read_excel(io='dbscan_0.02.xls')

colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black',
]

m = folium.Map(
    location=[47.6, 9.4],
    zoom_start=10,
    #tiles='Bodensee'
)

m.add_child(folium.LatLngPopup())

for i in sheet.owner.index:
    long = sheet.longitude[i]
    lati = sheet.latitude[i]

    cluster_idx = int(sheet.cluster[i].split('_')[1])
    if cluster_idx != 0:
        folium.Marker(
            location=[lati, long],
            popup=str(cluster_idx),
            icon=folium.Icon(color=colors[cluster_idx % 18])
        ).add_to(m)





#folium.Marker(
#    location=[45.3311, -121.7113],
#    popup='Timberline Lodge',
#    icon=folium.Icon(color='green')
#).add_to(m)
#
#folium.Marker(
#    location=[45.3300, -121.6823],
#    popup='Some Other Location',
#    icon=folium.Icon(color='red', icon='info-sign')
#).add_to(m)
#
m.save('Bodensee_0.02.html')