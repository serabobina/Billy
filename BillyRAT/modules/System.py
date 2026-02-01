import socket
import http.client
import re
import platform
import os
import getpass
import psutil
import json
from datetime import datetime
from uuid import getnode as mac
import constants
from utils import getarg, getMarkupModes, validate_time_argument, create_menu_markup, send_message


async def getipmac_callback(bot, call):
    markup = getMarkupModes()

    await send_message(bot, call.message.chat.id, text=getIpMac(), reply_markup=markup, parse_mode='HTML')


async def collectsysteminfo_callback(bot, call):
    markup = getMarkupModes()

    system_info = collect_system_info()

    system_info_mesasage = constants.system_collect_system_info_message

    for category, info in system_info.items():
        if not type(info) == dict:
            system_info_mesasage = system_info_mesasage.replace(
                f'{{{category}}}', str(info))
            continue

        for param, value in info.items():
            system_info_mesasage = system_info_mesasage.replace(
                f'{{{param}}}', str(value))

    await send_message(bot, call.message.chat.id, text=system_info_mesasage, reply_markup=markup, parse_mode='HTML')


async def collectdisksinfo_callback(bot, call):
    markup = getMarkupModes()

    disks = collect_disks_info()

    disks_info_message = ""

    for disk in disks:
        disks_info_message += constants.system_collect_disks_info_message

        for param, value in disk.items():
            disks_info_message = disks_info_message.replace(
                f'{{{param}}}', str(value))

    await send_message(bot, call.message.chat.id, text=disks_info_message, reply_markup=markup, parse_mode='HTML')


async def getprocesses_callback(bot, call):
    markup = getMarkupModes()

    processes = get_processes()

    processes_message = constants.system_getprocesses_message

    for process in processes:
        name = process['name']
        username = str(process['username'])
        pid = str(process['pid'])
        processes_message += f"\n<code>{name+' '*(16 - len(name))*(len(name) < 16)}</code> {username+' '*(16 - len(username))*(len(username) < 16)} {pid+' '*(16 - len(pid))*(len(pid) < 16)}"

    await send_message(bot, call.message.chat.id, text=processes_message, reply_markup=markup, parse_mode='HTML')


def collect_system_info():
    info = {}

    info['system'] = {
        'os': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
        'username': getpass.getuser()
    }

    mem = psutil.virtual_memory()
    info['memory'] = {
        'total_gb': mem.total // (1024**3),
        'available_gb': mem.available // (1024**3),
        'used_percent': mem.percent
    }

    info['cpu'] = {
        'cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(),
        'usage_percent': psutil.cpu_percent(interval=1),
        'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
    }

    info['collection_time'] = datetime.now().isoformat()

    return info


def collect_disks_info():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_gb': usage.total // (1024**3),
                'used_gb': usage.used // (1024**3),
                'free_gb': usage.free // (1024**3)
            })
        except:
            pass

    return disks


def get_processes():
    processes = []

    for proc in list(psutil.process_iter(['pid', 'name', 'username']))[:20]:
        processes.append(proc.info)
    return processes


def getIpMac():
    white_ip = socket.gethostbyname(socket.gethostname())

    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    gray_ip = conn.getresponse().read().decode()

    MAC = ':'.join(re.findall('..', '%012x' % mac()))

    return constants.system_getIpMac_message.format(white_ip=white_ip, gray_ip=gray_ip, MAC=MAC)


modes = {constants.SYSTEM_GETIPMAC_preview: constants.SYSTEM_GETIPMAC,
         constants.SYSTEM_COLLECT_SYSTEM_INFO_preview: constants.SYSTEM_COLLECT_SYSTEM_INFO,
         constants.SYSTEM_COLLECT_DISKS_INFO_preview: constants.SYSTEM_COLLECT_DISKS_INFO,
         constants.SYSTEM_GET_PROCESSES_preview: constants.SYSTEM_GET_PROCESSES}
