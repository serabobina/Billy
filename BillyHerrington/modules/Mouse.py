from pynput.mouse import Button, Controller
import time
import random
import constants
from modules import Screen

mouse = Controller()


def move(x, y):
    mouse.position = (x, y)


def right_click():
    mouse.click(Button.right)


def left_click():
    mouse.click(Button.left)


def double_click():
    mouse.click(Button.left, 2)


def press():
    mouse.press(Button.left)


def unpress():
    mouse.release(Button.left)


def get_position():
    return mouse.position


def scroll(key):
    mouse.scroll(0, key)


def block_mouse(time_working):
    start_time = time.time()
    x, y = get_position()

    while True:
        end_time = time.time()

        if end_time - start_time >= int(time_working):
            break

        move(x, y)


def spam_mouse(time_working):
    display = Screen.get_size()
    start_time = time.time()

    while True:
        x, y = random.randint(0, display[0]), random.randint(0, display[1])

        end_time = time.time()

        if end_time - start_time >= int(time_working):
            break

        move(x, y)

        functions = [left_click, right_click, double_click,
                     lambda: scroll(random.randint(1, 100))]
        function = random.choice(functions)
        function()


modes = {constants.MOUSE_MOVE_preview: constants.MOUSE_MOVE, constants.MOUSE_LEFTCLICK_preview: constants.MOUSE_LEFTCLICK,
         constants.MOUSE_RIGHTCLICK_preview: constants.MOUSE_RIGHTCLICK, constants.MOUSE_DOUBLECLICK_preview: constants.MOUSE_DOUBLECLICK,
         constants.MOUSE_PRESS_preview: constants.MOUSE_PRESS, constants.MOUSE_UNPRESS_preview: constants.MOUSE_UNPRESS,
         constants.MOUSE_GETPOSITION_preview: constants.MOUSE_GETPOSITION, constants.MOUSE_SCROLL_preview: constants.MOUSE_SCROLL,
         constants.MOUSE_BLOCK_preview: constants.MOUSE_BLOCK, constants.MOUSE_SPAM_preview: constants.MOUSE_SPAM}
