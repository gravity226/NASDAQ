import cPickle as pickle
from yahoo_finance import Share

import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import time

# my methods
import nmf_tweets as nt
from top_companies import hand_made_list
from predict_nmf import *

def pickle_model(class_name="class_model.pkl", regress_name="regress_model.pkl"):
    df_full = pd.read_csv('data_week_1/pd_data.csv')
    df_full.index = df_full['adj_date']
    df_full.pop('adj_date')

    # Get X and y values
    X_model_class, y_model_class = get_classifier_data(df_full)
    X_model_regress, y_model_regress = get_regressor_data(df_full)

    X_classify, y_classify  = get_classifier_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
    X_regress, y_regress = get_regressor_data(pd.DataFrame(df_test_full.ix['2016-04-11']))

    # Run models
    rf_class = RandomForestClassifier(n_estimators=2000, max_depth=8)
    rf_class.fit(X_model_class, y_model_class)
    #
    rf_regress = RandomForestRegressor(n_estimators=2000, max_depth=8)
    rf_regress.fit(X_model_regress, y_model_regress)

    with open(class_name, 'w') as f:
        pickle.dump(rf_class, f)

    with open(regress_name, 'w') as f:
        pickle.dump(rf_regress, f)

if __name__ == '__name__':
    pickle_model()
