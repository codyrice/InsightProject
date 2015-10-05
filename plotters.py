__author__ = 'christopherrivera'

from pandas import DataFrame
from sklearn import metrics
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_functions import *
from stats import *
########################################################################################################################
# This contains functions for plotting.
########################################################################################################################


def plot_confusion_matrix(target, predicted, normalize=True, cbar=True, cmap='Blues', sort=True):
    """plots a heatmap of the confusion matrix.
    Parameters:
        target(pd.Series): the target values
        predict (pd.Series): the predicted values.
        normalize(bool): If true, normalize
        cbar(bool): if false, no color bar.
        cmap(str): color map to use.
    Return (plt.axes) the axes of the object.
        """

    # caluculate the confusion matrix.
    confusion = compute_confusion_matrix(target, predicted, normalize, sort)
    # set up plot.
    sns.set_context('talk')
    sns.set_style('white')
    ax = sns.heatmap(confusion, cmap=cmap, linewidths=.5, vmin=0, vmax=1, cbar=cbar)
    ax.set_xlabel('Predicted Label', size=24)
    ax.set_ylabel('True Label', size=24)
    ax.tick_params(axis='both', labelsize=22)
    return ax


def plot_shuffled_confusion_matrix(y_test, normalize=True, cmap='Blues'):
    """ Shuffles the heat map of the heat map labels of the y_test and plots the heatmap"""
    y_test_shuffled = shuffle_dataframe(y_test)  # shuffle the data

    # plot and return axis
    return plot_confusion_matrix(y_test, y_test_shuffled, normalize, cmap)


def plot_accuracy_by_category(y_test, predicted):
    """Calculates the accuracy of each by category and plots it.
    Parameters:
        y_test (array): the y_test
        predicted (array): the predicted values
    Returns:
        ax (plot object)"""

    sns.set_context('talk')
    sns.set_style('white')
    accuracy = calculate_accuracy_by_category(y_test, predicted)
    ax = accuracy.plot('barh', figsize=(10, 12), alpha=0.5, edgecolor=None)

    plt.xlabel('% Accuracy', size=25)
    plt.ylabel('')
    sns.despine()
    ax.tick_params(axis='both', labelsize=20)
    plt.xlim(0, 100)
    return ax


def plot_random_predictions(y_test, n=1000):
    """ Plot the random data.
    Parameters:
        y_test (array): Labels
        n (int): the number of times randomize.
    Returns:
        A bar plot"""
    sns.set_context('talk')
    sns.set_style('white')
    mean_, sd = predict_random_category(y_test, n)
    ax = mean_.plot('barh', figsize=(10, 12), alpha=0.5, edgecolor=None)
    plt.xlabel('% Accuracy', size=25)
    plt.ylabel('')
    sns.despine()
    ax.tick_params(axis='both', labelsize=20)
    plt.xlim(0, 100)
    return ax


def set_style():
    """ Uses seaborn to set a simple style for plots."""
    sns.set(context='talk', style='white', font='Open Sans',
            font_scale=1.8)


def plot_accuracy_with_random_by_category(true, predicted, sort=True):
    """plots the random
    Parameters:
        true (array): the observed values
        predicted (array): the observed values.
        sort (bool): if true sort by the
    Returns:
        res, ax
        """
    # compute the values
    res = calcuate_accuracy_above_random_chance(true, predicted, sort)

    # set styles
    sns.set_style('white')
    sns.set_context('talk')

    # axes
    ax = sns.barplot(x='Model', y='Category', data=res, color='#c0cdf3')
    sns.barplot(x='Random', y='Category', data=res, color='#4f73dd', ax=ax)

    # configure the plot details
    plt.xlim(0, 100)
    plt.xlabel('Accuracy (%)', size=24)
    plt.ylabel('')
    ax.tick_params(axis='both', labelsize=22)
    sns.despine()

    return ax, res


def plot_sorted_df_column(df, column, n=3, ascending=False):
    """Takes a column and sorts it and plots the top n.
    Parameters:
        df (dataframe)
        column (str): the column to sort.
        n (int): the number to return
        ascending (bool): sort order
    Returns:
        Series: the plot and the series. """

    series = sort_df_column(df, column, n, ascending)

    # convert accuracy to percent
    series = series * 100

    set_style()
    ax = series.plot('barh', alpha=0.5)
    plt.xlim(0, 100)
    plt.xlabel('Accuracy (%)', size=26)
    plt.ylabel('')
    ax.tick_params(axis='both', labelsize=24)
    sns.despine()
    return ax, series
