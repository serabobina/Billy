from pynput.keyboard import Key, Controller, Listener
import random
import time
import constants
import config
import asyncio
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def block_callback(bot, call):
    message = constants.KEYBOARD_BLOCK_documentation.format(
        max_time_to_keyboard=config.max_time_to_keyboard_block)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def spam_callback(bot, call):
    message = constants.KEYBOARD_SPAM_documentation.format(
        max_time_to_keyboard=config.max_time_to_keyboard_spam)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.KEYBOARD_SHORTCUT_command,
    permission_name=constants.KEYBOARD_SHORTCUT,
)
async def keyboardshortcut(bot, message):
    argument = getarg(message.text, constants.KEYBOARD_SHORTCUT_command)

    answer = press_key(argument)

    markup = getMarkupModes()

    await send_message(bot, message.chat.id, text=answer, reply_markup=markup)


@registry.register(
    command_name=constants.KEYBOARD_BLOCK_command,
    permission_name=constants.KEYBOARD_BLOCK,
)
async def keyboardblock(bot, message):
    time_working = getarg(message.text, constants.KEYBOARD_BLOCK_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_keyboard_block:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    time_working = int(time_working)

    await send_message(bot, message.chat.id, text=constants.keyboardblock_blocked_message)

    await block_keyboard(time_working)

    await send_message(bot, message.chat.id, text=constants.keyboardblock_unblocked_message, reply_markup=markup)


@registry.register(
    command_name=constants.KEYBOARD_SPAM_command,
    permission_name=constants.KEYBOARD_SPAM,
)
async def keyboardspam(bot, message):
    time_working = getarg(message.text, constants.KEYBOARD_SPAM_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_keyboard_spam:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    time_working = int(time_working)

    await send_message(bot, message.chat.id, text=constants.keyboardspam_started_message)

    await spam(time_working)

    await send_message(bot, message.chat.id, text=constants.keyboardspam_finished_message, reply_markup=markup)


@registry.register(
    command_name=constants.KEYBOARD_PRINT_command,
    permission_name=constants.KEYBOARD_PRINT,
)
async def keyboardprint(bot, message):
    text = getarg(message.text, constants.KEYBOARD_PRINT_command)

    print_text(text)

    markup = getMarkupModes()

    await send_message(bot, message.chat.id, text=constants.keyboardprint_printed_message, reply_markup=markup)


keyboard = Controller()

spam_list = ['alt', 'alt_gr', 'alt_r', 'backspace', 'caps_lock', 'cmd', 'cmd_r', 'ctrl', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc',
             'home', 'insert', 'left', 'media_next', 'media_play_pause', 'media_previous', 'media_volume_down', 'media_volume_mute', 'media_volume_up', 'menu', 'num_lock', 'page_down', 'page_up', 'pause', 'print_screen', 'right', 'scroll_lock', 'shift', 'shift_r', 'space', 'tab', 'up',
             'n', '9', '5', 'c', '/', '\\', ',', 'u', 'l', "'", 'q', ']', '4', '.', 'p', '2', ';', 'a', '-', 'f', 'i', 'm', '7', '3', 'b', 'd', 'z', 'e', '[', '=', 'h', '1', 't', 'y', 'g', 'o', 's', 'j', 'k', 'v', '6', 'r', '8', '0', 'x', 'w']


class KeyboardBlocker:
    def __init__(self):
        self.listener = None

    def on_press(self, key):
        return None

    def start(self):
        if not self.listener:
            self.listener = Listener(
                on_press=self.on_press, suppress=True)
            self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None


keyboard_blocker_obj = KeyboardBlocker()


def print_text(text):
    keyboard.type(text)


def press_key(keys):
    answer = f'Successfully pressed {keys}.'
    keys = keys.split('+')
    try:
        for key in keys:
            press(key)

        for key in keys:
            release(key)
    except Exception as ex:
        answer = f'Invalid argument {keys}: ' + str(ex)
    return answer


def press(key):
    key_obj = getattr(Key, key, None)

    if key_obj:
        key = key_obj

    keyboard.press(key)


def release(key):
    key_obj = getattr(Key, key, None)

    if key_obj:
        key = key_obj

    keyboard.release(key)


async def block_keyboard(time_working=0):
    keyboard_blocker_obj.start()

    await asyncio.sleep(time_working)

    keyboard_blocker_obj.stop()


def press_random_key():
    count = random.randint(1, 4)
    keys = []
    for i in range(count):
        keys.append(random.choice(spam_list))
    key = '+'.join(keys)

    try:
        press_key(key)
    except Exception as ex:
        pass


async def spam(time_working):
    start_time = time.time()
    while True:
        end_time = time.time()

        if end_time - start_time >= int(time_working):
            break

        press_random_key()

        await asyncio.sleep(0.1)


modes = {constants.KEYBOARD_SHORTCUT_preview: constants.KEYBOARD_SHORTCUT,
         constants.KEYBOARD_BLOCK_preview: constants.KEYBOARD_BLOCK,
         constants.KEYBOARD_SPAM_preview: constants.KEYBOARD_SPAM,
         constants.KEYBOARD_PRINT_preview: constants.KEYBOARD_PRINT}
