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


def get_preds(features):  # features is the number of latents features that I want the nmf to run on
    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)

    df_test = get_nmf('data_wednesday', k=features) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    # Create models
    X_model_class, y_model_class = get_classifier_data(df_full)
    rf_class = RandomForestClassifier(n_estimators=1000)
    rf_class.fit(X_model_class, y_model_class)
    #
    X_model_regress, y_model_regress = get_regressor_data(df_full)
    rf_regress = RandomForestRegressor(n_estimators=1000)
    rf_regress.fit(X_model_regress, y_model_regress)

    # Get X and y values
    X_classify, y_classify  = get_classifier_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
    X_regress, y_regress = get_regressor_data(pd.DataFrame(df_test_full.ix['2016-04-11']))

    # Run models

    classifier_preds = rf_class.predict(X_classify)
    classifier_accuracy = accuracy(classifier_preds, y_classify)

    regressor_preds = rf_regress.predict(X_regress)
    regressor_mse = mean_squared_error(regressor_preds, y_regress)

    # I want to return the number of features, k, along with the accuracy of the classifier
    # and the MSE of the regressor.  This will give me an idea of how well things are doing
    # based on the number of features.
    return [k, classifier_accuracy, regressor_mse]


if __name__ == '__main__':
    # Running a for loop to check what the best number of k latent features is for a
    # classification and regression model.

    scores = []
    # looking at a range or features from 1 to 15
    for k in xrange(1,16):
        scores.append(get_preds(k))

    for score in scores:
        print score














#
