from PyQt5 import QtWidgets
from out import Ui_Form
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QShortcut
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
import sys

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result



class chat_main(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.uif = Ui_Form()
        self.uif.setupUi(self)
        self.uif.Send.pressed.connect(self.msg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.msg()

    def msg(self):
        text = self.uif.message_line.text()
        ints = predict_class(str(text), model)
        result = getResponse(ints, intents)
        self.uif.textBrowser.append("You: " + text)
        self.uif.textBrowser.append("Bot: " + result)
        self.uif.message_line.setText(str(''))




if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = chat_main()
    demo.show()

sys.exit(app.exec_())



