import json
from abc import ABCMeta, abstractmethod
from typing import Any

from src.api.exceptions import FileReadException
from src.utils import JSONLike


class AbstractReader(metaclass=ABCMeta):

    @abstractmethod
    def encode_load(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def decode_load(self, *args, **kwargs) -> Any:
        ...


class AbstractWriter(metaclass=ABCMeta):

    @abstractmethod
    def write(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def _prepare_deserialized(self, *args, **kwargs) -> bytes:
        ...


class AbstractLoader(AbstractReader, AbstractWriter, metaclass=ABCMeta):
    ...


class Loader(AbstractLoader):
    @staticmethod
    def _read(path: str) -> bytes:
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            raise FileReadException
        return data

    @classmethod
    def encode_load(cls, path: str) -> bytes:
        return cls._read(path=path)

    @classmethod
    def decode_load(cls, path: str) -> bytes:
        return cls._read(path=path)

    @staticmethod
    def write(data: bytes, path: str) -> None:
        with open(path, 'wb') as f:
            f.write(data)

    @staticmethod
    def _prepare_deserialized(data: str) -> bytes:
        return data.encode()

    @classmethod
    def write_deserialized(cls, data: Any, path: str) -> None:
        encoded = cls._prepare_deserialized(data)
        cls.write(data=encoded, path=path)


class BinaryLoader(Loader):
    ...


class PickleLoader(Loader):
    ...


class JSONLoader(Loader):

    @classmethod
    def encode_load(cls, path: str) -> JSONLike:
        return json.loads(cls._read(path=path))

    @staticmethod
    def _prepare_deserialized(data: JSONLike) -> bytes:
        return json.dumps(data).encode()


class NestedLoader(JSONLoader):
    ...
