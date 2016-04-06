# udpate on broken urls
company_info = []

for url in list_of_urls:    # [:num_iter]
    content = urlopen()

    for url in list_of_urls:    # [:num_iter]
        content =
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

    columns = ['name', 'date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(company_info)
    df.columns=columns

try:
    urlopen('http://www.nasdaq.com/symbol/{0}/historical').read()
except:
    print "didn't work"
