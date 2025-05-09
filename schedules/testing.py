import datetime
import logging

from utils.job import Job
from utils.scheduler import Scheduler

logger =  logging.getLogger(__name__)


class TestScheduler(Job):
    def __init__(self, *args, **kwargs):
        super().__init__('', '')
        self.active = True

        self._scheduled = False

    def test(self):
        logger.debug('test')
        self._scheduled = False

    def getNextEvent(self, scheduler: Scheduler):
        if not self._scheduled:
            scheduler.addEvent(self._now() + datetime.timedelta(seconds=10), self.update)
            self._scheduled = True

    def update(self):
        self.test()
