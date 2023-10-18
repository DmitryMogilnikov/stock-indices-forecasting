from db.db_settings import db_settings
from pydantic import validate_call


class RedisNameManager:
    @validate_call
    def create_redis_name(self, name: str, prefix: str) -> str:
        return "{0}{1}{2}".format(
            prefix,
            db_settings.db_separator,
            name,
            )

    @validate_call
    def redis_ts_name(self, name: str) -> str:
        return self.create_redis_name(name=name, prefix=db_settings.db_ts_prefix)
    
    @validate_call
    def from_redis_name(self, name: str) -> str:
        return name.split(db_settings.db_separator)[-1]

redis_name_manager = RedisNameManager()
