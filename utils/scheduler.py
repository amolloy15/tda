import datetime
import dateutil.tz
import heapq
import logging
import time

from calendar import Calendar

from typing import Callable, Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, calender: Calendar):
        self._calender = calender

        self._tz = dateutil.tz.gettz('America/Chicago')

        self._jobs: List[Any] = []
        self._queue: List[tuple[datetime.datetime, Dict[str, Any]]] = []

    def addEvent(self,
                 eventTime: datetime.datetime,
                 func: Callable,
                 args: Optional[List[Any]] = None,
                 kwargs: Optional[Dict[str, Any]] = None):
        heapq.heappush(self._queue, (eventTime, {
            'func': func,
            'args': args or [],
            'kwargs': kwargs or {}
        }))

        logger.debug(f'Scheduled event {func} for {eventTime}')

    def addJob(self, job: Any):
        self._jobs.append(job)
        logger.debug(f'Added schedule {job.__module__} to scheduler')

    def update(self):
        now = datetime.datetime.now(self._tz)
        while self._queue and self._queue[0][0] <= now:
            _, event = heapq.heappop(self._queue)
            try:
                logger.debug(f"Running {event['func']}")
                event['func'](*event['args'], **event['kwargs'])
            except Exception as e:
                logger.error(f"error running {event['func'].__name__: {e}}")

        for job in self._jobs:
            job.getNextEvent(self)

    def run(self):
        while True:
            self.update()
            now = datetime.datetime.now(self._tz)
            if self._queue:
                next_time = self._queue[0][0]
                sleep_time = max(0, (next_time - now).seconds)
                sleep_time += 1
            else:
                sleep_time = 1.0

            time.sleep(sleep_time)
