import config
import constants
import os
import pyaudio
import wave
import config
import asyncio
from command_registry import registry
from modules import File
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def getdevices_callback(bot, call):
    markup = getMarkupModes()

    devices = get_devices()

    message = constants.microphonegetdevices_devices_message
    for i in range(len(devices)):
        message += f"{i + 1}) {devices[i]['name']}\n"

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup)


async def record_callback(bot, call):
    markup = getMarkupModes()

    devices = get_devices()

    message = constants.MICROPHONE_RECORD_documentation.format(
        max_time_to_record_microphone=config.max_time_to_record_microphone)
    for i in range(len(devices)):
        message += f"{i + 1}) {devices[i]['name']}\n"

    await send_message(bot, call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')


@registry.register(
    command_name=constants.MICROPHONE_RECORD_command,
    permission_name=constants.MICROPHONE_RECORD,
)
async def record(bot, message):
    arguments = getarg(
        message.text, constants.MICROPHONE_RECORD_command).split()
    markup = getMarkupModes()

    device_index, time_working = arguments

    if not len(arguments) == 2 or not (device_index.isdigit() and time_working.isdigit()):
        await send_message(bot, message.chat.id, text=constants.INVALID_ARGUMENT, reply_markup=markup)
        return

    device_index, time_working = map(int, arguments)

    await send_message(bot, message.chat.id, text=constants.recordmicrophone_recording_started_message)
    print(device_index, time_working)
    loop = asyncio.get_event_loop()
    audio_path = await loop.run_in_executor(None, lambda: record_microphone_func(device_index, time_working))

    await send_message(bot, message.chat.id, text=constants.recordmicrophone_recording_finished_message, reply_markup=markup)

    with open(audio_path, 'rb') as f:
        await bot.send_audio(message.chat.id, f)

    File.delete_tmp_file(audio_path)


def get_devices():
    p = pyaudio.PyAudio()

    devices_count = p.get_device_count()

    devices = []

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            devices.append({
                'name': device_info['name'],
                'original_index': i,
                'channels': device_info['maxInputChannels']
            })

    p.terminate()
    return devices


def record_microphone_func(device_index, time_working):
    p = pyaudio.PyAudio()

    if not (0 < time_working <= config.max_time_to_record_microphone):
        raise Exception(constants.INVALID_ARGUMENT)

    devices = get_devices()

    if not (0 < device_index <= len(devices)):
        raise IndexError(
            f"Index not in range [1:{len(devices)}].")

    device_info = devices[device_index - 1]

    original_index = device_info['original_index']
    channels = min(1, device_info['channels'])

    chunk = 1024
    sample_format = pyaudio.paInt16
    rate = 44100

    fs = 44100
    duration = time_working
    filename = File.get_random_temp_file_name(sample='{file_name}.mp3')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input_device_index=original_index,
                    input=True)

    frames = []
    for _ in range(0, int(rate / chunk * time_working)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename


modes = {constants.MICROPHONE_GETDEVICES_preview: constants.MICROPHONE_GETDEVICES,
         constants.MICROPHONE_RECORD_preview: constants.MICROPHONE_RECORD}
