import folium
import pandas as pd

def map(path):
    sheet = pd.read_excel(io=path)
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
    )
    m.add_child(folium.LatLngPopup())
    for i in sheet.owner.index:
        long = sheet.longitude[i]
        lati = sheet.latitude[i]
        folium.Marker(
            location=[lati, long],
            popup=str(sheet.dbscan[i]),
            icon=folium.Icon(color=colors[sheet.dbscan[i] % 18])
        ).add_to(m)
    m.save('Bodensee_0.06_40.html')

