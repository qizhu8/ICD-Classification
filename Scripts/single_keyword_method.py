import pandas as pd
import numpy as np


csvFileName = "../Data/2022 Initial ICD-10-CM Mappings.csv"
DESCRIPTION = "Description"
ICDCODE = "Diagnosis\nCode"

df = pd.read_csv(csvFileName, delimiter=',', skiprows=3, skipfooter=7)

# get descriptions
descs = df[DESCRIPTION]
ICDs = df[ICDCODE]
ICDNum = len(descs)

# create ICDNum numbers of sets
hugeSets = [None for _ in range(ICDNum)]

# turn each ICD description into its set
for idx in range(ICDNum):
    desc = descs[idx]

    hugeSets[idx] = set(desc.split())

# do set minus
numOfICDCanBeUniquelyFoundByKeyword = 0
for tgtSetId in range(ICDNum):
    # print("processing {tgtSetId}/{totalNum} {desc}".format(tgtSetId=tgtSetId, totalNum=ICDNum, desc=descs[tgtSetId]))
    orgSet = set(descs[tgtSetId].split())
    for scanSetId in range(ICDNum):
        if tgtSetId == scanSetId:
            continue
        orgSet -= hugeSets[scanSetId]
    
    if len(orgSet): # we found one set that has unique 
        numOfICDCanBeUniquelyFoundByKeyword += 1
        print("{totalNum} {ICD} {desc} can be uniquely identified by {keywords}".format(
            totalNum = numOfICDCanBeUniquelyFoundByKeyword,
            ICD = ICDs[tgtSetId],
            desc = descs[tgtSetId],
            keywords = orgSet.__str__()
        ))

print("We found {} number of ICDs that can be uniquely discriminated by a special keyword".format(numOfICDCanBeUniquelyFoundByKeyword))