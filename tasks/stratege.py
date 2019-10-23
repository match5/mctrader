from multiprocessing import Process

import os
import shutil
import datetime
import json
from termcolor import cprint

import rqalpha

from . import running_strategy, running_process

next_sid = 101

def create_and_run(path, account, name):
    global next_sid
    sid = str(next_sid)
    next_sid = next_sid + 1
    info = {
        'sid': sid,
        'name': name,
        'path': path,
        'start_date': datetime.date.today().strftime("%Y-%m-%d"),
        'inited': False,
        'account': account,
        'status': 'running',
    }
    running_strategy[str(sid)] = info
    if 9 <= datetime.datetime.now().hour < 15:
        run_today(sid, True, False)

def pause(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    if info['status'] != 'running':
        raise Exception('sid:%s is not running' % (sid,))
    info['status'] = 'paused'
    proc = running_process.get(sid, None)
    if proc and proc.is_alive():
        proc.terminate()
        del running_process[sid]

def resume(sid, init):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    if info['status'] == 'running':
        raise Exception('sid:%s is running' % (sid,))
    info['status'] = 'running'
    if 9 <= datetime.datetime.now().hour < 15:
        run_today(sid, init or not info['inited'], True)

def delete(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    if info['status'] == 'running':
        raise Exception('sid:%s is running' % (sid,))
    shutil.rmtree(
        os.path.join('data', '%s_%s' % (sid, info['start_date'].replace('-', ''))),
        ignore_errors=True,
    )
    del running_strategy[sid]

def run_today(sid, init, resume):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    proc = running_process.get(sid, None)
    if proc and proc.is_alive():
        raise Exception('sid:%s is running' % (sid,))
    date = datetime.date.today().strftime("%Y-%m-%d")
    log_file = os.path.join('logs', '%s_%s_%s.log' % (sid, info['start_date'].replace('-', ''), datetime.date.today().strftime("%Y%m%d")))
    persist_dir = os.path.join('data', '%s_%s' % (sid, info['start_date'].replace('-', '')))
    cprint('starting {} {}'.format(sid, info['path']), 'green')
    config = {
        'base': {
            'start_date': date,
            'end_date': date,
            'persist': True,
            'persist_mode': 'real_time',
            'accounts': {
                'stock': info['account'],
            }
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
                'should_resume': resume,
                'should_run_init': init,
                'log_file': log_file,
                'persist_dir': persist_dir,
            },
        },
        'extra': {
            'context_vars': {
                'sid': sid,
            }
        }
    }
    def wapper():
        rqalpha.run_file(info['path'], config)
    proc = Process(target=wapper)
    proc.daemon = True
    running_process[sid] = proc
    proc.start()
    info['inited'] = True

def load():
    path = os.path.join('data', 'strateges.dat')
    if os.path.exists(path):
        with open(path, 'r') as fp:
            running_strategy.update(json.load(fp))
    global next_sid
    max_sid = max([int(sid) for sid in running_strategy.keys()] + [0])
    next_sid = max_sid + 1 if next_sid <= max_sid else next_sid
    if 9 <= datetime.datetime.now().hour < 15:
        start_trading()

def save():
    path = os.path.join('data', 'strateges.dat')
    with open(path, 'w') as fp:
        json.dump(running_strategy, fp)

def start_trading():
    for info in running_strategy.values():
        if info.get('status', 'running') == 'running':
            run_today(info['sid'], not info['inited'], info['inited'])
    