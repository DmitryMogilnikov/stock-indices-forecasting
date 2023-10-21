from datetime import datetime

def iso_to_timestamp(iso_date: str) -> float:
    iso_date = datetime.fromisoformat(iso_date)
    return iso_date.timestamp()


def timestamp_to_iso(timestamp: float) -> str:
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d')
