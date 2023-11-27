from fastapi import APIRouter, HTTPException

from db.redis.redis_ts_api import ts_api
from docs.moex import (
    add_data_by_ticker_description,
    add_data_by_ticker_responses,
)
from exceptions import MismatchSizeError, moex
from service import moex as moex_service

router = APIRouter(
    prefix="/moex",
    tags=["Moex Interaction API"],
)


@router.post(
    path="/add_data_by_ticker",
    name="Add data from moex by ticker",
    description=add_data_by_ticker_description,
    responses=add_data_by_ticker_responses
)
async def add_data_by_ticker_route(
    name: str,
    start: str,
    end: str,
) -> None:
    try:
        moex_service.add_data_by_ticker(ts_api, name, start, end)

    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))
