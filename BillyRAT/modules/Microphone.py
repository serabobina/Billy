import config
import constants
import os
import sounddevice as sd
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
    devices = []

    all_devices = sd.query_devices()
    
    for i, device in enumerate(all_devices):
        if device['max_input_channels'] > 0:
            devices.append({
                'name': device['name'],
                'original_index': i,
                'channels': device['max_input_channels']
            })
    
    return devices



def record_microphone_func(device_index, time_working):
    if not (0 < time_working <= config.max_time_to_record_microphone):
        raise Exception(constants.INVALID_ARGUMENT)
    
    devices = get_devices()
    
    if not (0 < device_index <= len(devices)):
        raise IndexError(f"Index not in range [1:{len(devices)}].")
    
    device_info = devices[device_index - 1]
    original_index = device_info['original_index']

    sample_rate = 44100
    channels = min(1, device_info['channels']) 
    
    duration = time_working
    filename = File.get_random_temp_file_name(sample='{file_name}.wav') 

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype='int16', 
        device=original_index
    )
    
    sd.wait() 
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())
    
    return filename


modes = {constants.MICROPHONE_GETDEVICES_preview: constants.MICROPHONE_GETDEVICES,
         constants.MICROPHONE_RECORD_preview: constants.MICROPHONE_RECORD}
