def processFile(infile,outfile):
    infilestream = open(infile,'r')
    fileData = infilestream.read()
    infilestream.close()
    st1 = fileData.replace('\n\n\n','\n')
    st1 = st1.replace('\t','')
    st1 = st1.replace('\n\n','\n')
    st1 = st1.replace('\n\t\n','\n')
    stringlist = st1.split('\n')
    for i in stringlist[:]:
        if i.find('/.') == -1 and i.find('/:') == -1:
            stringlist.remove(i)
    processed = ' \n\t'.join(stringlist)
    outfilestream = open(outfile,'w')
    outfilestream.write('\t')
    outfilestream.write(processed)
    outfilestream.close()

def processDir(indir, outdir):    
    import os
    for fileName in os.listdir (indir):
        fullInFileName = indir + fileName
        fullOutFileName = outdir + fileName
        processFile(fullInFileName ,fullOutFileName)

processDir('C:/Documents and Settings/Eric/My Documents/Coding/brown/',
           'C:/Documents and Settings/Eric/My Documents/Coding/processedBrown/')
