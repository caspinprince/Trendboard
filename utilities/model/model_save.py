import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import re
import string
import nltk
from nltk.corpus import stopwords
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import joblib
from utilities.model.TextCleaner import TextCleaner
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

df = pd.read_csv('tweets.csv', encoding='iso-8859-1')
df.columns = ['sentiment', 'id', 'date', 'flag', 'user', 'text']
df = df.drop(['id', 'date', 'flag', 'user'], axis=1)
df = shuffle(df, random_state=99)
encoder = LabelEncoder()
df['sentiment'] = encoder.fit_transform(df['sentiment'])
X = df['text']
y = df['sentiment']
X_train = X[:1400000]
y_train = y[:1400000]
X_val = X[1400000:]
y_val = y[1400000:]

finalModelPipe = Pipeline([('textclean', TextCleaner()), ('tfidf', TfidfVectorizer(ngram_range=(1, 2))), ('finalLSVC', LinearSVC(dual=True, penalty='l2', C=0.22))])

finalModelPipe.fit(X_train, y_train)

joblib.dump(finalModelPipe, 'finalTwitterModel.pkl', compress=('lzma', 5))


