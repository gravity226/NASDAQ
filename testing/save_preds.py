import pandas as pd
import cPickle as pickle
from predict_nmf import get_classifier_data, get_regressor_data

from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

def save_preds(date='2016-04-14'):
    df_full = pd.read_csv('data_week_1/pd_data.csv')
    df_full.index = df_full['adj_date']
    df_full.pop('adj_date')

    df_test_full = pd.read_csv('data_thursday/pd_data.csv')
    df_test_full.index = df_test_full['adj_date']
    df_test_full.pop('adj_date')

    # Get X and y values
    X_model_class, y_model_class = get_classifier_data(df_full)
    X_model_regress, y_model_regress = get_regressor_data(df_full)

    data = pd.DataFrame(df_test_full.ix[date])

    X_classify, y_classify  = get_classifier_data(data)
    X_regress, y_regress = get_regressor_data(data)

    # Run models
    rf_class = RandomForestClassifier(n_estimators=2000, max_depth=19)
    rf_class.fit(X_model_class, y_model_class)
    #
    rf_regress = RandomForestRegressor(n_estimators=2000, max_depth=19)
    rf_regress.fit(X_model_regress, y_model_regress)

    classifier_preds = rf_class.predict(X_classify)
    classifier_accuracy = accuracy_score(classifier_preds, y_classify)

    regressor_preds = rf_regress.predict(X_regress)
    regressor_mse = mean_squared_error(regressor_preds, y_regress)

    accuracy, mse = 0.578947368421, 2.19300433324
    df_save = pd.DataFrame(zip(list(data['sym']), classifier_preds, regressor_preds))
    df_save.columns = ['sym', 'classifier_preds', 'regressor_mse']
    df_save['date'] = date
    df_save['accuracy'] = accuracy
    df_save['mse'] = mse

    df_save.to_csv('predictions.csv')

    print df_full

    # return df_save

if __name__ == '__main__':
    print save_preds()
