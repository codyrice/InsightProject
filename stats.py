__author__ = 'christopherrivera'

from pandas import DataFrame
from data_functions import *
from sklearn import metrics


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


def calcuate_accuracy_above_random_chance(true, predicted, sort=True):
    """Calculates the random distribution.
    Parameters:
        true (array): the observed values
        predicted (array): the observed values.
        sort (bool): if true sort by the
    Returns:
        dataframe
        """

    # if the arrays are not series, cast as series.
    if not isinstance(true, pd.Series):
        true = pd.Series(true)
    if not isinstance(predicted, pd.Series):
        predicted = pd.Series(predicted)

    # calculate the accuracy and random accuracy
    accuracy = calculate_accuracy_by_category(true, predicted)
    random_accuracy = predict_random_category(true)[0]  # only get the mean values

    # create a new data frame to hold the data, and sort
    data = pd.DataFrame({'Model': accuracy, 'Random': random_accuracy})
    data.reset_index(inplace=True)

    #change the names of the columns:
    data.columns = ['Category', 'Model', 'Random']
    if sort:
        data.sort('Model', inplace=True, ascending = False)

    return data


def compute_confusion_matrix(target, predicted, normalize=True, sort = True):
    """ returns a confusion matrix as a data frame with labels
    Parameters:
        target (array): The values that are predicted.
        predicted (array): predicted values.
        normalize (bool): If True, Normalize
        normalize (bool): If true sort by value.
    Returns (DataFrame): df with the confusion matrix.
    """

    # Determine the uniqu values in the target list, sort them and assign as labels.
    labels = np.unique(list(target))
    labels.sort()

    # Compute the confusion matrix, place into data frame and normailize if desired.
    confusion = metrics.confusion_matrix(target, predicted, labels)
    confusion = DataFrame(confusion, index=labels, columns=labels)
    if normalize:
        confusion = confusion.apply(lambda x: x / np.sum(x), axis=1)

    # if sort is true: find the max value for each and then sort, the confusion matrix
    if sort:
        #get the max values, order and then use to order the confusion matrix on both axes
        max_values =confusion.max(axis = 1)
        max_values.sort(inplace = True, ascending=False)
        order = max_values.index
        confusion = confusion.loc[order,order]
    return confusion
