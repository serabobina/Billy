from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode
import os
import random
import encryption_keys


salt = encryption_keys.salt.encode()


def encrypt(string: str, password: str):
    string = string.encode()
    password = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = urlsafe_b64encode(kdf.derive(password))

    cipher_suite = Fernet(key)

    encrypted_string = cipher_suite.encrypt(string)

    return encrypted_string.decode()


def decrypt(string: str, password: str):

    string = string.encode()

    password = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = urlsafe_b64encode(kdf.derive(password))

    cipher_suite = Fernet(key)

    decrypted_string = cipher_suite.decrypt(string)

    return decrypted_string.decode()
