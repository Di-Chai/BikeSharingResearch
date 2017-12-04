from localPath import *
from utils.getJsonData import getJsonData
import os
import csv

def load_all_csv_data():
    csvFileNameList = [e for e in os.listdir(csvDataPath) if e.endswith(".csv")]
    # This will take a long time ...
    allRecords = []
    overAllRecordNumber = 0
    for csvFile in csvFileNameList:
        with open(os.path.join(csvDataPath, csvFile)) as f:
            print(csvFile)
            f_csv = csv.reader(f)
            headers = next(f_csv)
            for row in f_csv:
                overAllRecordNumber += 1
                allRecords.append(row)
    print('overAllRecordNumber :', overAllRecordNumber)
    return allRecords

def get_stationIDList():
    stationIDOrderByBuildTime = getJsonData('stationIdOrderByBuildTime.json')
    return stationIDOrderByBuildTime['stationID']



get_stationIDList()