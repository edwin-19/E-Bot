# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 21:33:45 2017

@author: Edwin
"""

import re
import collections
from itertools import product
from functools import cmp_to_key

VERBOSE = True
vowels = set('aeiouy')
alphabet = set('abcdefghijklmnopqrstuvwxyz')

def cmp(a, b):
    """python 3 replacement for python 2 cmp function"""
    return (a > b) - (a < b)

class SpellChecker:
    bestWord = ""

    def log(*args):
        if VERBOSE: print (''.join([ str(x) for x in args]))


    def words(self,text):
        """filter body of text for words"""
        return re.findall('[a-z]+', text.lower())

    def train(self,text, model = None):
        """generate or update a word model (dictionary of word:frequency)"""
        model = collections.defaultdict(lambda:0) if model is None else model
        for word in self.words(text):
            model[word] += 1
        return model

    def train_from_files(self,file_list, model = None):
        for f in file_list:
            model = self.train(open(f).read(), model)
        return model


    """ Utility Functions """
    def numberofdupes(self,string, idx):
        """return the number of times in a row the letter at index idx is duplicated"""
        # "abccdefgh", 2  returns 1
        initial_idx = idx
        last = string[idx]
        while idx + 1 < len(string) and string[idx+1] == last:
            idx += 1
        return idx-initial_idx

    def hamming_distance(self,word1, word2):
        if word1 == word2:
            return 0
        dist = sum(map(str.__ne__, word1[:len(word2)], word2[:len(word1)]))
        dist = max([word2, word1]) if not dist else dist+abs(len(word2)-len(word1))

        return dist

    def frequency(self,word, word_model):
        return word_model.get(word,0)

    """ Possibility Analysis """
    def variants(self,word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b for a, b in splits for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def double_variants(self,word):
        """get variants for the variants for a word"""
        return set(s for w in self.variants(word) for s in self.variants(w))

    def reductions(self,word):
        """return flat option list of all possible variations of the word by removing duplicate letters"""
        word = list(word)
        # ['h','i', 'i', 'i'] becomes ['h', ['i', 'ii', 'iii']]
        for idx, l in enumerate(word):
            n = self.numberofdupes(word,idx)
            # if letter appears more than once in a row
            if n:
                # generate a flat list of options ('hhh' becomes ['h','hh','hhh'])
                flat_dupes = [l*(r+1) for r in range(n+1)][:3] # only take up to 3, there are no 4 letter repetitions in english
                # remove duplicate letters in original word
                for _ in range(n):
                    word.pop(idx + 1)
                # replace original letter with flat list
                word[idx] = flat_dupes

        # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
        for p in product(*word):
            yield ''.join(p)

    def vowelswaps(self,word):
        """return flat option list of all possible variations of the word by swapping vowels"""
        word = list(word)
        # ['h','i'] becomes ['h', ['a', 'e', 'i', 'o', 'u', 'y']]
        for idx, l in enumerate(word):
            if type(l) == list:
                pass
            elif l in vowels:
                word[idx] = list(vowels)

         # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
        for p in product(*word):
             yield ''.join(p)

    def both(self,word):
        """permute all combinations of reductions and vowelswaps"""
        for reduction in self.reductions(word):
            for variant in self.vowelswaps(reduction):
                yield variant

    ### POSSIBILITY CHOOSING
    def suggesions(self,word, real_words, short_circuit = True):
        """get best spelling suggestion for word
        return on first match if short_circuit is true, otherwise collect all possible suggestions"""
        word = word.lower()
        if short_circuit:   # setting short_circuit makes the spellchecker much faster, but less accurate in some cases
            return ({word}                      & real_words or   #  caps     "inSIDE" => "inside"
                set(self.reductions(word))       & real_words or   #  repeats  "jjoobbb" => "job"
                set(self.vowelswaps(word))       & real_words or   #  vowels   "weke" => "wake"
                set(self.variants(word))         & real_words or   #  other    "nonster" => "monster"
                set(self.both(word))             & real_words or   #  both     "CUNsperrICY" => "conspiracy"
                set(self.double_variants(word))  & real_words or   #  other    "nmnster" => "manster"
                {"NO SUGGESTION"})

        else:
            return ({word}                      & real_words or
                (set(self.reductions(word))  | set(self.vowelswaps(word)) | set(self.variants(word)) | set(self.both(word)) | set(self.double_variants(word))) & real_words or
                {"NO SUGGESTION"})

    def best(self,inputted_word, suggestions, word_model = None):
        """choose the best suggestion in a list based on lowest hamming distance from original word, or based on frequency if word_model is provided"""
        suggestions = list(suggestions)

        def comparehamm(one, two):
            score1 = self.hamming_distance(inputted_word, one)
            score2 = self.hamming_distance(inputted_word, two)

            return cmp(score1, score2)

        def compareFreq(one, two):
            score1 = self.frequency(one, word_model)
            score2 = self.frequency(two, word_model)

            return cmp(score2, score1)

        freq_sorted = sorted(suggestions, key=cmp_to_key(compareFreq))[10:]     # take the top 10
        hamming_sorted = sorted(suggestions, key=cmp_to_key(comparehamm))[10:]  # take the top 10
        #print("Freq: " + str(freq_sorted))
        #print("Ham: " + str (hamming_sorted))

        return ''

    def trainSpeller(self, words):
        word_model = self.train(open('nlp/spellChecker/data/words.txt').read())
        real_words = set(word_model)

        texts= [
            'nlp/spellChecker/data/sherlockholmes.txt',
            'nlp/spellChecker/data/lemmas.txt',
        ]

        word_model = self.train_from_files(texts, word_model)

        """self.log('Total Word Set: ', len(word_model))
        self.log('Model Precision: %s' % (float(sum(word_model.values()))/len(word_model)))"""

        try:
            word = words

            possibilities = self.suggesions(word, real_words, short_circuit=False)
            short_circuit_result = self.suggesions(word, real_words, short_circuit=True)

            if VERBOSE:
                """
                print ([(x, word_model[x]) for x in possibilities])
                print (self.best(word, possibilities, word_model))
                print ('---')
                print ([(x, word_model[x]) for x in short_circuit_result]) """

                bestList = [(x, word_model[x]) for x in short_circuit_result]
                self.findBestWord(bestList)
            if VERBOSE:
                print( self.best(word, short_circuit_result, word_model))

        except (EOFError, KeyboardInterrupt) as ex:
            print("Exception Error:" + ex)

    def findBestWord(self, wordList):
        higghestPoss = sorted(wordList, key=lambda x: x[1], reverse=True)[0]
        self.bestWord = higghestPoss[0]

