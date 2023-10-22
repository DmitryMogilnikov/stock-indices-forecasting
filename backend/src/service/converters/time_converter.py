from datetime import datetime
from backend.src.exceptions import moex
import pytz


def iso_to_timestamp(iso_date: str) -> float:
    moscow_timezone = pytz.timezone('Europe/Moscow')
    try:
        iso_date = datetime.\
            fromisoformat(iso_date).\
            replace(tzinfo=moscow_timezone)
    except ValueError as err:
        raise moex.InvalidDateFormat(err)

    return iso_date.timestamp()


def timestamp_to_iso(timestamp: float) -> str:
    moscow_timezone = pytz.timezone('Europe/Moscow')
    dt_utc = datetime.utcfromtimestamp(timestamp)
    dt_moscow = dt_utc.replace(tzinfo=pytz.utc).astimezone(moscow_timezone)
    return dt_moscow.strftime('%Y-%m-%d')
