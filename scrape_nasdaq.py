import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen

def get_urls():
    companies = pd.read_csv('companylist.csv')
    return [ [com.strip(), 'http://www.nasdaq.com/symbol/{0}/historical'.format(com.strip())] for com in companies['Symbol'] ]

def get_com_info(list_of_urls, num_iter=1): #max num_iter = 6703 - 1
    company_info = []
    failures = []

    for url in list_of_urls:    # [:num_iter]
        try:
            content = urlopen(url[1]).read()
            soup = BeautifulSoup(content)
            titles = soup.select('div#quotes_content_left_pnlAJAX table tbody tr td')

            list_of_numbers = []
            for row in titles:  # parses all the values returned from beautiful soup pull
                if row.text.strip() != '':
                    list_of_numbers.append(row.text.strip())

            formatted_list = []
            # Need to skip the first row of data becuase it is not useful...
            for n in xrange(5, len(list_of_numbers)/6):   # creates an n by 6 list for each company
                #formatted_list.append([list_of_numbers[n * 6], list_of_numbers[n * 6 + 1], list_of_numbers[n * 6 + 2], list_of_numbers[n * 6 + 3], list_of_numbers[n * 6 + 4], list_of_numbers[n * 6 + 5]])
                company_info.append([url[0], list_of_numbers[n * 6], list_of_numbers[n * 6 + 1], list_of_numbers[n * 6 + 2], list_of_numbers[n * 6 + 3], list_of_numbers[n * 6 + 4], list_of_numbers[n * 6 + 5]])

            print url[0], 'Completed'
        except:
            print url[0], 'Failed'
            failures.append(url[0])

    columns = ['name', 'date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(company_info)
    df.columns=columns
    df.to_csv('data/company_data.csv')

    df_failures = pd.DataFrame(failures)
    df_failures.to_csv('data/fails.csv')

    #return df


if __name__ == '__main__':
    list_of_urls = get_urls()
    get_com_info(list_of_urls, 2)

    #print df

    # check out http://selenium-python.readthedocs.org/navigating.html#interacting-with-the-page
    # for check tags on webpage


















#
