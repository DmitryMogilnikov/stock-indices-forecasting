from fastapi import HTTPException, status

from core.redis_config import RedisTimeseriesPrefix
from db.redis.redis_ts_api import ts_api


def check_ts_exists(name: str, prefix: RedisTimeseriesPrefix):
    if not ts_api.check_existing_ts(name, prefix):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Timeseries with {name=} not found.")