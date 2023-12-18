add_one_point_route_description = """
    Route for add one point in Redis timeseries.

    Args:
    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)
    - date: date in iso format (2023-01-01).
        Defaults is "*" - datetime now
    - value: timestamp value.

    Returns: None
"""

add_points_route_description = """
    Route for add points in Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)
    - points: list of points (timestamp in milliseconds, value) in format:
        [
            [
                100,
                100
            ],
            [
                200,
                200
            ]
        ]

    Returns: None
"""

check_existing_ts_route_description = """
    Route for check existing ts in Redis.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)

    Returns:
    - bool
"""

get_last_point_route_description = """
    Route for get last point from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)

    Returns:
    - point in format:
        [
            timestamp in milliseconds,
            float value
        ]
"""

get_range_route_description = """
    Route for get range of points from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-01).
        Defaults is "+" - max date in timeseries
    - count: limit to points count in returns
    - reverse: order by date (True = ASC or False = DESC)

    Returns:
    - points in format:
        [
            [
                timestamp in milliseconds,
                float value
            ],
            [
                timestamp in milliseconds,
                float value
            ]
        ]
"""

get_range_route_responses = {
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

delete_range_route_description = """
    Route for delete range of points from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)
    - start: date in iso format (2023-01-01).
        Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-01).
        Defaults is "+" - max date in timeseries

    Returns:
    - delete points count (int)
"""

delete_ts_route_description = """
    Route for delete range of points from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (OPEN, CLOSE, MAX, MIN)

    Returns: None
"""
