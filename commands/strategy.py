from nubia import command, argument

from termcolor import cprint

from tasks import running_strategy
from tasks.stratege import create_and_run, pause, run, delete

@command('trade')
class Stratege:

    'run/manage strateges'

    @command
    def list(self):
        'list all strateges'
        lines = ''
        for info in running_strategy.values():
            lines = lines + ('%s\t%s\t\t%s\t%s\t%s\n' % (info['sid'], info['status'], info['start_date'], info['path'], info['broker']))
        if lines:
            cprint('sid\tstatus\t\tstart_date\tpath\t\t\t\tbroker\n' + lines, 'green')

    @command
    @argument('path', type=str, positional=True, description='path of you stratege file')
    @argument('broker', type=str, description='broker')
    def new(self, path, broker=None):
        'run a stratege form file'
        try:
            create_and_run(path, broker)
        except Exception as e:
            cprint(str(e), 'yellow')

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    def pause(self, sid):
        'pause a running stratege'
        try:
            pause(sid)
        except Exception as e:
            cprint(str(e), 'yellow')

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    @argument('init', type=bool, description='whether call init()')
    def resume(self, sid, init=False):
        'resume a paused stratege'
        try:
            run(sid, init, True)
        except Exception as e:
            cprint(str(e), 'yellow')

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    @argument('init', type=bool, description='whether call init()')
    @argument('resume', type=bool, description='whether run as resume')
    def restart(self, sid, init=False, resume=True):
        'restart a running stratege'
        try:
            pause(sid)
            run(sid, init, resume)
        except Exception as e:
            cprint(str(e), 'yellow')

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    def delete(self, sid):
        'delete a stratege, if it\'s running, pause it'
        try:
            delete(sid)
        except Exception as e:
            cprint(str(e), 'yellow')
