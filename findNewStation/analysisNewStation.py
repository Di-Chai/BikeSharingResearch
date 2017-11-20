# -*-  coding:utf-8 -*-
from localPath import *
import os
import csv
import json
from dateutil.parser import parse
dateTimeMode = '%Y-%m-%d'

def getDateFromTimeString(timeString):
    return parse(timeString).strftime(dateTimeMode)

if __name__ == '__main__':
    # get the new stations' data
    with open(os.path.join(jsonPath, 'stationAppearTime.json'), 'r') as f:
        stationAppearTimeDict = json.load(f)
    #######################################################################
    # 获取 bike station 随时间变化的数据
    #######################################################################
    dailyStationNumberDict = {}
    for stationID in stationAppearTimeDict.keys():
        appearTime = stationAppearTimeDict[stationID][0]
        appearTimeDate = getDateFromTimeString(appearTime)
        if appearTimeDate not in dailyStationNumberDict:
            dailyStationNumberDict[appearTimeDate] = 1
        else:
            dailyStationNumberDict[appearTimeDate] += 1
    dailyStationNumberList = [[parse(x), y] for x, y in dailyStationNumberDict.items()]
    dailyStationNumberList = sorted(dailyStationNumberList)
    totalStationNum = 0
    for i in range(dailyStationNumberList.__len__()):
        totalStationNum = totalStationNum + dailyStationNumberList[i][1]
        dailyStationNumberList[i][1] = totalStationNum
    if os.path.isfile(os.path.join(jsonPath, 'dailyStationNumber.json')) is False:
        with open(os.path.join(jsonPath, 'dailyStationNumber.json'), 'w') as f:
            json.dump({'x': [e[0].strftime(dateTimeMode) for e in dailyStationNumberList],
                       'y': [e[1] for e in dailyStationNumberList]}, f)
    #######################################################################
    # get bike location information
    #######################################################################
    # lat: lng: y:
    orderCounter = 0
    for timeString, order in dailyStationNumberList:
        dailyStationNumberDict[timeString.strftime(dateTimeMode)] = orderCounter
        orderCounter += 1
    lat = []
    lng = []
    buildOrder = []
    name = []
    for stationID in stationAppearTimeDict.keys():
        lat.append(stationAppearTimeDict[stationID][1])
        lng.append(stationAppearTimeDict[stationID][2])
        buildTime = getDateFromTimeString(stationAppearTimeDict[stationID][0])
        buildOrder.append(dailyStationNumberDict[buildTime])
        textToShow = 'AppearTime: %s' % buildTime
        stationName = stationAppearTimeDict[stationID][3].strip()
        name.append(textToShow)
    with open(os.path.join(jsonPath, 'bikeLocation.json'), 'w') as f:
        json.dump({'lat': lat, 'lng': lng, 'buildOrder': buildOrder, 'name': name}, f)