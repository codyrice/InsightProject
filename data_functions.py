__author__ = 'christopherrivera'

########################################################################################################################
#This contains some functions for manipulating the data, plot or what ever.
########################################################################################################################

import pandas as pd


def count_columns(df, column):
    '''
    Counts the values with in a column and returns as a data frame.
    Params:
        df(pd.DataFrame): data fram with the data
        column(str): string with the data of interest.
    Returns:
        dataframe'''

    # count the data and then encapsulate in a histogram
    counts = df[column].value_counts()
    hist =  pd.DataFrame({'Category': counts.index, 'Counts':counts})
    return hist