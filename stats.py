__author__ = 'christopherrivera'

from pandas import DataFrame
from data_functions import *


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


def shuffle_predict(y_test):
    """Shuffles the labels and determines which are correct. """
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


def calcuate_accuracy_above_random_chance(true, predicted):
    """Calculates the random distribution.
    Parameters:
        true (array): the observed values
        predicted (array): the observed values.
    Returns:
        dataframe
        """

    # if the arrays are not series, cast as series.
    if not isinstance(true, pd.Series):
        true = pd.Series(true)
    if not isinstance(predicted, pd.Series):
        predicted = pd.Series(predicted)

    # calculate the accuracy
    accuracy = calculate_accuracy_by_category(true, predicted)
    random_accuracy = predict_random_category(true)[0]  # only get the mean values

    # create a new data frame to hold the data, and sort
    data = pd.DataFrame({'Model': accuracy, 'Random': random_accuracy})
    data.reset_index(inplace=True)
    data.sort('index', inplace=True)
    return data
