import pandas as pd

DESCRIPTION = "Description"
ICDCODE = "Diagnosis\nCode"
HCCV24 = "CMS-HCC\nModel\nCategory\nV24"

def loadICDCSVasDF(csvFileName):
    df = pd.read_csv(csvFileName, delimiter=',', skiprows=3, skipfooter=7)
    return df



def cleanText(text:str):
    """
    Remove special characters, such as ",", "\", "["
    """
    text.replace(',', '') 
    text.replace('[', '') 
    text.replace(']', '') 
    text.replace('.', '') 
    text.replace('!', '')
    return text