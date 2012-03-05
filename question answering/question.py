import os
from string import maketrans
model = {}
sentenceProbs = {}
counts = 0
cwd = os.getcwd()
questionFile = open(cwd + '/sentence','r')
question = questionFile.read()
questionFile.close()

corpusFile = open(cwd + '/corpus','r')
corpus = corpusFile.read()
corpusFile.close()

intab = ':,."?!'
outtab = '      '
trantab = maketrans(intab,outtab)

sentences = corpus
sentences = sentences.replace('\n','.')
sentenceList = sentences.split('.')
while '' in sentenceList:
    sentenceList.remove('')
corpus = corpus.translate(trantab)
corpusList = corpus.split()

for word in corpusList:
    if word in model:
        model[word] = model[word] + 1
        counts = counts + 1
    else:
        model[word] = 1
        counts = counts + 1

from operator import itemgetter
for sentence in sentenceList:
    probability = 0.0
    sentWords = sentence.split(' ')
    for word in sentWords:
        questionList = question.split()
        for questionWord in questionList:
            if questionWord == word:
                if word in model:
                    relevance = (1.0/model[word])
                else:
                    relevance = 0
                probability = probability + relevance
    sentenceProbs[sentence] = probability

sortedRelevance = sorted(sentenceProbs.items(), key=itemgetter(1), reverse=True)

print sortedRelevance[0][0]
