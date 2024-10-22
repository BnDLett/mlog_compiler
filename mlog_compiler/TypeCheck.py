from typing import Any


class TypeCheck:
    @staticmethod
    def ensure_int(value: Any) -> bool:
        if value is None:
            return True

        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def ensure_str(value: Any) -> bool:
        if value is None:
            return True

        try:
            return (value[0] in ("'", '"')) and (value[0] == value[-1])
        except IndexError:
            return False

    @staticmethod
    def ensure_float(value: any):
        if value is None:
            return True

        try:
            float(value)
            return True
        except ValueError:
            return False
