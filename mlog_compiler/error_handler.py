from mlog_compiler.colors import BColors
from mlog_compiler.tokens import Token, Misc
from abc import ABC


class CError(ABC):
    token: Token
    note: str = ''

    def __init__(self, token: Token, additional_information: str = ''):
        self.token = token
        self.note = additional_information

    def throw(self):
        print(self.__repr__())

    def __repr__(self):
        return (f"{BColors.FAIL}"
                f"{self.__class__.__name__}: \n\tline {self.token.line} at column {self.token.column} from token "
                f"`{self.token.lexeme}` ({self.token.__class__.__name__})."
                f"{f"\nNote:\n\t{self.note}\n" if self.note != '' else '\n'}")

class ArgumentError(CError):
    pass

class UndefinedVariable(CError):
    pass

class UnbalancedBrackets(CError):
    def __init__(self, token: Token = None, additional_information: str = ''):
        if token is None:
            token = Misc.Program(0, 0)

        super().__init__(token, additional_information)
