from fastapi import APIRouter

from api.calculations import router as calculations_router
from api.health_check import router as health_check_router
from api.moex import router as moex_router
from api.ts import router as ts_router

router = APIRouter(prefix="/api")
router.include_router(health_check_router)
router.include_router(ts_router)
router.include_router(moex_router)
router.include_router(calculations_router)
