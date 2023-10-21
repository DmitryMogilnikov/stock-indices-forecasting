from datetime import datetime


def iso_to_timestamp(iso_date: str) -> float:
    iso_date = datetime.fromisoformat(iso_date)
    return iso_date.timestamp() * 1000


def timestamp_to_iso(timestamp: float) -> str:
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.isoformat()
