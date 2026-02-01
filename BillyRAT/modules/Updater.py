import config
import os
from modules import NetworkDrive
import shutil
from modules import Command
import constants


def rename_main_dir():
    if os.path.isdir(config.old_dir_name):
        shutil.rmtree(config.old_dir_name)

    os.rename(config.main_dir_path, config.old_dir_name)


def create_main_dir():
    os.mkdir(config.main_dir_path)


def install_new_billy():
    NetworkDrive.download(config.Billy_path, config.main_file_path)


def restore():
    if os.path.isdir(config.old_dir_name):
        if os.path.exists(config.main_dir_path):
            shutil.rmtree(config.main_dir_path)
        os.rename(config.old_dir_name, config.main_dir_path)


def make_script_executable(path):
    return Command.run_command(f"chmod +x {path}")


def check_update():
    if not os.path.isdir(config.main_dir_path):
        return 0
    if not os.path.isfile(config.main_file_path):
        return 0
    return 1


def update():
    is_update_successfully = True
    answer = "Update completed successfully. Restart system to start new Billy."

    try:
        rename_main_dir()

        create_main_dir()

        install_new_billy()

        if config.os_name == constants.Linux_OS:
            make_script_executable(config.main_file_path)
    except Exception as ex:
        answer = "An error occurred during the update: " + \
            str(ex) + "\nOld Billy restored"
        is_update_successfully = False

    else:
        if not check_update():
            answer = "An error occurred during the update: Billy not installed. \nOld Billy restored"
            is_update_successfully = False

    if not is_update_successfully:
        restore()

    return answer
