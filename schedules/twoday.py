import datetime

from cron_converter import Cron
from schwabdev import Client as SchwabClient
from typing import Any, Dict, List

from utils.calendar import Calendar
from utils.job import Job
from utils.scheduler import Scheduler


class TwoDaySPYTrader(Job):
    def __init__(self, cal: Calendar, sdc: SchwabClient):
        cronSchedule = '30 8 * * *'
        super().__init__(cal, sdc, Cron(cron_string=cronSchedule))

        # nextEvents: {'eventTime': datetime.datetime,
        #              'func': func,
        #              'args': Optional[List[Any]],
        #              'kwargs': Optional[Dict[str, Any]]}
        self._nextEvents: List[Dict[str, Any]] = []

    def update(self):
        # check previous 2 days of market movement
        # if check is actionable, submit multiple schedules to the scheduler
        pass

    def getNextEvent(self, scheduler: Scheduler):
        if self._nextEvents:
            while self._nextEvents:
                event = self._nextEvents.pop()
                scheduler.addEvent(event['eventTime'],
                                   event['func'],
                                   event['args'],
                                   event['kwargs'])
        else:
            cronSchedule = self._baseSchedule.schedule(self._now())

            scheduler.addEvent(cronSchedule.next(), self.update)
