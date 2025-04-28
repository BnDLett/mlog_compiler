from mlog_compiler.tokens import Token, Punctuation, Misc, Keyword, Type
from mlog_compiler.lexer import lex, example_source
from mlog_compiler.utils import get_nested_classes


def parse_tokens(token_list: list[Token]):
    ast = Misc.Program(0, 0)
    token_depth: list[Token] = [ast]
    last_keyword: Token | None = None
    variables: list[str]

    # TODO: assign into its own node and ignore semi-colons.
    # TODO: errors and syntax checking.
    for index, token in enumerate(token_list):
        if token.__class__ in get_nested_classes(Keyword, Token):
            last_keyword = token

        elif isinstance(token, Punctuation.LeftCurlyBracket):
            block_token = Misc.Block(last_keyword.line, last_keyword.column)
            last_keyword.next_tokens.append(block_token)
            token_depth.append(block_token)
            continue

        elif isinstance(token, Punctuation.LeftParentheses):
            token_depth.append(token_list[index - 1])
            continue

        elif isinstance(token, Punctuation.RightParentheses) or isinstance(token, Punctuation.RightCurlyBracket):
            token_depth.pop()
            continue

        elif token.__class__ in get_nested_classes(Type, Token):
            variable_token = Misc.Variable(token.line, token.column)
            token_depth.append(variable_token)
            # float x = 3.14159;

        # elif

        token_depth[-1].next_tokens.append(token)

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
    print_tree(ast)
