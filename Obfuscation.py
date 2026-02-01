from BlankOBFv2 import BlankOBFv2
import os
import config
from pathlib import Path
import shutil
import constants
import Colors

obfuscation_suffixes = ['.py', '.pyw']
modules_params = {'default': {'include_imports': True, 'obfuscation_mark': False},
                  Path(os.path.join(config.obfuscated_BillyHerrington_directory,
                                    'modules/Browser_windows.py')): {'include_imports': False, 'obfuscation_mark': True}}

obfuscation_mark_value = "# DONT_REMOVE_THIS_COMMENT_IT_SPECIFIES_WHERE_TO_OBFUSCATE_THE_FILE"


def get_python_files(dir):
    files = []

    for path in os.listdir(dir):
        path = Path(os.path.join(dir, path))

        if path.is_file():
            if path.suffix in obfuscation_suffixes:
                files.append(path)

        elif path.is_dir():
            files += get_python_files(path)

    return files


def copy_obfuscated_dir():
    delete_obfuscated_dir()

    shutil.copytree(config.BillyHerrington_directory,
                    config.obfuscated_BillyHerrington_directory)


def delete_obfuscated_dir():
    if os.path.exists(config.obfuscated_BillyHerrington_directory):
        shutil.rmtree(config.obfuscated_BillyHerrington_directory)


def get_params(module):
    params = modules_params['default']

    if module in modules_params.keys():
        params = modules_params[module]

    return params


def obfuscate_code(code, params):
    include_imports = params['include_imports']
    obfuscation_mark = params['obfuscation_mark']

    code_to_save = ''
    code_to_obfuscate = code

    if obfuscation_mark:
        code_to_save, code_to_obfuscate = code.split(obfuscation_mark_value)

    obfuscator = BlankOBFv2(code=code_to_obfuscate,
                            include_imports=include_imports)

    obfuscated_code = code_to_save + obfuscator.obfuscate()

    return obfuscated_code


def obfuscate():
    copy_obfuscated_dir()

    files = get_python_files(config.obfuscated_BillyHerrington_directory)

    files_count = len(files)
    obfuscated_files_count = 0
    for file in files:
        with open(file, encoding='utf-8') as f:
            code = f.read()

        progress = round(obfuscated_files_count / files_count * 100)

        print(constants.obfuscate_progress_message.format(files_count=files_count,
                                                          obfuscated_files_count=obfuscated_files_count, progress=progress, default_color=Colors.default_color))

        params = get_params(module=file)

        obfuscated_code = obfuscate_code(code, params)

        with open(file, 'w') as f:
            f.write(obfuscated_code)

        obfuscated_files_count += 1

        Colors.clearLine(2)
