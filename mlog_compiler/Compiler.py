from mlog_compiler import Assignment, Control
from mlog_compiler.Blocks import MessageBlock
from mlog_compiler.Exceptions import MissingEOL, CallDoesNotExist


def validate_line(line: str) -> bool:
    stripped_line = line.strip()
    can_ignore = stripped_line == "" or stripped_line.startswith("//")
    return not line.endswith(";") and not line.endswith("{") and not line.endswith("}") and not can_ignore


def validate_call(call: str | list, current_word: str, in_quotes: bool, in_parentheses: bool) -> bool:
    if type(call) is list:
        return current_word in call and not in_quotes and not in_parentheses

    return current_word == call and not in_quotes and not in_parentheses


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
        line_split = line.split(" ")
        arguments = []

        for char_index, char in enumerate(line):
            validate = lambda l_call: validate_call(l_call, current_word, in_quotes, in_parentheses)

            if validate(['int', 'float', 'bool']):
                var_name = line_split[index + offset]
                var_data = line_split[index + (offset + 2)]
                var = Assignment(var_data.removesuffix(";"), var_name)

                parsed.append(var.representation)
                break

            elif validate('str'):
                call_type = 'str'

            elif validate('print'):
                call_type = "print"

            elif validate('set_enabled'):
                call_type = "set_enabled"

            last_char = line[char_index - 1]

            if char == ";":
                if call_type == 'str':
                    var_name = line_split[index + offset]
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == "print":
                    data = arguments[0]
                    sink = arguments[1]
                    call = MessageBlock(int(sink), data)

                    parsed.append(call.get_processor_representation())

                elif call_type == "set_enabled":
                    block = arguments[0]
                    enabled = arguments[1]
                    call = Control(block, enabled)

                    parsed.append(call.representation)

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

            current_word += char

        offset -= 1

    return parsed
