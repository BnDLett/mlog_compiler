import inspect
from collections.abc import Iterable, Sized


# https://stackoverflow.com/a/42326409
def get_nested_classes(cls, parent_class) -> list:
    return [cls_attribute for cls_attribute in cls.__dict__.values()
            if inspect.isclass(cls_attribute)
            and issubclass(cls_attribute, parent_class)]


def is_number(x: str) -> bool:
    # "." isn't a numeral per se, but it can be used in floats.
    numerals = '1234567890.'

    for char in x:
        if char not in numerals:
            return False

    return True


def peek(current_index: int, iterable: Iterable) -> str:
    """
    Peeks at the next character in the sequence.
    """
    next_index = current_index + 1

    if next_index >= len(iterable):
        return ''

    return iterable[next_index]
