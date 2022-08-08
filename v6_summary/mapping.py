from v6_summary.aggregators import *
from v6_summary.constants import *
from v6_summary.sql_functions import *

AGGREGATORS = {
    MAX_FUNCTION: maximum,
    MIN_FUNCTION: minimum,
    AVG_FUNCTION: average,
    POOLED_STD_FUNCTION: pooled_std,
    HISTOGRAM: histogram_aggregator,
    BOXPLOT: boxplot,
    COUNT_FUNCTION: count,
    COUNT_NULL: sum_null,
    COUNT_DISCRETE: count_discrete,
    DESCRIBE: describe_aggregator,
}

FUNCTION_MAPPING = {
    COUNT_FUNCTION: {
        FUNCTIONS: [COUNT_FUNCTION]
    },
    AVG_FUNCTION: {
        FUNCTIONS: [COUNT_FUNCTION],
        METHOD: {
            NAME: SUM_FUNCTION,
            CALL: sum_values,
        },
    },
    MAX_FUNCTION: {
        FUNCTIONS: [MAX_FUNCTION]
    },
    MIN_FUNCTION: {
        FUNCTIONS: [MIN_FUNCTION]
    },
    SUM_FUNCTION: {
        FUNCTIONS: [SUM_FUNCTION]
    },
    POOLED_STD_FUNCTION: {
        FUNCTIONS: [STD_SAMP_FUNCTION]
    },
    HISTOGRAM: {
        METHOD: {
            NAME: HISTOGRAM,
            CALL: histogram,
        },
    },
    BOXPLOT: {
        FUNCTIONS: [MAX_FUNCTION, MIN_FUNCTION],
        METHOD: {
            NAME: QUARTILES,
            CALL: quartiles,
            FETCH: FETCH_ONE
        }
    },
    COUNT_NULL: {
        METHOD: {
            NAME: COUNT_NULL,
            CALL: count_null,
            FETCH: FETCH_ONE
        }
    },
    COUNT_DISCRETE: {
        METHOD: {
            NAME: COUNT_DISCRETE,
            CALL: count_discrete_values,
            FETCH: FETCH_ALL
        }
    },
    DESCRIBE: {
        METHOD: {
            NAME: DESCRIBE,
            CALL: describe,
        },
    }
}
