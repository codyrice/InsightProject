__author__ = 'christopherrivera'

########################################################################################################################
# This contains some functions for manipulating the data.
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


def create_map(df, key, value):
    """Takes two columns of a df and returns a dictionary for mapping
    Parameters:
        df (pd.DataFrame): pandas dataframe
        key (str): column for key
        value (str): column for the values
    returns (dict): dict with key:values"""
    return dict(zip(df[key], df[value]))


def subselect_categories(df, column, n, shuffle=True):
    """ subselects a data frame and returns n from each category.
    Parameters:
        df (pandas dataframe): the dataframe.
        column (str) the string to groupby.
        n (int): the number to take from each.
        shuffle(bool): Tag to determine if should be suffeld.
    Returns:
        dataframe"""

    df = df.copy()
    if shuffle:
        df = shuffle_dataframe(df)
    return df.groupby(column).apply(select_n, n)


def sort_df_column(df, column, n=3, ascending=False):
    """Takes a column and sorts it and returns the top n.
    Parameters:
        df (dataframe)
        column (str): the column to sort.
        n (int): the number to return
        ascending (bool): sort order
    Returns:
        Series: a single series. """
    series = df.copy()

    series = pd.Series(series[column])

    series.sort(inplace=True, ascending=ascending)
    return series.iloc[:n]
