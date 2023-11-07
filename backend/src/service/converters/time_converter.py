from datetime import datetime

import pytz

from exceptions import moex


def str_to_iso(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")


def iso_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def iso_to_timestamp(iso_date: str) -> float:
    moscow_timezone = pytz.timezone('Europe/Moscow')
    try:
        iso_date = datetime.\
            fromisoformat(iso_date).\
            replace(tzinfo=moscow_timezone)
    except ValueError as err:
        raise moex.InvalidDateFormat(err)

    return iso_date.timestamp() * 1000


def timestamp_to_iso(timestamp: float) -> str:
    moscow_timezone = pytz.timezone('Europe/Moscow')
    dt_utc = datetime.utcfromtimestamp(timestamp / 1000)
    dt_moscow = dt_utc.replace(tzinfo=pytz.utc).astimezone(moscow_timezone)
    return dt_moscow.strftime('%Y-%m-%d')
