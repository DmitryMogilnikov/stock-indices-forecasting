import numpy as np

from db.redis.redis_ts_api import ts_api
from service.converters.ts_converter import ts_to_dates, ts_to_values


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
        self.dates = ts_to_dates(self.ts) if len(self.ts) > 0 else np.array([])

        self.reduction = reduction
        self.tolerance = tolerance
        self.index_name = index_name

    def calc_integral_sum(self) -> None:
        self.integral_sum = np.cumsum(ts_to_values(ts=self.ts)) if len(self.ts) > 1 else np.array([])
    
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
