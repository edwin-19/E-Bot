# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 21:37:29 2017

@author: Edwin
"""
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

class NLP(object):    
    def breakSentence(self,sentence):
        sent_text = nltk.sent_tokenize(sentence)
        
        for text in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokenized_text)
            print(tagged)
            return tagged
    
    def removeStopWords(self, sentence):
        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.word_tokenize(sentence)
        
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        return self.joinSentence(filtered_sentence)
          
    def joinSentence(self,sentence):
        return ' '.join(sentence)
    
    def removePunc(self,s):
        return re.sub(r'[^\w]', ' ', s)
    
    def is_noun(self,tag):
        return tag in ['NN', 'NNS', 'NNP', 'NNPS']
    
    def is_verb(self,tag):
        return tag in ['VB','VBD','VBG','VBN','VBP','VBZ']
    
    def is_adverb(self, tag):
        return tag in ['RB', 'RBR', 'RBS']
    
    def is_adjective(self, tag):
        return tag in ['JJ','JJR','JJS']
    
    def penn_to_wn(self,tag):
        if self.is_adjective(tag):
            return wn.ADJ
        elif self.is_noun(tag):
            return wn.NOUN
        elif self.is_adverb(tag):
            return wn.ADV
        elif self.is_verb(tag):
            return wn.VERB
        return None
    
    def lemmetizeWords(self, sentence, tag):
        lemmetizer = WordNetLemmatizer()
        lemmetizeWords = []
        
        for x in range(0, len(sentence)):
            if self.penn_to_wn(tag[x][1]) is not None:
                lem = lemmetizer.lemmatize(sentence[x], self.penn_to_wn(tag[x][1]))
                print(lem)
                lemmetizeWords.append(lem)
            else:
                lem = lemmetizer.lemmatize(sentence[x])
                print(lem)
                lemmetizeWords.append(lem)
        
        return lemmetizeWords

    def get_continous_text(self, text):
        chuncked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))
        continous_chunkc = []
        current_chunked = []

        for i in chuncked:
            if type(i) == Tree:
                current_chunked.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunked:
                named_entity = " ".join(current_chunked)
                if named_entity not in continous_chunkc:
                    continous_chunkc.append(named_entity)
                    current_chunked = []
            else:
                continue

        return continous_chunkc

    def stanfordNE2BIO(self,tagged_sent):
        bio_tagged_sent = []
        prev_tag = "O"
        for token, tag in tagged_sent:
            if tag == "O": #O
                bio_tagged_sent.append((token, tag))
                prev_tag = tag
                continue
            if tag != "O" and prev_tag == "O": # Begin NE
                bio_tagged_sent.append((token, "B-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag == tag: # Inside NE
                bio_tagged_sent.append((token, "I-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag != tag:
                bio_tagged_sent.append((token, "B-" + tag))
                prev_tag = tag

        return bio_tagged_sent

    def stanfordNE2tree(self, ne_tagged_sent):
        bio_tagged_sent = self.stanfordNE2BIO(ne_tagged_sent)
        sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
        sent_pos_tags = [pos for token, pos in nltk.pos_tag(sent_tokens)]

        sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
        ne_tree = conlltags2tree(sent_conlltags)

        return ne_tree

    #Extracts only normal entities like place or percson
    def extractEntities(self, ne_tagged_sent):
        ne_tree = self.stanfordNE2tree(ne_tagged_sent)

        ne_in_sent = []
        for subtree in ne_tree:
            if type(subtree) == Tree:
                ne_label = subtree.label()
                ne_string = " ".join([token for token, pos in subtree.leaves()])
                ne_in_sent.append((ne_string, ne_label))

        return ne_in_sent

    
        












