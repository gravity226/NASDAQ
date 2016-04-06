from testing.top_companies import get_companies, hand_made_list
from googlefinance import getQuotes
import json

companies = hand_made_list().keys()
#print companies

print json.dumps(getQuotes(companies), indent=2)
