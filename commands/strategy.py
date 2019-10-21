from nubia import command, argument

from termcolor import cprint

from tasks import running_strategy
from tasks.stratege import create_and_run, pause, resume, delete

@command('trade')
class Stratege:

    'run/manage strateges'

    @command
    def list(self):
        'list all strateges'
        lines = ''
        for info in running_strategy.values():
            lines = lines + ('\t%s\t%s\t%s\t\t%s\t%s\n' % (info['sid'], info['status'], info['name'], info['start_date'], info['path']))
        if lines:
            cprint('\tsid\tstatus\tname\t\tstart_date\tpath\n' + lines, 'green')

    @command
    @argument('path', type=str, positional=True, description='path of you stratege file')
    @argument('account', type=int, description='starting account')
    @argument('name', type=str, description='name of the stratege')
    def new(self, path, account=100000, name='unnamed'):
        'run a stratege form file'
        try:
            create_and_run(path, account, name)
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
            resume(sid, init)
        except Exception as e:
            cprint(str(e), 'yellow')

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    def restart(self, sid):
        'restart a running stratege'
        try:
            pause(sid)
            resume(sid, True)
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
