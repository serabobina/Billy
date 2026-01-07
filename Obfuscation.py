from BlankOBFv2 import BlankOBFv2
import os
import config
from pathlib import Path
import shutil
import constants
import Colors

obfuscation_suffixes = ['.py', '.pyw']


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


def obfuscate_code(code):
    obfuscator = BlankOBFv2(code=code,
                            include_imports=True)

    obfuscated_code = obfuscator.obfuscate()

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

        obfuscated_code = obfuscate_code(code)

        with open(file, 'w') as f:
            f.write(obfuscated_code)

        obfuscated_files_count += 1

        Colors.clearLine(2)
