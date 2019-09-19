import gevent
from multiprocessing import Process

import os
import datetime

import rqalpha

from . import running_strategy, running_process

next_sid = 1001

def create_running(path, name='unnamed'):
    global next_sid
    sid = str(next_sid)
    next_sid = next_sid + 1
    info = {
        'sid': sid,
        'name': name,
        'path': path,
        'start_date': datetime.date.today().strftime("%Y-%m-%d"),
    }
    running_strategy[str(sid)] = info
    if 9 < datetime.datetime.now().hour < 15:
        run_today(sid)

def kill_running(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    pro = running_process.get(sid, None)
    if pro and pro.is_alive():
        pro.terminate()
        del running_process[sid]
    del running_strategy[sid]


def run_today(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    pro = running_process.get(sid, None)
    if pro and pro.is_alive():
        raise Exception('sid:%s is running' % (sid,))
    date = datetime.date.today().strftime("%Y-%m-%d")
    log_file = os.path.join('logs', '%s_%s.log' % (sid, info['start_date'].replace('-', '')))
    config = {
        'base': {
            'start_date': date,
            'end_date': date,
        },
        'mod': {
            'sys_simulation': {
                'enabled': False,
            },
            'sys_benchmark': {
                'enabled': False,
            },
            'mctrader': {
                'enabled': True,
                'log_file': log_file,
            },
        },
    }
    pro = Process(target=lambda: rqalpha.run_file(info['path'], config))
    pro.daemon = True
    running_process[sid] = pro
    pro.start()
