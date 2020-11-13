import numpy as np
from numpy import pi, sin, cos
import plotly.graph_objs as go


fig = go.Figure(go.Scattermapbox(
                    lat=[45.46427],
                    lon=[9.18951],
                    mode='markers',
                    text='Milan',
                    marker_size=9, marker_color='red',
                    hoverinfo='text'))

R = 0.75
center_lon = 9.18951
center_lat = 45.46427
t = np.linspace(0, 2*pi, 100)
circle_lon =center_lon + R*cos(t)
circle_lat =center_lat +  R*sin(t)

mapbox_access_token = \
    'pk.eyJ1Ijoiem9pcGh5IiwiYSI6ImNraGVwdm1qbjA0aTEzMW0yeGhmdTh3aGgifQ.uYmOx-yQ5hJdBQgRm7SO3w'
coords=[]
for lo, la in zip(list(circle_lon), list(circle_lat)):
    coords.append([lo, la])

layers=[dict(sourcetype = 'geojson',
             source={ "type": "Feature",
                     "geometry": {"type": "LineString",
                                  "coordinates": coords
                                  }
                    },
             color=   'red',
             type = 'line',
             line=dict(width=1.5)
            )]

fig.update_layout(
    title_text='Your title',
    width=850,
    height=850,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        layers=layers,
        bearing=0,
        center=dict(
            lat=45.8257,
            lon=10.8746,
        ),
        pitch=0,
        zoom=5.6,
        style='outdoors')
   )

fig.show()
