import json
import pickle
from abc import ABCMeta, abstractmethod

from typing import Any

from src.api.exceptions import FileReadException


class AbstractLoader(metaclass=ABCMeta):

    @abstractmethod
    def load(self, *args, **kwargs) -> Any:
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

    @staticmethod
    def write(data: bytes, path: str) -> None:
        with open(path, 'wb') as f:
            f.write(data)

    @classmethod
    def load(cls, path: str) -> bytes:
        return cls._read(path=path)


class BinaryLoader(Loader):
    @classmethod
    def load(cls, path: str) -> bytes:
        return super().load(path=path)


class PickleLoader(BinaryLoader):
    @classmethod
    def load(cls, path: str) -> Any:
        return pickle.loads(super().load(path=path))


class JSONLoader(BinaryLoader):
    @classmethod
    def load(cls, path: str) -> dict | list:
        return json.loads(super().load(path=path))
