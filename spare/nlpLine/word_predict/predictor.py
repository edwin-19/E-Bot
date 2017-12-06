import nlpLine.word_predict.bigramConditionalProbability as trainer
import nlpLine.word_predict.getTopBigram as biagram
import os

def checkIfFileExsists(filePath):
    if os.path.isfile(filePath):
        return True
    else:
        return False

def getPredictedWord(text):
    filePath = "pickleDumps/conditionalProbabilityDict.p"
    biagramsList = "pickleDumps/bigramsList.p"
    if checkIfFileExsists(filePath):
        if checkIfFileExsists(biagramsList):
            biagram.predictWord(text)
        else:
            trainer.generateTrainingData()
            biagram.predictWord(text)
    else:
        trainer.generateTrainingData()
        biagram.predictWord(text)


getPredictedWord(str(input("Word: ")))