import plotly.plotly as py
import plotly.graph_objs as go
import os
from utils.distance import haversine
import json
from localPath import *
import plotly


if __name__ == '__main__':
    with open(os.path.join(jsonPath, 'stationIdOrderByBuildTime.json'), 'r') as f:
        stationIdOrderByBuildTime = json.load(f)
    stationId = stationIdOrderByBuildTime['stationID']
    stationBuildTime = stationIdOrderByBuildTime['buildTime']

    with open(os.path.join(jsonPath, 'stationAppearTime.json'), 'r') as f:
        stationAppearTimeDict = json.load(f)

    precision = 10  # meter
    distanceDict = {}
    for station in stationId:
        print(station)
        with open(os.path.join(demandDataPath, station + '.json'), 'r') as f:
            currentStationDemand = json.load(f)
        for date in currentStationDemand:
            for hour in currentStationDemand[date]:
                for type in currentStationDemand[date][hour]:  # type = 'in' or 'out'
                    for targetStationID in currentStationDemand[date][hour][type]:
                        recordNumber = currentStationDemand[date][hour][type][targetStationID]
                        lat1 = float(stationAppearTimeDict[station][1])
                        lng1 = float(stationAppearTimeDict[station][2])
                        lat2 = float(stationAppearTimeDict[targetStationID][1])
                        lng2 = float(stationAppearTimeDict[targetStationID][2])
                        recordDistance = haversine(lng1, lat1, lng2, lat2)
                        recordDistance = int((recordDistance + precision / 2.0) / precision) * precision
                        if recordDistance not in distanceDict:
                            distanceDict[recordDistance] = 0
                        distanceDict[recordDistance] += recordNumber
    with open(os.path.join(jsonPath, 'distanceDict.json'), 'w') as f:
        json.dump(distanceDict, f)
