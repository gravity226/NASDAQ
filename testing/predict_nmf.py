from yahoo_finance import Share
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time

import nmf_tweets as nt

from top_companies import hand_made_list

def get_stock_data(sym, start_date, end_date):
    test = True     # Sometimes the yahoo api does not connect...
    while test:
        try:
            yahoo = Share(sym)
            data = yahoo.get_historical(start_date, end_date)        #'2016-01-01', '2016-01-02')
            test = False
        except:
            print "retry connection..."
            time.sleep(5)  # wait 5 seconds and try again

    return data

def get_nmf(path='data_week_1'):
    companies = hand_made_list()
    # companies = {'AAPL': "apple" }
    currencies = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "EURJPY", "EURGBP", "USD", "EUR", "JPY", "GBP", "CHF"]

    df = pd.DataFrame()
    no_data = []
    for sym in companies.keys():
        if sym not in currencies and sym != 'CAM': # drop CAM because not enough data in Yahoo Fiance
            try:
                temp_df = nt.nmf_to_df(sym, 4, path)  # symbol based on 4 features
                df = pd.concat([df, temp_df])
            except:
                no_data.append(sym)
    #df = nt.nmf_to_df('AAPL', 4)
    return df

def add_yahoo_to_df(df):
    print "***** Adding Yahoo Finance Data *****"
    stock_values = []
    count = 0

    # Look up stock symbol info by date
    for day in df.index:
        sym = df.ix[count]['sym']
        print "Getting", sym
        daily_data = get_stock_data(sym, str(day)[:-9], str(day + pd.DateOffset(4))[:-9])
        if len(daily_data) == 0:
            print "Daily Values: ", daily_data
            stock_values.append([ 0, 0, 0, 0, 0 ])  # Yahoo finance couldn't find any data for this day... wtf?
            print 'Added', sym
        else:
            try:
                print "Daily Values: ", daily_data # dict comes in backwards, start with -1 then -2...
                stock_values.append([ float(daily_data[-1]['Open']),
                                      float(daily_data[-1]['Close']),
                                      float(daily_data[-1]['High']),
                                      float(daily_data[-1]['Low']),
                                      float(daily_data[-2]['Close']) ])
                print 'Added', sym
            except:
                stock_values.append([ float(daily_data[-1]['Open']),
                                      float(daily_data[-1]['Close']),
                                      float(daily_data[-1]['High']),
                                      float(daily_data[-1]['Low']),
                                      float(daily_data[-1]['Close']) ])
        count += 1

    stock_values = np.array(stock_values)
    df['open'] = stock_values[:,0]
    df['close'] = stock_values[:,1]
    df['high'] = stock_values[:,2]
    df['low'] = stock_values[:,3]
    df['next_day_close'] = stock_values[:,4]

    df['pred'] = df.apply(lambda row: 1 if row['close'] < row['next_day_close'] else -1 if row['close'] > row['next_day_close'] else 0, axis=1)

    return df

def get_forest_data(df_full):
    X = df_full[['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    y = df_full['pred'].values
    return X, y

def get_forest_data_sym(df_full):
    X = df_full[['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low', 'sym']].values
    y = df_full['pred'].values
    return X, y

def add_zeros(df):
    companies = hand_made_list()
    # companies = {'AAPL': "apple" }
    currencies = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "EURJPY", "EURGBP", "USD", "EUR", "JPY", "GBP", "CHF"]

    df = pd.DataFrame()
    no_data = []
    for sym in companies.keys():
        if sym not in currencies and sym != 'CAM': # drop CAM because not enough data in Yahoo Fiance
            df[sym] = 0
    return df

def add_ones(df):
     return df

if __name__ == '__main__':
    df = get_nmf()
    df_full = add_yahoo_to_df(df)

    df_test = get_nmf('data_wednesday')
    df_test_full = add_yahoo_to_df(df_test)

    X, y = get_forest_data(df_full)
    rf = RandomForestClassifier(n_estimators=1000)
    rf.fit(X, y)

    search_on = df_full[df_full['sym'] =='GOOG'].ix['2016-04-08'][['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values

    test_on = df_test_full[df_test_full['sym'] =='GOOG'].ix['2016-04-11'][['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    test_on_12 = df_test_full[df_test_full['sym'] =='GOOG'].ix['2016-04-12'][['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    test_on_13 = df_test_full[df_test_full['sym'] =='GOOG'].ix['2016-04-13'][['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    rf.predict(search_on)













#
