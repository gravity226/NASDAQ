from math import pi
from bokeh.plotting import figure, show, output_file, save, curdoc
# from bokeh.sampledata.stocks import MSFT
from bokeh.io import output_notebook

from bokeh.models.widgets import TextInput
from bokeh.io import vform
from bokeh.client import push_session
from bokeh.driving import cosine


from yahoo_finance import Share
import pandas as pd

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

    session = push_session(curdoc())

    curdoc().add_periodic_callback(update, 1000)

    session.show() # open the document in a browser

    session.loop_until_closed() # run forever
    output_file("candlestick.html", title="candlestick.py example")
    # show(p)

if __name__ == '__main__':
    #df = get_data('AAPL')

    render_table('AAPL')















#
