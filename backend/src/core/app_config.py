from pydantic import Field, PositiveInt

from core.base_config import BaseConfig


class AppConfig(BaseConfig):
    service_host: str = Field(..., env="SERVICE_HOST")
    service_port: PositiveInt = Field(..., env="SERVICE_PORT")


app_config = AppConfig()
