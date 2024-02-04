import json
import os
import pickle
import warnings
from typing import Any, Type, Callable

import pytest

from src.api.loaders import BinaryLoader, Loader, JSONLoader, PickleLoader

save_path = './tests/data/binary_test'
encode_save_path = save_path + '_encode'
decode_save_path = save_path + '_decode'

warnings.simplefilter("always")


class _TestClass:
    x = 1
    y = '2'

    def __init__(self):
        self.z = 'wow'


class _TestLoader:
    loader: Loader = None
    encode_to_write: Any = None
    decode_to_write: Any = None

    @staticmethod
    def _return_type(func: Callable) -> Type:
        return func.__annotations__.get('return', object)

    def _write_test(self, data: bytes, path: str):
        self.loader.write(data, path)

        assert os.path.isfile(path)

        yield

        os.remove(path)

    @pytest.fixture
    def test_encode_write(self):
        yield from self._write_test(self.encode_to_write, encode_save_path)

    @pytest.fixture
    def test_decode_write(self):
        yield from self._write_test(self.decode_to_write, decode_save_path)

    def test_load(self, test_encode_write, test_decode_write):
        encode_type = self._return_type(self.loader.encode_load)
        r = self.loader.encode_load(encode_save_path)

        if encode_type is not Any:
            assert isinstance(r, encode_type)

        decode_type = self._return_type(self.loader.decode_load)
        r = self.loader.decode_load(decode_save_path)

        if decode_type is not Any:
            assert isinstance(r, decode_type)
        else:
            w = f'Function {self.loader.decode_load} have \'Any\' return annotation'
            warnings.warn(w, UserWarning)


class TestBinaryLoader(_TestLoader):
    loader = BinaryLoader

    encode_to_write = 'abc321'.encode()
    decode_to_write = 'abc321'.encode()


class TestJSONLoader(_TestLoader):
    loader = JSONLoader
    encode_to_write = json.dumps({1: 2, '3': [4, None]}).encode()
    decode_to_write = json.dumps({1: 2, '3': [4, None]}).encode()


class TestPickleLoader(_TestLoader):
    loader = PickleLoader

    encode_to_write = pickle.dumps(_TestClass)
    decode_to_write = pickle.dumps(_TestClass)
