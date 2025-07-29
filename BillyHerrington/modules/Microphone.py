import config
import constants
import os
import pyaudio
import wave


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


def record(device_index, time_working):
    p = pyaudio.PyAudio()

    try:
        if not (0 < time_working <= config.max_time_to_record_microphone):
            return (1, constants.INVALID_ARGUMENT)

        devices = get_devices()

        if not (0 < device_index <= len(devices)):
            return (1, 'Invalid index of device.')

        device_info = devices[device_index - 1]

        original_index = device_info['original_index']
        channels = min(1, device_info['channels'])

        chunk = 1024
        sample_format = pyaudio.paInt16
        rate = 44100

        fs = 44100
        duration = time_working
        filename = config.tmp_audio_path

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

        return (0, filename)

    except Exception as ex:
        return (1, f"Error: {str(ex)}")


def delete_tmp_file():
    if os.path.isfile(config.tmp_audio_path):
        os.remove(config.tmp_audio_path)


modes = {constants.MICROPHONE_GETDEVICES_preview: constants.MICROPHONE_GETDEVICES,
         constants.MICROPHONE_RECORD_preview: constants.MICROPHONE_RECORD}
