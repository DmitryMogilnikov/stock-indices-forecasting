import numpy as np
from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api
from exceptions.moex import InvalidDateFormat
from fastapi import HTTPException
from service.converters.time_converter import iso_to_timestamp
from service.converters.ts_converter import (
    merge_dates_and_values,
    ts_to_dates,
    ts_to_values,
)


class CalculationIndex:
    def __init__(
        self,
        index_name: str,
        prefix: str,
        start: int,
        end: int,
        reduction: float | None = None,
        tolerance: float | None = None
    ) -> None:
        self.ts = ts_api.get_range(name=index_name, start=start, end=end, prefix=prefix)
        self.dates = ts_to_dates(self.ts)

        self.reduction = reduction
        self.tolerance = tolerance
        self.index_name = index_name

    def calc_integral_sum(self) -> None:
        self.integral_sum = np.cumsum(ts_to_values(ts=self.ts))

    def calc_increase_percentage(self) -> None:
        self.increase_percentage = np.zeros(self.integral_sum.shape)
        if self.increase_percentage.shape[0] > 1:
            self.increase_percentage[1:] = (self.integral_sum[1:] / self.integral_sum[:-1] - 1) * 100

    def calc_days_to_target_reduction(self) -> None:
        self.days_to_reduction = np.zeros(self.increase_percentage.shape[0])
        percentage = self.increase_percentage[1:].copy() if len(self.increase_percentage) > 1 else np.array([])
        i = 1

        while True:
            if len(percentage) < 1:
                break
            mask = np.where((percentage[0] - percentage) > (self.reduction  - self.tolerance))[0]
            if not list(mask):
                break
            count_days = mask[0]
            percentage = percentage[count_days:]
            i += count_days
            if i < self.days_to_reduction.shape[0]:
                self.days_to_reduction[i] = count_days


def get_all_calculations(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
    reduction: float = 1.0,
    tolerance: float = 0.05,
):
    try:
        start = iso_to_timestamp(start_date)
        end = iso_to_timestamp(end_date)
    except InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start=start,
        end=end,
        reduction=reduction,
        tolerance=tolerance,
    )

    open = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.open.value, start, end))
    close = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.close.value, start, end))
    min = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.min.value, start, end))
    max = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.max.value, start, end))

    calculation_index.calc_integral_sum()
    calculation_index.calc_increase_percentage()
    calculation_index.calc_days_to_target_reduction()

    return merge_dates_and_values(
        calculation_index.dates,
        open,
        close,
        min,
        max,
        calculation_index.integral_sum,
        calculation_index.increase_percentage,
        calculation_index.days_to_reduction,
    )
