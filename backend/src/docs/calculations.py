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
}
