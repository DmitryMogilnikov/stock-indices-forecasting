from fastapi import APIRouter
from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api
from typing import Literal

router = APIRouter(
    prefix="/ts",
    tags=["Timeseries API"],
)


@router.post(path='/add_one_point', name="Add one point to timeseries")
async def add_one_point_route(
    name: str,
    value: float,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
    timestamp: str | int = "*",
) -> None:
    ts_api.add_one_point(name=name, value=value, timestamp=timestamp, prefix=prefix.value)


@router.post(path='/add_points', name="Add list of points to timeseries")
async def add_points_route(
    name: str,
    points: list[tuple[int, float]],
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> None:
    ts_api.add_points(name=name, points=points, prefix=prefix.value)


@router.get(path='/get_last_point', name="Get last point from timeseries")
async def get_last_point_route(
    name: str,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> tuple[int, float]:
    return ts_api.get_last_point(name=name, prefix=prefix.value)


@router.get(path='/get_range', name="Get range points from timeseries")
async def get_range_route(
    name: str,
    start: str | int = '-',
    end: str | int = '+',
    count: int | None = None,
    reverse: bool = False,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> list[tuple[float, float]]:
    return ts_api.get_range(
        name=name,
        start=start,
        end=end,
        count=count,
        reverse=reverse,
        prefix=prefix.value,
    )


@router.delete(path='/delete_range', name="Delete range points from timeseries")
async def delete_range_route(
    name: str,
    start: str | int = '-',
    end: str | int = '+',
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> int:
    return ts_api.delete_range(name=name, start=start, end=end, prefix=prefix.value)


@router.delete(path='/delete_ts', name="Delete timeseries")
async def delete_ts_route(
    name: str,
    prefix: RedisTimeseriesPrefix = RedisTimeseriesPrefix.cost,
) -> None:
    ts_api.delete_ts(name=name, prefix=prefix.value)
