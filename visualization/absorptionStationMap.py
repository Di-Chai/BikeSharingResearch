import os
from localPath import *
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import json
from utils.getJsonData import getJsonData

mapboxAccessToken = "pk.eyJ1Ijoicm1ldGZjIiwiYSI6ImNqN2JjN3l3NjBxc3MycXAzNnh6M2oxbGoifQ.WFNVzFwNJ9ILp0Jxa03mCQ"

# get all the station information
with open(os.path.join(jsonPath, 'bikeLocation.json'), 'r') as f:
    bikeLocation = json.load(f)
lat = bikeLocation['lat']
lng = bikeLocation['lng']
buildOrder = bikeLocation['buildOrder']
name = bikeLocation['name']
idList = bikeLocation['idList']

# get all the absorptionStation
absorptionStation = getJsonData('absorptionStation.json')
S_STAR = absorptionStation['S_STAR']
S_STAR_NN = absorptionStation['S_STAR_NN']

nearStationList = []
for e in S_STAR:
    for e1 in S_STAR_NN[e]:
        nearStationList.append(e1)

# get the check result
checkStation = getJsonData('checkStation.json')
obviousPairStation = checkStation['obviousPairStation']
unchangedPairStation = checkStation['unchangedPairStation']
reversedPairStation = checkStation['reversedPairStation']
# put result into list
checkCenterStation = []
obviousNN = []
unchangedNN = []
reversedNN = []
for pairStation in obviousPairStation:
    stationID = pairStation.split('-')
    checkCenterStation.append(stationID[0])
    obviousNN.append(stationID[1])
for pairStation in unchangedPairStation:
    stationID = pairStation.split('-')
    checkCenterStation.append(stationID[0])
    unchangedNN.append(stationID[1])
for pairStation in reversedPairStation:
    stationID = pairStation.split('-')
    checkCenterStation.append(stationID[0])
    reversedNN.append(stationID[1])

# set different color
color = []
delList = []
for i in range(idList.__len__()):
    stationID = idList[i]
    if stationID in S_STAR:
        color.append('rgb(0, 0, 255)')
    elif stationID in obviousNN:
        color.append('rgb(0, 255, 0)')
    elif stationID in unchangedNN:
        color.append('rgb(255, 255, 0)')
    elif stationID in reversedNN:
        color.append('rgb(255, 0, 255)')
    elif stationID in nearStationList:
        color.append('rgb(160, 160, 160)')
    else:
        delList.append(i)
        color.append('rgb(%s, %s, %s)' % (255, 195 - buildOrder[i], 195 - buildOrder[i]))
# delList.reverse()
# for position in delList:
#     del idList[position]
#     del lat[position]
#     del lng[position]
#     del buildOrder[position]
#     del name[position]


bikeStations = [Scattermapbox(
        lon = lng,
        lat = lat,
        text = name,
        mode='markers',
        marker = dict(
            size = 6,
            color = color,  # ['rgb(%s, %s, %s)' % (255, 195-e, 195-e) for e in buildOrder],
            opacity=1,
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
plotly.offline.plot(fig, filename=os.path.join(htmlPath, 'absorptionStationMap'))
