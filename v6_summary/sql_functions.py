from operator import le, lt, ge, gt, eq
import os

import numpy as np

from v6_summary.constants import *

validation_functions = {
    '>=': ge,
    '<=': le,
    '>': gt,
    '<': lt,
    '=': eq,
}

def sum_values(data, variable, arguments):
    """ Sum all the values for a variable
    """
    return data[variable].sum()

def histogram(data, variable, arguments):
    """ Create the SQL statement to obtain the necessary information
        for an histogram.
    """
    width = None
    if BIN_WIDTH in arguments:
        width = arguments[BIN_WIDTH]
        if not isinstance(width, int) or width < int(os.getenv(BIN_WIDTH_MINIMUM) or BIN_WIDTH_MINIMUM_DEFAULT):
            raise Exception("Invalid bin width provided, value must be a integer superior to 1.")
    else:
        raise Exception("Histogram requested but the bin width (argument: BIN_WIDTH) must be provided!")

    description = data[variable].describe()
    min_bin = width * ((description[3])//width)
    max_bin = width * (((description[7])//width) + 1)
    bins = np.linspace(min_bin, max_bin, int(1 + ((max_bin - min_bin) // width)))
    hist =  np.histogram(data[variable], bins)
    return [[hist[1][i], hist[0][i]] for i in range(len(hist[1]) - 1)]

def quartiles(data, variable, arguments):
    """ Create the SQL statement to obtain the 25th, 50th, and 75th 
        quartiles for a variable.
    """
    iqr_threshold = float(arguments.get(IQR_THRESHOLD) or IQR_THRESHOLD_DEFAULT)
    q1 = data[variable].quantile(0.25)
    q2 = data[variable].quantile(0.5)
    q3 = data[variable].quantile(0.75)
    lower_bound = q1 - ((q3 - q1) * iqr_threshold)
    upper_bound = q3 + ((q3 - q1) * iqr_threshold)

    return [
        q1,
        q2,
        q3,
        lower_bound,
        upper_bound,
        len(data[data[variable] < lower_bound]),
        len(data[data[variable] > upper_bound]),
    ]

def count_null(data, variable, arguments):
    """ Create the SQL statment to count the null values.
    """
    return int(data[variable].isnull().sum())

def count_discrete_values(data, variable, arguments):
    """ Count the discrete values.
    """
    return dict(data[variable].value_counts())

def cohort_count(data, definition):
    """ Count the number of persons in a possible cohort.
    """
    df_condition = None
    for component in definition:
        operator = validation_functions[OPERATOR]
        value = component[VALUE]
        if operator != '=':
            value = float(value)
        df_condition = (True if df_condition is None else df_condition) & [operator](data[component[VARIABLE]], value)
    return data[df_condition]

def describe(data, variable, arguments):
    """ Describe the variables available,
    """
    description_allowed = arguments.get(DESCRIPTION_ALLOWED) or True
    variables = []
    if description_allowed:
        variables = list(data.columns)
    return variables
