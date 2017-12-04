# -*- coding:utf-8 -*-
from utils.distance import haversine
from utils.getJsonData import *
from localPath import jsonPath
from dateutil.parser import parse
from loadData import *

distanceThresholdAbsorption = 200  # m
distanceThresholdStimulation = 1000  # m
timeThreshold = 30  # day

def get_distanceMatrix():
    # load data
    stationInfo = getJsonData('stationAppearTime.json')
    stationIDList = get_stationIDList()
    # compute the distance matrix
    distanceMatrix = []
    for row in stationIDList:
        rowStation = stationInfo[row]
        distance = []
        for col in stationIDList:
            colStation = stationInfo[col]
            distance.append(haversine(float(rowStation[2]), float(rowStation[1]),
                                      float(colStation[2]), float(colStation[1])))
        distanceMatrix.append(distance)
    return distanceMatrix

def get_timeMatrix():
    # load data
    stationInfo = getJsonData('stationAppearTime.json')
    stationIDList = get_stationIDList()
    # compute time matrix
    timeMatrix = []
    for row in stationIDList:
        rowStation = stationInfo[row]
        time = []
        for col in stationIDList:
            colStation = stationInfo[col]
            time.append((parse(rowStation[0]) - parse(colStation[0])).days)
        timeMatrix.append(time)
    return timeMatrix

def get_near_staion_list(distanceMatrix, d):
    # d is threshold
    nearStationMatrix = []
    for i in range(distanceMatrix.__len__()):
        nearStation = []
        for j in range(distanceMatrix[i].__len__()):
            if i != j:
                if distanceMatrix[i][j] < d:
                    nearStation.append(j)
        nearStationMatrix.append(nearStation)
    return nearStationMatrix

if __name__ == '__main__':
    S_STAR = []
    S_STAR_NN = {}

    # load data
    stationInfo = getJsonData('stationAppearTime.json')
    stationIDList = get_stationIDList()

    # compute the distance matrix
    distanceMatrix = get_distanceMatrix()

    # compute time matrix
    # timeMatrix = get_timeMatrix()

    # get station within distanceThreshold
    nearStationMatrix = get_near_staion_list(distanceMatrix, distanceThresholdAbsorption)
    nearStationMatrix_sti = get_near_staion_list(distanceMatrix, distanceThresholdStimulation)

    # Rule 1 : nearStationMatrix 移除建在一个月后的临近站点 如果有站点建在一个月内，直接清空
    for i in range(nearStationMatrix.__len__()):
        targetStationID = stationIDList[i]
        tsBuildTime = parse(stationInfo[targetStationID][0])
        nearStationNumber = nearStationMatrix[i].__len__()
        for j in range(nearStationNumber):
            nearStationID = stationIDList[nearStationMatrix[i][nearStationNumber - 1 - j]]
            nsBuildTime = parse(stationInfo[nearStationID][0])
            if abs((nsBuildTime - tsBuildTime).days) < timeThreshold:
                nearStationMatrix[i] = []
                break
            if (nsBuildTime - tsBuildTime).days > timeThreshold:
                del nearStationMatrix[i][nearStationNumber - 1 - j]
    print(nearStationMatrix)

    # Rule2 : 如果nearStationMatrix_sti内有站点建在1个月内，直接清空
    for i in range(nearStationMatrix_sti.__len__()):
        targetStationID = stationIDList[i]
        tsBuildTime = parse(stationInfo[targetStationID][0])
        for j in range(nearStationMatrix_sti[i].__len__()):
            nearStationID = stationIDList[nearStationMatrix_sti[i][j]]
            nsBuildTime = parse(stationInfo[nearStationID][0])
            if abs((tsBuildTime - nsBuildTime).days) < timeThreshold:
                nearStationMatrix_sti[i] = []
                nearStationMatrix[i] = []
                break
    print(nearStationMatrix)

    # get S_STAR and S_STAR_NN
    for i in range(nearStationMatrix.__len__()):
        if nearStationMatrix[i].__len__() != 0:
            tsID = stationIDList[i]
            tsNN = []
            for j in nearStationMatrix[i]:
                tsNN.append(stationIDList[j])
            S_STAR.append(tsID)
            S_STAR_NN[tsID] = tsNN

    absorptionStation = {'S_STAR': S_STAR, 'S_STAR_NN': S_STAR_NN}

    saveJsonData(absorptionStation, 'absorptionStation.json')