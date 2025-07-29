import config
import os
import shutil
from modules import NetworkDrive
import time
import constants


def getinf(file_path):
    if not os.path.exists(file_path):
        return "File or dir is not exist."

    file_size = os.path.getsize(file_path)

    file_mtime = time.ctime(os.path.getctime(file_path))

    return f'Size: {file_size} байт\nDate of change: {file_mtime}.'


def remove(path):
    if not os.path.exists(path):
        return "File or dir is not exist."

    if os.path.isfile(path):
        answer = remove_file(path)

    if os.path.isdir(path):
        answer = remove_dir(path)
    return answer


def remove_file(file_path):
    try:
        os.remove(file_path)
    except Exception as ex:
        return str(ex)
    else:
        return "File removed."


def remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path, ignore_errors=1)
    except Exception as ex:
        return str(ex)
    else:
        return "Directory removed."


def create_file(file_path, value=''):
    with open(file_path, 'w') as file:
        file.write(value)
    return "File created."


def copy_file(file_path1, file_path2):
    if not os.path.isfile(file_path1):
        return "File is not exist."

    shutil.copy2(file_path1, file_path2)
    return "File copied."


def upload(file_path, network_name):
    if not os.path.isfile(file_path):
        return "File is not exist."

    NetworkDrive.upload(file_path, config.uploads_path + network_name)

    return "File uploaded."


def download(network_name, file_path):
    if not NetworkDrive.check_if_file_exist(config.downloads_path + network_name):
        return "File is not exist."

    NetworkDrive.download(config.downloads_path + network_name, file_path)

    return "File downloaded."


def create_dir(dir_path):
    try:
        os.mkdir(dir_path)
    except Exception as ex:
        return str(ex)
    else:
        return "Directory created"


def create_full_dirs(dir_path):
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as ex:
        return str(ex)
    else:
        return "Directory created"


modes = {constants.FILE_GETINF_preview: constants.FILE_GETINF, constants.FILE_CREATEFILE_preview: constants.FILE_CREATEFILE,
         constants.FILE_CREATEDIR_preview: constants.FILE_CREATEDIR, constants.FILE_COPY_preview: constants.FILE_COPY,
         constants.FILE_REMOVE_preview: constants.FILE_REMOVE, constants.FILE_UPLOAD_preview: constants.FILE_UPLOAD,
         constants.FILE_DOWNLOAD_preview: constants.FILE_DOWNLOAD}
