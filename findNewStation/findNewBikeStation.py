from localPath import csvDataPath
import os
import csv
import json
import datetime
from dateutil.parser import parse

csvFileNameList = [e for e in os.listdir(csvDataPath) if e.endswith(".csv")]

def compareTime(startTime, oldTime):
    new = parse(startTime)
    old = parse(oldTime)
    if new < old:
        return True
    else:
        return False

stationAppearTime = {}
for csvFile in csvFileNameList:
    with open(os.path.join(csvDataPath, csvFile)) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(csvFile)
        for row in f_csv:
            # get all the data
            startTime = row[1]
            stopTime = row[2]
            startStationID = row[3]
            endStationID = row[7]
            # bikeID = row[11]
            # get the appearTime
            if startStationID not in stationAppearTime:
                startStationName = row[4]
                startStationLat = row[5]
                startStationLong = row[6]
                stationAppearTime[startStationID] = [startTime, startStationLat, startStationLong, startStationName]
            elif compareTime(startTime, stationAppearTime[startStationID][0]):
                stationAppearTime[startStationID] = [startTime, startStationLat, startStationLong, startStationName]
            if endStationID not in stationAppearTime:
                endStationName = row[8]
                endStationLat = row[9]
                endStationLong = row[10]
                stationAppearTime[endStationID] = [stopTime, endStationLat, endStationLong, endStationName]
            elif compareTime(stopTime, stationAppearTime[endStationID][0]):
                stationAppearTime[endStationID] = [stopTime, endStationLat, endStationLong, endStationName]
with open('stationAppearTime.json', 'w') as f:
    json.dump(stationAppearTime, f)