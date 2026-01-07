import functools
import threading
import asyncio
import inspect
import constants


def protected(timeout=30, bot=None, error_text=None):
    """
    Universal decorator for BOTH sync and async functions.
    """
    def decorator(func):
        @error_handler_smart(bot=bot, error_text=error_text)
        @limit_execution_time_smart(timeout)
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):

            return await func(*args, **kwargs)

        return async_wrapper

    return decorator


def error_handler_smart(bot=None, error_text=None):
    """
    Smart error handler for sync and async functions.
    Sends appropriate messages based on exception type.
    """
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            message = _find_message(args, kwargs)
            try:
                return await func(*args, **kwargs)
            except asyncio.TimeoutError:
                if bot and message:
                    await _send_async_message_safe(
                        bot, message,
                        constants.timeout_error_message
                    )

            except Exception as ex:

                if bot and message:

                    error_msg = error_text
                    if error_text == None:
                        error_msg = constants.exception_error_message.format(
                            ERROR=ex)
                    await _send_async_message_safe(bot, message, error_msg)

        return async_wrapper

    return decorator


def limit_execution_time_smart(timeout):
    """
    Smart timeout control ONLY.
    Raises TimeoutError (or asyncio.TimeoutError for async).
    NO message sending logic here!
    """
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):

            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=timeout
            )
        return async_wrapper

    return decorator


# ====================== HELPER FUNCTIONS ======================
def _find_message(args, kwargs):
    """Find Telegram message object in function arguments."""

    if 'message' in kwargs:
        message = kwargs['message']
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            return message

    for arg in args:
        if hasattr(arg, 'chat') and hasattr(arg.chat, 'id'):
            return arg
        # Также может найти call.message
        if hasattr(arg, 'message') and hasattr(arg.message, 'chat'):
            return arg.message

    return None


async def _send_async_message_safe(bot, message, text):
    """Safe async message sending."""
    try:
        if hasattr(bot, 'send_message'):
            await bot.send_message(message.chat.id, text)
    except Exception as ex:
        print("[PROTECTED] Error in sending async message", ex)
