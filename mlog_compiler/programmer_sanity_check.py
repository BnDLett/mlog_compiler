from mlog_compiler.error_handler import CTypeError, CError, UndefinedVariable
from mlog_compiler.tokens import Token, Arithmetic, Misc
from mlog_compiler.utils import get_nested_classes, get_type


def type_check_tree(token: Token) -> None | CError | Token:
    if isinstance(token, Arithmetic.Assign):
        return type_check_assignment(token)

    elif isinstance(token, Misc.Program):
        return type_check_tokens(token.next_tokens)

    elif token.__class__ not in get_nested_classes(Arithmetic, Token):
        return type_check_tokens(token.next_tokens)

    if len(token.next_tokens) == 0:
        if isinstance(token, Misc.Constant) or isinstance(token, Misc.Identifier):
            return get_type(token)

        return None

    elif len(token.next_tokens) == 2:
        return type_check_arithmetics(token)

    return None


def type_check_tokens(tokens: list[Token]):
    for token in tokens:
        result = type_check_tree(token)

        if isinstance(result, CTypeError):
            return result


def type_check_arithmetics(token: Token) -> CTypeError | Token:
    first_operand = token.next_tokens[0]
    second_operand = token.next_tokens[1]

    if len(second_operand.next_tokens) != 0:
        second_operand = type_check_tree(second_operand)

    if isinstance(second_operand, CTypeError):
        return second_operand

    first_operand_type = get_type(first_operand)
    second_operand_type = get_type(second_operand)

    if first_operand_type != second_operand_type:
        return CTypeError(token, first_operand, second_operand, "Type mismatch.")

    # Returns the type of the first operand so that nested arithmetics can be type checked.
    return first_operand


def type_check_assignment(token: Token) -> None | CError:
    identifier = token.next_tokens[0]
    value = token.next_tokens[1]

    if not isinstance(identifier, Misc.Identifier):
        return CError(token, "Expected identifier, but no identifier was found.")

    actual_type = get_type(value)

    if isinstance(actual_type, CError):
        # print(value)
        value = type_check_tree(value)
        actual_type = get_type(value)

    if isinstance(value, CError):
        return value

    elif actual_type != identifier.ctype:
        return CTypeError(token, identifier, actual_type, "Type mismatch.")

    return None


def __main__():
    from lexer import lex, example_source
    from abstract_syntax_tree import parse_tokens, print_tree
    from error_handler import CError

    tokens = lex(example_source)
    print(example_source)
    ast = parse_tokens(tokens)

    if isinstance(ast, CError) or isinstance(ast, UndefinedVariable):
        print(ast)
        exit(1)

    print_tree(ast)
    print()
    result = type_check_tree(ast)

    if isinstance(result, CTypeError):
        print(result)
        exit(1)

    print("No type errors found.")


if __name__ == "__main__":
    __main__()
