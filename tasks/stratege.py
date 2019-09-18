import gevent
from . import running_strategy, running_threads
import rqalpha
import datetime

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
    def wapper():
        info = running_strategy.get(sid, None)
        if info is None:
            raise Exception('sid:%s not exists' % (sid,))
        th = running_threads.get(sid, None)
        if th and th.ready():
            th.kill()
            del running_threads[sid]
        del running_strategy[sid]
    gevent.spawn(wapper)


def run_today(sid):
    info = running_strategy.get(sid, None)
    if info is None:
        raise Exception('sid:%s not exists' % (sid,))
    th = running_threads.get(sid, None)
    if th and not th.ready():
        raise Exception('sid:%s is running' % (sid,))
    date = datetime.date.today().strftime("%Y-%m-%d")
    config = {
        'base': {
            'start_date': date,
            'end_date': date,
        },
        'mod': {
            'sys_simulation': {
                'enabled': False,
            },
            'mctrader': {
                'enabled': True,
                'log_file': os.path.join(LOG_DIR, '%s.log' % (date.replace('-', ''))),
            },
        },
    }

    th = gevent.spawn(lambda: rqalpha.run_file(info['path'], config))
    running_threads[sid] = th
