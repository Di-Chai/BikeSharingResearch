# -*-  coding:utf-8 -*-
from localPath import *
import os
import json
from utils.symbols import *

def computeDailyDemand(stationID, date):
    with open(os.path.join(demandDataPath, stationID + '.json'), 'r') as f:
        currentStationDemand = json.load(f)
    try:
        dateDemand = currentStationDemand[date]
    except:
        return EMPTY_DATA
    hourDemandTotal = 0
    for hour in dateDemand:
        for type in dateDemand[hour]:
            for targetStation in dateDemand[hour][type]:
                hourDemandTotal += dateDemand[hour][type][targetStation]
    return hourDemandTotal