import inspect
from collections.abc import Iterable, Sized
from mlog_compiler.tokens import Type, Token, TokenType


# https://stackoverflow.com/a/42326409
def get_nested_classes(cls, parent_class) -> list:
    return [cls_attribute for cls_attribute in cls.__dict__.values()
            if inspect.isclass(cls_attribute)
            and issubclass(cls_attribute, parent_class)]


def update_token_dict():
    """
    Updates the token dictionary of **all** TokenType subclasses.
    """

    for token_type in TokenType.__subclasses__():
        token_type.tokens = {}

        classes = get_nested_classes(token_type, Token)

        for cls in classes:
            if cls.lexeme == '':
                continue

            token_type.tokens[cls.lexeme] = cls


def is_number(x: str) -> bool:
    # "." isn't a numeral per se, but it can be used in floats.
    numerals = '1234567890.'

    for char in x:
        if char not in numerals:
            return False

    return True


def get_number_type(x: str) -> Token:
    """
    Evaluates the type of number in a string. Returns Type.Float if it is a float, and Type.Int if it is an integer.
    This will throw a ValueError if the provided argument is not a number.
    """
    if not is_number(x):
        raise ValueError("Value provided is not a number.")

    if "." in x:
        return Type.Float

    return Type.Int


def peek(current_index: int, iterable: Iterable) -> str:
    """
    Peeks at the next character in the sequence.
    """
    next_index = current_index + 1

    if next_index >= len(iterable):
        return ''

    return iterable[next_index]


update_token_dict()
