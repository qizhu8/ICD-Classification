import pandas as pd
import numpy as np

import ourUtil.myIO as myIO

csvFileName = "../Data/2022 Initial ICD-10-CM Mappings.csv"
df = myIO.loadICDCSVasDF(csvFileName)

# get descriptions
descs = df[myIO.DESCRIPTION]
ICDs = df[myIO.ICDCODE]
ICDNum = len(descs)


hugeSet = {}


for ICD, desc in zip(ICDs, descs):
    left3char = ICD[:3]
    if left3char not in hugeSet:
        hugeSet[left3char] = set()
    hugeSet[left3char] = hugeSet[left3char].union(set(desc.split()))

print("number of distinct left3char ICDs", len(hugeSet))

numOfICDCanBeUniquelyFoundByKeyword = 0
for tgtLeft3 in hugeSet:
    # print("processing {tgtSetId}/{totalNum} {desc}".format(tgtSetId=tgtSetId, totalNum=ICDNum, desc=descs[tgtSetId]))
    orgSet = hugeSet[tgtLeft3]
    for scanLeft3 in hugeSet:
        if tgtLeft3 == scanLeft3:
            continue
        orgSet -= hugeSet[scanLeft3]
    
    # if len(orgSet): # we found one set that has unique 
    if len(orgSet) == 0:
        numOfICDCanBeUniquelyFoundByKeyword += 1
        print("{totalNum} {left3} cannot be uniquely identified by {keywords}".format(
            totalNum = numOfICDCanBeUniquelyFoundByKeyword,
            left3 = tgtLeft3,
            keywords = orgSet.__str__()
        ))