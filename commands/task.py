from nubia import command, argument

from termcolor import cprint

from tasks.scheduled import update_bundle


@command('task')
class Task:

    'run tasks'

    @command
    def update_bundle(self):
        'update rqalpha bundle data'
        update_bundle(True)
        