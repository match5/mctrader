import gevent
import schedule as scheduler
import time

import rqalpha

from . import running_strategy
from .stratege import run_today

def run_scheduled_tasks():
    scheduler.every().day.at('16:00').do(update_bundle)
    scheduler.every().day.at('09:00').do(start_trading)
    def wapper():
        while True:
            scheduler.run_pending()
            time.sleep(1)
    gevent.spawn(wapper)

def update_bundle():
    gevent.spawn(lambda: rqalpha.update_bundle())

def start_trading():
    for sid in running_strategy.keys():
        gevent.spawn(lambda: run_today(sid))
