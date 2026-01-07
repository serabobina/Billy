import config
import os
import shutil
from modules import NetworkDrive
import time
import constants
from pathlib import Path
import config
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_default_message, send_message


async def createfile_callback(bot, call):
    message = constants.FILE_CREATEFILE_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def copy_callback(bot, call):
    message = constants.FILE_COPY_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def upload_callback(bot, call):
    message = constants.FILE_UPLOAD_documentation.format()

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def download_callback(bot, call):
    message = constants.FILE_DOWNLOAD_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


@registry.register(
    command_name=constants.FILE_GETINF_command,
    permission_name=constants.FILE_GETINF,
)
async def getinffile(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_GETINF_command)

    await send_message(bot, message.chat.id, text=getinf(path), reply_markup=markup)


@registry.register(
    command_name=constants.FILE_REMOVE_command,
    permission_name=constants.FILE_REMOVE,
)
async def remove(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_REMOVE_command)

    await send_message(bot, message.chat.id, text=remove(path), reply_markup=markup)


@registry.register(
    command_name=constants.FILE_CREATEFILE_command,
    permission_name=constants.FILE_CREATEFILE,
)
async def createfile(bot, message):
    markup = getMarkupModes()

    args = list(map(str.strip, getarg(
        message.text, constants.FILE_CREATEFILE_command).split(config.special_separator)))
    value = ''

    if len(args) == 1:
        path = args

    elif len(args) == 2:
        path, value = args
    else:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(bot, message.chat.id, text=create_file(path, value), reply_markup=markup)


@registry.register(
    command_name=constants.FILE_CREATEDIR_command,
    permission_name=constants.FILE_CREATEDIR,
)
async def createdir(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_CREATEDIR_command)

    await send_message(bot, message.chat.id, text=create_dir(path), reply_markup=markup)


@registry.register(
    command_name=constants.FILE_COPY_command,
    permission_name=constants.FILE_COPY,
)
async def copyfile(bot, message):
    markup = getMarkupModes()

    paths = list(map(str.strip, getarg(
        message.text, constants.FILE_COPY_command).split(config.special_separator)))

    if not len(paths) == 2:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(bot, message.chat.id, text=copy_file(paths[0], paths[1]), reply_markup=markup)


@registry.register(
    command_name=constants.FILE_UPLOAD_command,
    permission_name=constants.FILE_UPLOAD,
)
async def upload(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_UPLOAD_command)

    if not os.path.isfile(path):
        raise Exception(constants.file_or_dir_is_not_exist)

    file_size_bytes = os.path.getsize(path)

    if not file_size_bytes < config.max_file_upload_size:
        raise Exception(constants.file_size_is_too_large.format(
            size_limit=config.max_file_upload_size//1048576))

    await bot.send_document(message.chat.id, reply_markup=markup)


@registry.register(
    command_name=constants.FILE_DOWNLOAD_command,
    permission_name=constants.FILE_DOWNLOAD,
)
async def download(bot, message):
    print(1)
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_UPLOAD_command)

    if not message.document and not message.photo and not message.video and not message.audio:
        raise Exception(constants.file_is_not_attached)

    if not path:
        raise Exception(constants.INVALID_ARGUMENT)

    if not check_path_protected(path):
        raise Exception(constants.file_or_directory_is_protected)

    try:
        create_file(path, value='TEMP')
    except:
        raise Exception(constants.invalid_file_path)

    save_path = Path(path)

    file_info = None
    file_name = save_path.name

    if message.document:
        file_info = await bot.get_file(message.document.file_id)
    elif message.photo:
        file_info = await bot.get_file(message.photo[-1].file_id)
        if not save_path.suffix:
            save_path = save_path.with_suffix('.jpg')
    elif message.video:
        file_info = await bot.get_file(message.video.file_id)
        if not save_path.suffix:
            save_path = save_path.with_suffix('.mp4')
    elif message.audio:
        file_info = await bot.get_file(message.audio.file_id)
        if not save_path.suffix:
            save_path = save_path.with_suffix('.mp3')

    if not file_info:
        raise Exception(constants.invalid_file)

    status_msg = await message.reply(constants.downloading_file)

    downloaded_file = await bot.download_file(file_info.file_path)

    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    file_size = os.path.getsize(save_path)

    await status_msg.edit_text(constants.file_downloaded.format(save_path=save_path, file_size=file_size / 1024))


def delete_tmp_file(tmp_file_path):
    """Delete temporary video file if it exists."""
    if os.path.isfile(tmp_file_path):
        os.remove(tmp_file_path)


def get_random_temp_file_name(sample='{file_name}.tmp'):
    import random

    alth = ''.join([chr(i) for i in range(48, 58)] + [chr(i)
                                                      for i in range(65, 91)] + [chr(i) for i in range(97, 123)])

    random_string_length = 30

    random_string = ''.join(random.choice(alth)
                            for _ in range(random_string_length))

    return os.path.join(config.tmp_dir_path, sample.format(file_name=random_string))


def getinf(file_path):
    if not os.path.exists(file_path):
        return constants.file_or_dir_is_not_exist

    file_size = os.path.getsize(file_path)

    file_mtime = time.ctime(os.path.getctime(file_path))

    return f'Size: {file_size} байт\nDate of change: {file_mtime}.'


def remove(path):
    if not os.path.exists(path):
        return constants.file_or_dir_is_not_exist

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


def check_path_protected(path):
    protected_paths = [config.main_dir_path,
                       config.startup_dir_path, config.old_dir_name]
    path = Path(path)

    for protected_path in protected_paths:
        if str(Path(protected_path)) in str(path):
            return 0

    return 1


modes = {constants.FILE_GETINF_preview: constants.FILE_GETINF, constants.FILE_CREATEFILE_preview: constants.FILE_CREATEFILE,
         constants.FILE_CREATEDIR_preview: constants.FILE_CREATEDIR, constants.FILE_COPY_preview: constants.FILE_COPY,
         constants.FILE_REMOVE_preview: constants.FILE_REMOVE, constants.FILE_UPLOAD_preview: constants.FILE_UPLOAD,
         constants.FILE_DOWNLOAD_preview: constants.FILE_DOWNLOAD}
