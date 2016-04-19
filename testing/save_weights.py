import pandas as pd
from predict_nmf import *
from nmf_tweets import *

def get_test():
    df_test = get_nmf(path='data_04_19', k=1) # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    df_test_full.to_csv('data_thursday/pd_data.csv')

    return df_test_full

def get_train():
    df = get_nmf(k=1)
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)

    df_train.to_csv('data_week_1/pd_data.csv')

    return df_train

if __name__ == '__main__':
    get_test()
    #get_train()












#
