from multiprocessing import Process
import threading

import time

import rqalpha
import schedule as scheduler

from . import running_strategy
from .stratege import run_today, start_trading

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

def update_bundle(join=False):
    def wapper():
        rqalpha.update_bundle()
    p = Process(target=wapper)
    p.start()
    if join:
        p.join()
