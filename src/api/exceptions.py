from dataclasses import dataclass
from typing import Optional


@dataclass
class _BaseException(Exception):
    @property
    def message(self) -> Optional[str]:
        return


@dataclass
class FileReadException(_BaseException):
    @property
    def message(self) -> str:
        return 'Error file read!'


@dataclass
class SerializationException(_BaseException):
    @property
    def message(self) -> str:
        return 'Serialization error. Empty serialization data!'


@dataclass
class DeSerializationException(_BaseException):

    @property
    def message(self) -> str:
        return 'Deserialization error. Probably empty deserialization data!'


@dataclass
class UndefinedSerializerException(_BaseException):
    serializer: str

    @property
    def message(self) -> str:
        return f'Undefined serializator named {self.serializer} data!'
