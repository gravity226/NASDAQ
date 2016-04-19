import pandas as pd
import requests
from top_companies import hand_made_list
import os

from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = os.urandom(12)

from yahoo_finance import Share
import pandas as pd

# ---------- DEFINE FUNCTIONS ----------

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

# ---------- START APP ----------

@app.route('/')
def form():
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            session['active'] = False
    companies = hand_made_list()
    return render_template('form.html',
                            companies=companies.keys())

@app.route('/error')
def error():
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            session['active'] = False
    companies = hand_made_list()
    return render_template('error.html')

@app.route('/display', methods=['POST', 'GET'])
def display():
    # Is the user coming from the form page?
    try:
        sym = str(request.form['user_input']).strip().upper() or 'SPY'
        session['active'] = True
        session['sym'] = sym
    except:
        # If a user goes to the display page and a session is not active
        if session.get('active') != True:
            sym = 'SPY'
            session['active'] = True
            session['sym'] = sym
        else:
            sym = session['sym'] # if a session is active leave the sym alone

    share = Share(sym)
    if 'start' not in share.get_info():  # is there information related to the stock symbol in Yahoo Finance?
        # if request.method == 'POST':
        #     print "This is a test"
        #     # if request.form['submit'] == 'Submit':
        #     #     print "before change session"
        #         # session['active'] = False
        print "before return"
        return redirect("/error")
        # return render_template('error.html',
        #                         sym=session['sym'])
    else:
        quote = float(share.get_price())
        com_name = sym #hand_made_list()[sym][0]

        try:  # Error handling...  Some Stock symbols exist but there is no historical and/or daily information in Yahoo Finance...
            historical = share.get_historical('2016-03-13', '2016-04-18')
            canvas_list = []
            for day in historical:
                canvas_list.append([int(day['Date'][:4]),
                                    int(day['Date'][5:7]) - 1,
                                    int(day['Date'][-2:]),
                                    float(day['Open']),
                                    float(day['High']),
                                    float(day['Low']),
                                    float(day['Close'])
                                    ])
            info = share.get_info()
            open = share.get_open()
            high = share.get_days_high()
            low = share.get_days_low()
            price = share.get_price()
            canvas_list.append([int(info['end'][:4]),
                                int(info['end'][5:7]) - 1,
                                int(info['end'][-2:]),
                                float(open),
                                float(high),
                                float(low),
                                float(price)
                                ])

            return render_template('display.html',
                                    sym=session['sym'],
                                    com_name=com_name,
                                    quote=quote,
                                    canvas_list=canvas_list)
        except:
            return redirect("/error")

@app.route('/history')
def history():
    # If a user goes to the display page and a session is not active
    if session.get('active') != True:
        sym = 'SPY'
        session['active'] = True
        session['sym'] = sym
    else:
        sym = session['sym'] # if a session is active leave the sym alone

    share = Share(sym)
    historical = share.get_historical('2016-03-13', '2016-04-15')
    canvas_list = []
    for day in historical:
        canvas_list.append([int(day['Date'][:4]),
                            int(day['Date'][5:7]) - 1,
                            int(day['Date'][-2:]),
                            float(day['Open']),
                            float(day['High']),
                            float(day['Low']),
                            float(day['Close'])
                            ])
    info = share.get_info()
    open = share.get_open()
    high = share.get_days_high()
    low = share.get_days_low()
    price = share.get_price()
    canvas_list.append([int(info['end'][:4]),
                        int(info['end'][5:7]) - 1,
                        int(info['end'][-2:]),
                        float(open),
                        float(high),
                        float(low),
                        float(price)
                        ])

    return render_template('history.html',
                            canvas_list=canvas_list,
                            sym=sym)

@app.route('/predict')
def predict():
    # If a user goes to the display page and a session is not active
    if session.get('active') != True:
        sym = 'SPY'
        session['active'] = True
        session['sym'] = sym
    else:
        sym = session['sym'] # if a session is active leave the sym alone

    try:  # Error handling...  Some Stock symbols exist but there is no historical information in Yahoo Finance...
        share = Share(sym)

        historical = share.get_historical('2016-04-12', '2016-04-18') # need to auto input the date...

        canvas_list = []

        info = share.get_info()
        open = share.get_open()
        high = share.get_days_high()
        low = share.get_days_low()
        price = share.get_price()
        canvas_list.append([int(info['end'][:4]),
                            int(info['end'][5:7]) - 1,
                            int(info['end'][-2:]),
                            float(price)
                            ])

        for day in historical:
            canvas_list.append([int(day['Date'][:4]),
                                int(day['Date'][5:7]) - 1,
                                int(day['Date'][-2:]),
                                float(day['Close'])
                                ])

        df_preds = pd.read_csv('data/predictions.csv')
        date = df_preds[df_preds['sym'] == sym]['date'].values[0]
        historical_day = float(share.get_historical(date, date)[0]['Close'])
        year = date[:4]
        month = date[5:7]
        day = date[-2:]

        predicted_value = historical_day + df_preds[df_preds['sym'] == sym]['regressor_mse'].values[0]
        predicted_rmse = df_preds[df_preds['sym'] == sym]['mse'].values[0] ** .5

        box1_low = predicted_value - (predicted_rmse / 2.)
        box1_high = predicted_value + (predicted_rmse / 2.)

        box2_low = predicted_value - (predicted_rmse)
        box2_high = predicted_value + (predicted_rmse)

        return render_template('predict.html',
                                canvas_list=canvas_list,
                                sym=sym,
                                box1_low=box1_low,
                                box1_high=box1_high,
                                box2_low = box2_low,
                                box2_high=box2_high,
                                year=year,
                                month=month,
                                day=day)
    except:
        return redirect("/error")

@app.route('/test')
def test():
    # Is the user coming from the form page?
    try:
        sym = str(request.form['user_input']).strip().upper() or 'SPY'
        session['active'] = True
        session['sym'] = sym
    except:
        # If a user goes to the display page and a session is not active
        if session.get('active') != True:
            sym = 'SPY'
            session['active'] = True
            session['sym'] = sym
        else:
            sym = session['sym'] # if a session is active leave the sym alone

    share = Share(sym)
    quote = float(share.get_price())
    com_name = hand_made_list()[sym][0]

    return render_template('test.html',
                            sym=session['sym'],
                            com_name=com_name,
                            quote=quote)

@app.route('/contact')
def contact():

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)














#
