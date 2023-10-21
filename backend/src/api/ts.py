from typing import Literal

from fastapi import APIRouter

from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api
from service import ts_service
from docs.ts import (add_one_point_route_description,
                     add_points_route_description,
                     delete_range_route_description,
                     delete_ts_route_description,
                     get_last_point_route_description,
                     get_range_route_description,
                     get_days_to_target_reduction)
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

@router.get(
    path="/get_days_to_target_reduction",
    name="Get the number of days the initial percentage increase decreases by a given percentage",
    description=get_days_to_target_reduction,
)
async def get_days_to_target_reduction(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
    target_reduction: float = 1.0,
) -> list[int]:
    if start != "-":
        start = iso_to_timestamp(start)
    if end != "+":
        end = iso_to_timestamp(end)

    percentage_changes_test: list[float] = [0.53, 0.50, 0.45, 0.32] # CHANGE AFTER PR #19
    return ts_service.calculate_days_to_target_reduction(percentage_changes_test, target_reduction)
