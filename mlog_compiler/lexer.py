from mlog_compiler.tokens import Token, Keyword, Misc, TokenType
from mlog_compiler.tokens import Punctuation
from mlog_compiler.utils import get_nested_classes, is_number


def peek(current_index: int, source_code: str) -> str:
    """
    Peeks at the next character in the sequence.
    """
    next_index = current_index + 1

    if next_index >= len(source_code):
        return ''

    return source_code[next_index]

def lex(source: str):
    current_word = ''
    lexed_tokens: list[Token] = []
    line = 1
    last_index = 0
    in_quotes = False

    for index, char in enumerate(source):
        if char == " " and not in_quotes:
            current_word = ''
            continue

        relative_char_index = (index - last_index) + 1
        current_word += char

        if char == '"' or char == "'":
            if in_quotes:
                lexed_tokens.append(Misc.Constant(line, relative_char_index, current_word))

            in_quotes = not in_quotes
            continue

        if in_quotes:
            continue

        if char in Punctuation.tokens.keys():
            lexed_tokens.append(Punctuation.tokens[char](line, relative_char_index))
            current_word = ''
            continue

        elif peek(index, source) in Punctuation.tokens or peek(index, source) == " ":
            found_token = False

            for token_type in TokenType.__subclasses__():
                if current_word not in token_type.tokens:
                    continue

                found_token = True
                lexed_tokens.append(token_type.tokens[current_word](line, relative_char_index))

            if not found_token:
                if is_number(current_word):
                    lexed_tokens.append(Misc.Constant(line, relative_char_index, current_word))
                    continue

                lexed_tokens.append(Misc.Identifier(line, relative_char_index, current_word))

            # else:
            #     lexed_tokens.append(Misc.Identifier(line, relative_char_index, current_word))

            current_word = ''

        if char == "\n":
            last_index = index
            line += 1
            current_word = ''
            continue

    print([x.__class__.__name__ for x in lexed_tokens])
    print([x.lexeme for x in lexed_tokens])
    print([(x.line, x.column) for x in lexed_tokens])


if __name__ == '__main__':
    example_source = "print(\"lorem ipsum\", 6);\nbool x = false;"
    print(example_source)
    lex(example_source)
