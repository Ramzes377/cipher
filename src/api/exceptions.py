from dataclasses import dataclass


@dataclass
class _BaseException(Exception):
    _message = None

    def __str__(self):
        return self._message


class FileReadException(_BaseException):
    _message = 'Error file read!'


class SerializationException(_BaseException):
    _message = 'Empty serialization data!'


class DeSerializationException(_BaseException):
    _message = 'Empty deserialization data!'
