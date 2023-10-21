add_one_point_route_description = """
    Route for add one point in Redis timeseries.

    Args:
    - name: name of timeseries
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)
    - date: date in iso format (2023-01-01T03:00:00). Defaults is "*" - datetime now
    - value: timestamp value.

    Returns: None
"""

add_points_route_description = """
    Route for add points in Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)
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

get_last_point_route_description = """
    Route for get last point from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)

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
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)
    - start: date in iso format (2023-01-01T03:00:00). Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-01T03:00:00). Defaults is "+" - max date in timeseries
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

delete_range_route_description = """
    Route for delete range of points from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)
    - start: date in iso format (2023-01-01T03:00:00). Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-01T03:00:00). Defaults is "+" - max date in timeseries

    Returns:
    - delete points count (int)
"""

delete_ts_route_description = """
    Route for delete range of points from Redis timeseries.

    - name: name of timeseries
    - prefix: prefix for timeseries (COST, OPEN, CLOSE, MAX, MIN)

    Returns: None
"""

get_days_to_target_reduction = """
    Route for get the number of days the initial percentage increase decreases by a given percentage.

    - name: name of timeseries
    - start: date in iso format (2023-01-01T03:00:00). Defaults is "-" - min date in timeseries
    - end: date in iso format (2023-01-01T03:00:00). Defaults is "+" - max date in timeseries
    - target_reduction: the number of percent by which there should be a reduction in float. Defaults is 1%

    Returns:
    - days in format:
        [
            int value,
            int value
        ]
"""
