from utils.getJsonData import *
from utils.dayType import *
from utils.symbols import EMPTY_DATA
from visualization.TimeSeries import timeSeries
from dateutil.parser import parse

stationAppearTimeDict = getJsonData('stationAppearTime.json')

absorptionAnalysis = getJsonData('absorptionAnalysis.json')
absorptionAnalysisDailyDict = getJsonData('absorptionAnalysisDaily.json')

absorptionAnalysisDaily = absorptionAnalysisDailyDict['absorptionAnalysisDaily']
workdayDict = absorptionAnalysisDailyDict['workday']
holidayDict = absorptionAnalysisDailyDict['holiday']

threshold = 0.2

# obvious
obviousCounter = 0
obviousStation = []
obviousNNStation = []
obviousPairStation = []
# unchanged
unchangedCounter = 0
unchangedPairStation = []
# reversed
reversedCounter = 0
reversedPairStation = []
dateTimeMode = '%Y-%m-%d'
# all station
allPairStations = []
print('Total pair-station number : %s' % absorptionAnalysis.__len__())

def check_list_negative(valueList):
    negative = False
    for e in valueList:
        if float(e) < 0:
            negative = True
            break
    return negative

stationInBuildPhaseNumber = 0
stationWithAllInformation = 0
for pairStation, contentList in absorptionAnalysis.items():
    # 去除信息有缺失的
    if check_list_negative(contentList[0:4]):
        continue
    stationWithAllInformation += 1
    stationID = pairStation.split('-')
    # 去除在三个扩建时期的
    if inBuildPhase(stationAppearTimeDict[stationID[0]][0]):
        stationInBuildPhaseNumber += 1
        continue
    allPairStations.append(pairStation)
    work0 = float(contentList[0])
    work1 = float(contentList[1])
    holiday0 = float(contentList[2])
    holiday1 = float(contentList[3])
    t0 = float(contentList[4])
    t1 = float(contentList[5])
    d = contentList[6]
    tChange = (t1 - t0)

    R = (float(work1) - float(work0)) / float(work0)

    if R <= -threshold:
        obviousCounter += 1
        # store information
        obviousStation.append(stationID[0])
        obviousNNStation.append(stationID[1])
        obviousPairStation.append(pairStation)
        # print information
        # print('****************************************')
        # print('new station %s' % stationID[0])
        # print('near station %s' % stationID[1])
        # print('workday before/after     : %.3f / %.3f' % (work0, work1))
        # print('holiday before/after     : %.3f / %.3f' % (holiday0, holiday1))
        # print('temperature before/after : %.3f / %.3f' % (t0, t1))
        # print('distance : ', d)
    if R > -threshold and R < threshold:
        unchangedCounter += 1
        unchangedPairStation.append(pairStation)
    if R >= threshold:
        reversedCounter += 1
        reversedPairStation.append(pairStation)

print('%s stations have all the information' % stationWithAllInformation)

print('%s stations appeared in building phase' % stationInBuildPhaseNumber)

print('reversedCounter:', reversedCounter,
      'unchangedCounter:', unchangedCounter,
      'obviousCounter:', obviousCounter)

saveDict = {'obviousPairStation': obviousPairStation,
            'unchangedPairStation': unchangedPairStation,
            'reversedPairStation': reversedPairStation,
            'allPairStation': allPairStations}

saveJsonData(saveDict, 'checkStation.json')


