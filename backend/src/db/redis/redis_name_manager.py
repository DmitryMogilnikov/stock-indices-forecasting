from core.redis_config import redis_config
from pydantic import validate_call


class RedisNameManager:
    @validate_call
    def create_redis_name(self, name: str, prefix: str) -> str:
        return "{0}{1}{2}".format(
            prefix,
            redis_config.redis_separator,
            name,
            )

    @validate_call
    def redis_ts_name(self, name: str) -> str:
        return self.create_redis_name(name=name, prefix=redis_config.redis_ts_key)
    
    @validate_call
    def from_redis_name(self, name: str) -> str:
        return name.split(redis_config.redis_separator)[-1]

redis_name_manager: RedisNameManager = RedisNameManager()
