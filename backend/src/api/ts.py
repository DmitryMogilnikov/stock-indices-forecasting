from fastapi import APIRouter
from db.redis.redis_ts_api import ts_api

router = APIRouter(
    prefix="/ts",
    tags=["Timeseries API"],
)

@router.post('/add_one_point')
async def add_one_point_route(name: str, value: float, timestamp: str | int = "*") -> None:
    ts_api.add_one_point(name=name, value=value, timestamp=timestamp)


@router.post('/add_points')
async def add_points_route(name: str, points: list[tuple[int, float]]) -> None:
    ts_api.add_points(name=name, points=points)


@router.get('/get_last_point')
async def get_last_point_route(name: str) -> tuple[int, float]:
    return ts_api.get_last_point(name=name)


@router.get('/get_range')
async def get_range_route(
    name: str,
    start: str | int = '-',
    end: str | int = '+',
    count: int | None = None,
    reverse: bool = False,
) -> list[tuple[float, float]]:
    return ts_api.get_range(name, start, end, count, reverse)


@router.delete('/delete_range')
async def delete_range_route(name: str, start: str | int = '-', end: str | int = '+') -> None:
    return ts_api.delete_range(name, start, end)


@router.delete('/delete_ts')
async def delete_ts_route(name: str) -> None:
    return ts_api.delete_ts(name)
