import numpy as np


def calc_integral_sum(prices: list[float]) -> np.ndarray[float]:
    if not prices:
        return np.array(0.0)
    return np.cumsum(prices)

def calc_increase_percentage(integ_sum: np.ndarray[float]) -> np.ndarray[float]:
    if integ_sum.ndim and integ_sum.size == 0:
        return np.array(0.0)
    return np.insert((integ_sum[1:] / integ_sum[:-1] - 1) * 100.0, 0, 0.0)
