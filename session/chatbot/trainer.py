# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 00:11:44 2017

@author: Edwin
"""

from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

class Trainer(object):
    chatbot = ChatBot("E-Bot")
     
    def __init__(self, chatbot):
        self.chatbot = chatbot
    
    def trainFromCorpus(self):
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)
        self.chatbot.train(
           'chatterbot.corpus.english'
        )
    
    def trainFromList(self):
        self.chatbot.trainer(ListTrainer)
        self.chatbot.train(
        )
    
    def trainBot(self):
        self.chatbot.set_trainer(UbuntuCorpusTrainer)
        self.chatbot.train()

        