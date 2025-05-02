import datetime
import dateutil.tz

from cron_converter import Cron
from schwabdev import Client as SchwabClient
from typing import Optional

from utils.calendar import Calendar
from utils.scheduler import Scheduler


class Job:
    def __init__(self, cal: Calendar, sdc: SchwabClient, baseSchedule: Optional[Cron] = None):

        self.active = False

        self._tz = dateutil.tz.gettz('America/Chicago')

        self._cal = cal

        self._baseSchedule = baseSchedule

    def _now(self) -> datetime.datetime:
        return datetime.datetime.now(self._tz)

    def getNextEvent(self, scheduler: Scheduler):
        cronSchedule = self._baseSchedule.schedule(self._now())

        scheduler.addEvent(cronSchedule.next(), self.update)

    def update(self):
        raise NotImplementedError('update and getNextEvent methods must be implemented by all subclasses')

