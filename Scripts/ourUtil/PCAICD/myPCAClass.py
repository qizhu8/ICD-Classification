import numpy as np
import ourUtil.myIO as myIO
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

class MyPCAClass:

    def __init__(self, csvFileName) -> None:
        self.csvFileName = csvFileName

        # load csv
        self.df = myIO.loadICDCSVasDF(self.csvFileName)
    
    def ICDDescs2Vector(self):
        """
        This function will turn each ICD description to a word vector, aka, embedding.
        """

        # collect the bag of all shown words
        self.bagOfWord = set()

        for desc in self.df[myIO.DESCRIPTION]:
            desc_clean = myIO.cleanText(desc)
            desc_clean_wordList = desc_clean.strip().lower().split()
            self.bagOfWord = self.bagOfWord.union(set(desc_clean_wordList))

        self.keywordNum = len(self.bagOfWord)
        print("number of keywords in set", self.keywordNum)

        # turn each keyword into dictionary
        self.keyword2IdDict = {}
        self.Id2KeywordDict = {}
        for keywordId, keyword in enumerate(self.bagOfWord):
            self.keyword2IdDict[keyword] = keywordId
            self.Id2KeywordDict[keywordId] = keyword
        
        # turn each description to a vector
        self.ICDVector = {}
        for ICD, desc in zip(self.df[myIO.ICDCODE], self.df[myIO.DESCRIPTION]):
            vector = np.zeros((self.keywordNum,))
            desc_clean = myIO.cleanText(desc)
            desc_clean_wordList = desc_clean.strip().lower().split()
            for keyword in desc_clean_wordList:
                wordId = self.keyword2IdDict[keyword]
                vector[wordId] = 1
            self.ICDVector[ICD] = vector
    
    def PCA(self):
        """
        Applying sklearn PCA module to reduce the dimension from self.keywordNum to 2 for visualization.
        """

        # compuse the ICDVector into a big matrix
        ICDPCAList = []

        for ICD in self.df[myIO.ICDCODE]:
            ICDPCAList.append(self.ICDVector[ICD])
        
        ICDPCAMatrix = np.stack(ICDPCAList, axis=0)
        print(ICDPCAMatrix.shape)

        pca = PCA(n_components=2, svd_solver='full')
        # pca.fit(ICDPCAMatrix)
        principalComponents = pca.fit_transform(ICDPCAMatrix)
        principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

        print("principalComponents", principalComponents.shape)
        plt.plot(principalComponents[:, 0], principalComponents[:, 1], '*')
        plt.show()





