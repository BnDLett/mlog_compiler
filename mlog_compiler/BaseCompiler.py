import logging
from typing import Callable, Any

from Exceptions import NoKeywordFound, MissingType
from Variable import Variable
from Keyword import Keyword
from TypeCheck import TypeCheck


class BaseCompiler:
    code: list[str]
    keywords: dict[str, Keyword]
    last_scope: str = 'global'
    compiled_result: list = []
    variables: dict[str, Variable]
    variable_types: list[str]
    logger: logging.Logger

    def __init__(self, code: str | list) -> None:
        if type(code) is str:
            code: list = code.split(';')

        self.code = code
        self.keywords = {}
        self.variables = {}
        self.variable_types = []
        self.logger = logging.Logger("Mlog Compiler Logger")

    # ---- NON-STATIC METHODS ----
    # -- Registering Data/Information --

    def register_keyword(self, keyword_name: str, parameters: int, *, raw_keyword: bool = False):
        """
        Register a new keyword into the compiler. Whenever your keyword is ran, it will be given `self` and the
        arguments in the line as parameters. Your function's parameter list should look like this: `(self, arguments)`.
        If your keyword is set as a raw keyword, then it will only be given the line itself instead for any special
        behavior.

        :param func: A lambda function that is executed whenever the keyword is found.
        :param keyword_name: The name of the keyword.
        :param parameters: The amount of parameters accepted in the keyword.
        :param raw_keyword: A boolean value that determines whether the line alone is given. If this is true, then it
        will return only the line WITHOUT any further checks (such as parameter count).
        :return:
        """

        def inner(func):
            # self.keywords[keyword_name] = (func, raw_keyword, parameters)
            self.keywords[keyword_name] = Keyword(func, parameters, raw_keyword)
            return func

        return inner

    def register_type(self, type_name: str, type_check: Callable[[Any], bool]) -> Callable[[Any, str, int], Any]:
        """
        A method that registers a type (such as int) into the compiler. A variable can be created with this type either
        via `int x;` or `float x = 3.14159`. The variables that are assigned during the compilation process can be
        accessed via the `find_variable` method.

        :param type_name: The name of the type. `int`, for example, would be `int x`; and float, for example, would be
        `float y`.
        :param type_check: pass
        :return:
        """

        self.variable_types.append(type_name)

        @self.register_keyword(type_name, 0, raw_keyword=True)
        def handle_variable(placeholder, line: str, index: int):  # noqa
            processed_line = self.process_variable_line(line, type_name)
            variable_name = f'{self.last_scope}_{processed_line[0]}'
            variable_data = None
            variable = None

            # TODO: it's really easy to make this A LOT more dynamic
            if len(processed_line) == 1:
                variable = Variable(variable_name, type_name)
            elif len(processed_line) == 3:
                variable = Variable(variable_name, type_name)
                variable_data = processed_line[2]
            elif len(processed_line) == 5:
                self.logger.warning("Comparisons in variables are not yet supported.")
            else:
                raise Exception(f"Line {index + 1} does not properly assign a variable. Ensure that you're not doing a"
                                f" comparison.")

            if not type_check(variable_data):
                raise TypeError(f"The data assigned to variable {variable_name} on line {index + 1} is invalid. Ensure "
                                f"that the data that was assigned is a(n) {type_name}.")

            self.variables[variable.name] = variable
            return f"set {variable.name} {variable_data if variable_data is not None else 'null'}"

        return handle_variable

    # -- General Methods --

    def create_variable(self, variable_name: str, variable_data: str | None, variable_type: str):
        """
        Creates and stores a variable at a specified line index.
        :param variable_name: The name of the variable.
        :param variable_data: The data that is contained with the variable. If it is `None`, then the data will be
        'null' in mlog.
        :param variable_type: The type that the variable is.
        """
        if variable_data is None:
            variable_data = "null"

        if variable_type not in self.variable_types:
            raise MissingType("The type that was specified does not exist. Ensure that it exists.")

        self.variables[variable_name] = Variable(variable_name, variable_data)
        self.compiled_result.append(f"set {variable_name} {variable_data}")

    def retrieve_variable(self, variable_name: str) -> Variable | None:
        if not (variable_name in self.variables):
            return None

        return self.variables[variable_name]

    def compile_line(self, index: int):
        """
        Do NOT call this function in random order. Always start at a specified index and iterate UP.
        :param index: The index of the line in the list.
        """
        line: str = self.code[index]
        if line.strip().startswith("//"):
            return

        keyword_name = self.find_keyword_in_line(line, index)
        keyword = self.keywords[keyword_name]

        if keyword.raw:
            result = keyword.callback(self, line, index)
            self.compiled_result.append(result)
            return

        parsed_tuple_data = self.parse_tuples_in_line(line, index)
        tuple_in_line = []
        for item in parsed_tuple_data:
            expected_var = f'{self.last_scope}_{item}'

            if not ((TypeCheck.ensure_float(item) or TypeCheck.ensure_str(item)) or
                    expected_var in self.variables.keys()):
                raise NameError(f"Value {item} on line {index + 1} does not exist.")

            if expected_var in self.variables.keys():
                tuple_in_line.append(expected_var)
                continue

            tuple_in_line.append(item)

        # print(tuple_in_line)

        length_difference = len(tuple_in_line) - keyword.expected_arguments
        if length_difference > 0:
            raise TypeError(f"Line {index} calls a function but provides {length_difference} extra argument(s) than"
                            f" what was expected.")
        if length_difference < 0:
            raise TypeError(f"Line {index} calls a function but provides {-length_difference} less argument(s) than"
                            f" what was expected.")

        result = keyword.callback(self, tuple_in_line, index)
        self.compiled_result.append(result)

    def find_keyword_in_line(self, line: str, line_index: int) -> str:
        current_word: str = ""
        for index, char in enumerate(line.strip()):
            current_word += char

            try:
                next_char = line.strip()[index + 1]
            except IndexError:
                next_char = ""

            if (current_word in self.keywords.keys()) and ((next_char == " ") or (next_char == "(")):
                return current_word

        raise NoKeywordFound(f"Could not find a keyword on line {line_index + 1}.\n"
                             f"\t{line}\n"
                             f"Ensure that you've properly spelled the keyword.")

    # ---- STATIC METHODS ----

    @staticmethod
    def parse_tuples_in_line(line: str, line_index: int) -> tuple:
        current_word: str = ""
        # previous_word: str = ""
        current_variables: list = []
        quotes = ['"', "'"]
        in_tuple: bool = False
        quote_char_used: str = ''

        for index, char in enumerate(line):
            # if quote_char_used != '':
            #     current_word += char
            #     continue

            if char in ['"', "'"] and quote_char_used == '':
                quote_char_used = char
                current_word += char
                continue

            elif char in quotes and quote_char_used == char:
                quote_char_used = ''
                current_word += char
                continue

            elif char == '(':
                in_tuple = True
                continue

            elif char == ',' and quote_char_used == '':
                current_variables.append(current_word)
                current_word = ""
                continue

            elif char == ' ' and quote_char_used == '':
                continue

            elif (index == len(line)) and in_tuple:
                raise SyntaxError(f'Line {line_index + 1} has a tuple that was not closed.')

            elif char == ")":
                if not in_tuple:
                    raise SyntaxError(f"Line {line_index + 1} closed a tuple but there wasn't an open tuple.")
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

        # print(f'{current_variables=}')
        return tuple(current_variables)

    @staticmethod
    def process_variable_line(line: str, expected_type: str) -> list[str]:
        # int x = 4;
        prepared_line = line.strip().removeprefix(f"{expected_type} ")
        current_word = ""
        in_quotes = False
        words = []

        for index, char in enumerate(prepared_line):
            current_word += char

            try:
                next_char = prepared_line[index + 1]
            except IndexError:
                next_char = ";"

            if char == '"':
                in_quotes = not in_quotes  # Inverts the current value of the variable "in_quotes."

            if (next_char in (" ", ";", ",", ")")) and not in_quotes:
                words.append(current_word.removeprefix(" "))
                current_word = ""

        return words


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
