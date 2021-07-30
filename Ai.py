import spacy
from spacy.lang.en.stop_words import STOP_WORDS
#from spacy.lang.am.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from tkinter import Tk
from tkinter.filedialog import askopenfilename




class Summarzation:
    punctuation = punctuation + '\n'
    stopwords = STOP_WORDS


    @classmethodc
    def load_text(cls):

        text = ''
        #fname = r'C:\Users\sam\Desktop\s.txt'
        #fname = r'C:\Users\sam\Desktop\stuff\anacodaprojects\summarization.txt'
        # if fname[-4:] == '.txt':
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
       # print(filename)
        f = open(filename, encoding="utf8") #open the file
        text = f.read() #read the open file and put it in text

        return text

    @classmethod
    def nlp_object(cls, text):
        nlp = spacy.load('en_core_web_sm') #load the trained pipeline
        doc = nlp(text) #the text is trained through the model

        return doc

    @classmethod
    def word_frequencies(cls, doc):
        word_frequencies = {}# creating a dictionary
        for word in doc:
            if word.text.lower() not in cls.stopwords:
                if word.text.lower() not in cls.punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1

        return word_frequencies

    @classmethod
    def tokens(cls, doc):
        tokens = [token.text for token in doc]
        sentence_tokens = [sent for sent in doc.sents]

        return tokens, sentence_tokens

    @classmethod
    def sentence_score(cls, word_frequencies, sentence_tokens):
        max_frequency = max(word_frequencies.values()) #find the maximum value
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / max_frequency #dividing the word value by the maximum value

        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()] #puts the sum vaule of the sentence
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

        return sentence_scores

    @classmethod
    def final(cls, sentence_tokens, sentence_scores):
        select_length = int(len(sentence_tokens) * 0.2) #reduce the total 100/100 to 20/100
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get) # take the largest value
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary) #final result
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        file = askopenfilename()
        f = open(file + '.txt','w') #open the file
        new_summary = f.write(summary) #we writed to disk just as you suggested as

        return summary



#print(len(STOP_WORDS))
text = Summarzation.load_text()
doc = Summarzation.nlp_object(text)
wf = Summarzation.word_frequencies(doc)
tokens, sentence_tokens= Summarzation.tokens(doc)
sentence_scores = Summarzation.sentence_score(wf, sentence_tokens)
summary = Summarzation.final(sentence_tokens, sentence_scores)
print(len(text))
print(len(summary))
print(summary)
#print(sentence_scores.get)
print()