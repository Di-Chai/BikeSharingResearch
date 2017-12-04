# coding:utf-8
from localPath import *
from utils.getJsonData import *
from utils.symbols import EMPTY_DATA
from visualization.TimeSeries import timeSeries
from dateutil.parser import parse
import datetime
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats

stationAppearTimeDict = getJsonData('stationAppearTime.json')
absorptionAnalysis = getJsonData('absorptionAnalysis.json')
absorptionAnalysisDailyDict = getJsonData('absorptionAnalysisDaily.json')
absorptionAnalysisDaily = absorptionAnalysisDailyDict['absorptionAnalysisDaily']
workdayDict = absorptionAnalysisDailyDict['workday']
holidayDict = absorptionAnalysisDailyDict['holiday']

demandThreshold = 5

def check_list_positive(valueList):
    positive = False
    for e in valueList:
        if e > 0:
            positive = True
            break
    return positive

def get_normal_mean(valueList):
    if check_list_positive(valueList):
        valueListPositive = [e for e in valueList if e > 0]
        valueListMean = np.mean(valueListPositive)
    else:
        valueListMean = 0
        if -1 in valueList:
            valueListMean += -1
        if -2 in valueList:
            valueListMean += -2
    return float('%.2f'%valueListMean)



dateTimeMode = '%Y-%m-%d'

# 画柱状图
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2-0.3, 1.0 + height, '%s' % float(height))

def weeklyLineChart(appearTime, workday, workday_y, pairStation, savePath, pValue):
    if pValue == 'error':
        return
    # 找到前四周后四周的时间范围
    weekTimeRange = []
    weekTimeRangeBefore = []
    weekTimeRangeAfter = []
    currentDate = appearTime
    currentDate = currentDate + datetime.timedelta(days=-1)
    for i in range(4):
        weekTime = []
        while currentDate.weekday() != 4:
            currentDate = currentDate + datetime.timedelta(days=-1)
        for i in range(5):
            weekTime.append(currentDate.strftime(dateTimeMode))
            currentDate = currentDate + datetime.timedelta(days=-1)
        weekTimeRangeBefore.insert(0, weekTime)
        weekTimeRange.insert(0, weekTime)
    currentDate = appearTime
    currentDate = currentDate + datetime.timedelta(days=1)
    for i in range(4):
        weekTime = []
        while currentDate.weekday() != 0:
            currentDate = currentDate + datetime.timedelta(days=1)
        for i in range(5):
            weekTime.append(currentDate.strftime(dateTimeMode))
            currentDate = currentDate + datetime.timedelta(days=1)
        weekTimeRangeAfter.append(weekTime)
        weekTimeRange.append(weekTime)
    # add together
    weeklyValue = [[],[],[],[],[],[],[],[]]
    for dateCounter in range(workday.__len__()):
        date = workday[dateCounter]
        dateString = date.strftime(dateTimeMode)
        for i in range(8):
            if dateString in weekTimeRange[i]:
                weeklyValue[i].append(workday_y[dateCounter])
    for i in range(weeklyValue.__len__()):
        weeklyValue[i] = get_normal_mean(weeklyValue[i])

    plotFlag = False
    for e in weeklyValue:
        if e > demandThreshold:
            plotFlag = True
    if plotFlag:
        plt.xlabel('week')
        plt.ylabel('workday daily demand (group by week)')
        plt.title('Demand Change of %s, %s, %s' % (pairStation, appearTime.strftime(dateTimeMode), pValue))
        rect = plt.bar(left=range(1,9), height=tuple(weeklyValue), width=0.2, align="center", color="orange")
        plt.ylim(0, max(weeklyValue)+50)
        plt.xlim(0, 9)
        autolabel(rect)
        # plt.show()
        plt.savefig(os.path.join(savePath, '%s.png' % pairStation))
        plt.close()

def drawStations(pairStationList):
    for pairStation in pairStationList:
        stationID = pairStation.split('-')
        dailyDemandChange = absorptionAnalysisDaily[pairStation]
        workday = workdayDict[pairStation]
        holiday = holidayDict[pairStation]
        appearTime = parse(stationAppearTimeDict[stationID[0]][0])
        # # 保存最细粒度的变化数据
        #         dailySaveList = [workDayDemandChange[0], workDayDemandChange[1],
        #                         holidayDemandChange[0], holidayDemandChange[1],
        #                         temperatureChange[0], temperatureChange[1], recordDistance]
        workday_y0 = dailyDemandChange[0]
        workday_y1 = dailyDemandChange[1]
        # 先不分析节假日
        # holiday_y0 = dailyDemandChange[2]
        # holiday_y1 = dailyDemandChange[3]
        workday_y = []
        for e in workday_y0:
            workday_y.append(e)
        for e in workday_y1:
            workday_y.append(e)
        workday = [parse(e) for e in workday]

        workday_y0 = [e for e in workday_y0 if e > 0]
        workday_y1 = [e for e in workday_y1 if e > 0]
        if workday_y0.__len__() > 1 and workday_y1.__len__() > 1:
            ttestResult = stats.ttest_ind(workday_y1, workday_y0, equal_var=False)
            pValue = ttestResult[1]
            ttestResultString = '%.2f,%s' % (ttestResult[0], pValue)
            if pValue < 0.1 and ttestResult[0] < 0:
                savePath = ObviousPngPath
            elif pValue < 0.1 and ttestResult[0] > 0:
                savePath = ReversePngPath
            else:
                savePath = UnchangedPngPath
            weeklyLineChart(appearTime, workday, workday_y, pairStation, savePath, ttestResultString)



if __name__ == '__main__':

    pngPathList = [ObviousPngPath, UnchangedPngPath, ReversePngPath]
    for path in pngPathList:
        pngFileNameList = [e for e in os.listdir(path) if e.endswith(".png")]
        for e in pngFileNameList:
            os.remove(os.path.join(path, e))

    checkStationDict = getJsonData('checkStation.json')
    # obviousPairStation = checkStationDict['obviousPairStation']
    # reversePairStation = checkStationDict['reversedPairStation']
    # unChangedPairStation = checkStationDict['unchangedPairStation']
    allPairStation = checkStationDict['allPairStation']

    drawStations(allPairStation)




