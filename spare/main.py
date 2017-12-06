# -*- coding: utf-8 -*-
"""
NOTES: 
1) USE NLP as the first step
2) USE Entity extractor first instead of spelling corrector
3) Convert date to unfied format: e.g - "All dates must be (2017/09/18) YYYY//MM/DD"    
"""

import nltk
from nlpLine.nlp import NLPLine

from session.nlp.spellChecker import SpellChecker

brokenDown = []

def sentenceCorrector(tokenize_sentence):
    spellChecker = SpellChecker() 
    
    for x in range(0,len(tokenize_sentence)):
        spellChecker.trainSpeller(tokenize_sentence[x])
        if spellChecker.bestWord != "NO SUGGESTION":
            print("Best Word: " +  spellChecker.bestWord)
            brokenDown.append(spellChecker.bestWord)
        else:
            print("Best Word: " + tokenize_sentence[x])
            brokenDown.append(tokenize_sentence[x])
    
    correctedSentence = NLPLine().joinSentence(brokenDown)
    
    return correctedSentence

def main():
    inputSentence = NLPLine().removePunc(input("Enter word: "))
    nlp = NLPLine()
    
    #Entity Extractor
    extracted = nlp.get_continous_text(inputSentence) 
    
    #Sentence Corrected/ Word Corrector
    print("\nInputted Word is: " + inputSentence +"\n")
    tokenize_sentence = nltk.word_tokenize(inputSentence)
    fixedSentence = sentenceCorrector(tokenize_sentence)
    
    #NLP pipeline
    print("Corrected Setence: " + fixedSentence +"\n")
    tag = nlp.breakSentence(fixedSentence)
    
    #Lemmetize Words
    lemmetized = nlp.lemmetizeWords(brokenDown, tag)
    
    print("\nEntity Extracted:\n" + str(extracted))
    print("\nSentence Lemtized:\n" + str(lemmetized))
    #nlp.findSynonyms(brokenDown)
    
if __name__ == "__main__":
    main()