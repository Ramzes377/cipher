import os.path

import pytest
from pytest import mark

from src.api.serializer import JSONSerializer, PlainSerializer, \
    AbstractSerializer, PickleSerializer

password: str = '1234567890987654321'
test_path: str = './tests/data/'


class _TestSerializer:
    serializer: AbstractSerializer = None

    test_save_name: str = None
    test_data: str = None

    @property
    def save_path(self) -> str:
        return os.path.join(test_path, self.test_save_name)

    @pytest.fixture
    def serialize(self):
        serialized = self.serializer.serialize(
            data=self.test_data,
            password=password
        )

        PlainSerializer.loader.write(
            data=serialized,
            path=self.save_path
        )

        assert os.path.isfile(self.save_path)

        yield

        os.remove(self.save_path)

    def test_deserialize(self, serialize):
        data = self.serializer.deserialize(
            path=self.save_path,
            password=password
        )

        assert self.test_data == data


class TestPlainSerializer(_TestSerializer):
    serializer = PlainSerializer

    test_save_name = 'plain-serialized'
    test_data = 'some data 321'


class TestJSONSerializer(_TestSerializer):
    serializer = JSONSerializer

    test_save_name = 'json-serialized'
    test_data = {'1': 2, '3': '4', '5': None}


@mark.skip  # currently not worked serializer
class TestNestedStructureSerializer(_TestSerializer):
    serializer = None

    test_save_name = 'nested-serialized'
    test_data = {'1': ['nested-data', 'another-data'], '2': ['kek']}


@mark.skip  # currently not worked serializer
class TestPickleSerializer(_TestSerializer):
    serializer = PickleSerializer

    test_save_name = 'pickle-serialized'
    test_data = type('TestClass', tuple(), dict(x=1, y=2))
