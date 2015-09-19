__author__ = 'christopherrivera'

from pandas import DataFrame
from sklearn import metrics
import numpy as np
import seaborn as sns

########################################################################################################################
# This contains functions for plotting.
########################################################################################################################


def compute_confusion_matrix(target, predicted, labels, normalize=True):
    """ returns a confusion matrix as a data frame with labels"""

    # get the labels and get the unique values sort.
    labels = list(labels.unique())
    labels.sort()
    # do calcs
    data = DataFrame(metrics.confusion_matrix(target, predicted), index=labels, columns=labels)
    if normalize:
        data = data.apply(lambda x: x / np.sum(x), axis=0)
    return data


def plot_confusion_matrix(target, predicted, labels, normalize=True):
    """plots a heatmap"""
    confusion = compute_confusion_matrix(target, predicted, labels, normalize)
    ax = sns.heatmap(confusion, cmap='Blues')
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
