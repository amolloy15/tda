import datetime

from enum import Enum


class TradeRelativeDay:
    class Status(Enum):
        tradingDay = 0
        nonTradingDay = 1


class TradeRelativeTime:
    class Status(Enum):
        preMarket = 0
        marketOpen = 1
        afterMarket = 2
        marketClosedToday = -1


class Calendar:
    def __init__(self, td):
        self.startDate = datetime.date.today()