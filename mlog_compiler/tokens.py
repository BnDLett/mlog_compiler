from __future__ import annotations
import typing

from mlog_compiler.library import BuiltinFunctions


class Token:
    lexeme: str = ''
    literal: typing.Any = None
    next_tokens = []
    line: int
    column: int
    # Whether you can reference the token/keyword/whatever in the source code.
    not_referencable = False

    def __init__(self, line: int, column: int, next_tokens: list[Token] | None = None):
        if next_tokens is None:
            next_tokens = []

        self.line = line
        self.column = column
        self.next_tokens = next_tokens


class TokenType:
    """
    A type of token. Such as keywords and punctuations.
    """
    tokens: [str, Token]


class Punctuation(TokenType):
    class LeftParentheses(Token):
        lexeme = "("

    class RightParentheses(Token):
        lexeme = ")"

    class LeftCurlyBracket(Token):
        lexeme = "{"

    class RightCurlyBracket(Token):
        lexeme = "}"

    class LeftSquareBracket(Token):
        lexeme = "["

    class RightSquareBracket(Token):
        lexeme = "]"

    class Colon(Token):
        lexeme = ":"

    class Semicolon(Token):
        lexeme = ";"

    class Comma(Token):
        lexeme = ","


class Constant(TokenType):
    class TrueConstant(Token):
        lexeme = 'true'

    class FalseConstant(Token):
        lexeme = 'false'


class Keyword(TokenType):
    class Print(Token):
        lexeme = "printf"
        literal = BuiltinFunctions.Printf

    class If(Token):
        lexeme = "if"
        literal = None


class Type(TokenType):
    class Int(Token):
        lexeme = 'int'

    class Float(Token):
        lexeme = 'float'

    class String(Token):
        lexeme = 'string'

    class Boolean(Token):
        lexeme = "bool"


class Arithmetic(TokenType):
    class Assign(Token):
        lexeme = "="

    class Add(Token):
        lexeme = "+"

    class Subtract(Token):
        lexeme = "-"

    class Multiply(Token):
        lexeme = "*"

    class Divide(Token):
        lexeme = "/"


class Misc(TokenType):
    class Identifier(Token):
        def __init__(self, line: int, column: int, lexeme: str, next_tokens: list[Token] | None = None):
            super().__init__(line, column, next_tokens)

            self.lexeme = lexeme

    class Constant(Token):
        constant_type: Token

        def __init__(self, line: int, column: int, lexeme: str, constant_type: Token,
                     next_tokens: list[Token] | None = None):
            super().__init__(line, column, next_tokens)

            self.lexeme = lexeme
            self.constant_type = constant_type

    class Program(Token):
        lexeme = "PROGRAM"
        not_referencable = True

    class Block(Token):
        lexeme = "CODE_BLOCK"
        not_referencable = True

    class Variable(Token):
        lexeme = "VARIABLE"
        not_referencable = True

    class Reassignment(Token):
        lexeme = "REASSIGNMENT"
        not_referencable = True


if __name__ == '__main__':
    print(Punctuation.tokens)
    print(Keyword.tokens)
    print(Misc.tokens)
