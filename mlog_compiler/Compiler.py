from mlog_compiler import Assignment, Control, Sense, Draw, DrawFlush, UnitRadar
from mlog_compiler.Blocks import MessageBlock
from mlog_compiler.Exceptions import MissingEOL, CallDoesNotExist, UnknownOperation

operations = {
    # Comparative
    '==': 'equalTo',
    '>': 'greaterThan',
    '>=': 'greaterThanEq',
    '<': 'lessThan',
    '<=': 'lessThanEq',
    '&&': 'land',
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
    '||': 'or',
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
    source_code_split = source_code.split("\n")
    parsed = []
    branch_queue = []
    branch_call_queue = {
        'if': 0,
        'while': 0,
    }

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

    for index, line in enumerate(source_code_split):
        if line.startswith("//"):
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

            if call_type != "":
                pass

            elif validate('str'):
                call_type = current_word

            elif validate('var'):
                call_type = current_word

            elif validate('print'):
                call_type = current_word

            elif validate('set_enabled'):
                call_type = current_word

            elif validate('if'):
                call_type = current_word

            elif validate('sense'):
                call_type = current_word

            elif validate('wait'):
                call_type = current_word

            elif validate('end'):
                parsed.append('end')
                break

            elif validate('clear'):
                call_type = current_word

            elif validate('color'):
                call_type = current_word

            elif validate('packed_color'):
                call_type = current_word

            elif validate('stroke'):
                call_type = current_word

            elif validate('line'):
                call_type = current_word

            elif validate('rectangle'):
                call_type = current_word

            elif validate('line_rectangle'):
                call_type = current_word

            elif validate('poly'):
                call_type = current_word

            elif validate('line_poly'):
                call_type = current_word

            elif validate('triangle'):
                call_type = current_word

            elif validate('image'):
                call_type = current_word

            elif validate('update'):
                call_type = current_word

            elif validate('bind'):
                call_type = current_word

            elif validate('move'):
                call_type = current_word

            elif validate('approach'):
                call_type = current_word

            elif validate('unit_radar'):
                call_type = current_word

            elif validate('floor'):
                call_type = current_word

            elif validate('ceil'):
                call_type = current_word

            elif validate('get_link'):
                call_type = current_word

            elif validate('stop'):
                parsed.append('stop')
                break

            elif validate('pack_color'):
                call_type = current_word

            elif validate('lookup'):
                call_type = current_word

            elif validate('while'):
                call_type = current_word

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
                        break

                    elif len(line_split) == 4 and line_split[3].startswith("!"):
                        # var_data = line_split[index + (offset + 3)]
                        var_data = current_word.removeprefix('!').removesuffix(";")
                        parsed.append(f"op notEqual {var_name} {var_data} 1")
                        break

                    var_data = line_split[3]
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == 'str':
                    var_name = line_split[1]
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == "print":
                    flush = True
                    data = arguments[0]
                    sink = arguments[1]
                    if len(arguments) == 3:
                        flush = arguments[2].title() == "True"

                    call = MessageBlock(int(sink), data)
                    call_repr_list = call.get_processor_representation().split("\n")

                    parsed.append(call_repr_list[0])
                    if flush:
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

                elif call_type == "clear":
                    red = arguments[0]
                    blue = arguments[1]
                    green = arguments[2]
                    call = Draw('clear', red, green, blue)

                    parsed.append(call.representation)

                elif call_type == "color":
                    red = arguments[0]
                    blue = arguments[1]
                    green = arguments[2]
                    alpha = arguments[3]
                    call = Draw('color', red, green, blue, alpha)

                    parsed.append(call.representation)

                elif call_type == "packed_color":
                    color = arguments[0]
                    call = Draw('col', color)

                    parsed.append(call.representation)

                elif call_type == "stroke":
                    width = arguments[0]
                    call = Draw('stroke', width)

                    parsed.append(call.representation)

                elif call_type == "line":
                    x1 = arguments[0]
                    y1 = arguments[1]
                    x2 = arguments[2]
                    y2 = arguments[3]
                    call = Draw('line', x1, y1, x2, y2)

                    parsed.append(call.representation)

                elif call_type == "rectangle":
                    x = arguments[0]
                    y = arguments[1]
                    width = arguments[2]
                    height = arguments[3]
                    call = Draw('rect', x, y, width, height)

                    parsed.append(call.representation)

                elif call_type == "line_rectangle":
                    x = arguments[0]
                    y = arguments[1]
                    width = arguments[2]
                    height = arguments[3]
                    call = Draw('lineRect', x, y, width, height)

                    parsed.append(call.representation)

                elif call_type == "poly":
                    x = arguments[0]
                    y = arguments[1]
                    sides = arguments[2]
                    radius = arguments[3]
                    rotation = arguments[4]
                    call = Draw('poly', x, y, sides, radius, rotation)

                    parsed.append(call.representation)

                elif call_type == "line_poly":
                    x = arguments[0]
                    y = arguments[1]
                    sides = arguments[2]
                    radius = arguments[3]
                    rotation = arguments[4]
                    call = Draw('linePoly', x, y, sides, radius, rotation)

                    parsed.append(call.representation)

                elif call_type == "triangle":
                    x = arguments[0]
                    y = arguments[1]
                    a = arguments[2]
                    b = arguments[3]
                    c = arguments[4]
                    d = arguments[5]  # Holy jeez, 5 arguments!
                    call = Draw('triangle', x, y, a, b, c, d)

                    parsed.append(call.representation)

                elif call_type == "image":
                    x = arguments[0]
                    y = arguments[1]
                    image = arguments[2]
                    size = arguments[3]
                    rotation = arguments[4]
                    call = Draw('image', x, y, image, size, rotation)

                    parsed.append(call.representation)

                elif call_type == "update":
                    display_id = arguments[0]
                    call = DrawFlush(display_id)

                    parsed.append(call.representation)

                elif call_type == "bind":
                    unit = arguments[0]
                    parsed.append(f"ubind @{unit}")

                elif call_type == "move":
                    x = arguments[0]
                    y = arguments[1]
                    parsed.append(f"ucontrol move {x} {y} 0 0 0")

                elif call_type == "approach":
                    x = arguments[0]
                    y = arguments[1]
                    radius = arguments[2]
                    parsed.append(f"ucontrol approach {x} {y} {radius} 0 0")

                elif call_type == "unit_radar":
                    target_var = arguments[0]
                    target_1 = arguments[1]
                    target_2 = arguments[2]
                    target_3 = arguments[3]
                    sort = arguments[4]
                    order = arguments[5]
                    call = UnitRadar(target_var, target_1, target_2, target_3, sort, order)

                    parsed.append(call.representation)

                elif call_type == 'floor':
                    target_var = arguments[0]
                    x = arguments[1]

                    parsed.append(f"op floor {target_var} {x} 0")

                elif call_type == 'ceil':
                    target_var = arguments[0]
                    x = arguments[1]

                    parsed.append(f"op ceil {target_var} {x} 0")

                elif call_type == 'get_link':
                    target_var = arguments[0]
                    link_num = arguments[1]

                    parsed.append(f'getlink {target_var} {link_num}')

                elif call_type == 'pack_color':
                    target_var = arguments[0]
                    red = arguments[1]
                    green = arguments[2]
                    blue = arguments[3]
                    alpha = arguments[4]

                    parsed.append(f'packcolor {target_var} {red} {green} {blue} {alpha}')

                elif call_type == 'lookup':
                    target_var = arguments[0]
                    lookup_type = arguments[1]
                    target_num = arguments[2]

                    parsed.append(f"lookup {lookup_type} {target_var} {target_num}")

                elif call_type == "":
                    print(line)
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
                parsed.append(f"START_OF_BLOCK_{call_type}_{index} {arguments[0]}")
                branch_queue.append(f"{call_type}_{index}")

                branch_call_queue[call_type] += 1
            elif char == "}" and not in_quotes:
                parsed.append(f"END_OF_BLOCK_{branch_queue.pop(-1)}")

            current_word += char

    while branch_call_queue['if'] >= 1:
        start_index = index_starts_with("START_OF_BLOCK_if", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("_")
        block_id = split_line[4].split(" ")[0]

        end_index = parsed.index(f"END_OF_BLOCK_if_{block_id}")
        condition_var = sof_line.split(" ")[1]

        parsed[start_index] = f"jump {end_index - branch_call_queue['if']} notEqual {condition_var} 1"
        parsed.pop(end_index)
        branch_call_queue['if'] -= 1

    while branch_call_queue['while'] >= 1:
        start_index = index_starts_with("START_OF_BLOCK_while", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("_")
        block_id = split_line[4].split(" ")[0]

        end_index = parsed.index(f"END_OF_BLOCK_while_{block_id}")
        condition_var = sof_line.split(" ")[1]

        parsed[end_index] = f"jump {start_index} notEqual {condition_var} 0"
        parsed.pop(start_index)
        branch_call_queue['while'] -= 1

    parsed.append('end')
    return parsed
