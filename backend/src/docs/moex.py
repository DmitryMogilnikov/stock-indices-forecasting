add_data_by_ticker_description = """
    Route for adding data from moex by ticker.

    - name: name of timeseries
    - start: date in iso format (2023-01-01)
    - end: date in iso format (2023-01-28)

    Returns: None
"""

add_data_by_ticker_responses = {
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
                    "detail1": "Ticker not found: NNNN",
                    "detail2": "Data not found for this time: from 2025-01-12 to 2025-10-25"
                },
            },
        },
    },
    500: {
        "description": "Mismatched sizes of dates and values error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Mismatched sizes of dates and values error"
                },
            },
        },
    },
}
