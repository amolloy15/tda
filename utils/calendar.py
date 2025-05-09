import datetime
import dateutil.tz
import logging

import schwab

from enum import Enum

logger = logging.getLogger(__name__)


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
    def __init__(self, sc: schwab.client, timezone: str = "America/Chicago"):
        self._startDate = datetime.date.today()

        self._timezone = dateutil.tz.gettz(timezone)
        self._currentTime = datetime.datetime.now(self._timezone)

        self._client: schwab.client = sc

        self._marketDay = TradeRelativeDay.Status.nonTradingDay
        self._marketTime = TradeRelativeTime.Status.marketClosedToday

        self.updateStatus()

    def updateTime(self):
        self._currentTime = datetime.datetime.now(self._timezone)

    def getMarketDay(self):
        self.updateStatus()
        return self._marketDay

    def setMarketDay(self, status: TradeRelativeDay.Status):
        self._marketDay = status

        if status == TradeRelativeDay.Status.nonTradingDay:
            self._marketTime = TradeRelativeTime.Status.marketClosedToday

    def getMarketTime(self):
        self.updateStatus()
        return self._marketTime

    def setMarketTime(self, status: TradeRelativeTime.Status):
        self._marketTime = status

        if status == TradeRelativeTime.Status.marketClosedToday:
            self._marketDay = TradeRelativeDay.Status.nonTradingDay
        else:
            self._marketDay = TradeRelativeDay.Status.tradingDay

    def updateStatus(self):
        self.updateTime()
        mkt = schwab.client.Client.MarketHours.Market.EQUITY

        resp = self._client.get_market_hours(mkt, date=self._currentTime.date())

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
        else:
            openTime = datetime.datetime.fromisoformat(hours['regularMarket'][0]['start'])
            closeTime = datetime.datetime.fromisoformat(hours['regularMarket'][0]['end'])

            if self._currentTime < openTime:
                self.setMarketTime(TradeRelativeTime.Status.preMarket)
            elif self._currentTime > closeTime:
                self.setMarketTime(TradeRelativeTime.Status.afterMarket)
            else:
                self.setMarketTime(TradeRelativeTime.Status.marketOpen)

        logger.debug(f'Market status: {self._marketDay}, {self._marketTime}')
