import Colors


WINDOWS_OS = 'Windows'
LINUX_OS = 'Linux'

special_length_substitute = 'count_of_branches'

default_get_network_token_message = '{input_pref}Please enter Yandex OAuth-token here: {value_color}'.format(
    input_pref=Colors.input_pref, value_color=Colors.value_color)
default_get_network_token_error_message = '{error_pref}Invalid token. Please try again: {value_color}'.format(
    error_pref=Colors.error_pref, value_color=Colors.value_color)

default_get_bot_token_message = '{input_pref}Write the bot token: {value_color}'.format(
    input_pref=Colors.input_pref, value_color=Colors.value_color)
default_get_bot_token_error_message = '{error_pref}Invalid token. Please try again: {value_color}'.format(
    error_pref=Colors.error_pref, value_color=Colors.value_color)

default_get_telegram_id_message = '{input_pref}Write your telegram id: {value_color}'.format(
    input_pref=Colors.input_pref, value_color=Colors.value_color)
default_get_telegram_id_error_message = '{error_pref}Id must be number and > 0. Please try again: {value_color}'.format(
    error_pref=Colors.error_pref, value_color=Colors.value_color)

default_get_branch_for_list_message = '{input_pref}Write name of the branch: {value_color}'
default_get_branch_for_list_error_message = '{error_pref}Incorrect. Input must be number and be in range [1-{special_length_substitute}]: {value_color}'.format(
    error_pref=Colors.error_pref, value_color=Colors.value_color, special_length_substitute=special_length_substitute)

obfuscate_progress_message = '{default_color}Obfuscation [{obfuscated_files_count}/{files_count}] {progress}%'

PROCESSING = '{default_color}Processing...'.format(
    default_color=Colors.default_color)

CTRL_C_message = '\n\n{error_pref}Seems like you pressed CTRL+C. Exit...'.format(
    error_pref=Colors.error_pref)
