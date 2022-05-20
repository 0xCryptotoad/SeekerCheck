from importlib.metadata import metadata
from operator import truediv
import requests
import json
import os
import time

atWarIds = []
lastIdListTimestamp = None
atWarFileName = "idList.txt"
hasReturnedFileName = "hasReturned.txt"
seekerMetadata = {}

def saveSeekerIds(seekerIds, fileName):
    with open(fileName, "w") as idFile:
        idFile.write("\n".join(seekerIds))

def syncChanges(seekerInfo):
    global atWarFileName
    global hasReturnedFileName
    hasReturned = loadIds(hasReturnedFileName)
    atWar = []
    hasChanged = False
    for seekerId, seekerReturned in seekerInfo.items():
        if seekerReturned: 
            hasChanged = True
            hasReturned.append(seekerId)
        else: 
            atWar.append(seekerId)
    if hasChanged:
        saveSeekerIds(hasReturned, hasReturnedFileName)
        saveSeekerIds(atWar, atWarFileName)
        print(f"These seekers have returned from war: {hasReturned}")


def checkSeeker(seekId):
    hasChanged = False
    response = requests.get(f"https://api.seekers.xyz/seeker/{seekId}")
    if response.status_code == 200:
        hasChanged = "beacon" not in response.text
        seekerMetadata[seekId] = response.json()
    return hasChanged


def loadIds(filename: str):
    if not os.path.exists(filename):
        return []
    ids = []
    idFile = open(filename, "r")
    with open(filename, "r") as idFile:
        ids = [seekId.strip() for seekId in idFile.readlines() if seekId.strip() != ""]
    return ids

def main():
    global lastIdListTimestamp
    global atWarIds
    #ids = loadIds("idList.txt")
    currentChangeTimestamp = os.stat(atWarFileName).st_mtime 
    if not lastIdListTimestamp or currentChangeTimestamp != lastIdListTimestamp:
        atWarIds = loadIds(atWarFileName)
        lastIdListTimestamp = currentChangeTimestamp
    seekerChanges = {}
    for seekId in atWarIds:
        hasChanged = checkSeeker(seekId)
        seekerChanges[seekId] = hasChanged
    syncChanges(seekerChanges)
    print("Checked for seekers at war :)")
    time.sleep(300)









if __name__ == "__main__":
    while True: 
        main()

