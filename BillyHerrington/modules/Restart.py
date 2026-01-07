from modules import Command
import config
import constants
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def restart_callback(bot, call):
    markup = getMarkupModes()

    restart()

    await send_message(bot, call.message.chat.id, text=constants.system_restarted_message, reply_markup=markup)


def restart():
    if config.os_name == constants.Linux_OS:
        shutdown_command = "systemctl reboot"
    if config.os_name == constants.Windows_OS:
        shutdown_command = "shutdown /r /t 0"
    Command.run_command(shutdown_command)
