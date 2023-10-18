from fastapi import APIRouter
from api.ts import router as ts_router

router = APIRouter(prefix="/api")
router.include_router(ts_router)
