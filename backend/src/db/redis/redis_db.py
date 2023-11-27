import redis
from pydantic import validate_call

from core.redis_config import redis_config
from db.abstract_db import AbstractDatabase


class RedisDatabase(AbstractDatabase):
    db: redis.Redis = redis.Redis.from_url(
        redis_config.redis_dsn,
        socket_connect_timeout=1
    )

    @validate_call
    def check_connection(self) -> bool:
        """Check connection to Redis DB.

        Returns:
            bool: is DB active
        """
        try:
            return self.db.ping()
        except redis.exceptions.TimeoutError:
            return False

    @validate_call
    def get_all_keys(self) -> set[str]:
        """Extract all keys from Redis DB.

        Returns:
            set[str]: set of keys
        """
        return {key.decode("utf-8") for key in self.db.scan_iter()}

    @validate_call
    def check_existing_key(self, key: str) -> bool:
        """Check is key exists in Redis DB

        Args:
            key (str): key name

        Returns:
            bool: is key exists
        """
        return key in self.get_all_keys()

    @validate_call
    def delete_key(self, key: str) -> None:
        """Delete key from Redis DB.

        Args:
        key (str): name key
        """
        self.db.delete(key)


redis_db: RedisDatabase = RedisDatabase()
