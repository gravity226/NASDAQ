import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import re
import json
from sklearn.decomposition import NMF
from pymongo import MongoClient

# input sym as a stock symbol 'AAPL'
# input k as the number features for nmf
# input coll as a collection in a mongo database
def nmf_df(sym, k, coll):
    data = [ item for item in coll.find({'text': { '$in' :[re.compile(sym)] }}) ]
    sents = [ sentence['text'] for sentence in data ]
    dates = [ str(text['created_at']) for text in data ]
    d = np.array(dates).T
    d = d.reshape(len(dates), 1)

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(sents)
    #features = vectorizer.get_feature_names()

    model = NMF(n_components=k, init='random', random_state=0)
    latent_features = model.fit_transform(X)

    # lat0 = list(latent_features[:,0])
    # lat1 = list(latent_features[:,1])
    # lat2 = list(latent_features[:,2])
    # lat3 = list(latent_features[:,3])

    df = pd.DataFrame(latent_features)   #np.concatenate((d, latent_features), axis=1)
    df.columns = [ 'lat'+ str(n) for n in xrange(len(df.columns)) ]
    df['time_stamp'] = d
    #print df.head()

    df['date'] = pd.to_datetime(df['time_stamp']).apply(pd.datetools.normalize_date)
    df.pop('time_stamp')
    #print df.head()
    grouped_data = df.groupby(['date']).mean()
    grouped_data['sym'] = sym

    return grouped_data

def graph_it(df):
    from yahoo_finance import Share
    import matplotlib.pyplot as plt
    sym = 'GOOG'
    start_date = '2016-04-03'
    end_date = '2016-04-07'
    yahoo = Share(sym)
    yahoo_days = yahoo.get_historical(start_date, end_date)

    y_money = [ day['Close'] for day in yahoo_days ]
    # for yahoo_day in yahoo_days:
    #     print yahoo_day
    # print y_money

    dates = ['2016-04-04', '2016-04-05', '2016-04-06', '2016-04-07']
    x = [4,5,6,7]
    print x

    from matplotlib import gridspec

    fig, ax1 = plt.subplots() #figsize=(30,15)
    ax1.plot(x, y_money)
    #ax1.set_xlabel('time (s)')
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('Close', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    y_sent = []
    for day in dates:
        y_sent.append(df['lat0'].ix[day].values[0])

    ax2 = ax1.twinx()
    ax2.plot(x, y_sent, color='r')
    ax2.set_ylabel('Sent1', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    y_sent = []
    for day in dates:
        y_sent.append(df['lat1'].ix[day].values[0])

    ax3 = ax1.twinx()
    ax3.plot(x, y_sent, color='r')
    ax3.set_ylabel('Sent2', color='g')
    for tl in ax3.get_yticklabels():
        tl.set_color('g')

    y_sent = []
    for day in dates:
        y_sent.append(df['lat1'].ix[day].values[0])

    ax4 = ax1.twinx()
    ax4.plot(x, y_sent, color='r')
    ax4.set_ylabel('Sent3', color='y')
    for tl in ax4.get_yticklabels():
        tl.set_color('y')

    y_sent = []
    for day in dates:
        y_sent.append(df['lat1'].ix[day].values[0])

    ax5 = ax1.twinx()
    ax5.plot(x, y_sent, color='r')
    ax5.set_ylabel('Sent4', color='c')
    for tl in ax5.get_yticklabels():
        tl.set_color('c')

    # plt.savefig('imgs/eda_nmf_quotes.png')
    plt.show()



if __name__ == '__main__':
    mongo_client = MongoClient()
    db = mongo_client.get_tweets
    coll = db.tweets

    symbols = ["GOOG", 'AAPL']
    k = 4

    df = pd.DataFrame()
    for sym in symbols:
        grouped_data = nmf_df(sym, k, coll)
        df = pd.concat([df, grouped_data])

    graph_it(df)
    # df[df['sym'] == 'AAPL'].head()
    # df.ix['2016-04-03']
    # db.tweets.aggregate( [ {$match: {'text': { $in :[/GOOG/, /AAPL/] }}}, {$sample: { size: 1 }} ] )
    # db.tweets.aggregate( [ {$match: {'text': { $in :[/GOOG/, /AAPL/] }, 'created_at': /Apr 03/}}, {$sample: { size: 1 }} ] )



# kmeans = KMeans()
# kmeans.fit(X)

#print "cluster centers:"
#print kmeans.cluster_centers_

# top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
# print "top features for each cluster:"
# for num, centroid in enumerate(top_centroids):
#     print "%d: %s" % (num, ", ".join(features[i] for i in centroid))
#
# #------
# distxy = squareform(pdist(top_centroids, metric='cosine'))
# link = linkage(distxy, method='complete')
#
# dendro = dendrogram(link, color_threshold=1.5, leaf_font_size=9)
# # fix spacing to better view dendrogram and the labels
# plt.subplots_adjust(top=.99, bottom=0.5, left=0.05, right=0.99)
# plt.show()
