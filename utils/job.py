import datetime
import dateutil.tz

from cron_converter import Cron
from schwab import client
from typing import Optional

from utils.calendar import Calendar
from utils.scheduler import Scheduler


class Job:
    def __init__(self, cal: Calendar, sc: client, baseSchedule: Optional[Cron] = None):

        self.active: bool = False

        self._tz = dateutil.tz.gettz('America/Chicago')

        self._sc: client = sc

        self._cal: Calendar = cal

        self._baseSchedule: Cron = baseSchedule

    def _now(self) -> datetime.datetime:
        return datetime.datetime.now(self._tz)

    def getNextEvent(self, scheduler: Scheduler):
        cronSchedule = self._baseSchedule.schedule(self._now())

        scheduler.addEvent(cronSchedule.next(), self.update)

    def update(self):
        raise NotImplementedError('update and getNextEvent methods must be implemented by all subclasses')

