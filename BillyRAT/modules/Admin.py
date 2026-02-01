from modules import Updater
from modules import Delete
from modules import Permissions
from modules import Exit
from modules import Log
import constants
import config
from command_registry import registry
from callback_system import callback_system
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


global permission_changeable
permission_changeable = ()


async def registerpermission_callback(bot, call):
    permission = constants.ADMIN_MANAGEPERMISSIONS

    if not Permissions.check(call, permission):
        await send_message(bot, call.message.chat.id, text=constants.you_have_not_this_permission)
        return

    callback = call.data.split('_')[0]

    action = callback.split(':')[1]
    mode = callback.split(':')[2]

    if len(permission_changeable) != 2:
        await send_message(bot, call.message.chat.id, text=constants.managepermissions_iderror_message)
        return

    if action == "allow":
        permission_changeable[1]["allowed"].append(mode)

    if action == "forbid":
        permission_changeable[1]["forbidden"].append(mode)


async def managepermissions_callback(bot, call):
    message = constants.ADMIN_MANAGEPERMISSIONS_documentation

    permissions = Permissions.get()
    for id, data in permissions.items():
        id_message = constants.managepermissions_id_message

        language = data['language']
        id_permissions = data['permissions']

        allowed = ''
        if len(id_permissions['allowed']) == 0:
            allowed = "---"
        else:
            for allowed_mode in id_permissions['allowed']:
                allowed += "--- " + allowed_mode + '\n'

        forbidden = ''
        if len(id_permissions['forbidden']) == 0:
            forbidden = "---"
        else:
            for forbidden_mode in id_permissions['forbidden']:
                forbidden += "--- " + forbidden_mode + '\n'

        id_message = id_message.format(
            id=id, allowed=allowed, forbidden=forbidden)

        message += id_message

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


async def savepermissions_callback(bot, call):
    global permission_changeable
    Permissions.add(permission_changeable)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=constants.savepermissions_saved_message, reply_markup=markup)


async def resetpermissions_callback(bot, call):
    global permission_changeable
    permission_changeable = (permission_changeable[0], {
        "allowed": [], "forbidden": []})

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=constants.resetpermissions_reseted_message, reply_markup=markup)


async def cancelpermissions_callback(bot, call):
    global permission_changeable
    permission_changeable = ()

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=constants.cancelpermissions_canceled_message, reply_markup=markup)


async def clearlogs_callback(bot, call):
    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=constants.PROCESSING)

    Log.clear()

    await send_message(bot, call.message.chat.id, text=constants.clearlogs_cleared_message, reply_markup=markup)


@registry.register(
    command_name=constants.ADMIN_GETLOGS_command,
    permission_name=constants.ADMIN_GETLOGS,
)
async def getlogs(bot, message):
    markup = getMarkupModes()

    await send_message(bot, message.chat.id, text=constants.PROCESSING)

    logs = Log.view()

    await send_message(bot, message.chat.id, logs, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)


@registry.register(
    command_name=constants.ADMIN_STOPBILLY_command,
    permission_name=constants.ADMIN_STOPBILLY,
)
async def stopBilly(bot, message):
    await send_message(bot, message.chat.id, text=constants.stopbilly_stopped_message)

    Exit.stopBilly()


@registry.register(
    command_name=constants.ADMIN_DELETE_command,
    permission_name=constants.ADMIN_DELETE,
)
async def delete(bot, message):
    markup = getMarkupModes({constants.RESTART_preview: constants.RESTART})

    await send_message(bot, message.chat.id, text=delete(), reply_markup=markup)


@registry.register(
    command_name=constants.ADMIN_MANAGEPERMISSIONS_command,
    permission_name=constants.ADMIN_MANAGEPERMISSIONS,
)
async def managepermissions(bot, message):
    global permission_changeable

    permission_id = getarg(
        message.text, constants.ADMIN_MANAGEPERMISSIONS_command)

    markup = getMarkupModes()

    if not permission_id.isdigit():
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    permission_changeable = (permission_id, {"allowed": [], "forbidden": []})

    callbacks = callback_system.callbacks

    sorted_callbacks = {}

    for callback in sorted(callbacks, key=lambda callback: callback.lower()):
        sorted_callbacks[callback] = callbacks[callback]

    callbacks = sorted_callbacks

    allow_prefix = constants.MANAGEPERMISSION_prefix + ':allow:'
    forbid_prefix = constants.MANAGEPERMISSION_prefix + ':forbid:'

    forbid_markup = {}
    allow_markup = {'ALL': allow_prefix + 'ALL'}

    for callback, callback_info in callbacks.items():
        callback_data = callback_info['data']
        callback_permission = callback_info['permission']

        if callback_data != callback_permission:
            continue

        allow_markup[callback] = allow_prefix + callback_permission
        forbid_markup[callback] = forbid_prefix + callback_permission

    allow_markup = getMarkupModes(allow_markup)
    forbid_markup = getMarkupModes(forbid_markup)

    await send_message(bot, message.chat.id, text=constants.managepermissions_allow_message, reply_markup=allow_markup)
    await send_message(bot, message.chat.id, text=constants.managepermissions_forbid_message, reply_markup=forbid_markup)

    markup = {}
    markup[constants.RESETPERMISSIONS_preview] = constants.RESETPERMISSIONS
    markup[constants.CANCELPERMISSIONS_preview] = constants.CANCELPERMISSIONS
    markup[constants.SAVEPERMISSIONS_preview] = constants.SAVEPERMISSIONS
    markup = getMarkupModes(markup)

    await send_message(bot, message.chat.id, text=constants.managepermissions_save_message, reply_markup=markup)


def update():
    answer = Updater.update()
    return answer


def delete():
    answer = Delete.delete()
    return answer


modes = {constants.ADMIN_DELETE_preview: constants.ADMIN_DELETE,
         constants.ADMIN_MANAGEPERMISSIONS_preview: constants.ADMIN_MANAGEPERMISSIONS,
         constants.ADMIN_GETLOGS_preview: constants.ADMIN_GETLOGS, constants.ADMIN_CLEARLOGS_preview: constants.ADMIN_CLEARLOGS,
         constants.ADMIN_STOPBILLY_preview: constants.ADMIN_STOPBILLY}
