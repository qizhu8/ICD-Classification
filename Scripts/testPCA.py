from ourUtil.PCAICD.myPCAClass import MyPCAClass

csvFileName = "../Data/2022 Initial ICD-10-CM Mappings.csv"
myPCA = MyPCAClass(csvFileName=csvFileName)

myPCA.ICDDescs2Vector()
myPCA.PCA()