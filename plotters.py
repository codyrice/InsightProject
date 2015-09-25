__author__ = 'christopherrivera'

from pandas import DataFrame
from sklearn import metrics
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
        data = data.apply(lambda x: x / np.sum(x), axis=0)
    return data


def plot_confusion_matrix(target, predicted, normalize=True):
    """plots a heatmap"""
    sns.set_context('talk')
    sns.set_style('white')
    confusion = compute_confusion_matrix(target, predicted, normalize)
    ax = sns.heatmap(confusion, cmap='Blues')
    ax.set_xlabel('Predicted Label',size = 20)
    ax.set_ylabel('True Label',size =20)
    ax.tick_params(axis='both', labelsize=15)
    return ax


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
    return ax
