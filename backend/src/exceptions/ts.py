from backend.src.exceptions import BusinessException

class TimestampExceptions(BusinessException):
    pass

class TickerNotFoundError(TimestampExceptions):
    pass

class DataNotFoundForThisTime(TimestampExceptions):
    pass
