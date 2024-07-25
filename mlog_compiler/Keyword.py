from typing import Callable


class Keyword:
    callback: Callable
    expected_arguments: int
    raw: bool

    def __init__(self, func: Callable, expected_arguments: int, raw: bool):
        self.callback = func
        self.expected_arguments = expected_arguments
        self.raw = raw
