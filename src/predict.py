import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download("stopwords", quiet=True)

class FakeNewsPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'model.h5')
        self.model = load_model(model_path)
        self.ps = PorterStemmer()
        self.vocab_size = 5000
        self.sent_length = 20
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, title):
        review = re.sub("[^a-zA-Z]", " ", str(title))
        review = review.lower()
        review = review.split()
        review = [self.ps.stem(word) for word in review if word not in self.stop_words]
        review = ' '.join(review)
        
        # one_hot returns a list of ints, we need it as a list of lists because 
        # pad_sequences expects a list of sequences
        onehot_repr = [one_hot(review, self.vocab_size)]
        embedded_doc = pad_sequences(onehot_repr, padding='pre', maxlen=self.sent_length)
        return np.array(embedded_doc)

    def predict(self, title):
        """
        Returns True if Fake News, False if Real News
        In our dataset, label 1 typically means False/Unreliable, label 0 means Reliable.
        """
        processed_title = self.preprocess_text(title)
        prediction = self.model.predict(processed_title)
        is_fake = prediction[0][0] > 0.5
        confidence = float(prediction[0][0]) if is_fake else 1.0 - float(prediction[0][0])
        return bool(is_fake), confidence
