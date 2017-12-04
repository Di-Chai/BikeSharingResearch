from localPath import *
import os
import csv
import json
import numpy as np
from dateutil.parser import parse
from utils.symbols import *
dateTimeMode = '%Y-%m-%d'

def getDateFromTimeString(timeString):
    return parse(timeString).strftime(dateTimeMode)

isBadDay = {}
temperature = {}
wind = {}
with open(os.path.join(csvDataPath, '1135040.csv'), 'r') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # date 05
        currentDate = row[5]
        dateString = getDateFromTimeString(currentDate)
        # 天气情况
        if dateString not in isBadDay:
            isBadDay[dateString] = 0
        weatherCondition = row[9]
        if weatherCondition != '':
            isBadDay[dateString] = 1
        # 气温
        if dateString not in temperature:
            temperature[dateString] = []
        if row[15] != '':
            temperature[dateString].append(float(row[15].replace('s', '')))
        # 风速
        if dateString not in wind:
            wind[dateString] = []
        if row[17] != '':
            wind[dateString].append(float(row[17]))

for key, value in temperature.items():
    temperature[key] = NO_TEM if temperature[key].__len__() == 0 else np.mean(value)
for key, value in wind.items():
    wind[key] = NO_TEM if wind[key].__len__() == 0 else np.mean(value)

weatherDict = {'isBadDay': isBadDay, 'temperature': temperature, 'wind': wind}

with open(os.path.join(jsonPath, 'weatherDict.json'), 'w') as f:
    json.dump(weatherDict, f)