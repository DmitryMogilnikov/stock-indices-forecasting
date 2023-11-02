import numpy as np
from exceptions import MismatchSizeError
from typing import Any
from db.redis.redis_ts_api import RedisTimeseriesAPI

def is_reduction_sufficient(
    initial_percent: float,
    percent_value: float,
    target_reduction: float,
    tolerance: float = 1e-6
) -> bool:
    reduction_difference = initial_percent - percent_value
    return initial_percent > percent_value and reduction_difference - target_reduction > tolerance


def get_days_to_reduce_procent(
    percentage_changes: list[float],
    initial_percent: float,
    target_reduction: float,
    tolerance: float = 1e-6
) -> int:
    if len(percentage_changes) == 0:
        return 0

    days: int = 0

    for percent_change in percentage_changes:
        days += 1
        if is_reduction_sufficient(
            initial_percent,
            percent_change,
            target_reduction,
            tolerance
        ):
            break

    if days == len(percentage_changes) and not is_reduction_sufficient(
        initial_percent,
        percentage_changes[-1],
        target_reduction,
        tolerance
    ):
        days = 0

    return days


def calculate_days_to_target_reduction(
    percentage_changes: list[float],
    target_reduction: float,
    tolerance: float = 1e-6
) -> list[int]:
    days: list[int] = []

    for i, percentage_change in enumerate(percentage_changes):
        days.append(get_days_to_reduce_procent(
            percentage_changes[i+1:],
            percentage_change,
            target_reduction,
            tolerance
        ))

    return days


def get_days_to_target_reduction_with_timestamp(
    ts_api: RedisTimeseriesAPI,
    ticker: str,
    start: str,
    end: str,
    target_reduction: float = 1e-6
) -> list[tuple[int, int]]:
    timestamps = [t[0] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    prices = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    integral_sum = calc_integral_sum(prices)
    increase_percentage = calc_increase_percentage(integral_sum)
    days = calculate_days_to_target_reduction(
        increase_percentage,
        target_reduction
    )
    return get_values_with_timestamps(timestamps, days)


def calc_integral_sum(prices: list[float]) -> list[float]:
    if not prices:
        return []
    return np.cumsum(prices).tolist()


def get_integral_sum_with_timestamp(
    ts_api: RedisTimeseriesAPI,
    ticker: str,
    start: str,
    end: str
) -> list[tuple[int, float]]:
    timestamps = [t[0] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    prices = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    integral_sum = calc_integral_sum(prices)
    return get_values_with_timestamps(timestamps, integral_sum)


def calc_increase_percentage(integ_sum: list[float]) -> list[float]:
    integ_sum_np = np.array(integ_sum)
    if (integ_sum_np.ndim and integ_sum_np.size == 0) or integ_sum_np.ndim == 0:
        return []
    return np.insert((integ_sum_np[1:] / integ_sum_np[:-1] - 1) * 100.0, 0, 0.0).tolist()


def get_increase_percentage_with_timestamp(
    ts_api: RedisTimeseriesAPI,
    ticker: str,
    start: str,
    end: str
) -> list[tuple[int, float]]:
    timestamps = [t[0] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    prices = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    integral_sum = calc_integral_sum(prices)
    increase_percentage = calc_increase_percentage(integral_sum)
    print(timestamps)
    print(increase_percentage)
    return get_values_with_timestamps(timestamps, increase_percentage)


def get_values_with_timestamps(
    timestamps: list[int],
    values: list[Any]
) -> list[tuple[int, Any]]:
    try:
        timestamps_with_values = np.column_stack([timestamps, values])
    except Exception:
        raise MismatchSizeError('Mismatched sizes of timestamps and values error')

    return [tuple(date_with_value) for date_with_value in timestamps_with_values]


def get_all_calculations(
    ts_api: RedisTimeseriesAPI,
    ticker: str,
    start: str,
    end: str,
    target_reduction: float = 1e-6
) -> dict[str, list[Any]]:
    timestamps = [t[0] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    costs = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='COST')]

    opens = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='OPEN')]

    closes = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='CLOSE')]

    maxs = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='MAX')]

    mins = [t[1] for t in ts_api.get_range(
        name=ticker,
        start=start,
        end=end,
        prefix='MIN')]

    integral_sum = calc_integral_sum(costs)
    percentage_changes = calc_increase_percentage(integral_sum)
    days_to_target_reduction = calculate_days_to_target_reduction(percentage_changes, target_reduction)

    return {
        "timestamp": timestamps,
        "cost": costs,
        "open": opens,
        "close": closes,
        "max": maxs,
        "min": mins,
        "integral_sum": integral_sum,
        "percentage_changes": percentage_changes,
        "days_to_target_reduction": days_to_target_reduction
    }
