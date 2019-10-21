import sys
from nubia import Nubia, Options

from tasks.scheduled import run_scheduled_tasks
from tasks.stratege import load, save

import commands

if __name__ == "__main__":
    shell = Nubia(
        name="mctrader",
        command_pkgs=commands,
    )
    load()
    run_scheduled_tasks()
    st = shell.run()
    save()
    sys.exit(st)