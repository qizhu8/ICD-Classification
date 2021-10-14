from ourUtil.PCAICD.myPCAClass import MyPCAClass

csvFileName = "../Data/2022 Initial ICD-10-CM Mappings.csv"
myPCA = MyPCAClass(csvFileName=csvFileName, visualDim=3, ICDLeftnChar=3)

myPCA.ICDDescs2Vector()

myPCA.kmeanThenPCA()

# principleResult = myPCA.PCA(cleanRun=True) #
principleResult = myPCA.PCA(cleanRun=False) #
# myPCA.plotPCAResult(principleResult, imshow=False)
# myPCA.plotPCAResult(principleResult, focusLabelSet={"F", "E", "C"}, imshow=False)

myPCA.plotPCAResult(principleResult, focusLabelSet={"E08", "E09", "E10", "E11", "E12", "E13", "C51", "C50", "A01", "F10", "F11"}, showLegend=True, imshow=True)

# focusLabelSet = set()
# for cancerId in range(51, 100):
#     focusLabelSet.add("C"+str(cancerId))
# myPCA.plotPCAResult(principleResult, focusLabelSet=focusLabelSet, showLegend=True, imshow=True)
