#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import pandas as pd
import json
import numpy as np
import time

from top_companies import get_companies, hand_made_list

#Variables that contains the user credentials to access Twitter API
access_token = "2355343910-2WPMYMG8srWvbbVBHD6wQBuRYMEHv61qDFpFZ6V"
access_token_secret = "rNx1po32JApw6PuvvIcHYGcGphaDkeaWOFyLK0u3Zi3K9"
consumer_key = "GclvOy6SP3M7HtACTg6uTlDPp"
consumer_secret = "IbwkIem9BzS8Ebt9SRgGFauvjxqrDS6ISjkXoZ1j8EnIwCV4rK"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, coll=''):
        self.coll = coll

    def on_data(self, data):
        print data
        self.coll.insert(json.loads(data)) # add instance to mongo db get_tweets
        return True

    def on_error(self, status):
        print status

# def get_companies():
#     df = pd.read_csv('../data/companylist.csv')
#     company_list = list(df['Symbol'])
#     company_list = [ "#" + company for company in company_list ]
#     return company_list
#
def run_twitter_query():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #names = list(np.array(get_companies())[:,1])
    #print names[num1:num2]
    d = hand_made_list()
    search_list = []
    for key, value in d.items():
        if key == 'SPY':
            search_list.append(value[0]) # append the full anme of the symbol
            search_list.append('#SP500') # Don't append #SPY because it's not helpful
            search_list.append('$SP500')
        elif key == 'F':
            # search_list.append(value[0]) # append the full name of the symbol
            search_list.append('Ford') # append the name of the symbol
        elif key == 'GE':
            search_list.append('General Electric') # append the full anme of the symbol
        elif key == 'S':
            search_list.append('Sprint') # append the full anme of the symbol
        elif key == 'T':
            search_list.append('AT&T') # append the full anme of the symbol
        elif key == 'MU':
            search_list.append('Micron Tech') # append the full anme of the symbol
        elif key == 'TRI':
            search_list.append('Thomson Reuters') # append the full anme of the symbol
        else:
            for cell in value:
                search_list.append(cell)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=search_list)

if __name__ == '__main__':
    from pymongo import MongoClient
    mongo_client = MongoClient()
    db = mongo_client.get_tweets_3
    coll = db.tweets

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener(coll)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # names = list(np.array(get_companies())[:,0])
    # symbols = list(np.array(get_companies())[:,1])
    # print symbols[:50]

    d = hand_made_list()
    search_list = []
    for key, value in d.items():
        for cell in value:
            search_list.append(cell)

    while True:
        try:
            stream.filter(track=search_list)
        except:
            print "error... who knows..."
            time.sleep(5)
