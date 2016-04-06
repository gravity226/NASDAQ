from top_companies import hand_made_list

from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.get_tweets
coll = db.tweets

companies = hand_made_list()

query_list = ['GOOG', 'Google']

print coll.find({'text': { '$in' :[/Goog/] }}).count()
# print coll.find_one()
