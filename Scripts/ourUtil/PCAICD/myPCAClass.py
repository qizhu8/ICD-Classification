import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import ourUtil.myIO as myIO


class MyPCAClass:

    def __init__(self, csvFileName, visualDim=3, ICDLeftnChar=3) -> None:
        self.csvFileName = csvFileName

        # initialize some other parameters
        self._isColorGen = False  # whether different colors has been generated
        self.nClass = 0  # total number of classes ICD will be classified into
        # we use the left ICDLeftnChar characters to classify ICDs into big classes.
        self.ICDLeftnChar = ICDLeftnChar
        self.visualDim = visualDim

        # load csv
        self.df = myIO.loadICDCSVasDF(self.csvFileName)

    def ICDDescs2Vector(self):
        """
        This function will turn each ICD description to a word vector, aka, embedding.
        We also classifiy ICD into classes by ICDCode's left 3 characters
        """

        # collect the bag of all shown words
        self.bagOfWord = set()
        self.bagOfICDClass = set()

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

            # add ICD to their class based on the left 3 or 4 characters
            self.bagOfICDClass.add(self._getICDPrefix(ICD))

        # build up the bi-directional mapping between ICDClassId and ICDPrefix
        self.classID2ICD = {}
        self.ICD2ClassId = {}
        for classId, ICDPrefix in enumerate(self.bagOfICDClass):
            self.classID2ICD[classId] = ICDPrefix
            self.ICD2ClassId[ICDPrefix] = classId
        self.nClass = len(self.bagOfICDClass)
        self._genColor()  # gen nClass number of different colors



    def PCA(self, cleanRun=False):
        """
        Applying sklearn PCA module to reduce the dimension from self.keywordNum to 2 for visualization, and plot.
        """
        filename = "PCA_{}d.npy".format(self.visualDim)
        if not cleanRun and os.path.isfile(filename):
            principalComponents = np.load(filename)
            print("load store PCA result from file", filename)
        else:
            print("Doing PCA. This may take some time")
            # compuse the ICDVector into a big matrix
            ICDPCAList = []

            for ICD in self.df[myIO.ICDCODE]:
                ICDPCAList.append(self.ICDVector[ICD])

            ICDPCAMatrix = np.stack(ICDPCAList, axis=0)
            print(ICDPCAMatrix.shape)

            pca = PCA(n_components=self.visualDim, svd_solver='full')
            # pca.fit(ICDPCAMatrix)
            principalComponents = pca.fit_transform(ICDPCAMatrix)

            # save PCA results for fast load
            np.save(filename, principalComponents)

        print("principalComponents", principalComponents.shape)
        return principalComponents

    
    def plotPCAResult(self, principalComponents, focusLabelSet={}, imshow=True, showLegend=False):
        """Ploting"""
        plotname = "PCA_{}d.png".format(self.visualDim)

        if self.visualDim == 2:
            ax = plt.axes()
        elif self.visualDim ==3:
            ax = plt.axes(projection ='3d')

        pointsInClass = {}
        for ICDId in range(principalComponents.shape[0]):
            label = self._getICDPrefix(self.df[myIO.ICDCODE][ICDId])
            if label not in pointsInClass:
                pointsInClass[label] = []
            pointsInClass[label].append(principalComponents[ICDId, :])

        for label in pointsInClass:
            if focusLabelSet and label not in focusLabelSet:
                continue
            classId = self._getClassIDFromICD(label)
            R, G, B = self.getColor(classId)

            xdata = [data[0] for data in pointsInClass[label]]
            ydata = [data[1] for data in pointsInClass[label]]

            if self.visualDim == 2:
                ax.plot(
                    xdata, ydata, '*', color=(R, G, B), label=label)
            elif self.visualDim == 3:
                zdata = [data[2] for data in pointsInClass[label]]
                ax.plot(xdata, ydata, zdata, '*', color=(R, G, B), label=label)
        
        if showLegend:
            plt.legend()

        plt.savefig(plotname)
        if imshow:
            plt.show()
    
    def kmeanThenPCA(self):
        kmeanDict = {}
        for ICD, desc in zip(self.df[myIO.ICDCODE], self.df[myIO.DESCRIPTION]):
            label = self._getICDPrefix(ICD)
            if label not in kmeanDict:
                kmeanDict[label] = []
            kmeanDict[label].append(self.ICDVector[ICD])
        
        labelList = list(kmeanDict.keys())
        kmeanMatrix = []
        for label in labelList:
            kmeanMatrix.append(np.mean(kmeanDict[label], axis=0))
        kmeanMatrix = np.stack(kmeanMatrix, axis=0)

        # apply PCA to kmeanMatrix
        pca = PCA(n_components=self.visualDim)
        principleComponents = pca.fit_transform(kmeanMatrix)
        print("kmean PCA shape", principleComponents.shape)

        # visualize
        figureName = "PCA_kmean_{}d.png".format(self.visualDim)

        if self.visualDim == 2:
            ax = plt.axes()
        elif self.visualDim ==3:
            ax = plt.axes(projection ='3d')

        for labelId, label in enumerate(labelList):
            R, G, B = self.getColor(labelId)
            if self.visualDim == 2:
                ax.plot(principleComponents[labelId, 0], principleComponents[labelId, 1], '*', color=(R, G, B), label=label)
            elif self.visualDim == 3:
                ax.plot(principleComponents[labelId, 0], principleComponents[labelId, 1], principleComponents[labelId, 2], '*', color=(R, G, B), label=label)

        plt.show()


    def _getICDPrefix(self, ICDCode):
        if len(ICDCode) >= self.ICDLeftnChar:
            return ICDCode[:self.ICDLeftnChar]
        else:
            return ICDCode + "0"*(self.ICDLeftnChar - len(ICDCode))

    def _getICDFromClassID(self, classId):
        return self.classID2ICD[classId]

    def _getClassIDFromICD(self, ICDCode):
        ICDPrefix = self._getICDPrefix(ICDCode)
        return self.ICD2ClassId[ICDPrefix]

    def _genColor(self):
        """
        Generate nClass number of different colors.
        nClass is the number of different colors we need to generate
        """
        if not self._isColorGen:
            colors = np.linspace(0, 255*255*255, self.nClass)
            colors = np.asarray(colors, dtype=np.int)
            np.random.seed(0)
            self.RList = (colors % 255) / 255
            self.GList = ((colors // 255 ) % 255) / 255
            self.BList = ((colors // 255 // 255 )% 255) / 255
            self._isColorGen = True

    def getColor(self, classId):
        if not self._isColorGen:
            self._genColor()
        return self.RList[classId], self.GList[classId], self.BList[classId]
