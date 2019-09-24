from multiprocessing import Process
import threading

import time

import rqalpha
import schedule as scheduler

from . import running_strategy
from .stratege import run_today

def run_scheduled_tasks():
    scheduler.every().day.at('20:00').do(update_bundle)
    scheduler.every().day.at('09:00').do(start_trading)
    def wapper():
        while True:
            scheduler.run_pending()
            time.sleep(1)
    t = threading.Thread(target=wapper)
    t.setDaemon(True)
    t.start()

def update_bundle():
    def wapper():
        rqalpha.update_bundle()
    t = threading.Thread(target=wapper)
    t.setDaemon(True)
    t.start()

def start_trading():
    for sid in running_strategy.keys():
        run_today(sid)
