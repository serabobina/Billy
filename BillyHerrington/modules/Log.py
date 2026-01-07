import config
from modules import NetworkDrive
from modules import Environment
from modules import Crypt
import encryption_keys
from threading import Timer
import json
import os

log = {}


def download_and_get():
    temp_path = get_random_temp_file_name()

    Environment.create()

    NetworkDrive.download(config.log_path,
                          temp_path, check_temp=True)

    with open(temp_path) as file:
        log = file.read()

    delete_tmp_log(temp_path)

    if log == '':
        return {}

    try:
        log = Crypt.decrypt(
            log, encryption_keys.log_ek)
        log = json.loads(log)

        return log

    except Exception as ex:
        print('[ERROR DOWNLOADING AND GETTING LOG]')
        print(ex)
        print(log)


def get():
    global log

    return log


def delete_tmp_log(temp_path):
    if os.path.isfile(temp_path):
        os.remove(temp_path)


def upload(log: dict):
    Environment.create()

    log = json.dumps(log)
    log = Crypt.encrypt(
        log, encryption_keys.log_ek)

    temp_path = get_random_temp_file_name()

    with open(temp_path, 'w') as file:
        file.write(log)

    while True:
        try:
            NetworkDrive.upload(temp_path,
                                config.log_path)
        except Exception as ex:
            print('[Error updating log]')
            print(ex)
        else:
            break

    delete_tmp_log(temp_path)


def add(message, date, status, action):
    global log

    id = str(message.from_user.id)
    user_info = {}

    info_params = ['first_name', 'full_name', 'id', 'is_bot',
                   'is_premium', 'language_code', 'last_name', 'username']

    for param in dir(message.from_user):
        if param not in info_params:
            continue

        value = getattr(message.from_user, param)

        user_info[param] = value

    if not id in log.keys():
        log[id] = []

    log[id].append({"user_info": user_info, "date": date,
                   "status": status, "action": action})


def clear():
    global log

    log = {}


def view():
    answer = ''

    log = get()

    for id in log.keys():
        username = get_username(log, id)

        telegram_url = 'https://t.me/' + str(username)

        html_id = f'<a href="{telegram_url}">{id}</a>'

        if username == None:
            html_id = id

        answer += html_id + ' ' + '-' * \
            (15 - len(id)) + ' ' + \
            '        TIME                      STATUS                   ACTION\n'

        for div in log[id]:
            date = div['date']
            status = div['status']
            action = div['action']

            answer += ' '*12 + '|\n'
            answer += ' '*13 + '-'*3 + ' '
            answer += f"{date}             {status}               {action}\n\n"

    return answer


def get_username(log, id):
    username = None

    for div in log[id]:
        user_info = div["user_info"]
        if user_info['username'] != None:
            username = user_info['username']

    return username


def auto_update():
    upload(log)

    print('[UPDATING LOG]')

    update_timer = Timer(
        interval=config.log_timeout, function=auto_update)
    update_timer.daemon = True
    update_timer.start()


def get_random_temp_file_name():
    import random

    alth = ''.join([chr(i) for i in range(48, 58)] + [chr(i)
                                                      for i in range(65, 91)] + [chr(i) for i in range(97, 123)])

    temp_file_name = '{file_name}.tmp'
    random_string_length = 30

    random_string = ''.join(random.choice(alth)
                            for _ in range(random_string_length))

    return os.path.join(config.tmp_dir_path, temp_file_name.format(file_name=random_string))


log = download_and_get()
