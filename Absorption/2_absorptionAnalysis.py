# -*-  coding:utf-8 -*-
import numpy as np
import datetime
from dateutil.parser import parse
from Absorption.getDemand import computeDailyDemand
from utils.getJsonData import getJsonData, saveJsonData
from utils.dayType import isWorkDay, isBadDay
from utils.symbols import *
from utils.distance import haversine

def check_list_positive(valueList):
    positive = False
    for e in valueList:
        if e > 0:
            positive = True
            break
    return positive

def get_normal_mean(valueList):
    if check_list_positive(valueList):
        valueList = [e for e in valueList if e > 0]
    valueListMean = np.mean(valueList)
    return valueListMean

dateTimeMode = '%Y-%m-%d'

def getDateFromTimeString(timeString):
    return parse(timeString).strftime(dateTimeMode)

if __name__ == '__main__':

    # get data
    stationAppearTimeDict = getJsonData('stationAppearTime.json')
    stationIdOrderByBuildTime = getJsonData('stationIdOrderByBuildTime.json')
    stationId = stationIdOrderByBuildTime['stationID']
    stationBuildTime = stationIdOrderByBuildTime['buildTime']

    weatherDict = getJsonData('weatherDict.json')
    temperature = weatherDict['temperature']
    wind = weatherDict['wind']

    # get the stationID set
    absorptionStation = getJsonData('absorptionStation.json')
    S_STAR = absorptionStation['S_STAR']
    S_STAR_NN = absorptionStation['S_STAR_NN']

    timeRange = 40 # day

    # save result
    absorptionAnalysis = {}
    absorptionAnalysisDaily = {}
    workday = {}
    holiday = {}

    for station in S_STAR:
        nearStationIDList = S_STAR_NN[station]
        newStationBuildDate = parse(stationAppearTimeDict[station][0])
        workDayChartDict = {}
        holidayChartDict = {}
        # print('#############################################################################################')
        print('New Station ID : %s' % station)
        # print('New station appear time: %s' % newStationBuildDate)
        for nearStationID in nearStationIDList:
            x_workday = []
            x_holiday = []
            workDayDemandChange = [[], []]
            holidayDemandChange = [[], []]
            temperatureChange = [[], []]

            lat1 = float(stationAppearTimeDict[station][1])
            lng1 = float(stationAppearTimeDict[station][2])
            lat2 = float(stationAppearTimeDict[nearStationID][1])
            lng2 = float(stationAppearTimeDict[nearStationID][2])
            recordDistance = haversine(lng1, lat1, lng2, lat2)

            # 前后30天
            for i in range(timeRange * -1, timeRange):
                currentDate = newStationBuildDate + datetime.timedelta(days=i)
                currentDateString = currentDate.strftime(dateTimeMode)

                currentDayDemand = computeDailyDemand(nearStationID, currentDateString)

                # 坏天气
                if isBadDay(currentDateString):
                    if currentDayDemand != EMPTY_DATA:
                        currentDayDemand = BAD_WEATHER

                # 工作日
                if isWorkDay(currentDateString):
                    x_workday.append(currentDateString)
                    if i < 0:
                        workDayDemandChange[0].append(currentDayDemand)
                    else:
                        workDayDemandChange[1].append(currentDayDemand)

                # 休息日
                else:
                    x_holiday.append(currentDateString)
                    if i < 0:
                        holidayDemandChange[0].append(currentDayDemand)
                    else:
                        holidayDemandChange[1].append(currentDayDemand)

                # 计算温度变化
                currentTemperature = temperature[currentDateString]
                if i < 0:
                    temperatureChange[0].append(temperature[currentDateString])
                else:
                    temperatureChange[1].append(temperature[currentDateString])
            ###########################################################################################################
            # 最细粒度的变化数据-daily
            ###########################################################################################################
            dailySaveList = [workDayDemandChange[0], workDayDemandChange[1],
                            holidayDemandChange[0], holidayDemandChange[1],
                            temperatureChange[0], temperatureChange[1], recordDistance]

            ###########################################################################################################
            # 求前后timeRange的日均demand
            ###########################################################################################################
            # 如果全是负值，就直接求均值
            # 如果存在正值，先去掉负值再求均值
            workDayDemandChange[0] = get_normal_mean(workDayDemandChange[0])
            workDayDemandChange[1] = get_normal_mean(workDayDemandChange[1])
            holidayDemandChange[0] = get_normal_mean(holidayDemandChange[0])
            holidayDemandChange[1] = get_normal_mean(holidayDemandChange[1])
            # 去除温度异常值, 然后求均值
            temperatureChange[0] = [e for e in temperatureChange[0] if e != NO_TEM]
            temperatureChange[1] = [e for e in temperatureChange[1] if e != NO_TEM]
            temperatureChange[0] = NO_TEM if temperatureChange[0].__len__() == 0 else np.mean(np.array(temperatureChange[0]))
            temperatureChange[1] = NO_TEM if temperatureChange[1].__len__() == 0 else np.mean(np.array(temperatureChange[1]))
            # 输出字符串
            printStr = "nearStation id :%s, workday[%s, %s], holiday[%s, %s], temperature[%s, %s], disntance: %s m" \
                       % (nearStationID, workDayDemandChange[0], workDayDemandChange[1],
                          holidayDemandChange[0], holidayDemandChange[1], temperatureChange[0],
                          temperatureChange[1], recordDistance)
            # 保存平均数据
            saveList = [workDayDemandChange[0], workDayDemandChange[1],
                        holidayDemandChange[0], holidayDemandChange[1],
                        temperatureChange[0], temperatureChange[1], recordDistance]
            absorptionAnalysis[station + '-' +nearStationID] = [str(e) for e in saveList]
            # 保存daily数据
            absorptionAnalysisDaily[station + '-' +nearStationID] = dailySaveList
            workday[station + '-' +nearStationID] = x_workday
            holiday[station + '-' +nearStationID] = x_holiday

    saveJsonData(absorptionAnalysis, 'absorptionAnalysis.json')
    saveJsonData({'absorptionAnalysisDaily': absorptionAnalysisDaily, 'workday': workday, 'holiday': holiday
                  }, 'absorptionAnalysisDaily.json')