from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_argparse import ArgumentParser


class Arguments(BaseModel):
    file: str = Field(description="a file path")
    password: str = Field(description="a required decrypt password")
    key: Optional[str] = Field(description="a required key")


def sys_args() -> dataclass:
    parser = ArgumentParser(
        model=Arguments,
        prog="Encrypting Program",
        description="Script that encrypt/decrypt binary files.",
        version="0.0.1",
    )
    return parser.parse_typed_args()
