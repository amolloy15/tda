import datetime


class Schedule:
    def __init__(self, nextEvent: datetime.datetime, recurring: bool = False,
                 recurringSchedule: datetime.timedelta = None):

        self.currentTime = datetime.datetime.now()

        self.nextEvent = nextEvent
        self.timeToNextEvent = nextEvent - self.currentTime

        self.recurring = recurring
        self.recurringSchedule = recurringSchedule

    def getNextEvent(self) -> datetime.datetime:
        event = self.nextEvent

        self.nextEvent = event + self.recurringSchedule

        return event
