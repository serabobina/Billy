import yadisk
import getpass
import json
import os
import network_token as network_token
import branch
import platform


username = getpass.getuser()
os_name = platform.system()
unique_program_name = branch.branch_name

if os_name == 'Windows':
    main_dir_path = f'C:/Users/{username}/AppData/Local/Comms/Unistore/data/5/a/billy/'
if os_name == 'Linux':
    main_dir_path = f'/home/{username}/.config/Billy/'

tmp_dir_path = main_dir_path + 'tmp/'
tmp_parser_path = tmp_dir_path + 'parser.json'
parser_path = '/Billy-Herrington/parser.json'
yadisk_token = network_token.token


def get():
    create_tmp_dir()

    download(parser_path, tmp_parser_path)

    with open(tmp_parser_path) as file:
        permissions = json.load(file)

    os.remove(tmp_parser_path)
    return permissions


def get_token():
    parser = get()

    return parser[unique_program_name]['token']


def get_root_path():
    parser = get()

    return parser[unique_program_name]['root_path']


def create_tmp_dir():
    if not os.path.isdir(tmp_dir_path):
        os.makedirs(tmp_dir_path, exist_ok=1)


def download(network_path, path):
    client = yadisk.Client(token=yadisk_token)

    with client:
        client.download(network_path, path)
