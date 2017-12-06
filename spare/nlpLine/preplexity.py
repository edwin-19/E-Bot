# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 23:16:40 2017

@author: Edwin
"""

import collections
from nltk.corpus import treebank
import nltk

class Preplexity:
    def unigram(self, tokens):
        model = collections.defaultdict(lambda: 0.01)
        for f in tokens:
            try:
                model[f] += 1
            except KeyError:
                model[f] = 1
                continue

        for word in model:
            model[word] = model[word] / float(len(model))

        return model

    def getTreeBanks(self):
        return ' '.join(treebank.words('wsj_0003.mrg'))

    def perplexity(self, testset, model):
        testset = testset.split()
        perplexity = 1
        N = 0
        for word in testset:
            N += 1
            perplexity = perplexity * (1 / model[word])
        perplexity = pow(perplexity, 1 / float(N))
        return perplexity

