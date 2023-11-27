from datetime import datetime

from pydantic import BaseModel, PositiveInt


class HealthCheckResponse(BaseModel):
    date_time: str = datetime.utcnow().isoformat()
    status_code: PositiveInt
    status_message: str
