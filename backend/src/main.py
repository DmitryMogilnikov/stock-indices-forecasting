from fastapi import FastAPI
import uvicorn
from api import router
from core.app_config import app_config


app = FastAPI(
    title="Stock indices forecasting service",
    description="Description",
    version="0.0.1",
    contact={
        "name": "Mogilnikov Dmitry",
        "email": "d.mogqs@gmail.com"
    },
)

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.service_host,
        port=app_config.service_port,
        reload=True,
    )
