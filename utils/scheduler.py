import datetime
import queue
import threading

from calendar import Calendar
from schedule import Schedule


class Scheduler:
    def __init__(self, calender: Calendar):
        self.calender = calender

        self.queue = {}

    def addSchedule(self, schedule: Schedule, func, priority: int):
        eventTime = schedule.getNextEvent()

        if eventTime in self.queue:
            eventTime = eventTime - (priority * datetime.timedelta(microseconds=1))

        self.queue[schedule.getNextEvent()] = func

    def update(self):
        now = datetime.datetime.now()
        for eventTime, event in self.queue:
            if eventTime <= now:
                event()
