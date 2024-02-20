from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import os


# Creating ChatBot Instancep

chatbot = ChatBot(
    'Chatty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.',
        'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
) 
 # Training with Personal Ques & Ans 
training_data_quesans = open('training_data/inspector.txt').read().splitlines()
training_data_personal = open('training_data/simple.txt').read().splitlines()
training_data_conv = open('training_data/waf.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal + training_data_conv

trainer = ListTrainer(chatbot)
trainer.train(training_data) 
# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)

app = Flask(__name__,template_folder='templates', static_folder='static')















@app.route('/')
def index():
    return render_template('index.html')





@app.route('/get_response', methods=['GET','POST'])


def get_response():
    user_input = request.form['user_input']
    response = chatbot.get_response(user_input)
    return jsonify({'response': str(response)})

if __name__ == "__main__":
 app.run(host='127.0.0.1', port=5000)








