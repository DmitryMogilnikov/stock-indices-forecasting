from pydantic import validate_call
from redis import Redis

from core.redis_config import redis_config, redis_ts_prefixes
from db.redis.redis_db import RedisDatabase
from db.redis.redis_name_manager import redis_name_manager


class RedisTimeseriesAPI:
    redis_db: RedisDatabase = RedisDatabase()
    db_ts: Redis.ts = redis_db.db.ts()

    def add_one_point(
        self,
        name: str,
        prefix: redis_ts_prefixes,
        value: float,
        timestamp: str | int = "*"
    ) -> None:
        """Add point to Redis timeseries.

        Args:
            ts_name (str): name
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        return self.db_ts.add(
            key,
            timestamp,
            value,
            duplicate_policy=redis_config.redis_duplicate_policy
        )

    @validate_call
    def add_points(
        self,
        name: str,
        prefix: redis_ts_prefixes,
        points: list[tuple[int, float]]
    ) -> None:
        """Add points to Redis timeseries.

        Args:
            name (str): name
            points (tuple[tuple[int, float]]): tuple of [date, value]
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        pipeline = self.db_ts.pipeline()
        for timestamp, value in points:
            pipeline.add(
                key,
                timestamp,
                value,
                duplicate_policy=redis_config.redis_duplicate_policy
            )
        pipeline.execute()
    
    @validate_call
    def check_existing_ts(self, name: str, prefix: str) -> bool:
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        return self.redis_db.check_existing_key(key=key)

    @validate_call
    def get_last_point(
        self,
        prefix: redis_ts_prefixes,
        name: str
    ) -> tuple[int, float]:
        """Get last point from Redis timeseries.

        Args:
            name (str): name

        Returns:
            tuple[int, float]: last point (timestamp, value)
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        return self.db_ts.get(key=key)

    @validate_call
    def get_range(
        self,
        name: str,
        prefix: redis_ts_prefixes,
        start: str | int = "-",
        end: str | int = "+",
        count: int | None = None,
        reverse: bool = False,
    ) -> list[tuple[float, float]]:
        """Get range points from Redis timeseries.

        Args:
            name (str): name
            start: (str | int): start timestamp. Defaults = '-'
            end: (str | int): end timestamp. Defaults = '-'
            count: (int | None): limit for count of return points.
                Defaults = None
            reverse (bool): is get range from end to start.
                Defaults = False

        Returns:
            list[tuple[float, float]]: list of points
                [(timestamp, value), (timestamp, value), ...]
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        if reverse:
            return self.db_ts.revrange(
                key=key,
                from_time=start,
                to_time=end,
                count=count
            )
        return self.db_ts.range(
            key=key,
            from_time=start,
            to_time=end,
            count=count
        )

    @validate_call
    def delete_range(
        self,
        name: str,
        prefix: redis_ts_prefixes,
        start: str | int = "-",
        end: str | int = "+",
    ) -> None:
        """Delete range points from Redis timeseries.

        Args:
            name (str): name
            start: (str | int): start timestamp. Defaults = '-'
            end: (str | int): end timestamp. Defaults = '-'
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        return self.db_ts.delete(key=key, from_time=start, to_time=end)

    @validate_call
    def delete_ts(self, name: str, prefix: redis_ts_prefixes) -> None:
        """Delete Redis timeseries.

        Args:
            name (str): name
        """
        key = redis_name_manager.redis_ts_name(name=name, prefix=prefix)
        self.redis_db.delete_key(key=key)


ts_api: RedisTimeseriesAPI = RedisTimeseriesAPI()
