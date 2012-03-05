"""
Author: Eric Waddell

A simple probability based tagger. This tagger is also quite simplistic,
but it does require some training unlike the trivialTagger. Training data
is analyzed by the tagger to create a table containing the probability of a
given word being each part of speech. The part of speech with the highest
probability is then emitted for each word.

My current corpus is in the format \t<Sentence>\n for each sentence in
each document. This method of building the model tags words at the beginning
of a sentence different from words in the middle of a sentence (they have \t
prepended to the word). I have maintained this functionality, instead of tagging
all words that are equivalent went lower() is applied to them, for two reasons.

One, these words would tag differently assuming correct English sentence
structure because they are capitalized, and capitalization cannot be ignored
due to certain proper nouns as compared to regular nouns (e.g. Polish vs.
polish). This might no longer be the case if a corpus where sentences do not
begin capitalized (e.g. informal internet messaging conversations).

Secondly, there is a reasonable chance that there is some information gained
from a word being used to begin a sentence and tagging them seperately from
words in the middle or end of sentences would possibly lead to more accurate
tagging. Something to test for later perhaps.
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

#Start by opening the file and splitting on spaces and removing extraneous empty
#strings. Then go through each word and split it to seperate the tag. Finally
#add the word to the nested dictionary structure. First level contains words
#mapped to dictionaries, Second level is tags mapped to counts.
def addFileToModel(model, file):
    trainingFile = open(file)
    trainingData = trainingFile.read()
    trainingFile.close()
    trainingDataList = trainingData.split(' ')
    while '' in trainingDataList:
        trainingDataList.remove('')
    for taggedWord in trainingDataList:
        wordTagPair = taggedWord.rsplit('/',1)
        word = wordTagPair[0]
        tag = wordTagPair[1]
        if word in model:
            if tag in model[word]:
                model[word][tag] = model[word][tag] + 1
            else:
                model[word][tag] = 1
        else:
            model[word] = {tag:1}

#Since the work is now done in the addFileToModel function, the build model
#function just lists the files in the directory and adds each one to the model
#using the above function. Files including '01' are not added to the model
#so that those files can be used for testing. There is also a little progress
#bar that updates the user every time 1/20th of the files are processed.
#It shouldn't be necessary on any sort of modern hardware for this model, but
#its there in case this model is on something really old, or is using a corpus
#with a few orders of magnitude more words.
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
    print '*'

#tagWord grabs the dictionary of tags for the given word to tag and then
#iterates down the dictionary until the tag with the highest probability is
#found and returns it.
def tagWord(model, word):
    max = ''
    maxCount = 0
    if word in model:
        tagDict = model[word]
        for key in tagDict.keys():
            if tagDict[key] > maxCount:
                maxCount = tagDict[key]
                max = key
        return max
    else:
        return 'nn'
            
#Build the model, read and split the data to tag while removing empty strings.
#Then tag the word and write everything to the destination file
model = {}
buildModel(model)
fileToTag = open(workspace + untagged + fileName,'r')
untaggedData = fileToTag.read()
fileToTag.close()
untaggedDataList = untaggedData.split(' ')
taggedData = ''
tag = 'nn'
while '' in untaggedDataList:
    untaggedDataList.remove('')
for word in untaggedDataList:
    taggedData = taggedData + word + '/' + tagWord(model, word) + ' '
taggedFile = open(workspace + tagged + fileName, 'w')
taggedFile.write(taggedData)
taggedFile.close()
