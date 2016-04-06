import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen

from math import pi
from bokeh.plotting import figure, show, output_file, save
# from bokeh.sampledata.stocks import MSFT
from bokeh.io import output_notebook

from bokeh.models.widgets import TextInput
from bokeh.io import vform

from testing.tweepy_search import get_twitter_data
from testing.tfidf_tweets import create_d3_list

from flask import Flask, render_template, request
app = Flask(__name__)

# ---------- DEFINE FUNCTIONS ----------

def scrape_page(sym):
    url = 'http://www.nasdaq.com/symbol/{0}/historical'.format(sym.strip())
    try:
        company_info = []
        content = urlopen(url).read()
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
            company_info.append(['aapl', list_of_numbers[n * 6],
                                         float(list_of_numbers[n * 6 + 1]),
                                         float(list_of_numbers[n * 6 + 2]),
                                         float(list_of_numbers[n * 6 + 3]),
                                         float(list_of_numbers[n * 6 + 4]),
                                         int(list_of_numbers[n * 6 + 5].replace(",",''))])


        return company_info
    except:
        return "Could not find company"

def render_table(sym):
    company_info = scrape_page(sym)
    columns = ['name', 'date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(company_info, columns=columns)
    df['date'] = pd.to_datetime(df['date']).apply(pd.datetools.normalize_date)

    text_input = TextInput(value=sym.upper(), title="Label:")
    mids = (df['open'] + df['close'])/2
    spans = abs(df['open'] - df['close'])
    inc = df['close'] > df['open']
    dec = df['close'] < df['open']
    w = 12*60*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=750, plot_height=300, toolbar_location="left")

    p.title = sym.upper() + " Candlestick"
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
    p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

    output_file("templates/candlestick.html", title="candlestick.py example")
    save(p)

    return "candlestick.html"

def get_com_name(sym):
    df = pd.read_csv('data/companylist.csv')

    try:
        return df[df['Symbol']==sym.strip().upper()]['Name'].values[0]
    except:
        return 'Nada.....'

# ---------- START APP ----------

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/display', methods=['POST'])
def display():
    sym = str(request.form['user_input']).strip().upper()
    com_name = get_com_name(sym)
    link_to_table = render_table(sym)
    historical_url = 'http://www.nasdaq.com/symbol/{0}/historical'.format(sym.strip())
    d3_data = create_d3_list(sym)[:30]

    return render_template('display.html',
                            sym=sym,
                            link_to_table=link_to_table,
                            historical_url=historical_url,
                            com_name=com_name,
                            d3_data=d3_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
