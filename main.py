import importlib
import inspect
import logging
import os
import platform

import schwabdev

from utils.calendar import Calendar
from utils.job import Job
from utils.scheduler import Scheduler


def load_schedules(cal: Calendar):
    schedules = []
    schedule_dir = 'schedules'

    for filename in os.listdir(schedule_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"{schedule_dir}.{filename[:-3]}"
            module = importlib.import_module(module_name)

            # Inspect each class in the module
            for name, cls in inspect.getmembers(module, inspect.isclass):
                # Ensure it's a subclass of Job and not Job itself
                if issubclass(cls, Job) and cls is not Job:
                    print(f"Loaded schedule: {name}")
                    obj = cls(cal)
                    if obj.active:
                        schedules.append(obj)

    return schedules


def main():
    logger = logging.getLogger()
    if platform.system() == 'Darwin':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info('Starting trading app')

    client = schwabdev.Client('key', 'secret')

    cal = Calendar(client)
    scheduler = Scheduler(cal)

    try:
        scheduler.run()
    except KeyboardInterrupt:
        print('Ending')


if __name__ == '__main__':
    main()
