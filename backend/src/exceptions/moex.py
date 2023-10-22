from backend.src.exceptions import BusinessException


class MoexExceptions(BusinessException):
    pass


class TickerNotFoundError(MoexExceptions):
    pass


class DataNotFoundForThisTime(MoexExceptions):
    pass
