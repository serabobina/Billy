import config
import os
import shutil
import mimetypes
import time
import constants
import aiohttp
from pathlib import Path
import config
from urllib.parse import urlparse
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def createfile_callback(bot, call):
    message = constants.FILE_CREATEFILE_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def copy_callback(bot, call):
    message = constants.FILE_COPY_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def upload_callback(bot, call):
    message = constants.FILE_UPLOAD_documentation

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def download_callback(bot, call):
    message = constants.FILE_DOWNLOAD_documentation.format(
        special_separator=config.special_separator)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.FILE_GETINF_command,
    permission_name=constants.FILE_GETINF,
)
async def getinffile(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_GETINF_command)

    await send_message(bot, message.chat.id, text=getinf(path), reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.FILE_REMOVE_command,
    permission_name=constants.FILE_REMOVE,
)
async def remove(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_REMOVE_command)

    await send_message(bot, message.chat.id, text=remove(path), reply_markup=markup, parse_mode='HTML')


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

    await send_message(bot, message.chat.id, text=create_file(path, value), reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.FILE_CREATEDIR_command,
    permission_name=constants.FILE_CREATEDIR,
)
async def createdir(bot, message):
    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_CREATEDIR_command)

    await send_message(bot, message.chat.id, text=create_dir(path), reply_markup=markup, parse_mode='HTML')


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

    await send_message(bot, message.chat.id, text=copy_file(paths[0], paths[1]), reply_markup=markup, parse_mode='HTML')


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
    markup = getMarkupModes()

    args = list(map(str.strip, getarg(
        message.text, constants.FILE_DOWNLOAD_command).split(config.special_separator)))

    if not len(args) == 2:
        raise Exception(constants.INVALID_ARGUMENT)

    file_url, path = args

    if not check_path_protected(path):
        raise Exception(constants.file_or_directory_is_protected)

    download_from_url(bot, message, file_url, path, markup)


async def download_from_url(bot, message, url, save_path, markup):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    status_msg = await send_message(bot, message.chat.id, constants.downloading_starting_message.format(url=url[:50]))

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                filename = get_filename_from_url(url, response)

                if os.path.isdir(save_path) or save_path.endswith('/') or save_path.endswith('\\'):
                    save_path = os.path.join(save_path, filename)

                content_length = response.headers.get('Content-Length')
                total_size = int(
                    content_length) if content_length else None

                downloaded = 0
                chunk_size = 8192

                with open(save_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size and downloaded % (1024 * 1024) < chunk_size:
                            progress = (downloaded / total_size) * 100
                            await bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=status_msg.message_id,
                                text=constants.downloading_progress_message.format(
                                    progress=progress,
                                    downloaded=downloaded//1024,
                                    total_size=total_size//1024
                                )
                            )

                file_size = os.path.getsize(save_path)

                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_msg.message_id,
                    text=constants.file_saved_message.format(
                        save_path=save_path,
                        file_size=file_size//1024,
                    )
                )
            else:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_msg.message_id,
                    text=constants.downloading_error_mesage.format(
                        status=response.status,
                    )
                )


def get_filename_from_url(url, response=None):
    if response:
        content_disp = response.headers.get('Content-Disposition')
        if content_disp:
            import re
            match = re.search(r'filename="?([^"]+)"?', content_disp)
            if match:
                return match.group(1)

    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    if not '.' in filename and response:
        content_type = response.headers.get('Content-Type')
        if content_type:
            ext = mimetypes.guess_extension(content_type.split(';')[0])
            if ext:
                filename += ext

    if not filename or filename == '/':
        filename = f"downloaded_file_{int(time.time())}.bin"

    return filename


def delete_tmp_file(tmp_file_path):
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

    return constants.file_information_message.format(file_mtime=file_mtime, file_size=file_size)


def remove(path):
    if not os.path.exists(path):
        return constants.file_or_dir_is_not_exist

    if os.path.isfile(path):
        answer = remove_file(path)

    if os.path.isdir(path):
        answer = remove_dir(path)
    return answer


def remove_file(file_path):
    os.remove(file_path)

    return constants.file_removed_message.format(file_path=file_path)


def remove_dir(dir_path):
    shutil.rmtree(dir_path, ignore_errors=1)

    return constants.directory_removed_message.format(dir_path=dir_path)


def create_file(file_path, value=''):
    with open(file_path, 'w') as file:
        file.write(value)
    return constants.file_created_message.format(file_path=file_path)


def copy_file(file_path1, file_path2):
    if not os.path.isfile(file_path1):
        return constants.invalid_file_path

    shutil.copy2(file_path1, file_path2)
    return constants.file_copied_message.format(file_path1=file_path1, file_path2=file_path2)


def create_dir(dir_path):
    os.mkdir(dir_path)

    return constants.directory_created_message.format(dir_path=dir_path)


def create_full_dirs(dir_path):
    os.makedirs(dir_path, exist_ok=True)


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
