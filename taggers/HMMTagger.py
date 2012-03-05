"""
Author: Eric Waddell

A hidden markov model tagger, using the viterbi algorithm for determining
the optimal tag sequence. Unlike the previous taggers which could tag words
individually, this tagger tags sequences of words, in this implimentation,
sentences.

For a better explanation, see chapter 5 of Speech and Language Processing by
Daniel Jurafsky and  James H. Martin. Or possibly wikipedia's page on the
viterbi algorithm

Using an HMM for part of speech tagging is a special case of bayesian inference.
We are looking for a tag sequence of n tags such that the probability that
the tags are correct given the words in the sentence is highest. Using bayes
rule we can transform that to the probability of the words given the tags times
the probability of the tags over the probability of the words. The probability
of the words do not change for any tag sequence however and can be ignored.
Unfortunately this still cannot be computed directly so two assumptions are
made, that the probability of a word appearing is dependent only on its part
of speech tag (independent of words and tags around it). And secondly an n-gram
assumption, (for this model a bigram) such that the probability of a tag
appearing is dependent only on the previous tag. Now the probabilities we are
maximizing are simply the product of the probability of each word given the tag
and the probability of a tag given the previous tag from word 1 to n.

The probability of the word given the tag (the observational likelihood) is
the number of times the tag is assigned to the given word, over the number of
times the tag occurs in general. The probability of the tag given the previous
tag (the transitional probability) is the number of times the first tag is
followed by the second, over the probability of the first tag.

Finally we need a way to compare these probabilities, so we generate a matrix
of words and tags, and the START symbol is given a 1.0 probability. Then for
each tag, you maximize the probability of the previous path, times the
likelihood that you came from the previous state, times the likelihood that the
word would occur at this tag. Then you have a backpointer to the most likely of
the previous tags. This is done for every word in the matrix until the END
symbol is reached. Now going from the END backpointer and through each previous
the most likely tag sequence is obtained.

Probabilities in this model are smoothed for the observational likelihood on
words that do not exist in the model, but _not_ tags not seen in the model.
Primarily because tag probabilities are calculated by the number of times
the previous tag transitions to the current tag, over the number of times
the previous tag is seen. Hence just putting one transition can result
in incredibly large probabilities if the tag has only been seen twice.
Obviously the amount should be more like one over the total number of tags
in the model, but thats something that needs to be researched more to properly
smooth.
"""

#Get paths to directories and the file to tag
import os
cwd = os.getcwd()
f = open(cwd + '/paths.txt','r')
pathList = f.read().split('\n')

workspace = pathList[0]
training = pathList[1]
untagged = pathList[2]
tagged = pathList[3]
fileName = pathList[4]

#
def addSentenceToModel(model, tags, sentence, totalCount):
    wordList = sentence.split(' ')
    while '' in wordList:
        wordList.remove('')
    for i,v in enumerate(wordList):
        wordTagPair = v.rsplit('/',1)
        word = wordTagPair[0]
        tag = wordTagPair[1]
        prevTag = ''
        if i == 0:
            prevTag = 'START'
        else:
            prevWord = wordList[i-1].rsplit('/',1)
            prevTag = prevWord[1]
        if prevTag in tags:
            if tag in tags[prevTag]:
                tags[prevTag][tag] = tags[prevTag][tag] + 1
                tags[prevTag]['count'] = tags[prevTag]['count'] + 1
            else:
                tags[prevTag][tag] = 1
                tags[prevTag]['count'] = tags[prevTag]['count'] + 1
        else:
            tags[prevTag] = {'count':1,tag:1}
        if word in model:
            if tag in model[word]:
                model[word][tag] = model[word][tag] + 1
            else:
                model[word][tag] = 1
        else:
            model[word] = {tag:1}
        if 'TOTALCOUNT' in model:
            model['TOTALCOUNT'] = model['TOTALCOUNT']+1
        else:
            model['TOTALCOUNT'] = 1
    if tag in tags:
        if 'END' in tags[tag]:
            tags[tag]['END'] = tags[tag]['END'] + 1
            tags[tag]['count'] = tags[tag]['count'] + 1
        else:
            tags[tag]['END'] = 1
            tags[tag]['count'] = tags[tag]['count'] + 1
    else:
        tags[tag] = {'END':1,'count':1}
    if 'END' in tags:
        tags['END']['count'] = tags['END']['count'] + 1
    else:
        tags['END'] = {'count':1}

#Unlike the previous taggers, addFileToModel no longer does the brunt of the
#work. Since sentences instead of words are tagged now, the model also adds
#each sentences to the model individually.
def addFileToModel(model, tags, file, totalCount):
    f = open(file)
    fileData = f.read()
    f.close() 
    fileDataList = fileData.split('\n')
    for sentence in fileDataList:
        addSentenceToModel(model, tags, sentence, totalCount)

#Build model has the same progress notification as all the other taggers,
#printing a * each time 1/20th of the files is loaded. Besides that it just
#passes in each file to the addFileToModel function
def buildModel(model, tags, totalCount):
    modelDir = os.listdir(workspace + trainingData)
    notifyUser = 0
    notifyLimit = len(modelDir)/20
    for fileName in modelDir:
        if fileName.find('01') == -1:
            addFileToModel(model, tags,workspace + trainingData + fileName, totalCount)
            notifyUser = notifyUser + 1
            if notifyUser == notifyLimit:
                notifyUser = 0
                print '*',
    print '*'


def tagSentence(model, tags, viterbi, sentence):
    tagList = tags.keys()
    for i,tag in enumerate(tagList):
        if tag == 'START':
            viterbi[str(i) +',0'] = [1.0,'-1,-1']
        else:
            viterbi[str(i) +',0'] = [0.0,'-1,-1']
    sentenceList = sentence.split(' ')
    while '' in sentenceList:
        sentenceList.remove('')
    print sentenceList
    for i,word in enumerate(sentenceList):
        for j,tag in enumerate(tagList):
            best = 0
            backPointer = '0,0'
            for l, paths in enumerate(tagList):
                likelihood = 0.0
                prevPathProbAndPointer = viterbi[str(l)+','+str(i)]
                prevPathProb = prevPathProbAndPointer[0]
                prevTag = tagList[l]
                currentTag = tagList[j]
                if currentTag in tags[prevTag]:
                    tranProb = float(tags[prevTag][currentTag])/float(tags[prevTag]['count'])
                else:
                    tranProb = 0
                if word in model:
                    if currentTag in model[word]:
                        obsLikelihood = float(model[word][currentTag])/float(tags[currentTag]['count'])
                    else:
                        obsLikelihood = 0
                else:
                    obsLikelihood = 1.0/float(tags[currentTag]['count'])
                likelihood = prevPathProb * tranProb * obsLikelihood * 100
                if float(likelihood) > float(best):
                    best = likelihood
                    backPointer = str(l)+','+str(i)
            viterbi[str(j)+','+str(i+1)] = [best,backPointer]
    for j,tag in enumerate(tagList):
        prevTag = tag
        currentTag = 'END'
        if currentTag in tags[prevTag]:
            tranProb = float(tags[prevTag][currentTag])/float(tags[prevTag]['count'])
        else:
            tranProb = 0
        obsLikelihood = 1
        prevPathProbAndPointer = viterbi[str(j)+','+str(i+1)]
        prevPathProb = prevPathProbAndPointer[0]
        likelihood = prevPathProb * tranProb * obsLikelihood
        if likelihood > best:
            best = likelihood
            backPointer = str(j)+','+str(i+1)
    stack = []
    viterbiTuple = []
    backPointerList = backPointer.split(',')
    wordIndex = int(backPointerList[1])
    tagIndex = int(backPointerList[0])
    while wordIndex > 0:
        taggedWord = sentenceList[wordIndex-1] + '/' + tagList[tagIndex]
        stack.append(taggedWord)
        viterbiTuple = viterbi[str(tagIndex)+','+str(wordIndex)]
        backPointerList = viterbiTuple[1].split(',')
        wordIndex = int(backPointerList[1])
        tagIndex = int(backPointerList[0])
    stack.reverse()
    taggedSentence = ' '.join(stack) + '\n'
    return taggedSentence

model = {}
tags = {}
viterbi = {}
totalCount = 0
buildModel(model, tags, totalCount)
print tags.keys()
f = open(workspace + untagged + fileName,'r')
untaggedData = f.read()
f.close()
untaggedDataList = untaggedData.split('\n')
taggedData = ''
while '' in untaggedDataList:
    untaggedDataList.remove('')
for sentence in untaggedDataList:
    taggedData = taggedData + tagSentence(model, tags, viterbi, sentence) + ' '
print taggedData

f = open(workspace + tagged + fileName, 'w')
f.write(taggedData)
f.close()

