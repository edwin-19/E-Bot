import pickle, os
from collections import OrderedDict

corpusPath = "pickleDumps/"
fileName = "w2_.txt"
pickleDumps = "pickleDumps/"
conditionalProbabilityFile = pickleDumps+"conditionalProbabilityDict.p"
bigramsListPath = pickleDumps + "bigramsList.p"

def generateTrainingData():
    with open(corpusPath+fileName) as f:
        lines = f.readlines()

    bigramsList = [] # List of all bigrams along with counts. [ ["24","hello","world"] , [ ... ], ...]
    unigramsDic = OrderedDict()
    singleLine = [] # a temporary variable
    for line in lines:
        # removing \n and \r that were due to readline and splitting by tab
        singleLine = line.replace('\r','').replace('\n','').split('\t')
        bigramsList.append(singleLine)
        # getting all the unigrams W(i-1)
        # if key exists then add the count of that unigram
        if singleLine[1] in unigramsDic:
            unigramsDic[singleLine[1]] += int(singleLine[0])
        else:
            unigramsDic[singleLine[1]] = int(singleLine[0])

    #print(bigramsList)
    #print(unigramsDic)

    #all the keys of a unigramsDict are unique unigrams, hence making a list
    unigramsList = [] #raw list of all unigrams
    for key in unigramsDic:
        unigramsList.append(key)

    #print(unigramsList)

    # OK so now you have a unigram list as well as bigram list with frequency.
    # Now calculating, for each bigram, its conditional probability for a its own unigram
    conditionalProbabilityDict  = OrderedDict()

    for biagram in bigramsList:
        firstWord = biagram[1]
        secondWord = biagram[2]
        count = int(biagram[0])
        cProb =  count*1.0 / unigramsDic[firstWord]
        conditionalProbabilityDict[firstWord + " " + secondWord] = cProb

    file = open(conditionalProbabilityFile , "wb")
    pickle.dump(conditionalProbabilityDict, file)

    file = open(bigramsListPath,"wb")
    pickle.dump(bigramsList, file)

generateTrainingData()