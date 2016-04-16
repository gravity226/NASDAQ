import pandas as pd
from predict_nmf import *
from nmf_tweets import *

def get_test():
    df_test = get_nmf('data_wednesday') # put in folder name where the json data is
    df_test_full = add_yahoo_to_df(df_test)
    df_test_full = add_dummies(df_test_full)

    df.to_json('data_wednesday/pd_data.json')

def get_train():
    df = get_nmf()
    df_full = add_yahoo_to_df(df)
    df_train = add_dummies(df_full)

    df.to_json('data_week_1/pd_data.json')














#
