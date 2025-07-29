import config
import os
import constants
from PIL import ImageGrab
import pyautogui


def screen():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(config.tmp_screen_path)
        return (0, config.tmp_screen_path)
    except Exception as ex:
        return (1, 'Error: ' + str(ex))


def delete_tmp_file():
    if os.path.isfile(config.tmp_screen_path):
        os.remove(config.tmp_screen_path)


def get_size():
    screen_width, screen_height = pyautogui.size()
    return (screen_width, screen_height)


modes = {constants.SCREEN_GETSIZE_preview: constants.SCREEN_GETSIZE,
         constants.SCREEN_SCREEN_preview: constants.SCREEN_SCREEN}
