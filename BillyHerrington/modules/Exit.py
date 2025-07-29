import sys
from modules import Command
import config
import constants


def stopBilly():
    if config.os_name == constants.Linux_OS:
        Command.run_command(
            f'systemctl --user stop {config.startup_file_name}')
        sys.exit()
    if config.os_name == constants.Windows_OS:
        sys.exit()
