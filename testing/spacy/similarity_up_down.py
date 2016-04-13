from top_companies import hand_made_list
import re
import json

from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.get_tweets
coll = db.tweets

from spacy.en import English
nlp = English()

sym = 'AAPL'
data = coll.find({'text': { '$in' :[re.compile(sym)] }})

up = 0
down = 0

text_data = [ nlp(cell['text']).noun_chunks for cell in data ]

# print text_data

for gen in text_data:
    for chunk in gen:
        if (u"their sector" not in chunk.orth_) and (u"$RXSF" not in chunk.orth_):
            u = chunk.similarity(nlp(u'buy'))
            #print "-------"
            #print "up:   ", chunk, u
            up += u

            d = chunk.similarity(nlp(u'sell'))
            #print "down: ", chunk, d
            down += d

print ''
print ''
print "up: ", up
print "down: ", down
