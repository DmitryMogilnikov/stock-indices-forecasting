import numpy as np

from db.redis.redis_ts_api import ts_api
from service.converters.ts_converter import ts_to_dates, ts_to_values


class CalculationIndex:
    def __init__(
        self,
        index_name: str,
        prefix: str,
        start_date: str,
        end_date: str,
        reduction: float | None = None,
        tolerance: float | None = None
    ) -> None:
        self.ts = ts_api.get_range(name=index_name, start=start_date, end=end_date, prefix=prefix)
        self.dates = ts_to_dates(self.ts)
        self.reduction = reduction
        self.tolerance = tolerance

    def calc_integral_sum(self) -> None:
        self.integral_sum = np.cumsum(ts_to_values(ts=self.ts))
    
    def calc_increase_percentage(self) -> None:
        self.increase_percentage = np.zeros(self.integral_sum.shape)
        self.increase_percentage[1:] = (self.integral_sum[1:] / self.integral_sum[:-1] - 1) * 100

    def calc_days_to_target_reduction(self) -> None:
        self.days_to_reduction = np.zeros(self.increase_percentage.shape[0])
        percentage = self.increase_percentage[1:].copy()
        i = 1

        while True:
            mask = np.where((percentage[0] - percentage) > (self.reduction  - self.tolerance))[0]
            if not list(mask):
                break
            count_days = mask[0]
            percentage = percentage[count_days:]
            i += count_days
            self.days_to_reduction[i] = count_days
