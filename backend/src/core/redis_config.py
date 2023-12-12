from enum import Enum
from typing import Literal

from pydantic import Field

from core.base_config import BaseConfig


class RedisConfig(BaseConfig):
    redis_dsn: str = Field(..., env="REDIS_DSN")
    redis_open_key: str = Field(..., env="REDIS_OPEN_KEY")
    redis_close_key: str = Field(..., env="REDIS_CLOSE_KEY")
    redis_max_key: str = Field(..., env="REDIS_MAX_KEY")
    redis_min_key: str = Field(..., env="REDIS_MIN_KEY")
    redis_separator: str = Field(..., env="REDIS_SEPARATOR")
    redis_duplicate_policy: str = Field(..., env="REDIS_DUPLICATE_POLICY")


redis_config = RedisConfig()


class RedisTimeseriesPrefix(str, Enum):
    open = redis_config.redis_open_key
    close = redis_config.redis_close_key
    max = redis_config.redis_max_key
    min = redis_config.redis_min_key


redis_ts_prefixes = Literal[
    tuple([prefix.value for prefix in RedisTimeseriesPrefix])
]
