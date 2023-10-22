from backend.src.exceptions import BusinessExpection

class TimestampExceptions(BusinessExpection):
    pass

class TickerNotFoundError(TimestampExceptions):
    pass

class DataNotFoundForThisTime(TimestampExceptions):
    pass
