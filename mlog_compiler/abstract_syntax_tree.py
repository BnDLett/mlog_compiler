from mlog_compiler.tokens import Token, Punctuation, Misc
from mlog_compiler.lexer import lex, example_source


def parse_tokens(token_list: list[Token]):
    token_depth: list[int] = []

    for index, token in enumerate(token_list):
        print(token_depth)

        if isinstance(token, Punctuation.LeftParentheses):
            token_depth.append(index)
            continue

        elif isinstance(token, Punctuation.RightParentheses):
            token_depth.pop()
            continue

        token_depth[index].next_tokens.append(token)

    return


if __name__ == '__main__':
    result = lex(example_source)
    print(example_source)
    parse_tokens(result)
    pass
