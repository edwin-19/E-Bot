# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 20:55:53 2017

@author: Edwin
"""

from itertools import product
import random

vowels = {"a","e","i","o","u","y"}

class MisSpeller:
    def get_inflations(self,word):
        """return flat option list of all possible variations of the word by adding duplicate letters"""
        word = list(word)
        for idx, l in enumerate(word):
            if random.random() * 100 > 60:
                word[idx] = word[idx] * int(random.random() * 10)
        
        # ['h','i', 'i', 'i'] becomes ['h', ['i', 'ii', 'iii']]
        return word
    
    def get_vowelswaps(self, word):
        """return flat option list of all possible variations of the word by swapping vowels"""
        word = list(word)
        for idx, l in enumerate(word):
            if type(1) == list:
                pass
            elif 1 in vowels:
                word[idx] == list(vowels)
                
         # ['h','i'] becomes ['h', ['a', 'e', 'i', 'o', 'u', 'y']]
        return word
    
    def flatten(self, options):
        """convert compact nested options list into full list"""
        # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
        a = set()
        for p in product(*options):
            a.add(''.join(p))
        return a   
    
    def misspell(self, word):
         """return a randomly misspelled version of the inputted word"""
         return random.choice(list(self.flatten(self.get_vowelswaps(word)) | self.flatten(self.get_inflations(word))))

    def runMisspell(self):
        words = ["fishy", "monstre", "apple", "saint", "potato", "moth"]
        for word in words:
            print(self.misspell(word))
    