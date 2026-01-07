import cv2
import config
import time
import os
import constants
from command_registry import registry
import asyncio
from modules import File
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def shot_callback(bot, call):
    message = constants.CAMERA_SHOT_documentation.format(
        available_cameras=beautiful_get_available_cameras())

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def video_callback(bot, call):
    message = constants.CAMERA_VIDEO_documentation.format(
        available_cameras=beautiful_get_available_cameras(), max_time_to_camera=config.max_time_to_camera_record)

    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


@registry.register(
    command_name=constants.CAMERA_SHOT_command,
    permission_name=constants.CAMERA_SHOT,
)
async def shot(bot, message):
    """
    Capture a photo from the specified camera.

    Args:
        bot: AsyncTeleBot instance
        message: Telegram message object

    Example:
        /shot 1
    """

    device_index = getarg(message.text, constants.CAMERA_SHOT_command)

    markup = getMarkupModes()

    if not device_index.isdigit():
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    await send_message(bot, message.chat.id, text=constants.PROCESSING)

    photo_path = shot_func(int(device_index))

    photo = open(photo_path, 'rb')
    await bot.send_photo(message.chat.id, photo, reply_markup=markup)

    File.delete_tmp_file(photo_path)


@registry.register(
    command_name=constants.CAMERA_VIDEO_command,
    permission_name=constants.CAMERA_VIDEO,
)
async def video(bot, message):
    """
    Record video from the specified camera for a given duration.

    Args:
        bot: AsyncTeleBot instance
        message: Telegram message object

    Example:
        /video 1 5
    """

    markup = getMarkupModes()

    arguments = getarg(message.text, constants.CAMERA_VIDEO_command).split()

    if len(arguments) != 2 or not (arguments[0].isdigit() and arguments[1].isdigit()):
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    device_index, time_working = arguments

    if not time_working.isdigit() or int(time_working) > config.max_time_to_camera_record:
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    device_index, time_working = map(int, arguments)

    await send_message(bot, message.chat.id, text=constants.video_recording_started_message)

    loop = asyncio.get_event_loop()
    video_path = await loop.run_in_executor(None, lambda: record_video_func(device_index, time_working))

    await send_message(bot, message.chat.id, text=constants.video_recording_finished_message)

    video = open(video_path, 'rb')
    await bot.send_video(message.chat.id, video, reply_markup=markup)

    File.delete_tmp_file(video_path)


def beautiful_get_available_cameras():
    """
    Get formatted string listing available cameras.

    Returns:
        Formatted string with available cameras or error message
    """
    available_cameras = get_available_cameras()

    answer = constants.camera_devices_message

    for i in range(0, len(available_cameras)):
        answer += f"{i + 1}) Camera{i + 1}\n"

    if len(available_cameras) == 0:
        answer = constants.you_havent_any_cameras

    return answer


def get_available_cameras(max_tests=5):
    """
    Detect available camera devices by testing indices.

    Args:
        max_tests: Maximum camera index to test (default: 5)

    Returns:
        List of available camera indices
    """
    available_cameras = []
    for i in range(max_tests):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()

    return available_cameras


def shot_func(camera_index):
    """
    Capture a single frame from the specified camera.

    Args:
        camera_index: Camera index (1-based)

    Returns:
        tuple: (error_flag, path_or_error_message)
               0 for success with file path
               1 for error with error message
    """

    list_of_available_cameras = get_available_cameras()

    if not (camera_index > 0 and camera_index <= len(list_of_available_cameras)):
        raise IndexError(
            f"Index not in range [1:{len(list_of_available_cameras)}].")

    cap = cv2.VideoCapture(camera_index - 1)

    if not cap.isOpened():
        raise Exception("Failed to open camera")

    for i in range(5):
        cap.read()

    ret, frame = cap.read()

    if not ret:
        raise Exception("Camera doesn't work.")

    tmp_photo_path = File.get_random_temp_file_name(
        sample='{file_name}.png')

    cv2.imwrite(tmp_photo_path, frame)

    cap.release()

    return tmp_photo_path


def record_video_func(camera_index, time_working):
    """
    Record video from the specified camera for given duration.

    Args:
        camera_index: Camera index (1-based)
        time_working: Recording duration in seconds

    Returns:
        tuple: (error_flag, path_or_error_message)
               0 for success with file path
               1 for error with error message
    """

    list_of_available_cameras = get_available_cameras()

    if not (camera_index > 0 and camera_index <= len(list_of_available_cameras)):
        raise IndexError(
            f"Index not in range [1:{len(list_of_available_cameras)}].")

    time_working += 1

    cap = cv2.VideoCapture(camera_index - 1)

    if not cap.isOpened():
        raise Exception("Failed to open camera")

    tmp_video_path = File.get_random_temp_file_name(
        sample='{file_name}.mp4')

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(tmp_video_path, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        out.write(frame)

        end_time = time.time()
        if end_time - start_time >= int(time_working):
            break

    cap.release()
    out.release()

    return tmp_video_path


modes = {
    constants.CAMERA_SHOT_preview: constants.CAMERA_SHOT,
    constants.CAMERA_VIDEO_preview: constants.CAMERA_VIDEO
}
