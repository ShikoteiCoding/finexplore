from __future__ import annotations

import asyncio

from typing import Type, TypeVar
from argparse import ArgumentParser
from typing import Any, TextIO

commands: dict[str, Type[Command]] = dict()

T = TypeVar("T", bound=Type["Command"])


def register(cmd: T) -> T:
    """
    Decorator to register a command to the commands module.
    """
    commands[cmd.name] = cmd
    return cmd


class Command:
    name: str

    def __init__(self, args: Any, stream: TextIO) -> None:
        self.args = args
        self.stream = stream

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        return

    def run(self):
        return asyncio.run(self.run_async())  # type: ignore
