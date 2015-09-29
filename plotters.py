__author__ = 'christopherrivera'

from pandas import DataFrame
from sklearn import metrics
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_functions import *

########################################################################################################################
# This contains functions for plotting.
########################################################################################################################


def compute_confusion_matrix(target, predicted, normalize=True):
    """ returns a confusion matrix as a data frame with labels"""

    # get the labels and get the unique values sort.
    labels = np.unique(list(target))
    labels.sort()
    # do calcs
    confusion = metrics.confusion_matrix(target, predicted, labels)
    data = DataFrame(confusion, index=labels, columns=labels)
    if normalize:
        data = data.apply(lambda x: x / np.sum(x), axis=1)
    return data


def plot_confusion_matrix(target, predicted, normalize=True, cmap='Blues'):
    """plots a heatmap of the confusion matrix. """
    sns.set_context('talk')
    sns.set_style('white')
    confusion = compute_confusion_matrix(target, predicted, normalize)
    ax = sns.heatmap(confusion, cmap=cmap, linewidths=.5)
    ax.set_xlabel('Predicted Label', size=20)
    ax.set_ylabel('True Label', size=20)
    ax.tick_params(axis='both', labelsize=15)
    return ax


def plot_shuffled_confusion_matrix(y_test, normalize=True, cmap='Blues'):
    """ Shuffles the heat map of the heat map labels of the y_test and plots the heatmap"""
    y_test_shuffled = shuffle_dataframe(y_test)  # shuffle the data

    # plot and return axis
    return plot_confusion_matrix(y_test, y_test_shuffled, normalize, cmap)


def calculate_accuracy_by_category(y_test, predicted):
    """Calculates the accuracy of each by category. This is used for the outcome of a classifier.
    Parameters:
        y_test (array): the y_test
        predicted (array): the predicted values
    Returns:
        A data frame with the predicted values"""

    df = DataFrame({'Target': y_test, 'Predicted': predicted})
    df['Score'] = df.Target == df.Predicted
    df = df.groupby('Target').apply(lambda x: 100.0 * sum(x.Score) / len(x))
    df.sort()
    return df


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


def shuffle_predict(y_test):
    """Shuffles labeles and caluclates the number that are correct. """
    return y_test == shuffle_dataframe(y_test)


def predict_random(y_test, n=1000):
    """ Uses boostrapping to compute the expected prediction by chance.
    Parameters:
        y_test (array): Labels
        n (int): the number of times to do shuffle.
    Returns:
        Series containg the accuracy."""

    samples = np.array([np.sum(shuffle_predict(y_test)) for i in xrange(n)]) * 100.0 / len(y_test)
    return np.mean(samples), np.std(samples)


def predict_random_category(y_test, n=1000):
    """ Uses boostrapping to compute the expected prediction by chance for each category.
    Parameters:
        y_test (array): Labels
        n (int): the number of times randomize.
    Returns:
        Series containg the accuracy for each class.."""

    # Create a data frame with random predictions.
    random_ = DataFrame({i: shuffle_predict(y_test) for i in xrange(n)})
    random_.index = y_test

    # Calculate the random and
    random_ = 1.0 * random_.sum(axis=1) / n
    grouped = random_.groupby(level=0)
    mean = grouped.mean() * 100.0
    sd = grouped.std() * 100.0
    return mean, sd


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
