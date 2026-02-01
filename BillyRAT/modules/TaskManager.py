import psutil
import time
from modules import Exit


forbidden_processes = ['taskmgr.exe', 'resmon.exe', 'perfmon.exe', 'procexp64.exe', 'procexp.exe',
                       'processhacker.exe', 'systeminformer.exe', 'procmon.exe', 'depends.exe', 'apimonitor.exe',
                       'gnome-system-monitor']
timeout_value = 0.3


def timeout():
    time.sleep(timeout_value)


def get_processes():
    return list(psutil.process_iter())


def check_task_manager():
    processes = list(map(lambda x: x.name().lower(), get_processes()))
    for forbidden_proc in forbidden_processes:
        if forbidden_proc.lower() in processes:
            return 1
    return 0


def exit():
    print('exit')
    Exit.stopBilly()


def exit_if_task_manager():
    while True:
        try:
            status = check_task_manager()
        except:
            status = 0

        if status:
            exit()

        timeout()
