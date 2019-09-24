from multiprocessing import Process

import os
import datetime
from termcolor import cprint

import rqalpha

from . import running_strategy, running_process, strategy_lock

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
        'inited': False,
    }
    running_strategy[str(sid)] = info
    if 9 < datetime.datetime.now().hour < 15:
        run_today(sid)

def kill_running(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    proc = running_process.get(sid, None)
    if proc and proc.is_alive():
        proc.terminate()
        del running_process[sid]
    del running_strategy[sid]


def run_today(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    proc = running_process.get(sid, None)
    if proc and proc.is_alive():
        raise Exception('sid:%s is running' % (sid,))
    date = datetime.date.today().strftime("%Y-%m-%d")
    log_file = os.path.join('logs', '%s_%s.log' % (sid, info['start_date'].replace('-', '')))
    persist_dir = os.path.join('data', '%s_%s' % (sid, info['start_date'].replace('-', '')))
    cprint('starting {} {}'.format(sid, info['path']), 'yellow')
    config = {
        'base': {
            'start_date': date,
            'end_date': date,
            'persist': True,
            'persist_mode': 'real_time',
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
                'sid': sid,
                'should_resume': True,
                'should_run_init': not info['inited'],
                'log_file': log_file,
                'persist_dir': persist_dir,
            },
        },
    }
    def wapper():
        rqalpha.run_file(info['path'], config)
    proc = Process(target=wapper)
    proc.daemon = True
    running_process[sid] = proc
    proc.start()
    info['inited'] = True
