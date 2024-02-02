import secrets

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TextCryptor:
    iterations = 123_456
    backend = default_backend()
    default_salt = secrets.token_bytes(16)

    @classmethod
    def derive_key(
            cls,
            encoded_password: bytes,
            salt: bytes,
            iterations: int
    ) -> bytes:
        """Derive a secret key from a given password and salt"""

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            backend=cls.backend,
            iterations=iterations,
            length=32,
        )

        return b64e(kdf.derive(encoded_password))

    @classmethod
    def encrypt(
            cls,
            binary_data: bytes,
            password: str,
    ) -> bytes:
        """ Encrypt binary data """

        key = cls.derive_key(
            password.encode(),
            salt=cls.default_salt,
            iterations=cls.iterations,
        )

        return b64e(
            b'%b%b%b' % (
                cls.default_salt,
                cls.iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(binary_data)),
            )
        )

    @classmethod
    def decrypt(
            cls,
            token: bytes,
            password: str,
    ) -> bytes:
        """ Decrypt binary data """

        decoded = b64d(token)
        salt, iter_, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter_, 'big')
        key = cls.derive_key(
            password.encode(),
            salt=salt,
            iterations=iterations
        )
        return Fernet(key).decrypt(token)
