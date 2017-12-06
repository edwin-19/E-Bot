import nltk
from nlp.nlpUtils import NLP
from nlp.spellChecker.spellcheckers import SpellChecker

class PreProcessor(object):
    brokenDown = []

    def correct_sentence(self,sentence):
        spellChecker = SpellChecker()
        new_sentence = []
        
        for x in range(0, len(sentence)):    
            spellChecker.trainSpeller(sentence[x])
            if spellChecker.bestWord != "NO SUGGESTION":
                print("Best Word: " +  spellChecker.bestWord)
                new_sentence.append(spellChecker.bestWord)
                self.brokenDown.append(spellChecker.bestWord)
            else:
                print("Best Word: " + sentence[x])
                new_sentence.append(sentence[x])
                self.brokenDown.append(spellChecker.bestWord)
        
        correctedSentence = NLP().joinSentence(new_sentence)
        
        return correctedSentence
    
    
    def pre_process(self, query):
        nlp = NLP()
        
        inputSentence = NLP().removePunc(query)
        clearSentence = NLP().removeStopWords(inputSentence)

        print(clearSentence)

        # Entity Extractor
        extracted = nlp.get_continous_text(inputSentence)

        tokenize_sentence = nltk.word_tokenize(clearSentence)
        fixedSentence = self.correct_sentence(tokenize_sentence)

        #NLP pipeline
        print("Corrected Setence: " + fixedSentence +"\n")
        tag = nlp.breakSentence(fixedSentence)

        # Lemmetize Words
        lemmetized = nlp.lemmetizeWords(self.brokenDown, tag)

        print("\nEntity Extracted:\n" + str(extracted))
        print("\nSentence Lemtized:\n" + str(lemmetized))

        #RE intialize brokenDown
        self.brokenDown.clear()
        return nlp.joinSentence(lemmetized)
