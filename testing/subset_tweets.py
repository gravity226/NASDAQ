from top_companies import hand_made_list
import re
import json

from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.get_tweets
coll = db.tweets

def load_data(sym):
    with open(sym) as output:
        data = json.loads(output.read())
        coll.insert(data)

if __name__ == '__main__':
    companies = hand_made_list()
    print companies

    query_list = ['SP500']
    date_list = [re.compile('Apr 01')]

    # for key, item in companies.items():
    #     query_list.append(key)
    #     #query_list.append(re.compile(item[0]))
    #
    # print coll.count({'text': { '$in' :query_list }})
    # print coll.count()
    #
    # for file_name in query_list:
    #     with open('data_dump/' + file_name + '.json', 'w+') as output:
    #         print file_name
    #         data = [ item for item in coll.find({'text': { '$in' :[re.compile(file_name)] }, 'created_at': { '$in' :date_list }}, {'_id': False}) ]
    #         json.dump(data, output)

#
# print data






#
