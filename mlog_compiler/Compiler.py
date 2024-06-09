from typing import override, List

from mlog_compiler import Assignment, Control, Sense
from mlog_compiler.Blocks import MessageBlock
from mlog_compiler.Exceptions import MissingEOL, CallDoesNotExist, UnknownOperation

operations = {
    # Comparative
    '==': 'equalTo',
    '>': 'greaterThan',
    '>=': 'greaterThanEq',
    '<': 'lessThan',
    '<=': 'lessThanEq',
    'and': 'land',
    '!=': 'notEqual',
    '===': 'strictEqual',

    # Mathematical
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '//': 'idiv',
    '%': 'mod',
    '**': 'pow',

    # Bitwise
    'or': 'or',
    '<<': 'shl',
    '>>': 'shr',
    '&': 'and',
    '^': 'xor',
}


def validate_line(line: str) -> bool:
    stripped_line = line.strip()
    can_ignore = stripped_line == "" or stripped_line.startswith("//")
    return not line.endswith(";") and not line.endswith("{") and not line.endswith("}") and not can_ignore


def validate_call(call: str | list, current_word: str, in_quotes: bool, in_parentheses: bool) -> bool:
    if type(call) is list:
        return current_word in call and not in_quotes and not in_parentheses

    return current_word == call and not in_quotes and not in_parentheses


def index_starts_with(starts_with: str, iterable: list | tuple):
    for index, item in enumerate(iterable):
        if item.startswith(starts_with):
            return index


def parse(source_code: str) -> list[str]:
    parsed = []
    source_code_split = source_code.split("\n")

    # for index, word in enumerate(source_code_split):
    #     if word == "//":
    #         break
    #     elif word in ['int', 'float']:
    #         # int var_name = 5
    #         # 0   1        2 3
    #         name = source_code_split[index + 1]
    #         data = source_code_split[index + 3]
    #         result = Assignment(data, name)
    #
    #         parsed.append(result.representation)
    #
    #     elif word == 'str':
    #         pass

    offset = 1

    for index, line in enumerate(source_code_split):
        if line.startswith("//"):
            offset -= 1
            continue
        elif validate_line(line):
            print(f"[{str(index).rjust(3, "0")}] {line}")
            raise MissingEOL()

        current_word = ""
        in_quotes = False
        in_parentheses = False
        call_type = ""
        line_split = line.strip().split(" ")
        arguments = []

        for char_index, char in enumerate(line):
            validate = lambda l_call: validate_call(l_call, current_word, in_quotes, in_parentheses)

            if validate('str'):
                call_type = 'str'

            elif validate('var'):
                call_type = 'var'

            elif validate('print'):
                call_type = "print"

            elif validate('set_enabled'):
                call_type = "set_enabled"

            elif validate('if'):
                call_type = "if"

            elif validate('sense'):
                call_type = "sense"

            elif validate('wait'):
                call_type = "wait"

            elif validate('end'):
                parsed.append('end')
                break

            last_char = line[char_index - 1]

            if char == ";":
                if call_type == 'var':
                    var_name = line_split[1]

                    # if "not" in line_split:
                    #     # var_data = line_split[index + (offset + 3)]
                    #     var_data = current_word
                    #     parsed.append(f"op notEqual {var_name} {var_data.removesuffix(";")} 1")
                    #     break
                    if len(line_split) == 6:
                        var_x = line_split[3]
                        operation = line_split[4]
                        var_y = line_split[5].removesuffix(";")

                        if operation not in operations.keys():
                            raise UnknownOperation
                        parsed.append(f'op {operations[operation]} {var_name} {var_x} {var_y}')

                    elif len(line_split) == 5 and "not" in line_split:
                        # var_data = line_split[index + (offset + 3)]
                        var_data = current_word
                        parsed.append(f"op notEqual {var_name} {var_data.removesuffix(";")} 1")
                        break

                elif call_type == 'str':
                    var_name = line_split[1]
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == "print":
                    data = arguments[0]
                    sink = arguments[1]
                    call = MessageBlock(int(sink), data)
                    call_repr_list = call.get_processor_representation().split("\n")

                    parsed.append(call_repr_list[0])
                    parsed.append(call_repr_list[1])

                elif call_type == "set_enabled":
                    block = arguments[0]
                    enabled = arguments[1]
                    call = Control(block, enabled)

                    parsed.append(call.representation)

                elif call_type == "sense":
                    target_var = arguments[0]
                    block = arguments[1]
                    to_sense = arguments[2]
                    call = Sense(block, to_sense, target_var)

                    parsed.append(call.representation)

                elif call_type == "wait":
                    time = arguments[0]
                    parsed.append(f"wait {time}")

                elif call_type == "":
                    raise CallDoesNotExist

                break
            elif char == " " and not in_quotes:
                current_word = ""
                continue
            elif char in ['"', "'"] and last_char != "\\":
                in_quotes = not in_quotes
            elif char == "(" and not in_quotes:
                current_word = ""
                in_parentheses = True
                continue
            elif char == ")" and in_parentheses and not in_quotes:
                in_parentheses = False
                arguments.append(current_word)
                continue
            elif char == "," and in_parentheses:
                arguments.append(current_word)
            elif char == "{" and not in_quotes:
                parsed.append(f"START_OF_IF {arguments[0]}")
            elif char == "}" and not in_quotes:
                parsed.append("END_OF_IF")

            current_word += char

    parsed: list

    while "END_OF_IF" in parsed:
        start_index = index_starts_with("START_OF_IF", parsed)
        end_index = parsed.index("END_OF_IF")
        sof_line: str = parsed[start_index]
        condition_var = sof_line.split(" ")[1]

        parsed[start_index] = f"jump {end_index} notEqual {condition_var} 1"
        parsed.pop(end_index)

    parsed.append('end')
    return parsed
