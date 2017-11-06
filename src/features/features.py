#!/usr/bin/env python

# script to write
# will have document as input and will do NLP processing to generate features/tokens

# some packages that may be useful
import nltk
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
# not sure if applicable right now, maybe for training after tokens are created?
import tensorflow as tf
import gensim
import pickle


if __name__ == "__main__":
    pkl_path = "C:\\Users\\kzecchini\\data\\jfk_data\\pkl\\"
    pickle_file = os.path.join(pkl_path, "documents.pkl")
    with open(pickle_file, 'rb') as f:
        docs = pickle.load(f)

    for doc in docs:
        print(doc)
