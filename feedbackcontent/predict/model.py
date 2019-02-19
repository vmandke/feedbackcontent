import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from feedbackcontent.predict.preprocess import Preprocess
from feedbackcontent.util.config import get_config


class Loader:
    def __init__(self, model_path):
        self.model_path = model_path

    def load_model(self, model_name):
        return Model(
                  np.load(os.path.join(
                              self.model_path,
                              '{}.npz'.format(model_name))))


class Model:
    def __init__(self, model):
        self.stop_words = set(model["stop_words"])
        self.vocab = self.load_vocab(model["vocab"])
        self.lr = np.hstack((model["lr"], model["intercept"]))
        self.vectorizer = TfidfVectorizer(vocabulary=self.vocab)
        self.vectorizer.idf_ = model["idf_"]
        self.preprocessor = Preprocess(
                                lang="en",
                                use_stemmer=True,
                                stop_words=self.stop_words)

    def tokenize(self, text):
        # Add a 1 for the intercept
        processed_text = " ".join(self.preprocessor.process(text))
        return np.hstack(
            (self.vectorizer.transform([processed_text]).toarray(), [[1]]))

    def load_vocab(self, vocab_arr):
        return dict(zip(vocab_arr, range(vocab_arr.shape[0])))

    def predict_lr(self, dv):
        return self._sigmoid_nlr(dv.dot(self.lr))

    def _sigmoid_nlr(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def predict(self, text):
        return self.predict_lr(self.tokenize(text))
