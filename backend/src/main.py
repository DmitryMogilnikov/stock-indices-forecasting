from fastapi import FastAPI
import uvicorn
from api import router

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
        host="localhost",
        port=8000,
        reload=True,
    )
