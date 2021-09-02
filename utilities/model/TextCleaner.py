from sklearn.base import BaseEstimator
import re
import nltk
from nltk.corpus import stopwords
import string

class TextCleaner(BaseEstimator):

    def __init__(self):
        pass

    def fit(self, documents, y=None):
        return self

    def transform(self, X):
        stopword_list = stopwords.words('english')
        stemmer = nltk.SnowballStemmer("english")
        for text in X:
            text = str(text).lower()
            text = re.sub('\[.*?\]', '', text)
            text = re.sub('https?://\S+|www\.\S+', '', text)
            text = re.sub('<.*?>+', '', text)
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
            text = re.sub('\n', '', text)
            text = re.sub('\w*\d\w*', '', text)
            text = ' '.join(word for word in text.split(' ') if word not in stopword_list)
            text = ' '.join(stemmer.stem(word) for word in text.split(' '))

        return X

if __name__ == "__main__":
    # code for standalone use
    t = TextCleaner()
    TextCleaner.__module__ = "text_cleaner"
    t.save("textclean.pkl")