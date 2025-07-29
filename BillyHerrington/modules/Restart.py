from modules import Command
import config
import constants


def restart():
    if config.os_name == constants.Linux_OS:
        shutdown_command = "systemctl reboot"
    if config.os_name == constants.Windows_OS:
        shutdown_command = "shutdown /r /t 0"
    Command.run_command(shutdown_command)
