from fastapi import APIRouter, HTTPException
from typing import Any

from exceptions import moex, MismatchSizeError
from service import calculations as calculations_service
from service import moex as moex_service
from db.redis.redis_ts_api import ts_api
import redis
from docs.calculations import (
    get_days_to_target_reduction_description,
    get_days_to_target_reduction_responses,
    get_integral_sums_description,
    get_integral_sums_response,
    get_increase_percentage_description,
    get_increase_percentage_response,
    get_all_calculations_description,
    get_all_calculations_response
)
from service.converters.time_converter import iso_to_timestamp

router = APIRouter(
    prefix="/calculations",
    tags=["Calculations API"],
)


@router.get(
    path="/get_days_to_target_reduction",
    name="Get the number of days the initial percentage increase decreases by a given percentage",
    description=get_days_to_target_reduction_description,
    responses=get_days_to_target_reduction_responses
)
async def get_days_to_target_reduction(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
    target_reduction: float = 1.0,
) -> list[tuple[float, int]]:
    start_date = start
    end_date = end
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    is_key_exist = True
    try:
        days_to_target_reduction = calculations_service.get_days_to_target_reduction_with_timestamp(
            ts_api=ts_api,
            ticker=name,
            start=start,
            end=end,
            target_reduction=target_reduction
        )
    except redis.ResponseError as err:
        is_key_exist = False

    if is_key_exist and len(days_to_target_reduction) != 0:
        return days_to_target_reduction

    if start_date == "-" or end_date == "+":
        return []

    try:
        moex_service.add_data_by_ticker(ts_api, name, start_date, end_date)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    return calculations_service.get_days_to_target_reduction_with_timestamp(
        ts_api=ts_api,
        ticker=name,
        start=start,
        end=end,
        target_reduction=target_reduction
    )


@router.get(
    path="/get_integral_sum",
    name="Obtaining the integral sums for a given time interval",
    description=get_integral_sums_description,
    responses=get_integral_sums_response
)
async def get_integral_sum(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
) -> list[tuple[float, float]]:
    start_date = start
    end_date = end
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    is_key_exist = True
    try:
        integral_sum = calculations_service.get_integral_sum_with_timestamp(
            ts_api=ts_api,
            ticker=name,
            start=start,
            end=end
        )
    except redis.ResponseError as err:
        is_key_exist = False

    if is_key_exist and len(integral_sum) != 0:
        return integral_sum

    if start_date == "-" or end_date == "+":
        return []

    try:
        moex_service.add_data_by_ticker(ts_api, name, start_date, end_date)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    return calculations_service.get_integral_sum_with_timestamp(
        ts_api=ts_api,
        ticker=name,
        start=start,
        end=end
    )


@router.get(
    path="/get_increase_percentage",
    name="Obtaining the increase percentages for a given time interval",
    description=get_increase_percentage_description,
    responses=get_increase_percentage_response
)
async def get_increase_percentage(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
) -> list[tuple[float, float]]:
    start_date = start
    end_date = end
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    is_key_exist = True
    try:
        increase_percentage = calculations_service.get_increase_percentage_with_timestamp(
            ts_api=ts_api,
            ticker=name,
            start=start,
            end=end
        )
    except redis.ResponseError as err:
        is_key_exist = False

    if is_key_exist and len(increase_percentage) != 0:
        return increase_percentage

    if start_date == "-" or end_date == "+":
        return []

    try:
        moex_service.add_data_by_ticker(ts_api, name, start_date, end_date)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    return calculations_service.get_increase_percentage_with_timestamp(
        ts_api=ts_api,
        ticker=name,
        start=start,
        end=end
    )


@router.get(
    path="/get_all_calculations",
    name="Get all calculations (cost, open, close, min, max, integral sum, percentage changes, days to target reduction) for a given time interval",
    description=get_all_calculations_description,
    responses=get_all_calculations_response
)
async def get_all_calculations(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
    target_reduction: float = 1.0,
) -> dict[str, Any]:
    start_date = start
    end_date = end
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    is_key_exist = True
    try:
        all_calculations = calculations_service.get_all_calculations(
            ts_api=ts_api,
            ticker=name,
            start=start,
            end=end,
            target_reduction=target_reduction
        )
    except redis.ResponseError as err:
        is_key_exist = False

    if is_key_exist and len(all_calculations["timestamp"]) != 0:
        return all_calculations

    if start_date == "-" or end_date == "+":
        return {}

    try:
        moex_service.add_data_by_ticker(ts_api, name, start_date, end_date)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    return calculations_service.get_all_calculations(
        ts_api=ts_api,
        ticker=name,
        start=start,
        end=end,
        target_reduction=target_reduction
    )
