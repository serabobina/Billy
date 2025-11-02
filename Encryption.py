import config
import random


def generate_random_string(length: int, alth: set):
    string = ''

    for _ in range(length):
        string += random.choice(alth)

    return string


def create_encryption_keys():
    encryption_keys = config.encryption_keys_sample

    configuration_ek = generate_random_string(
        config.encryption_key_length, config.encryption_alth)

    salt = "Billy_is_the_best"

    keylogger_ek = generate_random_string(
        config.encryption_key_length, config.encryption_alth)

    encryption_keys = encryption_keys.format(
        configuration_ek=configuration_ek, keylogger_ek=keylogger_ek, salt=salt)

    with open(config.encryption_keys_path, 'w', encoding='utf-8') as file:
        file.write(encryption_keys)

    answer = {'configuration_ek': ['Configuration encryption key', configuration_ek],
              'keylogger_ek': ['Keylogger encryption key', keylogger_ek],
              'salt': ['Salt', salt]}
    return answer
