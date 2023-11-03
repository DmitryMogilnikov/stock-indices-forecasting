import numpy as np


def ts_to_dates(ts: list[float]) -> np.ndarray[float]:
    ts = np.array(ts)
    return ts[:, 0]


def ts_to_values(ts: list[float]) -> np.ndarray[float]:
    ts = np.array(ts)
    return ts[:, 1]


def merge_dates_and_values(dates: list[int], *values: list[float])-> list[tuple[int, float]]:
    print(values)
    return np.column_stack([dates, *values]).tolist()