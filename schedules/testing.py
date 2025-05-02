import datetime

from utils.job import Job
from utils.scheduler import Scheduler


class TestScheduler(Job):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.active = True

    def test(self):
        print('test')

    def getNextEvent(self, scheduler: Scheduler):
        scheduler.addEvent(self._now() + datetime.timedelta(seconds=10), self.update)

    def update(self):
        self.test()
