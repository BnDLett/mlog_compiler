from mlog_compiler import Assignment
from mlog_compiler.Exceptions import MissingEOL


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
        if not line.endswith(";") and line.strip() != "":
            print(f"[{str(index).rjust(3, "0")}] {line}")
            raise MissingEOL()

        current_word = ""
        in_quotes = False
        var_type = ""
        line_split = line.split(" ")

        for char_index, char in enumerate(line):
            if current_word in ['int', 'float']:
                var_name = line_split[index + offset]
                var_data = line_split[index + (offset + 2)]
                var = Assignment(var_data.removesuffix(";"), var_name)

                parsed.append(var.representation)
                break

            elif current_word == 'str' and not in_quotes:
                var_type = 'str'

            last_char = line[char_index - 1]

            if char == ";":
                if var_type == 'str':
                    var_name = line_split[index + offset]
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)
                break
            elif char == " " and not in_quotes:
                current_word = ""
                continue
            elif char in ['"', "'"] and last_char != "\\":
                in_quotes = not in_quotes

            current_word += char

        offset -= 1

    return parsed
