import datetime
import queue
import threading


class Scheduler:
    def __init__(self, calender):
        self.calender = calender

