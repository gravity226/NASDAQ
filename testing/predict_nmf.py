from yahoo_finance import Share
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
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
            # print "Daily Values: ", daily_data
            stock_values.append([ 0, 0, 0, 0, 0, 0 ])  # Yahoo finance couldn't find any data for this day... wtf?
            print 'Added', sym
        else:
            try:
                # print "Daily Values: ", daily_data # dict comes in backwards, start with -1 then -2...
                stock_values.append([ float(daily_data[-1]['Open']),
                                      float(daily_data[-1]['Close']),
                                      float(daily_data[-1]['High']),
                                      float(daily_data[-1]['Low']),
                                      float(daily_data[-2]['Close']),
                                      float(daily_data[-2]['Close']) - float(daily_data[-1]['Close']) ])
                                      # last cell adds the difference in closing prices from "today" to "tomorrow"
                # print 'Added', sym
            except:
                stock_values.append([ float(daily_data[-1]['Open']),
                                      float(daily_data[-1]['Close']),
                                      float(daily_data[-1]['High']),
                                      float(daily_data[-1]['Low']),
                                      float(daily_data[-1]['Close']),
                                      0 ])
        count += 1

    stock_values = np.array(stock_values)
    print stock_values
    print "np shape", stock_values.shape
    print "df shape", df.shape


    df['open'] = stock_values[:,0]
    df['close'] = stock_values[:,1]
    df['high'] = stock_values[:,2]
    df['low'] = stock_values[:,3]
    df['next_day_close'] = stock_values[:,4]
    df['dif_in_close'] = stock_values[:,5]

    # you could change this formula to check if dif_in_close is positive or not..
    df['pred'] = df.apply(lambda row: 1 if row['close'] < row['next_day_close'] else -1 if row['close'] > row['next_day_close'] else 0, axis=1)

    return df

def get_classifier_data(df):
    y = df['pred'].values
    cols = list(df.columns)
    cols.remove('pred')
    cols.remove('sym')
    cols.remove('dif_in_close')
    cols.remove('next_day_close')
    X = df[cols].values
    return X, y

def get_regressor_data(df):
    y = df['dif_in_close'].values
    cols = df.columns
    cols.remove('pred')
    cols.remove('sym')
    cols.remove('dif_in_close')
    X = df[cols].values # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    return X, y

def add_dummies(df):
    companies = hand_made_list()
    # companies = {'AAPL': "apple" }
    currencies = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "EURJPY", "EURGBP", "USD", "EUR", "JPY", "GBP", "CHF"]

    for sym in companies.keys():
        if sym not in currencies and sym != 'CAM': # drop CAM because not enough data in Yahoo Fiance
            df[sym] = 0
            df[sym] = df['sym'].apply(lambda asdf: 1 if asdf == sym else 0)

    df.pop('GOOG')
    return df

if __name__ == '__main__':
    df = get_nmf()
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)
    # df_train.drop(['dif_in_close', 'pred', 'sym'], inplace=True, axis=1)

    df_test = get_nmf('data_wednesday') # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)
    #
    X_class, y_class = get_classifier_data(df_full)
    rf_class = RandomForestClassifier(n_estimators=1000)
    rf_class.fit(X_class, y_class)
    #
    # X_regress, y_regress = get_regressor_data(df_full)
    # rf_regress = RandomForestRegressor(n_estimators=1000)
    # rf_regress.fit(X_regress, y_regress)
    #
    # # search_on = df_full[df_full['sym'] =='GOOG'].ix['2016-04-08'][['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    #
    classify_on = get_classifier_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-11']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    classify_on_12 = get_classifier_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-12']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    classify_on_13 = get_classifier_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-13']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    #
    # regress_on = get_regressor_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-11']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    # regress_on_12 = get_regressor_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-12']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    # regress_on_13 = get_regressor_data(df_test_full[df_test_full['sym'] == 'GOOG'].ix['2016-04-13']) # [['lat0', 'lat1', 'lat2', 'lat3', 'open', 'close', 'high', 'low']].values
    #
    # print ''
    # print "Predict Tuesday", rf_class.predict(classify_on)
    # print "Predict Wednesday", rf_class.predict(classify_on_12)
    # print "Predict Thursday", rf_class.predict(classify_on_13)
    # print ''
    # print "Regress Pred Tuesday", rf_regress.predict(regress_on)
    # print "Regress Pred Wednesday", rf_regress.predict(regress_on_12)
    # print "Regress Pred Thursday", rf_regress.predict(regress_on_13)













#
