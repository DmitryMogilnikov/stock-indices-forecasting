from fastapi import APIRouter
from api.ts import router as ts_router
from api.health_check import router as health_check_router

router = APIRouter(prefix="/api")
router.include_router(health_check_router)
router.include_router(ts_router)
