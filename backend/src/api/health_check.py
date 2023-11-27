from fastapi import APIRouter, Response, status

from db.redis.redis_db import redis_db
from schemas.health_check.health_check_response import HealthCheckResponse

router = APIRouter(
    prefix="/health",
    tags=["Health check"],
)


@router.get(path="/service", name="Service health check")
async def health_check_service_route(response: Response):
    response.status_code = status.HTTP_200_OK
    return HealthCheckResponse(
        status_code=status.HTTP_200_OK,
        status_message="Service is running."
    )


@router.get(path="/redis", name="Redis health check")
async def health_check_redis_route(response: Response):
    if redis_db.check_connection():
        response.status_code = status.HTTP_200_OK
        return HealthCheckResponse(
            status_code=response.status_code,
            status_message="Redis is connected."
        )

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthCheckResponse(
        status_code=response.status_code,
        status_message="Redis is not connected."
    )
