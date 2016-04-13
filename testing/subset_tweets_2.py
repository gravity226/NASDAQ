from top_companies import hand_made_list
import re
import json

from pymongo import MongoClient


def save_json(sym, data): # sym is a stock symbol; data is dict to be put into json for one stock symbol
    with open('data_dump/' + sym + '.json', 'w+') as output:
        print "writing: ", sym
        json.dump(data, output)

def subset_data():
    mongo_client = MongoClient()
    db = mongo_client.get_tweets
    coll = db.tweets

    companies = hand_made_list()
    # print companies

    companies_json = {}
    for key, val in companies.items():
        companies_json[key] = []

    companies_json['SP500'] = []

    print "Reading Data from Mongo......"
    data = coll.find()

    ids = []

    for cell in data:
        # try:
        #     if cell['_id'] not in ids:
        #         ids.append(cell['id'])
        try:
            for sym, l in companies_json.items():
                if (sym == 'SP500' or sym == 'SPY'):
                    if 'SP500' in str(cell['text']).upper():
                        #pass
                        #print 'SP500'
                        companies_json['SPY'].append({'created_at': cell['created_at'], 'text': cell['text']})
                        print sym
                elif sym == 'T':
                    if 'AT&T' in str(cell['text']).upper():
                        #pass
                        #print 'AT&T'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                        print sym
                elif sym == 'S':
                    if 'SPRINT' in str(cell['text']).upper():
                        #pass
                        #print 'Sprint'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                        print sym
                elif sym == 'F':
                    if 'Ford' in str(cell['text']) or ' ford ' in str(cell['text']):
                        #pass
                        #print 'Ford'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                        print sym
                elif sym == 'GE':
                    if 'General Electric' in str(cell['text']).upper():
                        #pass
                        #print 'General Electric'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                        print sym
                elif sym == 'MU':
                    if 'Micron Tech' in str(cell['text']).upper():
                        #pass
                        #print 'General Electric'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                elif sym == 'TRI':
                    if 'Thomson Reuters' in str(cell['text']).upper() or '$TRI' in str(cell['text']).upper():
                        #pass
                        #print 'General Electric'
                        companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})

                elif '$' + str(sym) in str(cell['text']).upper() or '#' + str(sym) in str(cell['text']).upper() or str(companies[sym][0]).upper() in str(cell['text']).upper():
                    print sym
                    companies_json[sym].append({'created_at': cell['created_at'], 'text': cell['text']})
                else:
                    pass
                    #print 'nada'
        except:
            pass
            #print "unicode problem"
            # c = cell
            # break
        # except:
        #     pass

    return companies_json


if __name__ == '__main__':
    companies_json = subset_data()

    for sym, l in companies_json.items():
        save_json(sym, l)

    # date_list = [re.compile('Apr 01')]


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
