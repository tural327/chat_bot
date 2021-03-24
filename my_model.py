import json
from nltk.stem import WordNetLemmatizer
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD
import numpy as np
import random
import nltk

lemmatizer = WordNetLemmatizer()


words = [] # my words will be contain here
classes = [] # for each type of tags
documents = []
ignore_words = ["?","!"] # we dont need wods which is containing ? or !

data_file = open("intents.json").read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent["patterns"]:

        w = nltk.word_tokenize(pattern) # taking each word from patterns
        words.extend(w)


        documents.append((w,intent['tag']))



        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

words = sorted(list(set(words)))

training = []

output_empty = [0]*len(classes)

for document in documents:
    bag = []

    pattern_words = document[0]


    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)


    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training.append([bag,output_row])


random.shuffle(training)

training = np.array(training)


training_x = list(training[:,0])
training_y = list(training[:,1])


model = Sequential()
model.add(Dense(128, input_shape=(len(training_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(training_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))
history = model.fit(np.array(training_x), np.array(training_y), epochs=200, batch_size=5)
model.save('chatbot_model.h5', history)





