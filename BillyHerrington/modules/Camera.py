import cv2
import config
import time
import os
import constants


def beautiful_get_available_cameras():
    available_cameras = get_available_cameras()

    answer = 'Camera devices:\n'

    for i in range(0, len(available_cameras)):
        answer += f"{i + 1}) Camera{i + 1}\n"

    if len(available_cameras) == 0:
        answer = '! Seems like this device doesn\'t have any cameras.'

    return answer


def get_available_cameras(max_tests=5):
    available_cameras = []
    for i in range(max_tests):

        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


def shot(camera_index):
    try:
        list_of_available_cameras = get_available_cameras()

        if not (camera_index > 0 and camera_index <= len(list_of_available_cameras)):
            return (1, f"Index must be in range 1 - {len(list_of_available_cameras)}")

        cap = cv2.VideoCapture(camera_index - 1)

        if not cap.isOpened():
            return (1, "Failed to open camera")

        for i in range(15):
            cap.read()

        ret, frame = cap.read()

        if not ret:
            return (1, "Camera not working.")

        cv2.imwrite(config.tmp_photo_path, frame)

        cap.release()

    except Exception as ex:
        return (1, 'Error: ' + str(ex))

    else:
        return (0, config.tmp_photo_path)


def video(camera_index, time_working):
    try:
        list_of_available_cameras = get_available_cameras()

        if not (camera_index > 0 and camera_index <= len(list_of_available_cameras)):
            return (1, f"Index must be in range 1 - {len(list_of_available_cameras)}")

        time_working += 1

        cap = cv2.VideoCapture(camera_index - 1)

        if not cap.isOpened():
            return (1, "Failed to open camera")

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(config.tmp_video_path, fourcc, 20.0, (640, 480))

        start_time = time.time()
        while (True):
            ret, frame = cap.read()
            out.write(frame)

            end_time = time.time()
            if end_time - start_time >= int(time_working):
                break

        cap.release()
        out.release()

    except Exception as ex:
        return (1, 'Error while using camera')

    else:
        return (0, config.tmp_video_path)


def delete_tmp_video():
    if os.path.isfile(config.tmp_video_path):
        os.remove(config.tmp_video_path)


def delete_tmp_photo():
    if os.path.isfile(config.tmp_photo_path):
        os.remove(config.tmp_photo_path)


modes = {constants.CAMERA_SHOT_preview: constants.CAMERA_SHOT,
         constants.CAMERA_VIDEO_preview: constants.CAMERA_VIDEO}
