from __init__ import __version__
import requests
import config
import json


def check_for_update():
    try:
        latest_release_raw = requests.get(config.forge_api_latest_release).text
        latest_release_json = json.loads(latest_release_raw)
        latest_release_version = latest_release_json["tag_name"][1:]
        latest_release_url = latest_release_json['html_url']

        if latest_release_version != __version__:
            return (latest_release_version, latest_release_url)

    except Exception as error:
        return 0
