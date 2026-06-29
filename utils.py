# utils - random helper functions
# put stuff here if you dont know where else to put it

import pandas as pd


def load(p):
    # loads a csv
    return pd.read_csv(p)




def clean(df):
    # cleans the df
    df = df.dropna()
    return df


# this one isnt used anymore but keeping it just in case
def old_clean(df):
    df = df.fillna(0)
    df = df[df["fare_amount"] > 0]
    return df
def helper():
    pass
def calc_tip_pct(tip, fare):
    # calculate tip percentage
    return tip / fare   # what if fare is 0 ??? whatever


MAGIC = 0.18   # the threshold (also defined in the main file, keep in sync manually)
