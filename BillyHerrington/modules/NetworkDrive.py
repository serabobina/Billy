import config
import yadisk
import os


def download(network_path, path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        client.download(network_path, path)


def upload(path, network_path):
    client = yadisk.Client(token=config.yadisk_token)

    if check_if_file_exist(network_path):
        client.remove(network_path)

    with client:
        client.upload(path, network_path)


def check_if_file_exist(network_path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        return client.exists(network_path)


def mkdir(network_path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        return client.mkdir(network_path)


def upload_dir(dir_path, network_dir_path):
    client = yadisk.Client(token=config.yadisk_token)

    if not os.path.isdir(dir_path):
        return f"{dir_path} is not a dir!"

    if not client.is_dir(network_dir_path):
        return f"{network_dir_path} is not a dir!"

    stack = [(dir_path, network_dir_path)]
    with client:
        while True:
            if len(stack) == 0:
                return "Dir uploaded."
            dir_path, network_dir_path = stack.pop()

            for upload_name in os.listdir(dir_path):
                upload_path = dir_path + upload_name
                network_path = network_dir_path + upload_name

                if os.path.isdir(upload_path):
                    stack.append((upload_path + '/', network_path + '/'))
                    client.mkdir(network_path)

                elif os.path.isfile(upload_path):
                    upload(upload_path, network_path)


def list_dir(path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        if not client.is_dir(path):
            return [path]
        return client.listdir(path)


def is_dir(path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        return client.is_dir(path)


def is_file(path):
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        return client.is_file(path)


def clean_trash():
    client = yadisk.Client(token=config.yadisk_token)

    with client:
        return client.remove_trash('/')
