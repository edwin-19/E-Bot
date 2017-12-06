# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 17:17:17 2017

@author: Edwin
"""

import re
from collections import Counter

class SpellChecker:
    def __init__(self):
         return
         
    def words(text):
        return re.findall(r'\w+', text.lower())
    
    WORDS = Counter(words(open('sherlockholmes.txt').read()))
    
    def P(self,word, N=sum(WORDS.values())): 
        #Probability of a 'Word'
        return self.WORDS[word] / N
    
    def correction(self, word):
        return max(self.candidates(word), key=self.P)
    
    def candidates(self, word):
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
    
    def known(self, words):
        return set(w for w in words if w in self.WORDS)
    
    def edits1(self, word):
        #All edits that are one dit away from 'Word".
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
    
    def edits2(self,word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
    
spellChecker = SpellChecker()
inputWord = input("Inputted Word: ")

for x in range(len(inputWord.split())):
    print(spellChecker.correction(inputWord.split()[x]))

"""
for x in range(len(inputWord.split())):
    print(spellChecker.correction(inputWord.split[x]))
"""