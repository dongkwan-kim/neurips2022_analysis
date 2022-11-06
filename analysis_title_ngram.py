import pickle
from pprint import pprint

from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd

from nltk import word_tokenize
from nltk.stem import SnowballStemmer


class Stemmer:
    def __init__(self):
        self.engine = SnowballStemmer(language="english")

    def __call__(self, doc):
        return [self.engine.stem(t) for t in word_tokenize(doc)]


with open("data/pp_names.txt", "rb") as fp:  # Unpickling
    titles = list(pickle.load(fp))

titles = [t.replace("$", "").replace(":", "") for t in titles
          if "[Re]" not in t]


def get_ngrams(text, ngram_from=2, ngram_to=None, n=200, max_features=500):
    vec = CountVectorizer(
        ngram_range=(ngram_from, ngram_to or ngram_from),
        max_features=max_features,
        stop_words="english",
        tokenizer=Stemmer()
    ).fit(text)
    bag_of_words = vec.transform(text)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, i]) for word, i in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


ngrams = get_ngrams(titles, ngram_from=2)
for tk, freq in ngrams:
    print(f"{tk}\t{freq}")