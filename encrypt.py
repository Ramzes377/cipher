import secrets
import pickle
import argparse
from functools import partial
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
ITERATION_NUM = 123_456
password = ''


def derive_key(password: bytes,
               salt: bytes,
               iterations: int = ITERATION_NUM) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str,
                     iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


def encrypy_data(data) -> dict:
    func = partial(password_encrypt, password=password)
    return {
        func(k.encode()): [func(i.encode()) for i in v]
        for k, v in
        data.items()
    }


def dump_obj_to_file(file_name, object):
    with open(file_name, 'wb') as f:
        pickle.dump(object, f)


def decrypt_data(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    func = partial(password_decrypt, password=password)
    decoded = {func(k).decode(): [func(i).decode() for i in v] for k, v in
               data.items()}
    return decoded


def get_args():
    global password
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Destination file name", type=str, default='')
    parser.add_argument("-p", "--pass", dest="password", help="crypt password",
                        type=str, default='88005553535')
    parser.add_argument("-k", "--key", dest="key", help="requested item",
                        type=str, default='')
    args = parser.parse_args()
    password = args.password
    return args.filename, args.key


if __name__ == '__main__':
    file, key = get_args()
    print(
        f'Start find in file: {file}\n'
        f'With password: {password}\n'
        f'With Key: {key}'
    )
    item = decrypt_data(file_path).get(key)
    if item is not None:
        print(f'\n\nLogin: {item[0]}\nPassword: {item[1]}\n')
