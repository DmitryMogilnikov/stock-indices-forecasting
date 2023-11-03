from fastapi import APIRouter

from api.moex import add_data_by_ticker_route
from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api
from docs.calculations import (
    get_all_calculations_description,
    get_all_calculations_response,
    get_days_to_target_reduction_description,
    get_days_to_target_reduction_responses,
    get_increase_percentage_description,
    get_increase_percentage_response,
    get_integral_sums_description,
    get_integral_sums_response
)
from service import moex as moex_service
from service.calculations import CalculationIndex
from service.converters.time_converter import iso_to_timestamp
from service.converters.ts_converter import (
    merge_dates_and_values,
    ts_to_values,
)

router = APIRouter(
    prefix="/calculations",
    tags=["Calculations API"],
)

@router.get(
    path="/get_integral_sum",
    name="Get integral sum",
    description=get_integral_sums_description,
    responses=get_integral_sums_response
)
async def get_integral_sum_route(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
):
    moex_service.add_data_by_ticker(ts_api, index_name, start_date, end_date)
    start_date = iso_to_timestamp(start_date)
    end_date = iso_to_timestamp(end_date)

    calculation_index = CalculationIndex(index_name=index_name,
        prefix=prefix.value,
        start_date=start_date,
        end_date=end_date,
    )
    calculation_index.calc_integral_sum()
    return merge_dates_and_values(calculation_index.dates, calculation_index.integral_sum)


@router.get(
    path="/get_increase_percentage",
    name="Get increase percentage",
    description=get_increase_percentage_description,
    responses=get_increase_percentage_response,
)
async def get_days_to_target_reduction(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
):
    moex_service.add_data_by_ticker(ts_api, index_name, start_date, end_date)
    start_date = iso_to_timestamp(start_date)
    end_date = iso_to_timestamp(end_date)
    
    add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start_date=start_date,
        end_date=end_date,
    )

    calculation_index.calc_integral_sum()
    calculation_index.calc_increase_percentage()
    return merge_dates_and_values(calculation_index.dates, calculation_index.increase_percentage)


@router.get(
    path="/get_days_to_target_reduction",
    name="Get days to target reduction",
    description=get_days_to_target_reduction_description,
    responses=get_days_to_target_reduction_responses,
)
async def get_days_to_target_reduction(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
    reduction: float = 1.0,
    tolerance: float = 0.05,
):
    moex_service.add_data_by_ticker(ts_api, index_name, start_date, end_date)
    start_date = iso_to_timestamp(start_date)
    end_date = iso_to_timestamp(end_date)
    
    add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start_date=start_date,
        end_date=end_date,
        reduction=reduction,
        tolerance=tolerance,
    )

    calculation_index.calc_integral_sum()
    calculation_index.calc_increase_percentage()
    calculation_index.calc_days_to_target_reduction()
    return merge_dates_and_values(calculation_index.dates, calculation_index.days_to_reduction)


@router.get(
    path="/get_all_calculations",
    name="Get all calculations",
    description=get_all_calculations_description,
    responses=get_all_calculations_response,
)
async def get_all_calculations_route(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
    reduction: float = 1.0,
    tolerance: float = 0.05,
):
    moex_service.add_data_by_ticker(ts_api, index_name, start_date, end_date)
    start_date = iso_to_timestamp(start_date)
    end_date = iso_to_timestamp(end_date)
    
    add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start_date=start_date,
        end_date=end_date,
        reduction=reduction,
        tolerance=tolerance,
    )

    cost = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.cost.value, start_date, end_date))
    open = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.open.value, start_date, end_date))
    close = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.close.value, start_date, end_date))
    min = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.min.value, start_date, end_date))
    max = ts_to_values(ts_api.get_range(index_name, RedisTimeseriesPrefix.max.value, start_date, end_date))

    calculation_index.calc_integral_sum()
    calculation_index.calc_increase_percentage()
    calculation_index.calc_days_to_target_reduction()

    return merge_dates_and_values(
        calculation_index.dates,
        cost,
        open,
        close,
        min,
        max,
        calculation_index.integral_sum,
        calculation_index.increase_percentage,
        calculation_index.days_to_reduction,
    )