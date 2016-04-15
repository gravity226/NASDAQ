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

# Talked with Thomas; number of trees should be 1000 for 1 week of data and 3000 for 2 weeks. At some point increasing the number of trees will not help at all.
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
    classifier_accuracy = accuracy_score(classifier_preds, y_classify)

    regressor_preds = rf_regress.predict(X_regress)
    regressor_mse = mean_squared_error(regressor_preds, y_regress)

    # I want to return the number of features, k, along with the accuracy of the classifier
    # and the MSE of the regressor.  This will give me an idea of how well things are doing
    # based on the number of features.
    return [k, classifier_accuracy, regressor_mse]

def get_best_k():
    # Running a for loop to check what the best number of k latent features is for a
    # classification and regression model.

    scores = []
    # looking at a range or features from 1 to 15
    for k in xrange(1,16):
        scores.append(get_preds(k))

    for score in scores:
        print score

    return scores

"""
Results of changing k (nmf lanent features):

 k | classifier_accuracy | regressor_mse
[1, 0.56140350877192979, 2.1974000454301543] **
[2, 0.57894736842105265, 2.2452600812069834]
[3, 0.59649122807017541, 2.2370284583543385]
[4, 0.56140350877192979, 2.2970906146265389]
[5, 0.54385964912280704, 2.5255505926200668]
[6, 0.54385964912280704, 2.4648703921872124]
[7, 0.64912280701754388, 2.2597422456770997] **
[8, 0.50877192982456143, 2.5780246924461703]
[9, 0.52631578947368418, 2.2042888145023865]
[10, 0.54385964912280704, 2.2654013926589704]
[11, 0.56140350877192979, 2.3351928283392018]
[12, 0.56140350877192979, 2.3538218824115833]
[13, 0.56140350877192979, 2.4047433716326738]
[14, 0.57894736842105265, 2.6016246627065569]
[15, 0.52631578947368418, 2.4581636768588289]

"""

# Calculating the optimal tree depth
def check_best_depth(features=7):
    # this is how many trees will go into each forest
    depths = [ None, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]

    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)

    df_test = get_nmf('data_wednesday', k=features) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    # Get X and y values
    X_model_class, y_model_class = get_classifier_data(df_full)
    X_model_regress, y_model_regress = get_regressor_data(df_full)

    X_classify, y_classify  = get_classifier_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
    X_regress, y_regress = get_regressor_data(pd.DataFrame(df_test_full.ix['2016-04-11']))

    # Run models

    depth_list = []
    for depth in depths:
        # print "Checking depth of:", depth

        # Create models
        rf_class = RandomForestClassifier(n_estimators=1000, max_depth=depth)
        rf_class.fit(X_model_class, y_model_class)
        #
        rf_regress = RandomForestRegressor(n_estimators=1000, max_depth=depth)
        rf_regress.fit(X_model_regress, y_model_regress)

        classifier_preds = rf_class.predict(X_classify)
        classifier_accuracy = accuracy_score(classifier_preds, y_classify)

        regressor_preds = rf_regress.predict(X_regress)
        regressor_mse = mean_squared_error(regressor_preds, y_regress)

        depth_list.append([ depth, classifier_accuracy, regressor_mse ])
        print [ depth, classifier_accuracy, regressor_mse ]

    return depth_list

"""
Result of Depths where k = 1:

Depth | classifier_accuracy   | regressor_mse
[None, 0.52631578947368418, 2.1933871397405169]
[5, 0.63157894736842102, 2.2847668131098704]
[8, 0.61403508771929827, 2.2487532710807812]
[9, 0.64912280701754388, 2.1254666924103707]  ***
[10, 0.66666666666666663, 2.2115617230977227] **
[11, 0.63157894736842102, 2.2411273248738488]
[12, 0.66666666666666663, 2.1522936750320061] **
[13, 0.64912280701754388, 2.2323803219840079]
[14, 0.59649122807017541, 2.2070897058140595]
[15, 0.59649122807017541, 2.2129539849354307]
[16, 0.57894736842105265, 2.2013400014542688]
[17, 0.57894736842105265, 2.2097870078052586]
[18, 0.57894736842105265, 2.2274653710816268]
[19, 0.57894736842105265, 2.1934703949025542]
[20, 0.56140350877192979, 2.1979373026601778]
"""

"""
Result of Depths where k = 7:

Depth |  classifier_accuracy  | regressor_mse
[None, 0.63157894736842102, 2.2129582099444529]
[5, 0.66666666666666663, 2.2765806337887478]
[8, 0.63157894736842102, 2.3711845374294569]
[9, 0.66666666666666663, 2.3285225227015642]
[10, 0.63157894736842102, 2.2132327613074003]
[11, 0.68421052631578949, 2.248074453456558] ***
[12, 0.61403508771929827, 2.2059181125353255]
[13, 0.64912280701754388, 2.2023885029947561]
[14, 0.64912280701754388, 2.2783257708546691]
[15, 0.63157894736842102, 2.253376485859877]
[16, 0.64912280701754388, 2.2194322276732947]
[17, 0.66666666666666663, 2.2321510829001929]
[18, 0.64912280701754388, 2.1899636982247515]
[19, 0.63157894736842102, 2.1423237283439613] **
[20, 0.66666666666666663, 2.2909615968444488]

"""

def check_classifier_plus_regressor():
    pass

if __name__ == '__main__':
    # scores = get_best_k()
    depth_list = check_best_depth()
















#
