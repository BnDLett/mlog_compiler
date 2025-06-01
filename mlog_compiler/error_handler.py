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

class CTypeError(CError):
    def __init__(self, token: Token, operand_x: Token, operand_y: Token, additional_information: str = ''):
        explanation = (f"\n\tFirst operand is of type {__get_operand_type__(operand_x)} but second operand is of type"
                       f" {__get_operand_type__(operand_y)}.")

        super().__init__(token, additional_information + explanation)


def __get_operand_type__(operand: Token) -> str:
    if isinstance(operand, Misc.Identifier):
        return operand.ctype.__name__
    elif isinstance(operand, Misc.Constant):
        return operand.constant_type.__name__

    return operand.__name__
