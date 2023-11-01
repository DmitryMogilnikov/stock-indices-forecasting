import numpy as np


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


def calc_integral_sum(prices: list[float]) -> list[float]:
    if not prices:
        return [0.0]
    return np.cumsum(prices).tolist()


def calc_increase_percentage(integ_sum: list[float]) -> list[float]:
    integ_sum_np = np.array(integ_sum)
    if (integ_sum_np.ndim and integ_sum_np.size == 0) or integ_sum_np.ndim == 0:
        return [0.0]
    return np.insert((integ_sum_np[1:] / integ_sum_np[:-1] - 1) * 100.0, 0, 0.0).tolist()
