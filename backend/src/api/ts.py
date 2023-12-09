import redis
from fastapi import APIRouter, HTTPException

from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api
from docs.ts import (
    add_one_point_route_description,
    add_points_route_description,
    check_existing_ts_route_description,
    delete_range_route_description,
    delete_ts_route_description,
    get_last_point_route_description,
    get_range_route_description, get_range_route_responses,
)
from exceptions import MismatchSizeError, moex
from exceptions.ts import check_ts_exists
from service import moex as moex_service
from service.converters.time_converter import iso_to_timestamp

router = APIRouter(
    prefix="/ts",
    tags=["Timeseries API"],
)


@router.post(
    path="/add_one_point",
    name="Add one point to timeseries",
    description=add_one_point_route_description,
)
async def add_one_point_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
    date: str = "*",
    value: float = 0,
) -> None:
    if date != "*":
        date = iso_to_timestamp(date)

    ts_api.add_one_point(
        name=name,
        value=value,
        timestamp=date,
        prefix=prefix.value
    )


@router.post(
    path="/add_points",
    name="Add list of points to timeseries",
    description=add_points_route_description,
)
async def add_points_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
    points: list[tuple[int, float]],
) -> None:
    ts_api.add_points(
        name=name,
        points=points,
        prefix=prefix.value
    )

@router.get(
    path="/check_existing_key",
    name="Check if ts exist in Redis",
    description=check_existing_ts_route_description,
)
async def get_last_point_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
) -> bool:
    return ts_api.check_existing_ts(
        name=name,
        prefix=prefix.value
    )

@router.get(
    path="/get_last_point",
    name="Get last point from timeseries",
    description=get_last_point_route_description,
)
async def get_last_point_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
) -> tuple[int, float]:
    check_ts_exists(name, prefix)
    return ts_api.get_last_point(
        name=name,
        prefix=prefix.value
    )


@router.get(
    path="/get_range",
    name="Get range points from timeseries",
    description=get_range_route_description,
    responses=get_range_route_responses
)
async def get_range_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
    start: str | int = "-",
    end: str | int = "+",
    count: int | None = None,
    reverse: bool = False,
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
        ts_range = ts_api.get_range(
            name=name,
            start=start,
            end=end,
            count=count,
            reverse=reverse,
            prefix=prefix.value,
        )
    except redis.ResponseError:
        is_key_exist = False

    if is_key_exist and len(ts_range) != 0:
        return ts_range
    
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

    return ts_api.get_range(
        name=name,
        start=start,
        end=end,
        count=count,
        reverse=reverse,
        prefix=prefix.value,
    )


@router.delete(
    path="/delete_range",
    name="Delete range points from timeseries",
    description=delete_range_route_description,
)
async def delete_range_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
    start: str | int = "-",
    end: str | int = "+",
) -> int:
    if start != "-":
        start = iso_to_timestamp(start)
    if end != "+":
        end = iso_to_timestamp(end)
    return ts_api.delete_range(
        name=name,
        start=start,
        end=end,
        prefix=prefix.value
    )


@router.delete(
    path="/delete_ts",
    name="Delete timeseries",
    description=delete_ts_route_description,
)
async def delete_ts_route(
    name: str,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.close,
) -> None:
    ts_api.delete_ts(
        name=name,
        prefix=prefix.value
    )
