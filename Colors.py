from colorama import Style, Fore, ansi, init
import time

init()

default_color = Style.RESET_ALL + Style.BRIGHT + Fore.BLUE
input_color = default_color
question_color = default_color
error_color = Style.RESET_ALL + Fore.RED
greet_color1 = Style.RESET_ALL + Fore.WHITE
greet_color2 = default_color
value_color = Style.RESET_ALL + Fore.WHITE

default_pref = default_color + '[*] '
input_pref = input_color + '[+] '
error_pref = error_color + '[!] '
question_pref = question_color + '[?] '
about_pref = greet_color1 + ''


def clearConsole():
    print(ansi.clear_screen(), end='')
    print(ansi.Cursor.POS(), end='')


def clearLine(count_of_lines=1):
    for _ in range(count_of_lines):
        print(ansi.clear_line(), end='')
        print(ansi.Cursor.UP(), end='')
    print(ansi.Cursor.DOWN(), end='')
