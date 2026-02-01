"""
Command registry for automatic bot command registration.
"""
import functools
from typing import Dict, Callable, Any, Optional
from modules import Permissions
from utils import send_message
import constants


class CommandRegistry:
    """
    Bot command registry with integrated permission checking.
    """

    def __init__(self):
        self._commands: Dict[str, Dict] = {}
        print('[COMMANDREGISTRY] Initialized')

    def register(self,
                 command_name: str,
                 permission_name: str,
                 description: str = "",
                 timeout: int = 180):
        """
        Decorator for command registration.

        Args:
            command_name: Command name (without '/')
            permission_name: Permission constant name
            description: Command description for help
            timeout: Execution timeout in seconds
        """
        def decorator(func: Callable) -> Callable:
            self._commands[command_name] = {
                'handler': func,
                'permission_name': permission_name,
                'description': description,
                'timeout': timeout,
                'module': func.__module__
            }

            print(f'[COMMANDREGISTRY] Registered command: /{command_name} '
                  f'from {func.__module__} (permission: {permission_name})')

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            return wrapper
        return decorator

    def apply_to_bot(self, bot, tools_module):
        """
        Apply all registered commands to the bot.

        Args:
            bot: AsyncTeleBot instance
            tools_module: Module with protected decorator
        """
        print(
            f'[COMMANDREGISTRY] Applying {len(self._commands)} commands to bot...')

        for command_name, command_data in self._commands.items():
            handler = command_data['handler']
            timeout = command_data['timeout']
            permission_name = command_data['permission_name']

            async def command_wrapper(message,
                                      cmd_name=command_name,
                                      perm_name=permission_name,
                                      cmd_handler=handler,
                                      bot_instance=bot):

                if not Permissions.check(message, perm_name):
                    await send_message(
                        bot_instance,
                        message.chat.id,
                        constants.you_have_not_this_permission
                    )
                    return None

                return await cmd_handler(bot_instance, message)

            protected_handler = tools_module.protected(
                bot=bot,
                timeout=timeout
            )(command_wrapper)

            @bot.message_handler(commands=[command_name])
            async def final_handler(message,
                                    handler_func=protected_handler):

                return await handler_func(message)

            print(f'[COMMANDREGISTRY] Registered handler for /{command_name}')

    def get_command_info(self, command_name: str) -> Optional[Dict]:
        """Get command information."""
        return self._commands.get(command_name)

    def list_commands(self) -> list:
        """List all registered commands."""
        return [
            {
                'name': name,
                'description': data['description'],
                'permission': data['permission_name'],
                'module': data['module']
            }
            for name, data in self._commands.items()
        ]


registry = CommandRegistry()
