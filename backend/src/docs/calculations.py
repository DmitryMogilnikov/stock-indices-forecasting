get_days_to_target_reduction_description = """
    Route for get the number of days the initial percentage increase decreases by a given percentage.

    - name: name of timeseries
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-10).
        Defaults is "+" - max date in timeseries
    - target_reduction: the number of percent by which there should be a reduction in float.
        Defaults is 1%

    Returns:
    - days in format:
        [
            int value,
            int value
        ]
"""


get_days_to_target_reduction_responses = {
    400: {
        "description": "Invalid input format",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Invalid isoformat string: '3013-12:23'",
                    "detail2": "start (2029-01-01) cannot be greater than end (2023-01-01)"
                },
            },
        },
    },
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Ticker NNNN not found in database",
                },
            },
        },
    },
}

get_integral_sums_description = """
    Route to obtain values of the integral sum for a given time interval.

    - name: name of timeseries
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-10).
        Defaults is "+" - max date in timeseries

    Returns:
    - integral sums in format:
        [
            float value,
            float value
        ]
"""

get_integral_sums_response = {
    400: {
        "description": "Invalid input format",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Invalid isoformat string: '3013-12:23'",
                    "detail2": "start (2029-01-01) cannot be greater than end (2023-01-01)"
                },
            },
        },
    },
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Ticker NNNN not found in database",
                },
            },
        },
    },
}

get_increase_percentage_description = """
    Route to obtain values of the increase percentage for a given time interval.

    - name: name of timeseries
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-10).
        Defaults is "+" - max date in timeseries

    Returns:
    - increase percentage in format:
        [
            float value,
            float value
        ]
"""

get_increase_percentage_response = {
    400: {
        "description": "Invalid input format",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Invalid isoformat string: '3013-12:23'",
                    "detail2": "start (2029-01-01) cannot be greater than end (2023-01-01)"
                },
            },
        },
    },
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Ticker NNNN not found in database",
                },
            },
        },
    },
}

get_all_calculations_description = """
    Route to get all calculations (cost, open, close, min, max, integral sum, percentage changes, days to target reduction) for a given time interval.

    - name: name of timeseries
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-10).
        Defaults is "+" - max date in timeseries
    - target_reduction: the number of percent by which there should be a reduction in float.
        Defaults is 1%

    Returns:
    - all calculations in format:
        {
            "cost": [
                float value,
                float value
            ],
            "open": [
                float value,
                float value
            ],
            "close": [
                float value,
                float value
            ],
            "min": [
                float value,
                float value
            ],
            "max": [
                float value,
                float value
            ],
            "integral_sum": [
                float value,
                float value
            ],
            "percentage_changes": [
                float value,
                float value
            ],
            "days_to_target_reduction": [
                int value,
                int value
            ]
        }
"""

get_all_calculations_response = {
    400: {
        "description": "Invalid input format",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Invalid isoformat string: '3013-12:23'",
                    "detail2": "start (2029-01-01) cannot be greater than end (2023-01-01)"
                },
            },
        },
    },
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "detail1": "Ticker NNNN not found in database",
                },
            },
        },
    },
}