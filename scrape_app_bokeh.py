import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen

from math import pi
from bokeh.plotting import figure, show, output_file, save, curdoc
# from bokeh.sampledata.stocks import MSFT
from bokeh.io import output_notebook

from bokeh.models.widgets import TextInput
from bokeh.io import vform
from bokeh.client import push_session
from bokeh.driving import cosine
from bokeh.embed import components

from testing.tweepy_search import get_twitter_data
from testing.tfidf_tweets import create_d3_list

from flask import Flask, render_template, request
app = Flask(__name__)

from yahoo_finance import Share
import pandas as pd

# ---------- DEFINE FUNCTIONS ----------

share = Share('AAPL')

def get_data(sym):
    share = Share(sym)
    data = share.get_historical('2016-03-11', '2016-04-11')

    df = pd.DataFrame()
    df['date'] = [ day['Date'] for day in data ]
    df['date'] = pd.to_datetime(df['date']).apply(pd.datetools.normalize_date)

    df['open'] = [ float(open['Open']) for open in data ]
    df['close'] = [ float(close['Close']) for close in data ]
    df['high'] = [ float(high['High']) for high in data ]
    df['low'] = [ float(low['Low']) for low in data ]

    return df

def update():
    share.refresh()
    p.title = share.get_price()

def render_table(sym):
    df = get_data(sym)

    text_input = TextInput(value=sym.upper(), title="Label:")
    mids = (df['open'] + df['close'])/2
    spans = abs(df['open'] - df['close'])
    inc = df['close'] > df['open']
    dec = df['close'] < df['open']
    w = 12*60*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    global p
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=750, plot_height=300, toolbar_location="left")

    p.title = sym.upper() + " Candlestick"
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
    p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

    # session = push_session(curdoc())
    #
    # curdoc().add_periodic_callback(update, 1000)
    #
    # session.show() # open the document in a browser
    #
    # session.loop_until_closed() # run forever
    # output_file("candlestick.html", title="candlestick.py example")
    # show(p)
    script, div = components(p)
    return script, div

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
    script, div = render_table(sym)
    historical_url = 'http://www.nasdaq.com/symbol/{0}/historical'.format(sym.strip())
    d3_data = create_d3_list(sym)[:30]

    return render_template('display.html',
                            sym=sym,
                            script=script,
                            div=div,
                            historical_url=historical_url,
                            com_name=com_name,
                            d3_data=d3_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
