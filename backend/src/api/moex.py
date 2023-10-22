from fastapi import APIRouter, HTTPException

from core.redis_config import redis_config
from backend.src.service import moex as moex_service
from backend.src.exceptions import MismatchSizeError, moex
from docs.moex import (
    add_data_from_moex_by_ticker_description,
    add_data_from_moex_by_ticker_responses)
from db.redis.redis_ts_api import ts_api

router = APIRouter(
    prefix="/moex",
    tags=["Moex Interaction API"],
)


@router.post(
    path="/add_data_from_moex_by_ticker",
    name="Add data from moex by ticker",
    description=add_data_from_moex_by_ticker_description,
    responses=add_data_from_moex_by_ticker_responses
)
async def add_data_from_moex_by_ticker_route(
    name: str,
    start: str,
    end: str,
) -> None:
    start, end = moex_service.define_time_range_with_minimum_duration(
        start,
        end
    )

    try:
        df = moex_service.get_historical_information(name, start, end)
        costs_with_timestamps = moex_service.get_values_with_timestamps(
            df['TRADEDATE'],
            df['MARKETPRICE2']
        )
        opens_with_timestamps = moex_service.get_values_with_timestamps(
            df['TRADEDATE'],
            df['OPEN']
        )
        closes_with_timestamps = moex_service.get_values_with_timestamps(
            df['TRADEDATE'],
            df['CLOSE']
        )
        maxs_with_timestamps = moex_service.get_values_with_timestamps(
            df['TRADEDATE'],
            df['HIGH']
        )
        mins_with_timestamps = moex_service.get_values_with_timestamps(
            df['TRADEDATE'],
            df['LOW']
        )

    except MismatchSizeError as err:
        raise HTTPException(status_code=500, detail=str(err))

    except (moex.TickerNotFoundError, moex.DataNotFoundForThisTime) as err:
        raise HTTPException(status_code=404, detail=str(err))

    ts_api.add_points(
        name,
        redis_config.redis_cost_key,
        costs_with_timestamps
    )
    ts_api.add_points(
        name,
        redis_config.redis_open_key,
        opens_with_timestamps
    )
    ts_api.add_points(
        name,
        redis_config.redis_close_key,
        closes_with_timestamps
    )
    ts_api.add_points(
        name,
        redis_config.redis_max_key,
        maxs_with_timestamps
    )
    ts_api.add_points(
        name,
        redis_config.redis_min_key,
        mins_with_timestamps
    )
