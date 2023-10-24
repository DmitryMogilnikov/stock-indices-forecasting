from typing import List


def calc_integral_sum(prices: List[float]) -> List[float]:
    """
    :param prices:
        a prices list
    :return:
        a newly calculated integral sum list
    """

    if not prices:
        return []
    result: List[float] = prices
    for i in range(1, len(result)):
        result[i] = prices[i]+result[i-1]
    return result

def calc_increase_percentage(integ_sum: List[float]) -> list[float]:
    if not integ_sum:
        return []
    return [0.0]+[(integ_sum[i]/integ_sum[i - 1] - 1.0) * 100.0 for i in range(1, len(integ_sum))]
