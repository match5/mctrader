from nubia import command, argument
import typing

from termcolor import cprint

from tasks import running_strategy
from tasks.stratege import create_running, kill_running

@command('stratege')
class Stratege:

    'run/manage strateges'

    @command
    def list(self):
        'list all strateges'
        lines = ''
        for info in running_strategy.values():
            lines = lines + ('\t%s\t%s\t%s\t\t%s\n' % (info['sid'], info['start_date'], info['name'], info['path']))
        if lines:
            cprint('\tsid\tstart_date\tname\t\tpath\n' + lines, 'green')

    @command
    @argument('path', type=str, positional=True, description='path of you stratege file')
    @argument('name', type=str, description='name of the stratege')
    def run(self, path, name='unnamed'):
        'run a stratege form file'
        create_running(path, name)

    @command
    @argument('sid', type=str, positional=True, description='id of stratege')
    def kill(self, sid):
        'kill a stratege'
        kill_running(sid)
