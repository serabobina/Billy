from pynput.mouse import Button, Controller
import time
import random
import constants
from modules import Screen
import config
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def leftclick_callback(bot, call):

    markup = getMarkupModes()

    left_click()

    await send_message(bot, call.message.chat.id, text=constants.mouse_clicked_message, reply_markup=markup)


async def rightclick_callback(bot, call):
    markup = getMarkupModes()

    right_click()

    await send_message(bot, call.message.chat.id, text=constants.mouse_clicked_message, reply_markup=markup)


async def doubleclick_callback(bot, call):
    markup = getMarkupModes()

    double_click()

    await send_message(bot, call.message.chat.id, text=constants.mouse_clicked_message, reply_markup=markup)


async def pressmouse_callback(bot, call):
    markup = getMarkupModes()

    press()

    await send_message(bot, call.message.chat.id, text=constants.mousepress_pressed_message, reply_markup=markup)


async def unpressmouse_callback(bot, call):
    markup = getMarkupModes()

    unpress()

    await send_message(bot, call.message.chat.id, text=constants.mouseunpress_unpressed_message, reply_markup=markup)


async def getposition_callback(bot, call):
    markup = getMarkupModes()

    x, y = get_position()

    await send_message(bot, call.message.chat.id, text=f"<code>{x} {y}</code>", reply_markup=markup, parse_mode='HTML')


async def blockmouse_callback(bot, call):
    message = constants.MOUSE_BLOCK_documentation.format(
        max_time_to_mouse=config.max_time_to_mouse_block)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def spammouse_callback(bot, call):
    message = constants.MOUSE_SPAM_documentation.format(
        max_time_to_mouse=config.max_time_to_mouse_spam)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.MOUSE_MOVE_command,
    permission_name=constants.MOUSE_MOVE,
)
async def movemouse(bot, message):

    markup = getMarkupModes()

    coordinates = getarg(message.text, constants.MOUSE_MOVE_command).split()

    if len(coordinates) != 2 or not (coordinates[0].isdigit() and coordinates[1].isdigit()):
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    move(int(coordinates[0]), int(coordinates[1]))

    await send_message(bot, message.chat.id, text=constants.movemouse_moved_message, reply_markup=markup)


@registry.register(
    command_name=constants.MOUSE_SCROLL_command,
    permission_name=constants.MOUSE_SCROLL,
)
async def scrollmouse(bot, message):
    markup = getMarkupModes()

    scroll_key = getarg(message.text, constants.MOUSE_SCROLL_command)

    if not (scroll_key.isdigit() or (len(scroll_key) >= 2 and scroll_key[0] == '-' and scroll_key[1:].isdigit())):
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    scroll(int(scroll_key))

    await send_message(bot, message.chat.id, text=constants.scrollmouse_scrolled_message, reply_markup=markup)


@registry.register(
    command_name=constants.MOUSE_BLOCK_command,
    permission_name=constants.MOUSE_BLOCK,
)
async def blockmouse(bot, message):
    time_working = getarg(message.text, constants.MOUSE_BLOCK_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_mouse_block:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(bot, message.chat.id, text=constants.blockmouse_blocked_message)

    block_mouse(time_working)

    await send_message(bot, message.chat.id, text=constants.blockmouse_unblocked_message, reply_markup=markup)


@registry.register(
    command_name=constants.MOUSE_SPAM_command,
    permission_name=constants.MOUSE_SPAM,
)
async def mousespam(bot, message):
    time_working = getarg(message.text, constants.MOUSE_SPAM_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_mouse_spam:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(bot, message.chat.id, text=constants.mousespam_started_message)

    spam_mouse(time_working)

    await send_message(bot, message.chat.id, text=constants.mousespam_finished_message, reply_markup=markup)


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
