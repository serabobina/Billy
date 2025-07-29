import config
from modules import NetworkDrive
import json
import os


def downloadLog():
    NetworkDrive.download(config.log_path, config.tmp_log_path)

    return config.tmp_log_path


def getLog():
    if not os.path.isfile(config.tmp_log_path):
        downloadLog()

    with open(config.tmp_log_path) as file:
        return json.load(file)


def delete_tmp_file():
    if os.path.isfile(config.tmp_log_path):
        os.remove(config.tmp_log_path)


def uploadlog():
    if os.path.isfile(config.tmp_log_path):
        NetworkDrive.upload(config.tmp_log_path, config.log_path)
        delete_tmp_file()
        NetworkDrive.clean_trash()


def addLog(message, date, status, action):
    id = str(message.from_user.id)
    username = message.from_user.username
    log = getLog()

    if not id in log.keys():
        log[id] = []

    log[id].append({"username": username, "date": date,
                   "status": status, "action": action})

    with open(config.tmp_log_path, 'w') as file:
        json.dump(log, file)


def clearLogs():
    log = {}

    with open(config.tmp_log_path, 'w') as file:
        json.dump(log, file)

    uploadlog()


def viewLog():
    answer = ''

    logs = getLog()

    for id in logs.keys():
        username = get_username(logs, id)

        telegram_url = 'https://t.me/' + str(username)

        html_id = f'<a href="{telegram_url}">{id}</a>'

        if username == None:
            html_id = id

        answer += html_id + ' ' + '-' * \
            (15 - len(id)) + ' ' + \
            '        TIME                      STATUS                   ACTION\n'

        for div in logs[id]:
            date = div['date']
            status = div['status']
            action = div['action']

            answer += ' '*12 + '|\n'
            answer += ' '*13 + '-'*3 + ' '
            answer += f"{date}             {status}               {action}\n\n"

    return answer


def get_username(logs, id):
    username = None

    for div in logs[id]:
        if div['username'] != None:
            username = div['username']

    return username
