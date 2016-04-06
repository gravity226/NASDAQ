# Yahoo Finance RSS Feed
# http://finance.yahoo.com/rss/headline?s=ticker(s)

import time

import feedparser
import json
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.get_yahoo_news
coll = db.news

from top_companies import hand_made_list

def get_feed(sym):  # run once, then run update_feed(sym)
    base_url = "http://finance.yahoo.com/rss/headline?s="
    url = base_url + sym

    feed = feedparser.parse(url)

    for entry in feed.entries:
        if coll.count({'id': entry.id}) == 0:
            try:
                entry['published_parsed'] = time.strftime('%Y-%m-%d %H:%M:%S', entry['published_parsed'])
                #print a
                coll.insert(entry)
                print "new", entry.id
            except:
                print "insert didn't work (probably no date)"
        else:
            print "not new"

    # return feed.entries[0]

if __name__ == '__main__':
    companies = hand_made_list()

    while True:
        for sym in companies.keys():
            get_feed(sym)
        time.sleep(60)


















#
