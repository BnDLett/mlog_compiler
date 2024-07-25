from typing import Callable

from Exceptions import NoKeywordFound
from Variable import Variable
from Keyword import Keyword


class BaseCompiler:
    code: list[str]
    keywords: dict[str, Keyword]
    last_scope: str = 'global'
    compiled_result: list = []
    variables: dict[str, Variable]

    def __init__(self, code: str | list) -> None:
        if type(code) is str:
            code: list = code.split(';')

        self.code = code
        self.keywords = {}

    def register_keyword(self, keyword_name: str, parameters: int, *, raw_keyword: bool = False):
        """
        Register a new keyword into the compiler.
        :param func: A lambda function that is executed whenever the keyword is found.
        :param keyword_name: The name of the keyword.
        :param parameters: The amount of parameters accepted in the keyword.
        :param raw_keyword: A boolean value that determines whether the line alone is given. True to give the line
        itself, False to give the regular parameters.
        :return:
        """

        def inner(func):
            # self.keywords[keyword_name] = (func, raw_keyword, parameters)
            self.keywords[keyword_name] = Keyword(func, parameters, raw_keyword)
            return func

        return inner

    def compile_line(self, index):
        """
        Do NOT call this function in random order. Always start at a specified index and iterate UP.
        """
        line: str = self.code[index]
        if line.strip().startswith("//"):
            return

        keyword_name = self.find_keyword_in_line(line, index)
        keyword = self.keywords[keyword_name]

        if keyword.raw:
            result = keyword.callback(self, line)
            self.compiled_result.append(result)

        tuple_in_line = self.parse_tuples_in_line(line, index)

        length_difference = len(tuple_in_line) - keyword.expected_arguments
        if length_difference > 0:
            raise TypeError(f"Line {index} calls a function but provides {length_difference} extra argument(s) than"
                            f" what was expected.")
        if length_difference < 0:
            raise TypeError(f"Line {index} calls a function but provides {-length_difference} less argument(s) than"
                            f" what was expected.")

        result = keyword.callback(self, tuple_in_line)
        self.compiled_result.append(result)

    def find_keyword_in_line(self, line: str, line_index: int) -> str:
        current_word: str = ""
        for index, char in enumerate(line):
            current_word += char

            try:
                next_char = line[index + 1]
            except IndexError:
                next_char = ""

            if (current_word in self.keywords.keys()) and (next_char != " "):
                return current_word

        raise NoKeywordFound(f"Could not find a keyword on line {line_index + 1}.\n"
                             f"\t{line}\n"
                             f"Ensure that you've properly spelled the keyword.")

    def parse_tuples_in_line(self, line: str, line_index: int) -> tuple:
        current_word: str = ""
        # previous_word: str = ""
        current_variables: list = []
        in_tuple: bool = False

        for index, char in enumerate(line):
            if char == '(':
                in_tuple = True
                continue

            elif char == ',':
                current_variables.append(current_word)
                current_word = ""
                continue

            elif char == ' ':
                continue

            elif (index == len(line)) and in_tuple:
                raise SyntaxError(f'Line {line_index} has a tuple that was not closed.')

            elif char == ")":
                if not in_tuple:
                    raise SyntaxError(f"Line {line_index} closed a tuple but there wasn't an open tuple.")
                elif current_word == '':
                    break

                current_variables.append(current_word)
                break

            # elif char == "=":
            #     current_variables.append(current_word)
            #     break

            # previous_word = current_word
            if in_tuple:
                current_word += char

        print(f'{current_variables=}')
        return tuple(current_variables)


if __name__ == "__main__":
    test_code = [
        'test(4, 5)',
    ]
    compiler = BaseCompiler(test_code)

    @compiler.register_keyword(keyword_name='test', parameters=2, raw_keyword=False)
    def test(self, arguments: tuple):
        return f'op add x {arguments[0]} {arguments[1]}'

    print(compiler.keywords)
    compiler.compile_line(0)
    print(compiler.compiled_result)
