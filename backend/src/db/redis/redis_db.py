from redis import Redis
from db.abstract_db import AbstractDatabase
from db.db_settings import db_settings
from pydantic import validate_call


class RedisDatabase(AbstractDatabase):
    db: Redis = Redis.from_url(db_settings.db_connection_string)

    @validate_call
    def delete_key(self, key_name: str) -> None:
        self.db.delete(key_name)
