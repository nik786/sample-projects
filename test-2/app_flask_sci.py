import random
import numpy as np
import json
from flask import Flask, render_template, request
#import ssl
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

class ChatBot:
    def __init__(self, intents_file):
        self.intents_file = intents_file
        self.load_intents()
        self.prepare_data()
        self.train_classifier()

    def load_intents(self):
        with open(self.intents_file, "r") as file:
            self.intents = json.load(file)

    def prepare_data(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?']

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [nltk.stem.WordNetLemmatizer().lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    def bow(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [nltk.stem.WordNetLemmatizer().lemmatize(word.lower()) for word in sentence_words]
        bag = [0]*len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
        return np.array(bag)

    def train_classifier(self):
        training = []
        output_empty = [0] * len(self.classes)

        for doc in self.documents:
            bag = self.bow(' '.join(doc[0]))
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        try:
            bag_of_words = [item[0] for item in training]
            output_rows = [item[1] for item in training]
            bag_of_words_array = np.array(bag_of_words)
            output_rows_array = np.array(output_rows)
            training_data = np.hstack((bag_of_words_array, output_rows_array))
            np.random.shuffle(training_data)
            train_x = training_data[:, :-len(self.classes)]
            train_y = training_data[:, -len(self.classes):]
            train_y = np.argmax(train_y, axis=1)

            # Train the classifier (Random Forest)
            self.classifier = RandomForestClassifier(n_estimators=100)
            self.classifier.fit(train_x, train_y)
        except ValueError as e:
            print("Error occurred while preparing the training data:", e)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])

def chatbot_response():
    msg = request.form["msg"]
    
    # Predict the intent
    p = chatbot.bow(msg)
    prediction = chatbot.classifier.predict([p])[0]
    # Get the tag from the prediction
    predicted_tag = chatbot.classes[prediction]
    
    # Find the corresponding responses for the predicted tag
    tag_response = None
    for intent in chatbot.intents['intents']:
        if intent['tag'] == predicted_tag:
            tag_response = intent['responses']
            break
    
    # Find responses based on patterns if tag-based response not found
    if tag_response is None:
        for intent in chatbot.intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in msg.lower():
                    tag_response = intent['responses']
                    break
            if tag_response is not None:
                break

    # If no tag or pattern-based response found, use a default response
    if tag_response is None:
        tag_response = ["Sorry, I couldn't understand that."]
    
    # Check if any response contains a link
    for i, response in enumerate(tag_response):
        if "<a href=" in response:
            # Add target="_blank" to open the link in a new tab
            tag_response[i] = response.replace("<a href=", "<a target='_blank' href=")
    
    return " ".join(tag_response)



if __name__ == "__main__":
#    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#    context.load_cert_chain('server.crt', 'server.key')
    chatbot = ChatBot("intents.json")
    #app.run(host='0.0.0.0', port=8080, ssl_context=context)
    app.run(host='0.0.0.0', port=8080)

