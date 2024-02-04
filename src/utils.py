from enum import Enum
from typing import Optional, Callable, TypeAlias

from pydantic import BaseModel, Field
from pydantic_argparse import ArgumentParser

JSONLike: TypeAlias = dict | list


class CryptionMode(Enum):
    encrypt = 'encrypt'
    decrypt = 'decrypt'


class SerializerEnum(Enum):
    plain = 'plain'
    json = 'json'
    pickle = 'pickle'
    nested = 'nested'


class Arguments(BaseModel):
    mode: CryptionMode = Field(
        description='encrypt/decrypt mode',
        default=CryptionMode.encrypt
    )

    input_file: Optional[str] = Field(description='path to a file to encode')
    output_file: Optional[str] = Field(
        description='path to output file',
        default='output'
    )

    password: str = Field(description='a required decrypt password')
    key: Optional[str] = Field(description='a required key')

    serializer: SerializerEnum = Field(
        description='Serializers. Default: plain',
        default='plain'
    )


def sys_args() -> Arguments:
    parser = ArgumentParser(
        model=Arguments,
        prog='Encrypting Program',
        description='Script that encrypt/decrypt binary files.',
        version='0.0.1',
    )
    return parser.parse_typed_args()


def apply_recursive(func: Callable, obj: JSONLike) -> JSONLike:
    if isinstance(obj, dict):
        return {func(k): apply_recursive(func, v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [apply_recursive(func, elem) for elem in obj]

    return func(obj)
