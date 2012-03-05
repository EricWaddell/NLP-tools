def processFile(infile,outfile):
    infilestream = open(infile,'r')
    fileData = infilestream.read()
    infilestream.close()
    processed = ''
    fileData = fileData.replace('-hl','')
    fileData = fileData.replace('-tl','')
    fileData = fileData.replace('fw-','')
    fileData = fileData.replace('-nc','')
    fileDataList = fileData.split(' ')
    while '' in fileDataList:
        fileDataList.remove('')
    for taggedWord in fileDataList:
        twList = taggedWord.rsplit('/',1)
        word = twList[0]
        tag = twList[1]
        if '+' in tag:
            tag = 'cmp'
        
        simplifiedWord = word +'/'+ tag + ' '
        processed = processed + simplifiedWord
#    print processed

    outfilestream = open(outfile,'w')
    outfilestream.write(processed)
    outfilestream.close()
    
def processDir(indir, outdir):    
    import os
    for fileName in os.listdir (indir):
        fullInFileName = indir + fileName
        fullOutFileName = outdir + fileName
        processFile(fullInFileName ,fullOutFileName)

#processFile('C:/Documents and Settings/Eric/My Documents/Coding/processedBrown/ca01',
#            'C:/Documents and Settings/Eric/My Documents/Coding/lowStateBrown/ca01')
processDir('C:/Documents and Settings/Eric/My Documents/Coding/processedBrown/',
           'C:/Documents and Settings/Eric/My Documents/Coding/lowStateBrown/')
