import datetime

import tda

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
    def __init__(self, td: tda):
        self.startDate = datetime.date.today()

        self._currentTime = datetime.datetime.now()

        self._td = td

        self._marketDay = TradeRelativeDay.Status.nonTradingDay
        self._marketTime = TradeRelativeTime.Status.marketClosedToday

        self.getStatus()

    def action(self, func):
        def wrapper():
            self._currentTime = datetime.datetime.now()
            func()
        return wrapper

    def getMarketDay(self):
        return self._marketDay

    def setMarketDay(self, status: TradeRelativeDay.Status):
        self._marketDay = status

        if status == TradeRelativeDay.Status.nonTradingDay:
            self._marketTime = TradeRelativeTime.Status.marketClosedToday

    def getMarketTime(self):
        return self._marketTime

    def setMarketTime(self, status: TradeRelativeTime.Status):
        self._marketTime = status

        if status == TradeRelativeTime.Status.marketClosedToday:
            self._marketDay = TradeRelativeDay.Status.nonTradingDay
        else:
            self._marketDay = TradeRelativeDay.Status.tradingDay

    @action
    def getStatus(self):
        mkt = tda.client.Client.Markets.EQUITY

        resp = self._td.client.get_hours_for_single_market(mkt, self._currentTime)

        assert resp.status_code == 200

        hours = resp.json()['equity']
        equityKeys = hours.keys()

        if 'EQ' in equityKeys:
            equityKey = 'EQ'
        else:
            equityKey = 'equity'

        hours = hours[equityKey]['sessionHours']

        if hours is None:
            self.setMarketTime(TradeRelativeTime.Status.marketClosedToday)
