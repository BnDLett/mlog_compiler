from http.cookiejar import cut_port_re

from mlog_compiler.tokens import Token, Misc, TokenType, Type
from mlog_compiler.tokens import Punctuation
from mlog_compiler.utils import is_number, peek, get_number_type


def lex(source: str):
    """
    Lexes source code into a list of tokens.
    """
    current_word = ''
    lexed_tokens: list[Token] = []
    line = 1
    last_index = 0
    in_quotes = False
    in_comment = False

    for index, char in enumerate(source):
        if char == " " and not in_quotes:
            current_word = ''
            continue

        relative_char_index = (index - last_index) + 1
        current_word += char

        if (char == '"' or char == "'") and not in_comment:
            if in_quotes:
                lexed_tokens.append(Misc.Constant(line, relative_char_index, current_word, Type.String))

            in_quotes = not in_quotes
            continue

        elif char == "/" and peek(index, source) == "/":
            in_comment = True

        elif char == "\n":
            if in_comment:
                in_comment = False

            last_index = index + 1
            line += 1
            current_word = ''
            continue

        if in_quotes or in_comment:
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

                token = token_type.tokens[current_word](line, relative_char_index)

                if token.not_referencable:
                    continue

                found_token = True
                lexed_tokens.append(token)

            if not found_token:
                if is_number(current_word):
                    number_type = get_number_type(current_word)
                    lexed_tokens.append(Misc.Constant(line, relative_char_index, current_word, number_type))
                    continue

                lexed_tokens.append(Misc.Identifier(line, relative_char_index, current_word))

            current_word = ''

    return lexed_tokens


example_source = """printf("Hello, world", 1);
// printf("// This is not a comment");
// x;

if (true) {
    if (true) {
        printf("moai", 3);
    }

    printf(\"lorem ipsum\", 6);
    bool x = false;
    // hello, world!
    
    float y = 3.14159 * 2.;
    float z = 3 + y * y + 2;
}
"""

if __name__ == '__main__':
    print(example_source)
    result = lex(example_source)

    print([x.lexeme for x in result])
    print([x.__class__.__name__ for x in result])
    print([(x.line, x.column) for x in result])
