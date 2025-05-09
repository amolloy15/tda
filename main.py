import importlib
import inspect
import logging
import os
import platform

from schwab.auth import easy_client

from utils.calendar import Calendar
from utils.job import Job
from utils.scheduler import Scheduler

logger = logging.getLogger(__name__)


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


def load_schedules_dumb(cal, sc) -> list:
    from schedules.testing import TestScheduler
    from schedules.twoday import TwoDaySPYTrader
    # return [TestScheduler(), TwoDaySPYTrader(cal, sc)]
    return [TestScheduler()]


def get_client():
    api_key = os.environ['app_key']
    app_secret = os.environ['app_secret']
    callback_url = os.environ['callback_url']
    token_path = '/tmp/token.json'

    return easy_client(api_key, app_secret, callback_url, token_path)


def main():
    if platform.system() == 'Darwin':
        level = logging.DEBUG
    else:
        level = logging.INFO

    fmt = '%(asctime)s: %(message)s'
    logging.basicConfig(filename='log.log', level=level, format=fmt)

    logger.info('Starting trading app')

    client = get_client()
    logger.debug('Initialized client')

    cal = Calendar(client)
    scheduler = Scheduler(cal)

    for sched in load_schedules_dumb(cal, client):
        scheduler.addJob(sched)

    try:
        logger.info('Beginning scheduler loop')
        scheduler.run()
    except KeyboardInterrupt:
        print('Ending')


if __name__ == '__main__':
    main()
