from pydantic import BaseModel, PositiveInt
from datetime import datetime


class HealthCheckResponse(BaseModel):
    date_time: str = datetime.utcnow().isoformat()
    status_code: PositiveInt
    status_message: str
