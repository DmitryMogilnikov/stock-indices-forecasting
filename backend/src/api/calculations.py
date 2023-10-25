from fastapi import APIRouter, HTTPException

from exceptions import moex
from service import calculations as calculations_service
from docs.calculations import (
    get_days_to_target_reduction_description,
    get_days_to_target_reduction_responses
)
from service.converters.time_converter import iso_to_timestamp

router = APIRouter(
    prefix="/calculations",
    tags=["Calculations API"],
)


@router.get(
    path="/get_days_to_target_reduction",
    name="Get the number of days the initial percentage increase decreases by a given percentage",
    description=get_days_to_target_reduction_description,
    responses=get_days_to_target_reduction_responses
)
async def get_days_to_target_reduction(
    name: str,
    start: str | int = "-",
    end: str | int = "+",
    target_reduction: float = 1.0,
) -> list[int]:
    try:
        if start != "-":
            start = iso_to_timestamp(start)
        if end != "+":
            end = iso_to_timestamp(end)
    except moex.InvalidDateFormat as err:
        raise HTTPException(status_code=400, detail=str(err))

    percentage_changes_test: list[float] = [0.53, 0.50, 0.45, 0.32] # CHANGE AFTER PR #29
    return calculations_service.calculate_days_to_target_reduction(
        percentage_changes_test,
        target_reduction
    )
