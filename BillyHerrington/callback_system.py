"""
Enhanced callback handling system for Billy bot with protected decorator.
"""
from utils import send_message, send_default_message, getMarkupModes
from modules import Permissions
import importlib
import config
import constants


class CallbackSystem:
    """
    Smart callback system with automatic configuration detection and protected decorator.
    """

    def __init__(self, bot=None, tools_module=None):
        self.callbacks = {}
        self.bot = bot
        self.tools_module = tools_module

    def set_bot_and_tools(self, bot, tools_module):
        """
        Set bot and tools module for protected decorator.
        Should be called from Billy.py after bot initialization.
        """
        self.bot = bot
        self.tools_module = tools_module

    def initialize(self):
        import constants

        all_attrs = [attr for attr in dir(
            constants) if not attr.startswith('_')]

        callback_base_names = set()

        for attr_name in all_attrs:
            if attr_name.endswith('_preview'):

                base_name = attr_name[:-8]
                callback_base_names.add(base_name)

        for base_name in callback_base_names:

            if hasattr(constants, base_name):
                callback_data = getattr(constants, base_name)

                if isinstance(callback_data, str):
                    callback_info = self.extract_callback_info(
                        constants, base_name, callback_data)

                    if callback_info:
                        self.callbacks[callback_data] = callback_info

        print(
            f"[CallbackSystem] Found {len(self.callbacks)} callbacks with previews")

    def extract_callback_info(self, constants, attr_name, callback_data):
        """
        Extract callback information from constants.
        """
        callback_info = {
            'data': callback_data,
            'name': attr_name
        }

        suffixes = {
            '_preview': 'preview',
            '_command': 'command',
            '_documentation': 'documentation',
            '_handler': 'handler',
            '_permission': 'permission',
            '_module': 'module'
        }

        for suffix, key in suffixes.items():
            suffix_attr = f"{attr_name}{suffix}"
            if hasattr(constants, suffix_attr):
                callback_info[key] = getattr(constants, suffix_attr)

        callback_info['type'] = self.determine_callback_type(callback_info)

        callback_info['module'] = self.determine_module(callback_info)

        callback_info['permission'] = self.determine_permission(callback_info)

        return callback_info

    def determine_callback_type(self, callback_info):
        """
        Determine callback type based on available attributes.
        """
        if 'handler' in callback_info:
            return 'DIRECT_ACTION'
        elif 'command' in callback_info:
            return 'TUTORIAL'
        else:
            return 'SUBMENU'

    def determine_module(self, callback_info):
        """
        Automatically determine module name.
        """
        if 'module' in callback_info:
            return callback_info['module']

        if 'handler' in callback_info:
            handler = callback_info['handler']
            if '.' in handler:
                return handler.split('.')[0]

        callback_data = callback_info['data']
        if '/' in callback_data:
            module_part = callback_data.split('/')[0]

            return module_part.capitalize()

        return callback_info['name'].split('_')[0].capitalize()

    def determine_permission(self, callback_info):
        """
        Automatically determine module permission.
        """

        if 'permission' in callback_info:
            return callback_info['permission']
        else:
            return callback_info['data']

    async def handle_callback(self, bot, call):
        """
        Main callback handler.
        """

        await bot.answer_callback_query(call.id)

        callback_data = call.data

        if callback_data not in self.callbacks:
            await self.handle_unknown_callback(bot, call, callback_data)
            return

        callback_info = self.callbacks[callback_data]

        permission = callback_info['permission']
        if not Permissions.check(call, permission):
            await send_message(
                bot,
                call.message.chat.id,
                constants.you_have_not_this_permission
            )
            return

        callback_type = callback_info['type']

        if callback_type == 'SUBMENU':
            await self.handle_submenu(bot, call, callback_info)
        elif callback_type == 'TUTORIAL':
            await self.handle_tutorial(bot, call, callback_info)
        elif callback_type == 'DIRECT_ACTION':
            await self.handle_direct_action(bot, call, callback_info)

    async def handle_submenu(self, bot, call, callback_info):
        """
        Handle submenu callbacks.
        """
        module_name = callback_info['module']

        try:
            module = importlib.import_module(f"modules.{module_name}")
            modes = getattr(module, 'modes', {})

            title = callback_info.get('preview', callback_info['data'])

            await send_default_message(
                bot,
                call.message,
                text=title,
                markup_arg=modes
            )

        except Exception as e:
            print(
                f"[CallbackSystem] Error in submenu {callback_info['data']}: {e}")
            await send_message(
                bot,
                call.message.chat.id,
                f"Error in {callback_info['data']} {e}"
            )

    async def handle_tutorial(self, bot, call, callback_info):
        """
        Handle tutorial callbacks.
        """
        documentation = callback_info.get('documentation', '')

        if not documentation:
            command = callback_info.get('command', '')
            documentation = f"Use /{command} with appropriate arguments."

        await send_default_message(
            bot,
            call.message,
            text=documentation
        )

    async def handle_direct_action(self, bot, call, callback_info):
        """
        Handle direct action callbacks with protected decorator.
        """
        handler_str = callback_info['handler']

        try:
            module_name, func_name = handler_str.split('.')

            module = importlib.import_module(f"modules.{module_name}")
            func = getattr(module, func_name, None)

            if not func:
                raise AttributeError(
                    f"Function {func_name} not found in module {module_name}")

            timeout = config.default_callback_timeout

            if hasattr(constants, f"{callback_info['name']}_timeout"):
                timeout = getattr(
                    constants, f"{callback_info['name']}_timeout")

            if self.tools_module and self.bot:
                protected_func = self.tools_module.protected(
                    bot=self.bot,
                    timeout=timeout
                )(func)

                await protected_func(bot, call)
            else:
                await func(bot, call)

        except Exception as e:
            print(
                f"[CallbackSystem] Error in direct action {callback_info['data']}: {e}")

            if not self.tools_module:
                await send_message(
                    bot,
                    call.message.chat.id,
                    f"Error executing action: {type(e).__name__}"
                )

    async def handle_unknown_callback(self, bot, call, callback_data):
        """
        Handle unknown callbacks.
        """
        import constants
        await send_message(
            bot,
            call.message.chat.id,
            f"{constants.command_not_found}{callback_data}"
        )


callback_system = CallbackSystem()
