from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load and preprocess training data
training_data_path = 'training_data/inspector.txt'
with open(training_data_path, 'r', encoding='utf-8') as file:
    training_sentences = file.readlines()

# Tokenize training data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(training_sentences)
total_words = len(tokenizer.word_index) + 1

# Create sequences
input_sequences = []
for line in training_sentences:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Create predictors and labels
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

# Define and compile the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_len-1),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150)),
    tf.keras.layers.Dense(total_words, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(xs, ys, epochs=100, verbose=1)

# Function to generate response
def generate_response(user_input):
    # Tokenize user input
    input_sequence = tokenizer.texts_to_sequences([user_input])
    input_sequence = pad_sequences(input_sequence, maxlen=max_sequence_len-1, padding='pre')
    
    # Generate response
    predicted = model.predict_classes(input_sequence, verbose=0)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    return output_word

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
