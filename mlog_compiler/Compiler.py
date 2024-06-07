from mlog_compiler import Assignment
from mlog_compiler.Blocks import MessageBlock
from mlog_compiler.Exceptions import MissingEOL


def validate_line(line: str) -> bool:
    stripped_line = line.strip()
    can_ignore = stripped_line == "" or stripped_line.startswith("//")
    return not line.endswith(";") and not line.endswith("{") and not line.endswith("}") and not can_ignore


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
        if validate_line(line):
            print(f"[{str(index).rjust(3, "0")}] {line}")
            raise MissingEOL()

        current_word = ""
        in_quotes = False
        in_parentheses = False
        call_type = ""
        line_split = line.split(" ")
        arguments = []

        for char_index, char in enumerate(line):
            if current_word in ['int', 'float']:
                var_name = line_split[index + offset]
                var_data = line_split[index + (offset + 2)]
                var = Assignment(var_data.removesuffix(";"), var_name)

                parsed.append(var.representation)
                break

            elif current_word == 'str' and not in_quotes:
                call_type = 'str'

            elif current_word == "print":
                call_type = "print"

            last_char = line[char_index - 1]

            if char == ";":
                if call_type == 'str':
                    var_name = line_split[index + offset]
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == "print":
                    print(arguments)
                    data = arguments[0]
                    sink = arguments[1]
                    call = MessageBlock(int(sink), data)

                    parsed.append(call.get_processor_representation())

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
