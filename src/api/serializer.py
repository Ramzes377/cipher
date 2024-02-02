import json
from abc import ABCMeta, abstractmethod

from typing import Optional, Any, Callable

from src.api.encryptor import TextCryptor
from src.api.exceptions import SerializationException, DeSerializationException
from src.api.loader import BinaryLoader, PickleLoader


class CryptorDecodeMixin:
    @staticmethod
    def _encrypt(data: bytes, password: str) -> bytes:
        return TextCryptor.encrypt(data, password=password)

    @staticmethod
    def _decrypt(data: bytes, password: str) -> str:
        return TextCryptor.decrypt(data, password=password).decode()


class AbstractSerializer(metaclass=ABCMeta):
    output_name: str = 'output'
    input_name: str = 'input'

    @abstractmethod
    def serialize(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def deserialize(self, *args, **kwargs) -> Any:
        ...


class BaseSerializer(AbstractSerializer, CryptorDecodeMixin):
    loader = BinaryLoader

    @classmethod
    def serialize(
            cls,
            password: str,
            data: Optional[str] = None,
            path: Optional[str] = None,
            data_preprocess: Optional[Callable] = None,
    ) -> bytes:

        if path is not None:
            data = cls.loader.load(path)
            if data_preprocess:
                data = data_preprocess(data)
            return cls._encrypt(data=data, password=password)

        if data is None:
            raise SerializationException

        if data_preprocess:
            data = data_preprocess(data)

        return cls._encrypt(data=data.encode(), password=password)

    @classmethod
    def deserialize(
            cls,
            password: str,
            data: Optional[dict] = None,
            path: Optional[str] = None,
            data_postprocess: Optional[Callable] = None,
    ) -> Any:
        if path is not None:
            data = cls.loader.load(path)

        if data is None:
            raise DeSerializationException
        decrypted = cls._decrypt(data=data, password=password)

        if data_postprocess:
            return data_postprocess(decrypted)

        return decrypted


class PlainSerializer(BaseSerializer):
    ...


class JSONSerializer(BaseSerializer):

    @classmethod
    def serialize(cls, *args, **kwargs) -> bytes:
        return super().serialize(*args, **kwargs, data_preprocess=json.dumps)

    @classmethod
    def deserialize(cls, *args, **kwargs) -> dict | list:
        return super().deserialize(*args, **kwargs, data_postprocess=json.loads)


class PickleSerializer(PlainSerializer):
    loader = PickleLoader

# class NestedStructureSerializer(JSONSerializer):
#
#     @classmethod
#     def _dict_serialize(
#             cls,
#             handler: Callable,
#             data: dict,
#             password: str,
#     ) -> dict:
#         handle = partial(handler, password=password)
#         return {
#             handle(k): [handle(i) for i in v]
#             for k, v in data.items()
#         }
#
#     @classmethod
#     def serialize(cls, *args, **kwargs) -> bytes:
#         print(args, kwargs)
#         data = cls._dict_serialize(handler=cls._encrypt, **kwargs)
#         return super().serialize(*args, **kwargs)
#         # if path is not None:
#         #     data = cls.loader.load(path)
#         #
#         # # data = pickle.dumps(data)
#         #
#         # return cls._dict_serialize(cls._encrypt, data, password)
#
#     @classmethod
#     def deserialize(cls, *args, **kwargs) -> dict | list:
#         return cls._dict_serialize(*args, **kwargs)
#         # data = cls.loader.load(path)
#         # return cls._dict_serialize(cls._decrypt, data, password)
