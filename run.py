from gevent import monkey
monkey.patch_all()

import sys
from nubia import Nubia, Options

from tasks.scheduled import run_scheduled_tasks

import commands

if __name__ == "__main__":
    run_scheduled_tasks()
    shell = Nubia(
        name="mctrader",
        command_pkgs=commands,
    )
    sys.exit(shell.run())