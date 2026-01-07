import config
import constants
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_default_message, send_message


async def getversion_callback(bot, call):
    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=getVersion(), reply_markup=markup)


async def author_callback(bot, call):
    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=getAuthor(), reply_markup=markup)


def getVersion():
    return config.version


def getAuthor():
    return "Created by Serabobina."


modes = {constants.ABOUT_GETVERSION_preview: constants.ABOUT_GETVERSION,
         constants.ABOUT_AUTHOR_preview: constants.ABOUT_AUTHOR}
