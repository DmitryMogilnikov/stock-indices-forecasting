from fastapi import APIRouter, HTTPException
from typing import Any

from exceptions import moex
from service import calculations as calculations_service
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
) -> list[int]:
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

        prices = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='COST')]
    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    except redis.ResponseError as err:
        raise HTTPException(status_code=404, detail=f'Ticker {name} not found in database')

    integral_sums: list[float] = calculations_service.calc_integral_sum(prices)
    percentage_changes: list[float] = calculations_service.calc_increase_percentage(integral_sums)
    return calculations_service.calculate_days_to_target_reduction(
        percentage_changes,
        target_reduction
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
) -> list[float]:
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

        prices = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='COST')]
    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    except redis.ResponseError as err:
        raise HTTPException(status_code=404, detail=f'Ticker {name} not found in database')

    return calculations_service.calc_integral_sum(prices)

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
) -> list[float]:
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

        prices = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='COST')]
    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    except redis.ResponseError as err:
        raise HTTPException(status_code=404, detail=f'Ticker {name} not found in database')

    integral_sum = calculations_service.calc_integral_sum(prices)
    return calculations_service.calc_increase_percentage(integral_sum)


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
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)

        costs = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='COST')]

        opens = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='OPEN')]
        
        closes = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='CLOSE')]
        
        maxs = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='MAX')]
        
        mins = [t[0] for t in ts_api.get_range(
            name=name,
            start=start,
            end=end,
            prefix='MIN')]
    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    except redis.ResponseError as err:
        raise HTTPException(status_code=404, detail=f'Ticker {name} not found in database')

    integral_sum = calculations_service.calc_integral_sum(costs)
    percentage_changes = calculations_service.calc_increase_percentage(integral_sum)
    days_to_target_reduction = calculations_service.calculate_days_to_target_reduction(percentage_changes, target_reduction)

    return {
        "cost": costs,
        "open": opens,
        "close": closes,
        "max": maxs,
        "min": mins,
        "integral_sum": integral_sum,
        "percentage_changes": percentage_changes,
        "days_to_target_reduction": days_to_target_reduction
    }
