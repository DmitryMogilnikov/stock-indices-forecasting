from typing import Literal

from fastapi import APIRouter, HTTPException

from core.redis_config import RedisTimeseriesPrefix, redis_config
from service import ts_data as ts_data_service
from backend.src.exceptions import MismatchSizeError, ts
from db.redis.redis_ts_api import ts_api
from docs.ts import (add_one_point_route_description,
                     add_points_route_description,
                     delete_range_route_description,
                     delete_ts_route_description,
                     get_last_point_route_description,
                     get_range_route_description,
                     add_data_from_moex_by_ticker_description)
from service.converters.time_converter import iso_to_timestamp

router = APIRouter(
    prefix="/ts",
    tags=["Timeseries API"],
)

t = Literal["COST", "MAX", "MIN"]


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

    ts_api.add_one_point(name=name, value=value, timestamp=date, prefix=prefix.value)


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
    ts_api.add_points(name=name, points=points, prefix=prefix.value)


@router.get(
    path="/get_last_point",
    name="Get last point from timeseries",
    description=get_last_point_route_description,
)
async def get_last_point_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
) -> tuple[int, float]:
    return ts_api.get_last_point(name=name, prefix=prefix.value)


@router.get(
    path="/get_range",
    name="Get range points from timeseries",
    description=get_range_route_description,
)
async def get_range_route(
    name: str,
    prefix: RedisTimeseriesPrefix,
    start: str | int = "-",
    end: str | int = "+",
    count: int | None = None,
    reverse: bool = False,
) -> list[tuple[float, float]]:
    if start != "-":
        start = iso_to_timestamp(start)
    if end != "+":
        end = iso_to_timestamp(end)

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
    return ts_api.delete_range(name=name, start=start, end=end, prefix=prefix.value)


@router.delete(
    path="/delete_ts",
    name="Delete timeseries",
    description=delete_ts_route_description,
)
async def delete_ts_route(
    name: str,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> None:
    ts_api.delete_ts(name=name, prefix=prefix.value)

@router.post(
    path="/add_data_from_moex_by_ticker",
    name="Add data from moex by ticker",
    description=add_data_from_moex_by_ticker_description,
)
async def add_data_from_moex_by_ticker_route(
    name: str,
    start: str,
    end: str,
) -> None:
    start, end = ts_data_service.define_time_range_with_minimum_duration(start, end)
    try:
        df = ts_data_service.get_historical_information(name, start, end)
        costs_with_timestamps = ts_data_service.get_values_with_timestamps(df['TRADEDATE'], df['MARKETPRICE2'])
        opens_with_timestamps = ts_data_service.get_values_with_timestamps(df['TRADEDATE'], df['OPEN'])
        closes_with_timestamps = ts_data_service.get_values_with_timestamps(df['TRADEDATE'], df['CLOSE'])
        maxs_with_timestamps = ts_data_service.get_values_with_timestamps(df['TRADEDATE'], df['HIGH'])
        mins_with_timestamps = ts_data_service.get_values_with_timestamps(df['TRADEDATE'], df['LOW'])

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))

    except (ts.TickerNotFoundError, ts.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    ts_api.add_points(name, redis_config.redis_cost_key, costs_with_timestamps)
    ts_api.add_points(name, redis_config.redis_open_key, opens_with_timestamps)
    ts_api.add_points(name, redis_config.redis_close_key, closes_with_timestamps)
    ts_api.add_points(name, redis_config.redis_max_key, maxs_with_timestamps)
    ts_api.add_points(name, redis_config.redis_min_key, mins_with_timestamps)
