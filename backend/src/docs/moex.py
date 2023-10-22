add_data_from_moex_by_ticker_description = """
    Route for adding data from moex by ticker.

    - name: name of timeseries
    - start: date in iso format (2023-01-01)
    - end: date in iso format (2023-01-28)

    Returns: None
"""

add_data_from_moex_by_ticker_responses = {
    404: {
        "description": "Ticker not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ticker not found: NNNN"},
            },
        },
    },
    404: {
        "description": "Data not found for this time",
        "content": {
            "application/json": {
                "example": {"detail": "Data not found for this time: from 2025-01-12 to 2025-10-25"},
            },
        },
    },
    500: {
        "description": "Mismatched sizes of dates and values error",
        "content": {
            "application/json": {
                "example": {"detail": "Mismatched sizes of dates and values error"},
            },
        },
    },
}
