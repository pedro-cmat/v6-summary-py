BIN_WIDTH = "BIN_WIDTH"

def histogram(variable, table, arguments):
    """ Create the SQL statement to obtain the necessary information
        for an histogram.
    """
    width = None
    if BIN_WIDTH in arguments:
        width = arguments[BIN_WIDTH]
        if not isinstance(width, int) or width <= 1:
            raise Exception("Invalid bin width provided, value must be a integer superior to 1.")
    else:
        raise Exception("Histogram requested but the bin width (argument: BIN_WIDTH) must be provided!")

    return f"""SELECT floor("{variable}"/{width})*{width} as bins, COUNT(*) 
        FROM {table} GROUP BY 1 ORDER BY 1;"""

def quartiles(variable, table, arguments):
    """ Create the SQL statement to obtain the 25th, 50th, and 75th 
        quartiles for a variable.
    """
    return f"""SELECT current_database() as db,
        percentile_cont(0.25) within group (order by "{variable}" asc) as q1,
        percentile_cont(0.50) within group (order by "{variable}" asc) as q2,
        percentile_cont(0.75) within group (order by "{variable}" asc) as q3
        FROM {table};
    """

def count_null(variable, table, arguments):
    """ Create the SQL statment to count the null values.
    """
    return f"""SELECT count("{variable}") FROM {table} WHERE "{variable}" IS NULL;"""

def count_discrete_values(variable, table, arguments):
    """ Count the discrete values.
    """
    return f"""SELECT "{variable}", count(*) FROM {table} GROUP BY "{variable}";"""
