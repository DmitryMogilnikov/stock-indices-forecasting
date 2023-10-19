from pydantic import Field
from core.base_config import BaseConfig


class RedisConfig(BaseConfig):
    redis_dsn: str = Field(..., env="REDIS_DSN")
    redis_ts_key: str = Field(..., env="REDIS_TS_KEY")
    redis_separator: str = Field(..., env="REDIS_SEPARATOR")

redis_config = RedisConfig()
