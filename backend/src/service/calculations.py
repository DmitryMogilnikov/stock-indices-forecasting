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
        tolerance: float | None = None,
        days_count : float | None = None,
    ) -> None:
        self.ts = ts_api.get_range(name=index_name, start=start, end=end, prefix=prefix)
        self.dates = ts_to_dates(self.ts)
        self.values = ts_to_values(self.ts)
        self.len_data = self.dates.shape[0]

        self.reduction = reduction
        self.tolerance = tolerance
        self.index_name = index_name
        self.days_count = days_count

    def calc_integral_sum(self) -> None:
        self.integral_sum = np.cumsum(self.values)

    def calc_increase_percentage(self) -> None:
        self.increase_percentage = np.zeros(self.len_data)
        if self.increase_percentage.shape[0] > 1:
            self.increase_percentage[1:] = (self.integral_sum[1:] / self.integral_sum[:-1] - 1) * 100

    def calc_days_to_target_reduction(self) -> None:
        self.days_to_reduction = np.zeros(self.len_data)
        percentage = self.increase_percentage[1:].copy() if len(self.increase_percentage) > 1 else np.array([])
        idx = 1

        while True:
            if len(percentage) < 1:
                break
            mask = np.where((percentage[0] - percentage) > (self.reduction  - self.tolerance))[0]
            if not list(mask):
                break
            count_days = mask[0]
            percentage = percentage[count_days:]
            idx += count_days
            if idx < self.days_to_reduction.shape[0]:
                self.days_to_reduction[idx] = count_days
    
    def calc_predict_data(self) -> None:
        self.predict_increase_percentage = np.zeros(self.len_data)
        self.predict_integral_sum = np.zeros(self.len_data)
        self.predict_cost = np.zeros(self.len_data)
        self.error = np.zeros(self.len_data)
        idx = 1
        count = 0

        while idx < self.len_data:
            if self.days_to_reduction[idx] >= self.days_count:
                count = self.days_to_reduction[idx] * 2
                decrease_percent = 1 / count
                calc_first = True

            if count > 0:
                if calc_first:
                    self.predict_increase_percentage[idx] = self.increase_percentage[idx - 1] - decrease_percent
                    self.predict_integral_sum[idx] = self.integral_sum[idx - 1] * (1 + self.predict_increase_percentage[idx] / 100)
                    self.predict_cost[idx] = self.predict_integral_sum[idx] - self.integral_sum[idx - 1]
                    calc_first = False
                        
                else:
                    self.predict_increase_percentage[idx] = self.predict_increase_percentage[idx - 1] - decrease_percent
                    self.predict_integral_sum[idx] = self.predict_integral_sum[idx - 1] * (1 + self.predict_increase_percentage[idx] / 100)
                    self.predict_cost[idx] = self.predict_integral_sum[idx] - self.predict_integral_sum[idx - 1]

                self.error[idx] = abs(self.predict_cost[idx] - self.values[idx]) * 100 / self.values[idx]
                count -= 1

            idx += 1


def get_all_calculations(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
    reduction: float = 1.0,
    tolerance: float = 0.05,
    days_count: float = 5,
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
        days_count=days_count,
    )

    open = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.open.value, start, end))
    close = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.close.value, start, end))
    min = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.min.value, start, end))
    max = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.max.value, start, end))

    calculation_index.calc_integral_sum()
    calculation_index.calc_increase_percentage()
    calculation_index.calc_days_to_target_reduction()
    calculation_index.calc_predict_data()

    return merge_dates_and_values(
        calculation_index.dates,
        open,
        close,
        min,
        max,
        calculation_index.integral_sum,
        calculation_index.increase_percentage,
        calculation_index.days_to_reduction,
        calculation_index.predict_increase_percentage,
        calculation_index.predict_integral_sum,
        calculation_index.predict_cost,
        calculation_index.error,
    )
