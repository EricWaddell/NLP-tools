def stripTags(infile, outfile):
    f = open(infile,'r')
    evaluationData = f.read()
    f.close()
    evaluationData = evaluationData.replace('./.','./. ')
    evaluationDataList = evaluationData.split(' ')
    while '' in evaluationDataList:
        evaluationDataList.remove('')
    tuplesList = [[]] * len(evaluationDataList)
    for i,v in enumerate(evaluationDataList):
        tuplesList[i] = v.split('/')
    taglessData = ''
    for i in tuplesList:
        taglessData = taglessData + i[0] + ' '
    f = open(outfile,'w')
    f.write(taglessData)
    f.close()

import os
workspace = 'C:/Documents and Settings/Eric/My Documents/Coding/'
inDir = 'processedBrown/'
outDir = 'strippedBrown/'
for fileName in os.listdir(workspace + inDir):
    if fileName.find('01') > 0:
        stripTags(workspace + inDir + fileName, workspace + outDir + fileName)
