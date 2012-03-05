"""
Author: Eric Waddell

This tagger implements the trivial case of tagging, each word is
tagged nn (singular or mass noun). Using 8 parts of speech, nouns
make up something like 70% of words used in discourse (that number
is from recollection and varies a bit with the type of discourse,
e.g. internet messenger conversations vs. medical journals, in any
case it generally forms at least a majority of the parts of speech).
This number is obviously a bit lower when your tags are finer grained
as the brown corpus is, but its a good starting point.
"""

#Grabbing paths
import os
cwd = os.getcwd()
pathsFile = open(cwd + '/paths.txt','r')
pathList = pathsFile.read().split('\n')

workspace = pathList[0]
training = pathList[1]
untagged = pathList[2]
tagged = pathList[3]
fileName = pathList[4]


#No model to build
def buildModel():
    return

#Always return mass noun
def tagWord(word):
    return 'nn'

#Read in the file and split it along spaces, remove extraneous empty strings
#and move everything into a big string once you tag the word, then output to
#a new file in your tagged directory
buildModel()
fileToTag = open(workspace + untagged + fileName,'r')
untaggedData = fileToTag.read()
fileToTag.close()
untaggedDataList = untaggedData.split(' ')
taggedData = ''
while '' in untaggedDataList:
    untaggedDataList.remove('')
for word in untaggedDataList:
    taggedData = taggedData + word + '/' + tagWord(word) + ' '
taggedFile = open(workspace + tagged + fileName, 'w')
taggedFile.write(taggedData)
taggedFile.close()
