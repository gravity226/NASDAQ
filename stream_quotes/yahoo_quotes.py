from yahoo_finance import Share
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def add_dummies():
    sym = 'spy'
    yahoo = Share(sym)

    historical_train = yahoo.get_historical('2010-01-01', '2016-01-01')
    historical_test = yahoo.get_historical('2016-01-01', '2016-04-04')

    for n in xrange(1, len(historical_train)):
        if historical_train[n-1]['Close'] > historical_train[n]['Close']:
            historical_train[n]['Pred'] = 1
        elif historical_train[n-1]['Close'] < historical_train[n]['Close']:
            historical_train[n]['Pred'] = -1
        else:
            historical_train[n]['Pred'] = 0
        #print historical[n]['Pred']

    for n in xrange(1, len(historical_test)):
        if historical_test[n-1]['Close'] > historical_test[n]['Close']:
            historical_test[n]['Pred'] = 1
        elif historical_test[n-1]['Close'] < historical_test[n]['Close']:
            historical_test[n]['Pred'] = -1
        else:
            historical_test[n]['Pred'] = 0

    #historical.pop()
    df_train = pd.DataFrame(historical_train[1:len(historical_train)])
    df_train['Date_Time'] = pd.to_datetime(df_train['Date']).apply(pd.datetools.normalize_date)
    df_train['DOW'] = df_train['Date_Time'].dt.dayofweek
    df_train['DOY'] = df_train['Date_Time'].dt.dayofyear
    df_train['WOY'] = df_train['Date_Time'].dt.weekofyear
    df_train['Year'] = df_train['Date_Time'].dt.year
    df_train['Month'] = df_train['Date_Time'].dt.month
    df_train['Quarter'] = df_train['Date_Time'].dt.quarter

    df_test = pd.DataFrame(historical_test[1:len(historical_test)])
    df_test['Date_Time'] = pd.to_datetime(df_test['Date']).apply(pd.datetools.normalize_date)
    df_test['DOW'] = df_test['Date_Time'].dt.dayofweek
    df_test['DOY'] = df_test['Date_Time'].dt.dayofyear
    df_test['WOY'] = df_test['Date_Time'].dt.weekofyear
    df_test['Year'] = df_test['Date_Time'].dt.year
    df_test['Month'] = df_test['Date_Time'].dt.month
    df_test['Quarter'] = df_test['Date_Time'].dt.quarter

    df_train['Close'] = df_train['Close'].apply(lambda a: float(a))
    df_train['Open'] = df_train['Open'].apply(lambda a: float(a))
    df_train['High'] = df_train['High'].apply(lambda a: float(a))
    df_train['Low'] = df_train['Low'].apply(lambda a: float(a))

    df_test['Close'] = df_test['Close'].apply(lambda a: float(a))
    df_test['Open'] = df_test['Open'].apply(lambda a: float(a))
    df_test['High'] = df_test['High'].apply(lambda a: float(a))
    df_test['Low'] = df_test['Low'].apply(lambda a: float(a))

    df_train = pd.concat([df_train, pd.get_dummies(df_train['DOW'], prefix='dow')], axis=1)
    df_test = pd.concat([df_test, pd.get_dummies(df_test['DOW'], prefix='dow')], axis=1)

    features = ['Open', 'Close', 'High', 'Low', 'dow_1', 'dow_2', 'dow_3', 'dow_4']

    X_train = df_train[features].values
    y_train = df_train['Pred'].values

    X_test = df_test[features].values
    y_test = df_test['Pred'].values

    rfc_model = RandomForestClassifier(n_estimators=1000)
    rfc_model.fit(X_train, y_train)

    pred = rfc_model.predict(X_test)

    print "Accuracy Score:", accuracy_score(y_test, pred)

def second_attempt():
    sym = 'goog'
    yahoo = Share(sym)

    historical_train = yahoo.get_historical('2010-01-01', '2016-01-01')
    historical_test = yahoo.get_historical('2016-01-01', '2016-04-04')

    for n in xrange(1, len(historical_train)-1):
        if historical_train[n+1]['Close'] > historical_train[n]['Close']:
            historical_train[n]['Pred'] = 'above'
        elif historical_train[n+1]['Close'] < historical_train[n]['Close']:
            historical_train[n]['Pred'] = 'below'
        else:
            historical_train[n]['Pred'] = 'equal'
        #print historical[n]['Pred']

    for n in xrange(1, len(historical_test)-1):
        if historical_test[n+1]['Close'] > historical_test[n]['Close']:
            historical_test[n]['Pred'] = 'above'
        elif historical_test[n+1]['Close'] < historical_test[n]['Close']:
            historical_test[n]['Pred'] = 'below'
        else:
            historical_test[n]['Pred'] = 'equal'

    #historical.pop()
    df_train = pd.DataFrame(historical_train[1:len(historical_train)])
    df_train['Date_Time'] = pd.to_datetime(df_train['Date']).apply(pd.datetools.normalize_date)
    df_train['DOW'] = df_train['Date_Time'].dt.dayofweek
    df_train['DOY'] = df_train['Date_Time'].dt.dayofyear
    df_train['WOY'] = df_train['Date_Time'].dt.weekofyear
    df_train['Year'] = df_train['Date_Time'].dt.year
    df_train['Month'] = df_train['Date_Time'].dt.month
    df_train['Quarter'] = df_train['Date_Time'].dt.quarter

    df_test = pd.DataFrame(historical_test[1:len(historical_test)])
    df_test['Date_Time'] = pd.to_datetime(df_test['Date']).apply(pd.datetools.normalize_date)
    df_test['DOW'] = df_test['Date_Time'].dt.dayofweek
    df_test['DOY'] = df_test['Date_Time'].dt.dayofyear
    df_test['WOY'] = df_test['Date_Time'].dt.weekofyear
    df_test['Year'] = df_test['Date_Time'].dt.year
    df_test['Month'] = df_test['Date_Time'].dt.month
    df_test['Quarter'] = df_test['Date_Time'].dt.quarter

    #features = ['Open', 'Close', 'High', 'Low', 'DOW', 'DOY', 'WOY', 'Year', 'Month', 'Quarter']
    features = ['Open', 'Close', 'High', 'Low']

    X_train = df_train[features].values
    y_train = df_train['Pred'].values

    X_test = df_test[features].values
    y_test = df_test['Pred'].values

    rfc_model = RandomForestClassifier(n_estimators=100)
    rfc_model.fit(X_train, y_train)

    pred = rfc_model.predict(X_test)

    print "Accuracy Score:", accuracy_score(y_test, pred)
    # return df_train
    print pred[:10]
    print df_train.head()


def first_attempt():
    sym = 'goog'
    yahoo = Share(sym)

    historical_train = yahoo.get_historical('2010-01-01', '2016-01-01')
    historical_test = yahoo.get_historical('2016-01-02', '2016-04-03')

    for n in xrange(1, len(historical_train)-1):
        if historical_train[n+1]['Close'] > historical_train[n]['Close']:
            historical_train[n]['Pred'] = 'above'
        elif historical_train[n+1]['Close'] < historical_train[n]['Close']:
            historical_train[n]['Pred'] = 'below'
        else:
            historical_train[n]['Pred'] = 'equal'
        #print historical[n]['Pred']

    for n in xrange(1, len(historical_test)-1):
        if historical_test[n+1]['Close'] > historical_test[n]['Close']:
            historical_test[n]['Pred'] = 'above'
        elif historical_test[n+1]['Close'] < historical_test[n]['Close']:
            historical_test[n]['Pred'] = 'below'
        else:
            historical_test[n]['Pred'] = 'equal'

    #historical.pop()
    df_train = pd.DataFrame(historical_train[1:len(historical_train)])

    df_test = pd.DataFrame(historical_test[1:len(historical_test)])

    X_train = df_train[['Open', 'Close', 'High', 'Low']].values
    y_train = df_train['Pred'].values

    X_test = df_test[['Open', 'Close', 'High', 'Low']].values
    y_test = df_test['Pred'].values

    rfc_model = RandomForestClassifier(n_estimators=100)
    rfc_model.fit(X_train, y_train)

    pred = rfc_model.predict(X_test)

    print "Accuracy Score:", accuracy_score(y_test, pred)







#
