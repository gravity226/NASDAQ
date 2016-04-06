from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.get_tweets
coll = db.tweets

import streaming_example2 as se2

if __name__ == '__main__':
    se2.run_twitter_query(coll)




















#
