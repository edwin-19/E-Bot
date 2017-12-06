# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 16:00:46 2017

@author: Edwin
"""

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.tree import Tree
import re
from nltk.sem import relextract

class NLPLine:
    def breakSentence(self,sentence):
        sent_text = nltk.sent_tokenize(sentence)
        
        for text in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokenized_text)
            print(tagged)
            return tagged
    
    def joinSentence(self,sentence):
        return ' '.join(sentence)
    
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
    
    def lemmetizeWords(self,sentence, tag):
        lemmatizer = WordNetLemmatizer()
        lemmatizedWords =[]
        
        for x in range(0, len(sentence)):
            if self.penn_to_wn(tag[x][1]) is not None:
                print(lemmatizer.lemmatize(sentence[x], self.penn_to_wn(tag[x][1]) ))
                lemmatizedWords.append(lemmatizer.lemmatize(sentence[x], self.penn_to_wn(tag[x][1]) ))
            else:
                print(lemmatizer.lemmatize(sentence[x]))
                lemmatizedWords.append(lemmatizer.lemmatize(sentence[x]))
        
        return self.joinSentence(lemmatizedWords)
        
    def removePunc(self,s):
        return re.sub(r'[^\w]', ' ', s)
            
    #Extracts human text 
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

    def findRelations(self,text):
        roles = """
        (.*(                   
        analyst|
        editor|
        librarian).*)|
        researcher|
        spokes(wo)?man|
        writer|
        ,\sof\sthe?\s*  # "X, of (the) Y"
        """
        
        ROLES = re.compile(roles, re.VERBOSE)
        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences)


        for doc in chunked_sentences:
            print(doc)
            for rel in relextract.extract_rels('PER', 'ORG', doc, corpus='ace', pattern=ROLES):
                #it is a tree, so you need to work on it to output what you want
                print(relextract.show_raw_rtuple(rel) )
                return relextract.show_raw_rtuple(rel) 
    
    def findSynonyms(self, sentence):
        for token in sentence:
            syn_sets = wn.synsets(token)
            for syn_set in syn_sets:
                print(syn_set, syn_set.lemma_names())
                print(syn_set.hyponyms())

 
