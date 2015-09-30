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


def compute_confusion_matrix(target, predicted, normalize=True):
    """ returns a confusion matrix as a data frame with labels
    Parameters:
        target (array): The values that are predicted.
        predicted (array): predicted values.
        normalize (bool): If True, Normalize
    Returns (DataFrame): df with the confusion matrix.
    """

    # Determine the uniqu values in the target list, sort them and assign as labels.
    labels = np.unique(list(target))
    labels.sort()

    # Compute the confusion matrix, place into data frame and normailize if desired.
    confusion = metrics.confusion_matrix(target, predicted, labels)
    data = DataFrame(confusion, index=labels, columns=labels)
    if normalize:
        data = data.apply(lambda x: x / np.sum(x), axis=1)
    return data


def plot_confusion_matrix(target, predicted, normalize=True, cbar=True, cmap='Blues'):
    """plots a heatmap of the confusion matrix. """

    sns.set_context('talk')
    sns.set_style('white')
    confusion = compute_confusion_matrix(target, predicted, normalize)
    ax = sns.heatmap(confusion, cmap=cmap, linewidths=.5, vmin=0, vmax=1, cbar=cbar)
    ax.set_xlabel('Predicted Label', size=20)
    ax.set_ylabel('True Label', size=20)
    ax.tick_params(axis='both', labelsize=15)
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
