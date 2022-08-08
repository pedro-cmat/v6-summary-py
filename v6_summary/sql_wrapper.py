import os

from v6_summary.constants import *
from v6_summary.utils import compare_with_minimum
from v6_summary.sql_functions import cohort_count

PD_SUMMARY_MAP = {
    COUNT_FUNCTION: 0,
    AVG_FUNCTION: 1,
    STD_SAMP_FUNCTION: 2,
    MIN_FUNCTION: 3,
    '1q': 4,
    '2q': 5,
    '3q': 6,
    MAX_FUNCTION: 7,
}

def cohort_finder(cohort, data):
    """ Retrieve the results for the cohort finder option
    """
    # Check if the number of records in the table is enough
    count = len(data)
    # If the total count for the cohort is below the accepted threshold
    # then the information won't be sent to the mater node
    if int(count[1]) >= int(os.getenv(TABLE_MINIMUM) or TABLE_MINIMUM_DEFAULT):
        cohort_data = cohort_count(
            data,
            cohort[COHORT_DEFINITION],
        )
        return (compare_with_minimum(len(cohort_data)), cohort_data)
    else:
        return (
            {
                WARNING: f"Not enough records in database {count[0]}."
            }, 
            None
        )

def summary_results(data, columns):
    """ Retrieve the summary results for the requested functions
    """
    summary = {}
    #sql_functions = None
    for column in columns:
        # validate the number of records available prior to obtaining any
        # summary statistics
        n_records = data[column[VARIABLE]].notnull().sum()
        summary[column[VARIABLE]] = {}
        if n_records >= int(os.getenv(TABLE_MINIMUM) or TABLE_MINIMUM_DEFAULT):
            if REQUIRED_FUNCTIONS in column and len(column[REQUIRED_FUNCTIONS]) > 0:
                result = data[column[VARIABLE]].describe()
                # parse the results
                for i, function in enumerate(column[REQUIRED_FUNCTIONS]):
                    summary[column[VARIABLE]][function] = result[PD_SUMMARY_MAP[function]]

            if REQUIRED_METHODS in column and len(column[REQUIRED_METHODS]) > 0:
                for method in column[REQUIRED_METHODS]:
                    summary[column[VARIABLE]][method[NAME]] = method[CALL](
                        data, column[VARIABLE], column)
                    #summary[column[VARIABLE]][method[NAME]] = run_sql(
                    #    db_client, sql_statement, fetch_all = method[FETCH]==FETCH_ALL
                    #)
        else:
           summary[column[VARIABLE]][WARNING] = f"Not enough records in database {n_records}" + \
               " to execute the summary statistics." 
    return summary
