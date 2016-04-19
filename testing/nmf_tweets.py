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


def load_json(sym, path='data_week_1'):  # pull the subsetted json file containing the json tweets
    with open(path + '/' + sym.upper() + '.json') as data_file:
        data = json.load(data_file)

    print "***** Loaded tweets, %i found for %s.. *****" % (len(data), sym)
    return data

def nmf_to_df(sym, k=4, path='data_week_1'):  # Find the weights of latents features in a group of tweets and return them in a df
    data = load_json(sym, path)

    sents = [ sentence['text'] for sentence in data ]
    dates = [ str(text['created_at']) for text in data ]
    d = np.array(dates).T
    d = d.reshape(len(dates), 1)

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(sents)
    #features = vectorizer.get_feature_names()
    print "Tweets vectorized..."
    feats = vectorizer.get_feature_names()

    model = NMF(n_components=k, init='random', random_state=0)
    latent_features = model.fit_transform(X)
    print "Model created..."
    coms = model.components_

    df = pd.DataFrame(latent_features)   #np.concatenate((d, latent_features), axis=1)
    df.columns = [ 'lat'+ str(n) for n in xrange(len(df.columns)) ]
    df['time_stamp'] = d
    #print df.head()

    df['date'] = pd.to_datetime(df['time_stamp']).apply(pd.datetools.normalize_date)
    df.pop('time_stamp')

    # Add Saturday's and Sunday's features to the previous Friday.  ( Stock don't run on the weekends )

    df['dow'] = df['date'].dt.dayofweek
    df['adj_date'] = df.apply(lambda row: row['date'] - pd.DateOffset(2) if row['dow'] == 6 else row['date'] - pd.DateOffset(1) if row['dow'] == 5 else row['date'], axis=1 )
    print "Adjusted dates..."
    #-----

    #print df.head()
    df.pop('date')
    df.pop('dow')
    grouped_data = df.groupby(['adj_date']).mean()
    grouped_data['sym'] = sym

    print "DataFrame created and aggregated..."
    return grouped_data

def datetime_to_str_date(dt):
    return re.sub(r'\T.+$','', dt.isoformat())

def get_date_list(start_date='2016-04-04', end_date='2016-04-08'):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    num_of_days = (end_date - start_date).days + 1

    date_list = map(datetime_to_str_date,
                [(start_date + datetime.timedelta(days=x)) for x in range(0, num_of_days)])
    return date_list, [ datetime.datetime.strptime(d, '%Y-%m-%d').day for d in date_list ]

def graph_it(sym, k=4, start_date='2016-04-04', end_date='2016-04-08'): # Specificy a stock symbol, number of latent features k, a start and an end date
    df = nmf_to_df(sym, k)
    yahoo = Share(sym)
    yahoo_days = yahoo.get_historical(start_date, end_date)
    print "Completed Yahoo historical API search..."

    y_money = [ day['Close'] for day in yahoo_days ] # the closing prices for each day from start to end

    date_list, day_list = get_date_list(start_date, end_date)

    color_list = ['b','g','r','c','m','y','k','w']  # usable colors for matplotlib

    print "Creating plots..."

    fig, ax1 = plt.subplots() #figsize=(30,15)
    ax1.plot(day_list, y_money)
    ax1.set_ylabel('Close', color=color_list[0])
    for tl in ax1.get_yticklabels():
        tl.set_color(color_list[0])

    for sp in range(k):
        y_sent = []
        lat_feat = 'lat' + str(sp)
        for day in date_list:
            print df[lat_feat]
            y_sent.append(df[lat_feat].ix[day])

        ax2 = ax1.twinx()
        ax2.plot(day_list, y_sent, color=color_list[sp+1])
        ax2.set_ylabel('Sent'+str(sp), color=color_list[sp+1])
        for tl in ax2.get_yticklabels():
            tl.set_color(color_list[sp+1])

    plt.show()


if __name__ == '__main__':
    'who knows...'















#
