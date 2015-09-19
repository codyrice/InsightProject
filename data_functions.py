__author__ = 'christopherrivera'

########################################################################################################################
# This contains some functions for manipulating the data, plot or what ever.
########################################################################################################################

import pandas as pd
import numpy as np


def count_columns(df, column):
    """
    Counts the values with in a column and returns as a data frame.
    Params:
        df(pd.DataFrame): data fram with the data
        column(str): string with the data of interest.
    Returns:
        dataframe"""

    # count the data and then encapsulate in a histogram
    counts = df[column].value_counts()
    hist = pd.DataFrame({'Category': counts.index, 'Counts': counts})
    return hist


def shuffle_dataframe(df):
    """shuffles the order of a data frame using the np.permutation """
    df = df.copy()  # copy the index.
    return df.iloc[np.random.permutation(len(df))]


def select_n(group_df, n=200):
    """ select the first n rows of a group. It assumes that the df has already be shuffled.
    If the length is less than the group return the group unaltered. """
    group_df = group_df.copy()

    if len(group_df) >= n:
        return group_df.iloc[:n, :]
    else:
        return group_df
