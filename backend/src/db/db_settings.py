from pydantic import BaseModel, RedisDsn, AnyUrl
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_connection_string: str = "redis://localhost:6379/0"
    db_ts_prefix: str = "TS"
    db_separator: str = "@"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


db_settings = DatabaseSettings()
