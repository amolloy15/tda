import datetime
import dateutil.tz
import heapq
import logging
import time

from calendar import Calendar

from typing import Callable, Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Scheduler:
    """
    A simple event and job scheduler.

    This scheduler allows scheduling one-off events at specific datetimes
    using a min-heap priority queue, as well as recurring jobs that
    determine their next execution time using a `getNextEvent(self)` method.

    All times are handled in America/Chicago timezone.
    """

    def __init__(self, calender: Calendar):
        """
        Initialize the scheduler.

        Args:
            calender (Calendar): Market calendar information
        """
        self._calender = calender

        self._tz = dateutil.tz.gettz('America/Chicago')

        # List to hold recurring job instances
        self._jobs: List[Any] = []

        # Min-heap priority queue for scheduled one-off events:
        # each element is a tuple of (event datetime, event dict containing func, args, kwargs)
        self._queue: List[tuple[datetime.datetime, Dict[str, Any]]] = []

    def addEvent(self,
                 eventTime: datetime.datetime,
                 func: Callable,
                 args: Optional[List[Any]] = None,
                 kwargs: Optional[Dict[str, Any]] = None):
        """
        Schedule a one-time event to run at the specified datetime.

        Args:
            eventTime (datetime.datetime): When to execute the function.
            func (Callable): The function to execute.
            args (Optional[List[Any]]): Positional arguments for the function.
            kwargs (Optional[Dict[str, Any]]): Keyword arguments for the function.
        """
        heapq.heappush(self._queue, (eventTime, {
            'func': func,
            'args': args or [],
            'kwargs': kwargs or {}
        }))

        logger.debug(f'Scheduled event {func} for {eventTime}')

    def addJob(self, job: Any):
        """
        Add a recurring job to the scheduler.

        The job should implement a `getNextEvent(self)` method,
        which will call `scheduler.addEvent()` to schedule its next execution.

        Args:
            job (Any): The job instance to add.
        """
        self._jobs.append(job)
        logger.debug(f'Added schedule {job.__module__} to scheduler')

    def update(self):
        """
        Check and run due events and update recurring jobs.

        This will:
        - Execute all one-off events whose scheduled time <= now.
        - Call `getNextEvent(self)` on each recurring job to allow them to schedule their next execution.
        """
        now = datetime.datetime.now(self._tz)

        # Run all due events
        while self._queue and self._queue[0][0] <= now:
            _, event = heapq.heappop(self._queue)
            try:
                logger.debug(f"Running {event['func']}")
                event['func'](*event['args'], **event['kwargs'])
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                logger.error(f"error running {event['func'].__name__: {e}}")

        # Allow each job to schedule its next event
        for job in self._jobs:
            job.getNextEvent(self)

    def run(self):
        """
        Continuously run the scheduler loop.

        This will:
        - Repeatedly call `update()` to execute due events and jobs.
        - Sleep until the next scheduled event if one exists, otherwise sleep for 1 second.
        """
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
