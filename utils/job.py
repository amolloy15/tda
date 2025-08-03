import datetime
import dateutil.tz

from cron_converter import Cron
from schwab import client
from typing import Optional

from utils.calendar import Calendar
from utils.scheduler import Scheduler


class Job:
    """
    Base Job class for use with the Scheduler system.

    This class defines the structure and interface for a job that can:
    - Determine its next execution time based on a cron schedule.
    - Be registered with the Scheduler to run periodically.

    Intended to be subclassed with a concrete `update` method that defines
    what the job does during execution.
    """

    def __init__(self, cal: Calendar, sc: client, baseSchedule: Optional[Cron] = None):
        """
        Initialize the Job.

        Args:
            cal (Calendar): Calendar object with market info
            sc (client): Schwab client for API interactions.
            baseSchedule (Optional[Cron]): A Cron object defining the base cron schedule for this job.
        """
        self.active: bool = False

        self._tz = dateutil.tz.gettz('America/Chicago')

        self._sc: client = sc

        self._cal: Calendar = cal

        self._baseSchedule: Cron = baseSchedule

    @property
    def now(self) -> datetime.datetime:
        """
        Get the current datetime in the configured timezone.

        Returns:
            datetime.datetime: Current datetime in America/Chicago timezone.
        """
        return datetime.datetime.now(self._tz)

    def getNextEvent(self, scheduler: Scheduler):
        """
        Determine and schedule the next execution time of this job using its base cron schedule.

        This uses the `cron_converter` library to compute the next execution time
        and registers the `update` method of this job with the scheduler.

        Args:
            scheduler (Scheduler): The scheduler instance to add the event to.
        """
        # Compute the next scheduled time using the cron schedule
        cronSchedule = self._baseSchedule.schedule(self.now)

        # Schedule this job's `update` method to run at the next cron-scheduled time
        scheduler.addEvent(cronSchedule.next(), self.update)

    def update(self, scheduler: Optional[Scheduler] = None):
        """
        The core logic to be executed when the job runs.

        Must be implemented by subclasses. This method should define what the job actually does
        (e.g., fetch data, place trades, log reports).

        Raises:
            NotImplementedError: Always, unless overridden by a subclass.
        """
        raise NotImplementedError('update and getNextEvent methods must be implemented by all subclasses')
