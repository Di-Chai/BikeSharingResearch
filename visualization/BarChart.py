import plotly.plotly as py
import plotly.graph_objs as go
import os
from utils.distance import haversine
import json
from localPath import *
import plotly

def BarChart(xList, yList, fileName):
    data = [go.Bar(
        x= xList,
        y= yList
    )]
    plotly.offline.plot(data, filename=os.path.join(htmlPath, fileName))

if __name__ == '__main__':
    with open(os.path.join(jsonPath, 'distanceDict.json'), 'r') as f:
        distanceDict = json.load(f)
    distanceTupleList = sorted(distanceDict.items(), key=lambda x: int(x[0]), reverse=False)
    x = [int(e[0]) for e in distanceTupleList]
    y = [e[1] for e in distanceTupleList]
    BarChart(x[1:1414], y[1:1414], 'distance.html')