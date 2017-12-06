import math
from collections import deque
import nltk
from nltk.corpus import treebank
from word_predictor import WordPredictor

def getTreeBanks():
    return treebank.words('wsj_0003.mrg')

def getGuterbergCorpus():
    gutenber_files = nltk.corpus.gutenberg.fileids()
    return gutenber_files

def validate():
    try:
        wp = WordPredictor()
        #Train on 75% of files (not neccessarily 75 % of sentences)
        training_set_size = int(math.floor(len(getGuterbergCorpus()) * 0.07))
        for corpus in getGuterbergCorpus()[0 : training_set_size]:
            wp.learn_from_text(nltk.corpus.gutenberg.raw(corpus))

        #Test
        num_correct = 0
        num_total = 0
        print("Trained...")

        for corpus in getGuterbergCorpus()[training_set_size:]:
            text = nltk.corpus.gutenberg.raw(corpus)
            terms = wp._tokenize_phrase(text)
            recent = deque([], maxlen=wp.order)

            #Esitmate for each pair of words
            for term in terms:
                tokens =  wp._predict_from_tokens(list(recent))
                # If one of top 3 predictions is word, count as correct prediction
                """if term in map(lambda x: x[0], tokens[0:3]):
                    num_correct += 1"""
                num_total += 1
                recent.append(term)

        print("%d / %d" % (num_correct, num_total))
    except TypeError as tp:
        print("Error: " + str(tp))
        raise

wp = WordPredictor()
for s in getTreeBanks():
    wp.learn_from_text(s)

predict = wp.predict("That is")
print(predict)


