from mlog_compiler.error_handler import UndefinedVariable, CError, UnbalancedBrackets
from mlog_compiler.tokens import Token, Punctuation, Misc, Keyword, Type, Arithmetic, Constant
from mlog_compiler.lexer import lex, example_source
from mlog_compiler.utils import get_nested_classes, is_number


def parse_tokens(token_list: list[Token]) -> Misc.Program | CError:
    ast = Misc.Program(0, 0)
    token_depth: list[Token] = [ast]
    last_keyword: Token | None = None
    last_type: Token | None = None
    variables: list[str] = []
    line_depth: int = 0

    # TODO: assign into its own node and ignore semi-colons.
    # TODO: errors and syntax checking.
    for index, token in enumerate(token_list):
        if token.__class__ in get_nested_classes(Keyword, Token):
            last_keyword = token

        elif isinstance(token, Punctuation.LeftCurlyBracket):
            block_token = Misc.Block(token.line, token.column)
            last_keyword.next_tokens.append(block_token)
            token_depth.append(block_token)
            continue

        elif isinstance(token, Punctuation.LeftParentheses):
            token_depth.append(token_list[index - 1])
            continue

        elif isinstance(token, Punctuation.RightParentheses) or isinstance(token, Punctuation.RightCurlyBracket):
            if len(token_depth) <= 1:
                return UnbalancedBrackets(token, "Make sure you're not closing a non-existing code "
                                                 "block.")

            token_depth.pop()
            continue

        elif token.__class__ in get_nested_classes(Type, Token):
            last_type = token
            continue
            # float x = 3.14159 + 1;

        elif token.__class__ in get_nested_classes(Arithmetic, Token):
            variable = token_depth[-1].next_tokens.pop()

            if not is_number(variable.lexeme):
                variables.append(variable.lexeme)

            token_depth[-1].next_tokens.append(token)
            token.next_tokens.append(token_list[index - 1])
            token_depth.append(token)
            line_depth += 1

            continue

        elif isinstance(token, Punctuation.Semicolon):
            last_type = None

            for _ in range(line_depth):
                token_depth.pop()

            line_depth = 0
            continue

        elif isinstance(token, Punctuation.Comma):
            # I don't intend on making the commas a requirement in the grammar.
            continue

        elif isinstance(token, Misc.Identifier):
            if (token.lexeme not in variables) and (token_list[index - 1].__class__ not in get_nested_classes(Type, Token)):
                return UndefinedVariable(token, "Make sure you've initialized the variable.")

        token_depth[-1].next_tokens.append(token)

    if len(token_depth) != 1:
        return UnbalancedBrackets(token_depth[-1], "Make sure the brackets for this code block are closed.")

    return ast


# https://simonhessner.de/python-3-recursively-print-structured-tree-including-hierarchy-markers-using-depth-first-search/
def print_tree(root, marker_str="+- ", level_markers=[]):
    empty_str = " "*len(marker_str)
    connection_str = "|" + empty_str[:-1]

    level = len(level_markers)
    mapper = lambda draw: connection_str if draw else empty_str
    markers = "".join(map(mapper, level_markers[:-1]))
    markers += marker_str if level > 0 else ""
    print(f"{markers}{(root.__class__.__name__ + ": ").ljust(30, " ")}{root.lexeme}")

    for i, child in enumerate(root.next_tokens):
        is_last = i == len(root.next_tokens) - 1
        print_tree(child, marker_str, [*level_markers, not is_last])


if __name__ == '__main__':
    result = lex(example_source)
    print(example_source)
    ast = parse_tokens(result)

    if isinstance(ast, CError):
        print(ast)
        exit(1)

    print_tree(ast)
