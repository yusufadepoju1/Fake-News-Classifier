import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
import os

nltk.download("stopwords", quiet=True)

def train_model():
    print("Loading data...")
    # Assume data is in the parent directory of src
    data_path = os.path.join(os.path.dirname(__file__), '..', 'train.csv')
    data = pd.read_csv(data_path)
    data = data.dropna()
    data.reset_index(inplace=True)
    
    X = data.drop("label", axis=1)
    y = data["label"]

    messages = X.copy()
    ps = PorterStemmer()
    corpus = []
    
    print("Preprocessing text...")
    for i in range(len(messages)):
        review = re.sub("[^a-zA-Z]", " ", str(messages['title'][i]))
        review = review.lower()
        review = review.split()
        review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        corpus.append(review)

    vocab_size = 5000
    onehot_repr = [one_hot(words, vocab_size) for words in corpus]
    sent_length = 20
    embedded_docs = pad_sequences(onehot_repr, padding='pre', maxlen=sent_length)
    
    X_final = np.array(embedded_docs)
    y_final = np.array(y)

    print("Building model...")
    embedding_vector_features = 40
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_vector_features, input_length=sent_length))
    model.add(LSTM(100))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.33, random_state=42)

    print("Training model...")
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=64)
    
    print("Saving model...")
    model_path = os.path.join(os.path.dirname(__file__), 'model.h5')
    model.save(model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
