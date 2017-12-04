import os
from localPath import *
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import json

mapboxAccessToken = "pk.eyJ1Ijoicm1ldGZjIiwiYSI6ImNqN2JjN3l3NjBxc3MycXAzNnh6M2oxbGoifQ.WFNVzFwNJ9ILp0Jxa03mCQ"

with open(os.path.join(jsonPath, 'bikeLocation.json'), 'r') as f:
    bikeLocation = json.load(f)

lat = bikeLocation['lat']
lng = bikeLocation['lng']
buildOrder = bikeLocation['buildOrder']
name = bikeLocation['name']

# get the new plot list
newLat = []
newLng = []
newBuildOrder = []
newName = []
threshold = 10
for i in range(buildOrder.__len__()):
    if buildOrder[i] < threshold:
        newLat.append(lat[i])
        newLng.append(lng[i])
        newBuildOrder.append(buildOrder[i])
        newName.append(name[i])

# bikeStations = [Scattermapbox(
#         lon = lng,
#         lat = lat,
#         text = name,
#         mode='markers',
#         marker = dict(
#             size = 6,
#             color = ['rgb(%s, %s, %s)' % (255, 195-e, 195-e) for e in buildOrder],
#             opacity=1
#         ))]

maxBuildOrder = max(newBuildOrder)

bikeStations = [Scattermapbox(
        lon = newLng,
        lat = newLat,
        text = newName,
        mode='markers',
        marker = dict(
            size = 6,
            color = ['rgb(%s, %s, %s)' % (255, 195-e, 195-e) for e in newBuildOrder],
            opacity=1
        ))]

layout = Layout(
    title='Bike Station Location & The latest built stations with deeper color',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapboxAccessToken,
        bearing=0,
        center=dict(
            lat=40.7381765,
            lon=-73.97738662
        ),
        pitch=0,
        zoom=11,
        style='light'
    ),
)

fig = dict(data=bikeStations, layout=layout)
plotly.offline.plot(fig, filename=os.path.join(htmlPath, 'BikeStationLocationWithBuildTimePartStation'))
