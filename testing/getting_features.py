import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import re
import datetime
import json
from sklearn.decomposition import NMF
from yahoo_finance import Share
import matplotlib.pyplot as plt

from nmf_tweets import load_json

sym='YHOO'
path='data_week_1'
data = load_json(sym, path)

sents = [ sentence['text'] for sentence in data ]
dates = [ str(text['created_at']) for text in data ]
d = np.array(dates).T
d = d.reshape(len(dates), 1)

vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(sents)
#features = vectorizer.get_feature_names()

k = 1
model = NMF(n_components=k, init='random', random_state=0)
latent_features = model.fit_transform(X)

feats = vectorizer.get_feature_names()
coms = model.components_

zipped = zip(feats, coms[0,:])
sorted_feats = sorted(zipped, key=lambda tup: tup[1], reverse=True)
sorted_feats[:10]

from wordcloud import WordCloud
wc = WordCloud(background_color='white')

wc.generate_from_frequencies(sorted_feats[:20])
plt.axis("off")
plt.imshow(wc)
plt.savefig('YHOO_wc.png')
plt.show()





















#
