import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from localPath import *
import os
import json
import numpy as np


def linePlot(xList, yList, nameList=None, fileName='LinePlot'):
    data = []
    for i in range(yList.__len__()):
        data.append(go.Scatter(
            x = xList,
            y = yList[i],
            mode='lines',
            name='lines' if nameList == None else nameList[i]
        ))
    plotly.offline.plot(data, filename=os.path.join(htmlPath, fileName))

if __name__ == '__main__':
    with open(os.path.join(jsonPath, 'stationIdOrderByBuildTime.json'), 'r') as f:
        stationIdOrderByBuildTime = json.load(f)
    stationId = stationIdOrderByBuildTime['stationID']
    stationBuildTime = stationIdOrderByBuildTime['buildTime']

    linePlot([1,2,3,4], [[1,2,3,4]], ['y=x'], 'y_x')