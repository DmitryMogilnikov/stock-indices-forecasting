from pydantic_settings import BaseSettings
from pathlib import Path

class BaseConfig(BaseSettings):

    class Config:
        env_file = Path("backend\environments\.env")
        env_file_encoding = "utf-8"
        extra="ignore"

