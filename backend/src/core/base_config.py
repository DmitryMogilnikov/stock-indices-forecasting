from pathlib import Path

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):

    class Config:
        env_file = (rf"{Path().resolve()}/environments/.env")
        env_file_encoding = "utf-8"
        extra = "ignore"
