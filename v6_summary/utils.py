""" Utility functions.
"""
import os

from v6_summary.constants import *

def parse_error(error_message):
    """ Parse an error message.
    """
    return {
        ERROR: error_message 
    }

def check_keys_in_dict(keys, map):
    """ Check if all keys are present in a dictionary.
    """
    return all([key in map for key in keys])

def compare_with_minimum(value):
    """ Compare the value with the minimum value allowed.
    """
    count_minimum = int(os.getenv(COUNT_MINIMUM) or COUNT_MINIMUM_DEFAULT)
    return value if value > count_minimum else f"< {count_minimum}"
