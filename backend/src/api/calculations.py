import io

import pandas as pd
from api.moex import add_data_by_ticker_route
from core.redis_config import RedisTimeseriesPrefix
from docs.calculations import (
    get_all_calculations_description,
    get_all_calculations_response,
    get_days_to_target_reduction_description,
    get_days_to_target_reduction_responses,
    get_increase_percentage_description,
    get_increase_percentage_response,
    get_integral_sums_description,
    get_integral_sums_response,
)
from exceptions.moex import InvalidDateFormat
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from service.calculations import CalculationIndex, get_all_calculations
from service.converters.time_converter import (
    iso_to_timestamp,
    timestamp_to_iso,
)
from service.converters.ts_converter import merge_dates_and_values

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
    try:
        start = iso_to_timestamp(start_date)
        end = iso_to_timestamp(end_date)
    except InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    await add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(index_name=index_name,
        prefix=prefix.value,
        start=start,
        end=end,
    )
    calculation_index.calc_integral_sum()
    return merge_dates_and_values(calculation_index.dates, calculation_index.integral_sum)


@router.get(
    path="/get_increase_percentage",
    name="Get increase percentage",
    description=get_increase_percentage_description,
    responses=get_increase_percentage_response,
)
async def get_increase_percentage(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
):
    try:
        start = iso_to_timestamp(start_date)
        end = iso_to_timestamp(end_date)
    except InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    await add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start=start,
        end=end,
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
    try:
        start = iso_to_timestamp(start_date)
        end = iso_to_timestamp(end_date)
    except InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    await add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    calculation_index = CalculationIndex(
        index_name=index_name,
        prefix=prefix.value,
        start=start,
        end=end,
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
    days_count: float = 5,
):
    await add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)
    return get_all_calculations(index_name, prefix, start_date, end_date, reduction, tolerance, days_count)

@router.get(
    path="/get_excel_with_all_calculations",
    name="Get excel with all calculations",
    description=get_all_calculations_description,
    responses=get_all_calculations_response,
)
async def get_excel_with_all_calculations_route(
    index_name: str,
    prefix: RedisTimeseriesPrefix,
    start_date: str = "2020-01-01",
    end_date: str = "2023-11-03",
    reduction: float = 1.0,
    tolerance: float = 0.05,
    days_count: float = 5,
):
    await add_data_by_ticker_route(name=index_name, start=start_date, end=end_date)

    header_list = [
        "date", "open", "close", "min", "max", 
        "integral_sum", "increase_percentage", "days_to_reduction",
        "predict_increase_percentage", "predict_integral_sum", "predict_cost",
        "error",
    ]
    df = get_all_calculations(index_name, prefix, start_date, end_date, reduction, tolerance, days_count)
    df = pd.DataFrame(df, columns=header_list)
    df["date"] = df["date"].apply(lambda x: timestamp_to_iso(x))

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)

    return StreamingResponse(
        content=io.BytesIO(buffer.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{index_name}.xlsx"'}
    )