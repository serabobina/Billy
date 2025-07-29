import subprocess
import constants
import config


if config.os_name == constants.Windows_OS:
    default_system_encoding = 'cp866'
if config.os_name == constants.Linux_OS:
    default_system_encoding = 'utf-8'


def check_if_symb_default(symb):
    byte = ord(symb)
    if (byte >= 0 and byte <= 160) or (byte >= 1040 and byte <= 1103):
        return 1
    return 0


def check_encoding(output):
    for symb in output:
        if not check_if_symb_default(symb):
            return 0
    return 1


def run_command(command):
    return run_command_system(command, shell=1, encoding='utf-8')


def run_command_system(command, shell=1, encoding='cp866'):
    if type(command) == str and shell == 0:
        command = command.split()

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
        )

        output = result.stdout.decode(encoding, errors='ignore')

        if not check_encoding(output):
            output = result.stdout.decode(
                default_system_encoding, errors='ignore')

        if result.returncode != 0 and result.stderr != b'':
            error = "Error: " + result.stderr.decode(encoding, errors='ignore')
            if not check_encoding(error):
                error = "Error: " + \
                    result.stderr.decode(
                        default_system_encoding, errors='ignore')

            return error
        else:
            return output

    except Exception as ex:
        return str(ex)


modes = {constants.COMMAND_RUNCOMMAND_preview: constants.COMMAND_RUNCOMMAND}
