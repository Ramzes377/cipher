import json
import pickle
from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Optional, Any, Type

from src.api.encryptor import TextCryptor
from src.api.exceptions import SerializationException, DeSerializationException
from src.api.loaders import BinaryLoader, PickleLoader, Loader, JSONLoader, \
    NestedLoader
from src.utils import apply_recursive, JSONLike, SerializerEnum


class CryptorDecodeMixin:
    @staticmethod
    def _encrypt(data: bytes, password: str) -> bytes:
        return TextCryptor.encrypt(data, password=password)

    @staticmethod
    def _decrypt(data: bytes, password: str) -> bytes:
        return TextCryptor.decrypt(data, password=password)


class AbstractSerializer(metaclass=ABCMeta):
    loader: Loader = None

    @abstractmethod
    def encode(self, *args, **kwargs) -> bytes:
        ...

    @abstractmethod
    def serialize(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def decode(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def deserialize(self, *args, **kwargs) -> Any:
        ...


class BaseSerializer(AbstractSerializer, CryptorDecodeMixin):
    loader = BinaryLoader

    @staticmethod
    def encode(data: Any, *args, **kwargs) -> bytes:
        return data.encode()

    @classmethod
    def serialize(
            cls,
            password: str,
            data: Optional[bytes] = None,
            path: Optional[str] = None,
    ) -> bytes:

        if path is not None:
            data = cls.loader.encode_load(path)

        if data is None:
            raise SerializationException

        serialized = cls.encode(data, password=password)
        encrypted = cls._encrypt(data=serialized, password=password)
        return encrypted

    @staticmethod
    def decode(data: bytes, *args, **kwargs) -> str:
        return data.decode()

    @classmethod
    def deserialize(
            cls,
            password: str,
            path: Optional[str] = None,
            data: Optional[JSONLike] = None,
    ) -> Any:
        if path is not None:
            data = cls.loader.decode_load(path)

        if data is None:
            raise DeSerializationException

        decrypted = cls._decrypt(data=data, password=password)
        deserialized = cls.decode(data=decrypted, password=password)
        return deserialized


class PlainSerializer(BaseSerializer):
    """Simplest serializer. """


class JSONSerializer(BaseSerializer):
    """ Serializer for JSON-like objects. """

    loader = JSONLoader

    @staticmethod
    def encode(data: JSONLike, *args, **kwargs) -> bytes:
        return json.dumps(data).encode()

    @staticmethod
    def decode(data: Any, *args, **kwargs) -> dict:
        return json.loads(data)


class PickleSerializer(BaseSerializer):
    """ Serializer for dump python objects. """

    loader = PickleLoader

    @staticmethod
    def encode(data: Any, *args, **kwargs) -> bytes:
        return pickle.dumps(data)

    @staticmethod
    def decode(data: Any, *args, **kwargs) -> JSONLike:
        return pickle.loads(data)


class NestedStructureSerializer(BaseSerializer):
    """ Stronger than JSONSerializer serializer for JSON-like objects. """

    loader = NestedLoader

    @classmethod
    def encode(cls, data: Any, *args, **kwargs) -> bytes:
        def handler(x):
            return cls._encrypt(data=x.encode(), password=kwargs['password'])

        nested_modified = apply_recursive(func=handler, obj=data)
        encoded = pickle.dumps(nested_modified)

        return encoded

    @classmethod
    def decode(cls, data: Any, *args, **kwargs) -> JSONLike:
        decrypt = partial(super()._decrypt, password=kwargs['password'])
        return apply_recursive(func=lambda x: decrypt(x).decode(), obj=data)

    @staticmethod
    def _decrypt(data: bytes, password: str) -> Any:
        return pickle.loads(TextCryptor.decrypt(data, password=password))


serializers: dict[SerializerEnum, Type[BaseSerializer]] = {
    SerializerEnum.plain: PlainSerializer,
    SerializerEnum.json: JSONSerializer,
    SerializerEnum.pickle: PickleSerializer,
    SerializerEnum.nested: NestedStructureSerializer,
}
