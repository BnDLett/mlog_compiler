from abc import ABC, abstractmethod


class BuiltinFunction(ABC):
    arguments: tuple[type]

    # TODO: Figure this out
    @abstractmethod
    def get_representation(self, arguments: list) -> tuple[str]:
        pass


# TODO: Name this better
class BuiltinFunctions:
    class Printf(BuiltinFunction):
        arguments = (str, int)

        def get_representation(self, arguments: list[str, int]) -> tuple[str, str]:
            return f'print {list[0]}', f'printflush message{arguments[1]}'
