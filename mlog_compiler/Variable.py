from time import time_ns


class Variable:
    id: int
    name: str
    type: str

    def __init__(self, name: str, type: str):
        self.name = name
        self.id = time_ns()
