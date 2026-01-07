import requests
import config
import os
from PIL import Image
import ctypes
from modules import File
import constants
from modules import Command
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def changewallpapers_callback(bot, call):
    markup = getMarkupModes()

    message = constants.PHOTO_CHANGEWALLPAPERS_documentation

    flag_error, photo_path = get_wallpaper_path()

    if flag_error:
        await send_message(bot, call.message.chat.id, text=photo_path + message, reply_markup=markup)
        return

    await bot.send_photo(call.message.chat.id, photo=open(photo_path, 'rb'), caption=message, reply_markup=markup)

    delete_tmp_photo()


@registry.register(
    command_name=constants.PHOTO_OPENPHOTO_command,
    permission_name=constants.PHOTO_OPENPHOTO,
)
async def openphoto(bot, message):
    markup = getMarkupModes()

    link = getarg(message.text, constants.PHOTO_OPENPHOTO_command)

    await send_message(bot, message.chat.id, text=open_image(link), reply_markup=markup)


@registry.register(
    command_name=constants.PHOTO_CHANGEWALLPAPERS_command,
    permission_name=constants.PHOTO_CHANGEWALLPAPERS,
)
async def changewallpapers(bot, message):
    markup = getMarkupModes()

    link = getarg(message.text, constants.PHOTO_CHANGEWALLPAPERS_command)

    await send_message(bot, message.chat.id, text=change_wallpaper(link), reply_markup=markup)


SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

default_path_wallpapers = "C:/Windows/Web/Wallpaper/Windows/img19.jpg"


def open_image(image_url):
    try:
        download_image_for_link(image_url, config.tmp_photo_path)

        image = Image.open(config.tmp_photo_path)
        image.show()
        delete_tmp_photo()
    except Exception as ex:
        return str(ex)
    return constants.image_opened_message


def get_wallpaper_path():
    try:
        if config.os_name == constants.Windows_OS:
            wallpaper_path = f"C:/Users/{config.username}/AppData/Roaming/Microsoft/Windows/Themes/TranscodedWallpaper"
        if config.os_name == constants.Linux_OS:
            wallpaper_path = Command.run_command(
                "gsettings get org.gnome.desktop.background picture-uri").replace("file://", '').replace("'", '').strip()
            if wallpaper_path[-4:] == '.xml':
                return (1, 'Preview: Wallpaper path not found. ')

        return (0, wallpaper_path)
    except Exception as ex:
        return (1, str(ex))


def change_wallpaper(image_url):
    if config.os_name == constants.Windows_OS:
        return change_wallpaper_windows(image_url)
    if config.os_name == constants.Linux_OS:
        return change_wallpaper_linux(image_url)


def change_wallpaper_linux(image_url):
    try:
        download_image_for_link(image_url, config.tmp_photo_path)

        wallpaper_path = config.home_path + '.local/share/backgrounds/wallpaper'

        File.create_full_dirs(wallpaper_path)

        File.copy_file(config.tmp_photo_path, wallpaper_path)

        Command.run_command(
            f'gsettings set org.gnome.desktop.background picture-uri "{wallpaper_path}"')

        delete_tmp_photo()
    except Exception as ex:
        return str(ex)
    return constants.wallpaper_changed_message


def change_wallpaper_windows(image_url):
    try:
        download_image_for_link(image_url, config.tmp_photo_path)

        set_wallpaper(config.tmp_photo_path)

        delete_tmp_photo()
    except Exception as ex:
        return str(ex)
    return constants.wallpaper_changed_message


def download_image_for_link(image_url, path):

    img_data = requests.get(image_url).content

    with open(path, 'wb') as file:
        file.write(img_data)


def delete_tmp_photo():
    if os.path.isfile(config.tmp_photo_path):
        os.remove(config.tmp_photo_path)


def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)


def set_default_wallpapers():
    set_wallpaper(default_path_wallpapers)


modes = {constants.PHOTO_OPENPHOTO_preview: constants.PHOTO_OPENPHOTO,
         constants.PHOTO_CHANGEWALLPAPERS_preview: constants.PHOTO_CHANGEWALLPAPERS}
