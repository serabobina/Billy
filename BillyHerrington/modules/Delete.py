import os
import config
import constants
from modules import File


def delete_autostart():
    if os.path.isfile(config.startup_file_path):
        File.remove_file(config.startup_file_path)


def delete_Billy_Linux():
    File.remove_dir(config.main_dir_path)
    File.remove_file(config.default_target_wants_path)


def create_delete_startup():
    if config.os_name == constants.Windows_OS:
        with open(config.delete_bat_path, 'w') as file:
            file.write(config.delete_bat_file_value)


def delete():
    try:
        if config.os_name == constants.Windows_OS:
            create_delete_startup()
        if config.os_name == constants.Linux_OS:
            delete_Billy_Linux()
        delete_autostart()

        return "Billy will be removed on the next system startup, but you can restart system."
    except Exception as ex:
        return "Error: " + str(ex)
