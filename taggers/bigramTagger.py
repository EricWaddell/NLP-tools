"""
Author: Eric Waddell

A less simple probability based tagger. This method considers the words
surrounding (in this implementation just the first word preceeding the word
to be tagged) a given word to give context to the types of tags to be
considered. As a small example, consider the sentence "I asked him to book
me a flight." 'book' can be either a verb (as in the example) or a noun like
those things full of paper we love. The simple probability tagger would likely
tag book as a noun given a reasonable corpus, because people are more likely to
mention books than reserving something. This tagger however would have the
counts of the bigrams (groups of two words) involving book. 'to book' is much
more likely to mean that book is a verb now, because 'to' is a preposition*
which are followed by verbs, articles, and Proper nouns in grammatical Enlish.

*The brown corpus tags 'to' as 'to' when used as an infinitive marker, which
technically means it is not always a preposition
"""

#Grab the paths to all the directories/files
import os
cwd = os.getcwd()
f = open(cwd + '/paths.txt','r')
pathList = f.read().split('\n')

workspace = pathList[0]
trainingData = pathList[1]
untagged = pathList[2]
tagged = pathList[3]
fileName = pathList[4]

#For each file the typical reading, splitting on spaces, removing empty strings
#occurs. Then for each word we construct a bigram consisting of the previous
#word and the current word with a space between them. If it is the first word
#the symbol START is used instead. Then both the bigram and the word are put
#into the model and the count of the tag is incremented. 
def addFileToModel(model, file):
    trainingFile = open(file)
    trainingData = trainingFile.read()
    trainingFile.close()
    trainingDataList = trainingData.split(' ')
    while '' in trainingDataList:
        trainingDataList.remove('')
    for i,v in enumerate(trainingDataList):
        wordTagPair = v.split('/')
        word = wordTagPair[0]
        tag = wordTagPair[1]
        bigram = ''
        if i == 0:
            bigram = 'START ' + word
        else:
            prevPair = fileDataList[i-1].split('/')
            bigram = prevPair[0] + ' ' + word
        if bigram in model:
            if tag in model[bigram]:
                model[bigram][tag] = model[bigram][tag] + 1
            else:
                model[bigram][tag] = 1
        else:
            model[bigram] = {tag:1}
        if word in model:
            if tag in model[word]:
                model[word][tag] = model[word][tag] + 1
            else:
                model[word][tag] = 1
        else:
            model[word] = {tag:1}

#Similar to the other taggers, the directory is listed and each file without
#the string 01 is added to the model. A progress update shows each 1/20th
#of the directory as a '*'
def buildModel(model):
    modelDir = os.listdir(workspace + trainingData)
    notifyUser = 0
    notifyLimit = len(modelDir)/20
    for fileName in modelDir:
        if fileName.find('01') == -1:
            addFileToModel(model, workspace + trainingData + fileName)
            notifyUser = notifyUser + 1
            if notifyUser == notifyLimit:
                notifyUser = 0
                print '*',

#Word tagging is just the slightest bit more complex than the simple probability
#tagger. First the program searches for the bigram and if it exists, returns the
#tag with the highest probability given the bigram. Otherwise a search for the
#word itself is done and the tag with the highest probablity given the word is
#returned. Failing that, noun is returned.
def tagWord(model, bigram):
    max = ''
    maxCount = 0
    if bigram in model:
        tagDict = model[bigram]
        for key in tagDict.keys():
            if tagDict[key] > maxCount:
                maxCount = tagDict[key]
                max = key
        return max
    else:
        pair = bigram.split(' ')
        if pair[1] in model:
            tagDict = model[pair[1]]
            for key in tagDict.keys():
                if tagDict[key] > maxCount:
                    maxCount = tagDict[key]
                    max = key
            return max
        else:
            return 'nn' 

#Finally we get everything moving, build the model, read the data we need to
#tag, split on spaces and remove empty strings, then create bigrams for each
#word we are attempting to tag, and have tagWord tag them. Write the result
#to the destination file
model = {}
buildModel(model)
f = open(workspace + untagged + fileName,'r')
untaggedData = f.read()
f.close()
untaggedDataList = untaggedData.split(' ')
taggedData = ''
while '' in untaggedDataList:
    untaggedDataList.remove('')
for i,word in enumerate(untaggedDataList):
    if i == 0:
        bigram = 'START ' + word
    else:
        bigram = untaggedDataList[i-1] + ' ' + word
    taggedData = taggedData + word + '/' + tagWord(model, bigram) + ' '
f = open(workspace + tagged + fileName, 'w')
f.write(taggedData)
f.close()
