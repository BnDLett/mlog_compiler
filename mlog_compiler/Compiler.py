import json

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


def get_target_var(last_func: str, arguments: list[str], functions: dict) -> str:
    target_var = arguments[0]
    target_var_split = target_var.split("_")

    if target_var[0] not in "0123456789\'\"" and target_var_split[0] not in functions.keys():
        target_var = f'{last_func}_{target_var}'

    return target_var


def get_var(last_func: str, arguments: list[str], functions: dict, index) -> str:
    x = get_target_var(last_func, [arguments[index]], functions)
    return x


def parse(source_code: str) -> list[str]:
    source_code_split = source_code.split("\n")
    parsed = [
        'set main_exit 1',
        'jump main always',
    ]
    branch_queue = []
    branch_call_queue = {
        'if': 0,
        'while': 0,
        'def': 0,
    }
    functions = {}
    func_references = 0
    last_func = ''

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
        if line.strip().startswith("//"):
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
        func_name = ''

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

            elif validate('read'):
                call_type = current_word

            elif validate('write'):
                call_type = current_word

            elif validate('def'):
                call_type = current_word

            elif validate('return'):
                call_type = current_word

            elif current_word in functions.keys():
                call_type = 'func_call'
                func_name = current_word

            last_char = line[char_index - 1]

            if char == ";":
                if call_type == 'var':
                    var_name = f'{last_func}_{line_split[1]}'

                    # if "not" in line_split:
                    #     # var_data = line_split[index + (offset + 3)]
                    #     var_data = current_word
                    #     parsed.append(f"op notEqual {var_name} {var_data.removesuffix(";")} 1")
                    #     break
                    if len(line_split) == 6:
                        var_x = line_split[3]
                        operation = line_split[4]
                        var_y = line_split[5].removesuffix(";")

                        var_x = get_target_var(last_func, [var_x], functions)
                        var_y = get_target_var(last_func, [var_y], functions)

                        if operation not in operations.keys():
                            raise UnknownOperation
                        parsed.append(f'op {operations[operation]} {var_name} {var_x} {var_y}')
                        break

                    elif len(line_split) == 4 and line_split[3].startswith("!"):
                        # var_data = line_split[index + (offset + 3)]
                        var_data = current_word.removeprefix('!').removesuffix(";")
                        var_data = get_target_var(last_func, [var_data], functions)

                        parsed.append(f"op notEqual {var_name} {var_data} 1")
                        break

                    var_data = get_var(last_func, line_split, functions, 3)
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == 'str':
                    var_name = f'{last_func}_{line_split[1]}'
                    var_data = current_word
                    var = Assignment(var_data.removesuffix(";"), var_name)

                    parsed.append(var.representation)

                elif call_type == "print":
                    arg_index = -1
                    flush = True
                    data = get_target_var(last_func, arguments, functions)

                    sink = get_var(last_func, arguments, functions, 1)
                    if len(arguments) == 3:
                        flush = get_var(last_func, arguments, functions, arg_index + 1).title() == "True"

                    call = MessageBlock(int(sink), data)
                    call_repr_list = call.get_processor_representation().split("\n")

                    parsed.append(call_repr_list[0])
                    if flush:
                        parsed.append(call_repr_list[1])

                elif call_type == "set_enabled":
                    block = arguments[0]
                    enabled = get_var(last_func, arguments, functions, 1)
                    call = Control(block, enabled)

                    parsed.append(call.representation)

                elif call_type == "sense":
                    target_var = get_var(last_func, arguments, functions, 0)
                    block = arguments[1]
                    to_sense = arguments[2]
                    call = Sense(block, to_sense, target_var)

                    parsed.append(call.representation)

                elif call_type == "wait":
                    arg_index = -1
                    time = get_var(last_func, arguments, functions, arg_index + 1)
                    parsed.append(f"wait {time}")

                elif call_type == "clear":
                    arg_index = -1

                    red = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    green = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    blue = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('clear', red, green, blue)

                    parsed.append(call.representation)

                elif call_type == "color":
                    arg_index = -1

                    red = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    blue = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    green = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    alpha = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('color', red, green, blue, alpha)

                    parsed.append(call.representation)

                elif call_type == "packed_color":
                    arg_index = -1

                    color = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('col', color)

                    parsed.append(call.representation)

                elif call_type == "stroke":
                    arg_index = -1

                    width = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('stroke', width)

                    parsed.append(call.representation)

                elif call_type == "line":
                    arg_index = -1

                    x1 = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y1 = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    x2 = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y2 = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('line', x1, y1, x2, y2)

                    parsed.append(call.representation)

                elif call_type == "rectangle":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    width = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    height = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('rect', x, y, width, height)

                    parsed.append(call.representation)

                elif call_type == "line_rectangle":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    width = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    height = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('lineRect', x, y, width, height)

                    parsed.append(call.representation)

                elif call_type == "poly":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    sides = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    radius = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    rotation = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('poly', x, y, sides, radius, rotation)

                    parsed.append(call.representation)

                elif call_type == "line_poly":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    sides = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    radius = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    rotation = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('linePoly', x, y, sides, radius, rotation)

                    parsed.append(call.representation)

                elif call_type == "triangle":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    a = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    b = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    c = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    d = get_var(last_func, arguments, functions, arg_index + 1)  # Holy jeez, 5 arguments!
                    call = Draw('triangle', x, y, a, b, c, d)

                    parsed.append(call.representation)

                elif call_type == "image":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    image = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    size = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    rotation = get_var(last_func, arguments, functions, arg_index + 1)
                    call = Draw('image', x, y, image, size, rotation)

                    parsed.append(call.representation)

                elif call_type == "update":
                    arg_index = -1

                    display_id = get_var(last_func, arguments, functions, arg_index + 1)
                    call = DrawFlush(display_id)

                    parsed.append(call.representation)

                elif call_type == "bind":
                    unit = arguments[0]
                    parsed.append(f"ubind @{unit}")

                elif call_type == "move":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index + 1)
                    parsed.append(f"ucontrol move {x} {y} 0 0 0")

                elif call_type == "approach":
                    arg_index = -1

                    x = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    y = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    radius = get_var(last_func, arguments, functions, arg_index + 1)
                    parsed.append(f"ucontrol approach {x} {y} {radius} 0 0")

                elif call_type == "unit_radar":
                    target_var = get_target_var(last_func, arguments, functions)
                    target_1 = arguments[1]
                    target_2 = arguments[2]
                    target_3 = arguments[3]
                    sort = arguments[4]
                    order = arguments[5]
                    call = UnitRadar(target_var, target_1, target_2, target_3, sort, order)

                    parsed.append(call.representation)

                elif call_type == 'floor':
                    target_var = get_target_var(last_func, arguments, functions)

                    x = get_var(last_func, arguments, functions, 1)

                    parsed.append(f"op floor {target_var} {x} 0")

                elif call_type == 'ceil':
                    target_var = get_target_var(last_func, arguments, functions)
                    x = get_var(last_func, arguments, functions, 1)

                    parsed.append(f"op ceil {target_var} {x} 0")

                elif call_type == 'get_link':
                    arg_index = -1

                    target_var = get_target_var(last_func, arguments, functions)
                    link_num = get_var(last_func, arguments, functions, arg_index + 1)

                    parsed.append(f'getlink {target_var} {link_num}')

                elif call_type == 'pack_color':
                    arg_index = -1

                    target_var = get_target_var(last_func, arguments, functions)
                    red = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    green = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    blue = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    alpha = get_var(last_func, arguments, functions, arg_index + 1)

                    parsed.append(f'packcolor {target_var} {red} {green} {blue} {alpha}')

                elif call_type == 'lookup':
                    arg_index = -1

                    target_var = get_target_var(last_func, arguments, functions)
                    lookup_type = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    target_num = get_var(last_func, arguments, functions, arg_index + 1)

                    parsed.append(f"lookup {lookup_type} {target_var} {target_num}")

                elif call_type == 'read':
                    arg_index = -1

                    target_var = get_target_var(last_func, arguments, functions)
                    target_value = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    storage_type = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    target_id = get_var(last_func, arguments, functions, arg_index + 1)

                    parsed.append(f"read {target_var} {storage_type}{target_id} {target_value}")

                elif call_type == 'write':
                    arg_index = -1

                    target_var = get_target_var(last_func, arguments, functions)
                    target_value = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    storage_type = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    target_id = get_var(last_func, arguments, functions, arg_index + 1)

                    parsed.append(f"write {target_var} {storage_type}{target_id} {target_value}")

                elif call_type == 'func_call':
                    # print(functions[func_name]['arguments'])
                    func_references += 1
                    parsed.append(f'FUNC_REFERENCE_{func_name}-["{'", "'.join(arguments)}"]-{last_func}')

                elif call_type == "return":
                    # return var;
                    line_split = line.strip().split(" ")
                    part_to_return = line_split[1].removesuffix(";")
                    full_to_return = f"set {last_func}_ret {last_func}_{part_to_return}"

                    parsed.append(full_to_return)

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
            elif char == "," and in_parentheses and not in_quotes:
                arguments.append(current_word)
            elif char == "{" and not in_quotes:
                if call_type == 'def':
                    line_split = line.split(" ")
                    function_name = line_split[1].split('(')[0]
                    # print(function_name)

                    functions[function_name] = {
                        'arguments': arguments,
                    }

                    last_func = function_name
                    parsed.append(f"START_OF_BLOCK_{call_type}_{index}_{function_name} {arguments}")
                else:
                    parsed.append(f"START_OF_BLOCK_{call_type}_{index} {arguments[0]} {last_func}")

                branch_queue.append(f"{call_type}_{index}")

                branch_call_queue[call_type] += 1

            elif char == "}" and not in_quotes:
                parsed.append(f"END_OF_BLOCK_{branch_queue.pop(-1)}")

            current_word += char

    while func_references >= 1:
        # FUNC_REFERENCE_foo-(X, Y, Z)-main
        # 0    1         2
        #                0   1         2
        start_index = index_starts_with("FUNC_REFERENCE_", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("_")
        # split_line[2] will look like this: foo-(X, Y, Z)
        split_end = split_line[2].split("-")
        func_name = split_end[0]

        args: tuple = json.loads(split_end[1])

        next_index = start_index

        for index, arg_name in enumerate(functions[func_name]['arguments']):
            arg = get_target_var(split_end[2], [args[index]], functions)
            parsed.insert(next_index := next_index + 1, f'set {func_name}_{arg_name} {arg}')

        parsed.insert(next_index := next_index + 1, f'op add {func_name}_exit @counter 1')
        parsed.insert(next_index + 1, f'jump {func_name} always')
        parsed.pop(start_index)

        func_references -= 1

    while branch_call_queue['def'] >= 1:
        # START_OF_BLOCK_def_1_foo ['arg_1', 'arg_2', 'arg_3']
        # 0     1  2     3   4 5         6        7        8
        # 0                        1
        start_index = index_starts_with("START_OF_BLOCK_def", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("_")
        block_id = split_line[4].split(" ")[0]
        end_index = parsed.index(f"END_OF_BLOCK_def_{block_id}")

        func_name = split_line[5].split(" ")[0]

        parsed[start_index] = f"{func_name}:"
        parsed[end_index] = f"set @counter {func_name}_exit"
        branch_call_queue['def'] -= 1

    while branch_call_queue['if'] >= 1:
        # START_OF_BLOCK_if_id COND DEF
        # 0                    1    2
        # 0     1  2     3  4

        start_index = index_starts_with("START_OF_BLOCK_if", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split(" ")
        split_start = split_line[0].split("_")

        block_id = split_start[4]
        func_name = split_line[2]
        condition_var = get_var(func_name, split_line, functions, 1)

        end_index = parsed.index(f"END_OF_BLOCK_if_{block_id}")

        parsed[start_index] = f"jump l{block_id} notEqual {condition_var} 1"
        parsed[end_index] = f"l{block_id}:"
        branch_call_queue['if'] -= 1

    while branch_call_queue['while'] >= 1:
        # START_OF_BLOCK_while_id COND DEF
        # 0                       1    2
        # 0     1  2     3     4

        start_index = index_starts_with("START_OF_BLOCK_while", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split(" ")
        split_start = split_line[0].split("_")

        block_id = split_start[4]
        func_name = split_line[2]
        condition_var = get_var(func_name, split_line, functions, 1)

        end_index = parsed.index(f"END_OF_BLOCK_while_{block_id}")

        parsed[end_index] = f"jump w{block_id} notEqual {condition_var} 0"
        parsed[start_index] = f"w{block_id}:"
        branch_call_queue['while'] -= 1

    parsed.append('end')
    return parsed
