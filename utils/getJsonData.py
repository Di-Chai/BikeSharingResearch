from localPath import jsonPath
import json
import os

def getJsonData(fileName):
    with open(os.path.join(jsonPath, fileName), 'r') as f:
        data = json.load(f)
    return data

def saveJsonData(dataDict, fileName):
    with open(os.path.join(jsonPath, fileName), 'w') as f:
        json.dump(dataDict, f)