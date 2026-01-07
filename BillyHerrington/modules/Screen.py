import constants
from PIL import ImageGrab, Image
from modules import File
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def getsize_callback(bot, call):
    markup = getMarkupModes()

    width, height = get_size()

    await send_message(bot, call.message.chat.id, text=f"{width} {height}", reply_markup=markup)


async def screen_callback(bot, call):
    markup = getMarkupModes()

    screen_path = screen()

    await bot.send_photo(call.message.chat.id, open(screen_path, 'rb'), reply_markup=markup)

    File.delete_tmp_file(screen_path)


def screen():
    screenshot = ImageGrab.grab()

    tmp_screen_path = File.get_random_temp_file_name(
        sample='{file_name}.png')
    screenshot.save(tmp_screen_path)
    return tmp_screen_path


def get_size():
    screen_path = screen()

    img = Image.open(screen_path)

    width, height = img.size

    File.delete_tmp_file(screen_path)

    return (width, height)


modes = {constants.SCREEN_GETSIZE_preview: constants.SCREEN_GETSIZE,
         constants.SCREEN_SCREEN_preview: constants.SCREEN_SCREEN}
