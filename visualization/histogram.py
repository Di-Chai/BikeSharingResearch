import plotly.plotly as py
import plotly.graph_objs as go
import os
import plotly
from localPath import *

import numpy as np
x0 = np.random.randn(500)
x1 = np.random.randn(500)+1

trace1 = go.Histogram(
    x=x0,
    histnorm='count',
    name='control',
    xbins=dict(
        start=-4.0,
        end=3.0,
        size=0.5
    ),
    marker=dict(
        color='#FFD7E9',
    ),
    opacity=0.75
)
trace2 = go.Histogram(
    x=x1,
    name='experimental',
    xbins=dict(
        start=-3.0,
        end=4,
        size=0.5
    ),
    marker=dict(
        color='#EB89B5'
    ),
    opacity=0.75
)
data = [trace1, trace2]

layout = go.Layout(
    title='Sampled Results',
    xaxis=dict(
        title='Value'
    ),
    yaxis=dict(
        title='Count'
    ),
    bargap=0.2,
    bargroupgap=0.1
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename=os.path.join(htmlPath, 'histogramTest.html'))