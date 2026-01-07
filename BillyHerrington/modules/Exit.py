import sys
from modules import Command
import config
import constants
import os


def stopBilly():
    if config.os_name == constants.Linux_OS:
        Command.run_command(
            f'systemctl --user stop {config.startup_file_name}')

    if config.os_name == constants.Windows_OS:
        pass

    try:
        sys.exit()
    except:
        os._exit(0)
