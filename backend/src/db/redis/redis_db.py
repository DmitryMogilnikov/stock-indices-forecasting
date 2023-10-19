from redis import Redis
from db.abstract_db import AbstractDatabase
from core.redis_config import redis_config
from pydantic import validate_call


class RedisDatabase(AbstractDatabase):
    db: Redis = Redis.from_url(redis_config.redis_dsn, socket_connect_timeout=1)

    @validate_call
    def check_connection(self) -> bool:
        """Check connection to Redis DB.
        
        Returns:
            bool: is DB active
        """
        try:
            if self.db.ping():
                return True
        except:
            return False
    
    @validate_call
    def get_all_keys(self) -> set[str]:
        """Extract all keys from Redis DB.

        Returns:
            set[str]: set of keys
        """
    
    @validate_call
    def check_existing_key(self, key: str) -> bool:
        """Check is key exists in Redis DB

        Args:
            key (str): key name
        
        Returns:
            bool: is key exists
        """

    @validate_call
    def delete_key(self, key: str) -> None:
        """Delete key from Redis DB.
        
        Args:
        key (str): name key
        """
        self.db.delete(key)

redis_db: RedisDatabase = RedisDatabase()