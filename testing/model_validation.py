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
def get_preds(features, trees=3000, depth=19):  # features is the number of latents features that I want the nmf to run on
    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)   # Why aren't you using df_full?

    df_test = get_nmf('data_wednesday', k=features) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    # Create models
    X_model_class, y_model_class = get_classifier_data(df_full)
    rf_class = RandomForestClassifier(n_estimators=trees, max_depth=depth)
    rf_class.fit(X_model_class, y_model_class)
    #
    X_model_regress, y_model_regress = get_regressor_data(df_full)
    rf_regress = RandomForestRegressor(n_estimators=trees, max_depth=depth)
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
    return [features, classifier_accuracy, regressor_mse]

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

"""
Setting 3000 trees and depth 19

[1, 0.57894736842105265, 2.1791716966865917]
[2, 0.56140350877192979, 2.2280989888786409]
[3, 0.56140350877192979, 2.3549755545716797]
[4, 0.54385964912280704, 2.3346274700742717]
[5, 0.56140350877192979, 2.5639916392998958]
[6, 0.54385964912280704, 2.360563505070961]
[7, 0.64912280701754388, 2.298865093546838]
[8, 0.49122807017543857, 2.5145548560596547]
[9, 0.52631578947368418, 2.3604469166415778]
[10, 0.52631578947368418, 2.2837704588383803]
[11, 0.54385964912280704, 2.3399798163237007]
[12, 0.52631578947368418, 2.3702842061238076]
[13, 0.54385964912280704, 2.3486366415035294]
[14, 0.54385964912280704, 2.5039893925533541]
[15, 0.56140350877192979, 2.5882828069373294]
"""

# Calculating the optimal tree depth
def check_best_depth(features=1):
    # this is how many trees will go into each forest
    depths = [ None, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]

    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_full = add_dummies(df_full)

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

changed to add dull_df with dummies...
[None, 0.57894736842105265, 2.2017808484037746]
[5, 0.64912280701754388, 2.2433095636031593]
[8, 0.64912280701754388, 2.171797148220568]
[9, 0.64912280701754388, 2.2155791216970546]
[10, 0.61403508771929827, 2.1946808744114876]
[11, 0.64912280701754388, 2.1981812588802843]
[12, 0.61403508771929827, 2.1236642763633973]
[13, 0.61403508771929827, 2.1659399767879957]
[14, 0.59649122807017541, 2.284174077687136]
[15, 0.57894736842105265, 2.2558817632929244]
[16, 0.57894736842105265, 2.1410387338733754]
[17, 0.56140350877192979, 2.2370648920394425]
[18, 0.54385964912280704, 2.1887951769338505]
[19, 0.57894736842105265, 2.07015634218331]  *****
[20, 0.57894736842105265, 2.1471268910122823]

[None, 0.54385964912280704, 2.0717128719385154]  ***
[5, 0.61403508771929827, 2.3133394844996573]
[8, 0.63157894736842102, 2.213111982440636]
[9, 0.64912280701754388, 2.2362104257178603]
[10, 0.64912280701754388, 2.1773856296815546]
[11, 0.66666666666666663, 2.2654293521807993]  **
[12, 0.63157894736842102, 2.2384199257786528]
[13, 0.63157894736842102, 2.2306566305003361]
[14, 0.59649122807017541, 2.2519711249709511]
[15, 0.56140350877192979, 2.1913248121557332]
[16, 0.56140350877192979, 2.3687865972631359]
[17, 0.59649122807017541, 2.2123882903209786]
[18, 0.57894736842105265, 2.1983269140608979]
[19, 0.61403508771929827, 2.2772757110963351]
[20, 0.61403508771929827, 2.1580559641972381]
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

Changed to add dummies in df_full...

[None, 0.63157894736842102, 2.1982287230071162]
[5, 0.64912280701754388, 2.194372819893454]
[8, 0.64912280701754388, 2.1575430975849756] **
[9, 0.68421052631578949, 2.2390462128646385]  ***
[10, 0.64912280701754388, 2.1859153362366706]
[11, 0.66666666666666663, 2.3452450556949627]
[12, 0.63157894736842102, 2.3050391571533488]
[13, 0.66666666666666663, 2.1789300161603289]
[14, 0.66666666666666663, 2.3348227437701299]
[15, 0.64912280701754388, 2.3008082182624112]
[16, 0.64912280701754388, 2.1674116515944792]
[17, 0.63157894736842102, 2.2092996540516858]
[18, 0.64912280701754388, 2.251684031650512]
[19, 0.64912280701754388, 2.1621298193648495]
[20, 0.63157894736842102, 2.2096159961424808]


Thoughts.  There are not enough trees here.  I think this because there are fluctuations in
the finally scores.
"""

def check_best_avg_depth(features=1):
    # this is how many trees will go into each forest
    depths = [ None, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]

    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_full = add_dummies(df_full)

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
        class_list = []
        regress_list = []

        for n in range(20):
            # Create models
            rf_class = RandomForestClassifier(n_estimators=3000, max_depth=depth)
            rf_class.fit(X_model_class, y_model_class)
            #
            rf_regress = RandomForestRegressor(n_estimators=3000, max_depth=depth)
            rf_regress.fit(X_model_regress, y_model_regress)

            classifier_preds = rf_class.predict(X_classify)
            classifier_accuracy = accuracy_score(classifier_preds, y_classify)

            regressor_preds = rf_regress.predict(X_regress)
            regressor_mse = mean_squared_error(regressor_preds, y_regress)

            class_list.append(classifier_accuracy)
            regress_list.append(regressor_mse)

        depth_list.append([ depth, class_list, regress_list ])
        print depth

    return depth_list

def check_num_trees(features=1):
    trees = [ 1000, 2000, 3000, 4000, 5000 ]  # There are roughly 4000 observations here...

    # Create dataframes
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_full = add_dummies(df_full)

    df_test = get_nmf('data_wednesday', k=features) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    # Get X and y values
    X_model_class, y_model_class = get_classifier_data(df_full)
    X_model_regress, y_model_regress = get_regressor_data(df_full)

    X_classify, y_classify  = get_classifier_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
    X_regress, y_regress = get_regressor_data(pd.DataFrame(df_test_full.ix['2016-04-11']))

    # Run models

    tree_list = []
    for forest in trees:
        # print "Checking depth of:", depth

        # Create models
        rf_class = RandomForestClassifier(n_estimators=forest, max_depth=19)
        rf_class.fit(X_model_class, y_model_class)
        #
        rf_regress = RandomForestRegressor(n_estimators=forest, max_depth=19)
        rf_regress.fit(X_model_regress, y_model_regress)

        classifier_preds = rf_class.predict(X_classify)
        classifier_accuracy = accuracy_score(classifier_preds, y_classify)

        regressor_preds = rf_regress.predict(X_regress)
        regressor_mse = mean_squared_error(regressor_preds, y_regress)

        tree_list.append([ forest, classifier_accuracy, regressor_mse ])
        print [ forest, classifier_accuracy, regressor_mse ]

    return tree_list

"""
Ran with k = 7 and max_depth = 11:

[1000, 0.63157894736842102, 2.2919523154750259]
[2000, 0.68421052631578949, 2.2604153289260442]
[3000, 0.68421052631578949, 2.2010793990696582]  ***
[4000, 0.66666666666666663, 2.228108550504273]
[5000, 0.66666666666666663, 2.2182657415400913]

"""

"""
Ran with k = 1 and max_depth = 11:

[1000, 0.66666666666666663, 2.1689095324032226]
[2000, 0.66666666666666663, 2.1670750884525676] ***
[3000, 0.63157894736842102, 2.1985202152007455]
[4000, 0.63157894736842102, 2.2402596842582341]
[5000, 0.64912280701754388, 2.2614219015092809]

"""

"""
Ran with k = 1 and max_depth = 19:

[1000, 0.61403508771929827, 2.076833522747997]
[2000, 0.57894736842105265, 2.209193216573484]
[3000, 0.61403508771929827, 2.1600652520307184]
[4000, 0.57894736842105265, 2.2374395646382381]
[5000, 0.56140350877192979, 2.1959898635947979]

"""

# The classifier gett a better score based on number of k and depth than the regressor and vice versa.
# Check to see if adding the prediction of the classifier wil help the regressor.  This might be helpful
# because the classifier will use a different number of features than the regressor.
def get_df_of_k(features):
    df = get_nmf(k=features)
    df_full = add_yahoo_to_df(df)
    df_full = add_dummies(df_full)

    df_test = get_nmf('data_wednesday', k=features) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    return df_train, df_test_full

# Probably not necessary to to and add the prediction from the classifier to the regressor
# because the prediction values are currently fluctuating more than .20 on each test.
# def check_classifier_plus_regressor():
#     # Create dataframes
#     df_train_classifier, df_test_full_classifier = get_df_of_k(7)
#     df_train_regressor, df_test_full_regressor = get_df_of_k(1)
#
#     # Get X and y values
#     X_model_class, y_model_class = get_classifier_data(df_full)
#     X_classify, y_classify  = get_classifier_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
#
#     rf_class = RandomForestClassifier(n_estimators=1000, max_depth=11)
#     rf_class.fit(X_model_class, y_model_class)
#     #
#
#     X_model_regress, y_model_regress = get_regressor_data(df_full)
#     X_regress, y_regress = get_regressor_data(pd.DataFrame(df_test_full.ix['2016-04-11']))
#
#     rf_regress = RandomForestRegressor(n_estimators=1000, max_depth=9)
#     rf_regress.fit(X_model_regress, y_model_regress)
#
#     classifier_preds = rf_class.predict(X_classify)
#     classifier_accuracy = accuracy_score(classifier_preds, y_classify)
#
#     regressor_preds = rf_regress.predict(X_regress)
#     regressor_mse = mean_squared_error(regressor_preds, y_regress)
#
#     depth_list.append([ depth, classifier_accuracy, regressor_mse ])
#     print [ depth, classifier_accuracy, regressor_mse ]

def most_important_features():
    pass

if __name__ == '__main__':
    scores = get_best_k()
    # depth_list = check_best_depth()
    # tree_list = check_num_trees()
















#
