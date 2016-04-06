from tweepy_search import get_twitter_data

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk.data
import numpy as np
import enchant

def get_top_values(lst, n, labels):
    '''
    INPUT: LIST, INTEGER, LIST
    OUTPUT: LIST

    Given a list of values, find the indices with the highest n values.
    Return the labels for each of these indices.

    e.g.
    lst = [7, 3, 2, 4, 1]
    n = 2
    labels = ["cat", "dog", "mouse", "pig", "rabbit"]
    output: ["cat", "pig"]
    '''
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1] if labels[i].isalpha()]

def create_d3_list(sym):
    tweets = []

    twitter_data = get_twitter_data(sym).items(100)
    for tweet in twitter_data:
        tweets.append(tweet.text)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(tweets).toarray()
    words = vectorizer.get_feature_names()
    #words = [ word for word in words if word.isalpha() ]

    avg = np.sum(vectors, axis=0) #/ np.sum(vectors > 0, axis=0)

    print "top 10 by average tf-idf"
    d = enchant.Dict("en_US")
    #top_vals = [ str(word) for word in get_top_values(avg, 100, words) if d.check(word) ]
    words_avg = zip(words, avg)
    words_avg.sort(key=lambda tup: tup[1], reverse=True)

    d3_list = []
    sizing_d3 = (110 / words_avg[0][1])
    for cell in words_avg:
        if d.check(cell[0]):
            if cell[0] != 'rt':
                d3_list.append({"text": str(cell[0]), "size": cell[1] * sizing_d3})

    return d3_list
#print top_vals[:20]














#
