"""
Common utilities for all modules.
"""
from telebot import types
import constants
import asyncio


def getarg(message_text: str, suffix: str) -> str:
    """
    Extract arguments from command text.

    Args:
        message_text: Full message text
        suffix: Command suffix (without '/')

    Returns:
        Extracted arguments string
    """
    if not message_text:
        return ""
    return message_text.replace(f'/{suffix}', '').strip()


def getMarkupModes(modes=None, is_main=0, row_lenght=2):
    """
    Create inline keyboard with buttons.

    Args:
        modes: Dictionary with button names and callbacks
        is_main: If True, don't add menu button
        row_lenght: Number of buttons per row

    Returns:
        InlineKeyboardMarkup object
    """
    if modes is None:
        modes = {}

    markup = types.InlineKeyboardMarkup()
    row = []

    for name, callback in modes.items():
        row.append(types.InlineKeyboardButton(name, callback_data=callback))
        if len(row) >= row_lenght:
            markup.add(*row)
            row = []

    if row:
        markup.add(*row)

    if not is_main:
        markup.add(types.InlineKeyboardButton(
            constants.MENU_preview,
            callback_data=constants.MENU
        ))

    return markup


async def send_message(bot, chat_id, text, reply_markup={}, parse_mode=0, disable_web_page_preview=False, timeout=300):
    """
    Send message with automatic splitting for long texts.

    Args:
        bot: AsyncTeleBot instance
        chat_id: Target chat ID
        text: Text to send
        reply_markup: Inline keyboard markup
        parse_mode: Telegram parse mode
        disable_web_page_preview: Disable link preview
    """

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
        await repeat_sending_message(
            bot,
            chat_id,
            text_part,
            reply_markup={},
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            timeout=timeout,
        )
    await repeat_sending_message(
        bot,
        chat_id,
        texts[-1],
        reply_markup=reply_markup,
        parse_mode=parse_mode,
        disable_web_page_preview=disable_web_page_preview,
        timeout=timeout
    )


async def repeat_sending_message(bot, chat_id, message, reply_markup, parse_mode, disable_web_page_preview, timeout, attempt=3):
    for attempt in range(3):
        try:
            await bot.send_message(
                chat_id,
                message,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                timeout=timeout
            )
            return
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(0.5)


def get_finish_symb(text, max_length):
    """
    Find optimal split position for text.

    Args:
        text: Text to split
        max_length: Maximum length of each part

    Returns:
        Index to split at, or -1 if text fits
    """
    if len(text) < max_length:
        return -1

    length = 0
    for part in text.split('\n'):
        part += '\n'
        if length + len(part) > max_length:
            return length
        length += len(part)


def validate_time_argument(time_str: str, max_time: int) -> tuple[bool, str]:
    """
    Validate time arguments.

    Args:
        time_str: Time string to validate
        max_time: Maximum allowed time in seconds

    Returns:
        tuple[is_valid, error_message]
    """
    if not time_str:
        return False, "Time not specified"

    if not time_str.isdigit():
        return False, "Time must be a number"

    time_int = int(time_str)
    if time_int > max_time:
        return False, f"Maximum time: {max_time} seconds"

    if time_int <= 0:
        return False, "Time must be greater than 0"

    return True, ""


def create_menu_markup(modes_dict, row_length=2):
    """
    Create menu markup from modes dictionary.

    Args:
        modes_dict: Dictionary with display names and command constants
        row_length: Buttons per row

    Returns:
        InlineKeyboardMarkup object
    """
    return getMarkupModes(modes=modes_dict, row_lenght=row_length)
