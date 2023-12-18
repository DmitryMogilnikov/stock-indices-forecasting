import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.app_config import app_config

app = FastAPI(
    title="Stock indices forecasting service",
    description="Description",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.service_host,
        port=app_config.service_port,
        reload=True,
    )
