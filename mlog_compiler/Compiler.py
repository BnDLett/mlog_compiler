import json
import warnings
from pathlib import Path

from mlog_compiler import Assignment, Control, Sense, Draw, DrawFlush, UnitRadar
from mlog_compiler.Blocks import MessageBlock
from mlog_compiler.Exceptions import MissingEOL, CallDoesNotExist, UnknownOperation, InvalidPath

operations = {
    # Comparative
    '==': 'equal',
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
    '~': 'not',
}


def validate_line(line: str) -> bool:
    stripped_line = line.strip()
    can_ignore = stripped_line == "" or stripped_line.startswith("//")
    return not line.endswith(";") and not line.endswith("{") and not line.endswith("}") and not can_ignore


def validate_call(call: str | list, current_word: str, in_quotes: bool, in_parentheses: bool, char_index: int,
                  line: str) -> bool:
    if type(call) is str:
        message = "Using strings for validating a call are deprecated and will no longer work in future updates."
        warnings.warn(message, DeprecationWarning)
        return current_word == call and not in_quotes and not in_parentheses and line[char_index] != "_"

    if line[char_index] not in '( ':
        return False

    return current_word in call and not in_quotes and not in_parentheses


def index_starts_with(starts_with: str, iterable: list | tuple):
    for index, item in enumerate(iterable):
        if item.startswith(starts_with):
            return index


def get_target_var(last_func: str, arguments: list[str], functions: dict) -> str:
    target_var = arguments[0]
    target_var_split = target_var.split("_")

    if len(target_var) == 0:
        print(f'Warning: target_var was zero for the below argument list:\n{arguments}')
        return ''

    if (target_var[0] not in "!-@0123456789\'\"" and target_var_split[0] not in functions.keys()
            and not target_var_split[-1].startswith('ret')):
        target_var = f'{last_func}_{target_var}'

    return target_var


def get_var(last_func: str, arguments: list[str], functions: dict, index: int) -> str:
    x = get_target_var(last_func, [arguments[index]], functions)
    return x


calls = [
    'str',
    'var',
    'print',
    'set_enabled',
    'if',
    'sense',
    'wait',
    'end',
    'clear',
    'color',
    'packed_color',
    'stroke',
    'line',
    'rectangle',
    'line_rectangle',
    'poly',
    'line_poly',
    'triangle',
    'image',
    'update',
    'bind',
    'move',
    'approach',
    'unit_radar',
    'floor',
    'ceil',
    'get_link',
    'stop',
    'pack_color',
    'lookup',
    'while',
    'read',
    'write',
    'sin',
    'cos',
    'sqrt',
    'def',
    'return',
    'max',
    'min',
    'angle',
    'angle_difference',
    'len',
    'noise',
    'absolute',
    'log',
    'log10',
    'random',
    'tan',
    'asin',
    'acos',
    'atan',
    'idle',
    'stop',
    'pathfind',
    'automatic_pathfind',
    'boost',
    'target',
    'targetp',
    'drop_item',
    'take_item',
    'drop_payload',
    'take_payload',
    'enter_payload',
    'mine',
    'flag',
    'build',
    'get_block',
    'within',
    'unbind',
    
    'import',
]


def parse(source_code: str, parent_path: Path, expose_funcs: bool = False) -> list[str] | tuple:
    source_code_split = source_code.split("\n")
    parsed = []
    branch_queue = []
    branch_call_queue = {
        'if': 0,
        'while': 0,
        'def': 0,
    }
    functions = {
        'global': {
            'arguments': []
        }
    }
    func_references = 0
    last_func = 'global'

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
        previous_word = ""
        in_quotes = False
        in_parentheses = False
        in_assign_tuple = False
        in_assignment = False
        call_type = ""
        # line_split = line.strip().split(" ")
        arguments = []
        assignments = []
        func_name = ''

        for char_index, char in enumerate(line):
            validate = lambda l_call: validate_call(l_call, current_word, in_quotes, in_parentheses, char_index, line)
            try:
                next_char = line[char_index + 1]
            except IndexError:
                next_char = ""
            last_char = line[char_index - 1]

            # Dev vent: it was supposed to be `and not "var"` but it was instead `and not "assignment"`. Somehow, it
            # didn't cause issues?? Wtf???
            # Dev vent part 2: I accidentally wrote `and not "var"` instead of `or call_type == "var"`
            if call_type != "" and call_type != "var":
                pass

            elif validate(calls):
                call_type = current_word

            elif current_word in functions.keys():
                if char != "_":
                    call_type = 'func_call'
                    func_name = current_word

            if char == ";":
                if call_type == 'var':
                    assignment_split = line.split(" = ")
                    value_split = assignment_split[1].strip().split(" ")
                    # var var_x, var_y = 3;
                    # 0                x 1

                    # var_name = f'{last_func}_{line_split[1]}'
                    # var_name = get_target_var(last_func, [line_split[1]], functions)

                    # if "not" in line_split:
                    #     # var_data = line_split[index + (offset + 3)]
                    #     var_data = current_word
                    #     parsed.append(f"op notEqual {var_name} {var_data.removesuffix(";")} 1")
                    #     break
                    if len(value_split) == 3:
                        var_x = value_split[0]
                        operation = value_split[1]
                        var_y = value_split[2].removesuffix(";")

                        var_x = get_target_var(last_func, [var_x], functions)
                        var_y = get_target_var(last_func, [var_y], functions)

                        if operation not in operations.keys():
                            print(operation)
                            print(line)
                            raise UnknownOperation

                        for assignment_target in assignments:
                            var_name = get_target_var(last_func, [assignment_target], functions)
                            parsed.append(f'op {operations[operation]} {var_name} {var_x} {var_y}')
                        break

                    elif value_split[0].startswith("!"):
                        # var_data = line_split[index + (offset + 3)]
                        var_data = current_word.removeprefix('!').removesuffix(";")
                        var_data = get_target_var(last_func, [var_data], functions)

                        for assignment_target in assignments:
                            var_name = get_target_var(last_func, [assignment_target], functions)
                            parsed.append(f"op notEqual {var_name} {var_data} 1")
                        break

                    var_data = get_var(last_func, value_split, functions, 0)
                    for assignment_target in assignments:
                        var_name = get_target_var(last_func, [assignment_target], functions)
                        var = Assignment(var_data.removesuffix(";"), var_name)

                        parsed.append(var.representation)

                elif call_type == 'str':
                    var_data = current_word
                    for assignment_target in assignments:
                        var_name = get_target_var(last_func, [assignment_target], functions)
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
                    block = arguments[0]
                    to_sense = arguments[1]
                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
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
                    target_1 = arguments[0]
                    target_2 = arguments[1]
                    target_3 = arguments[2]
                    sort = arguments[3]
                    order = arguments[4]
                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        call = UnitRadar(target_var, target_1, target_2, target_3, sort, order)

                        parsed.append(call.representation)

                elif call_type == 'floor':
                    x = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op floor {target_var} {x} 0")

                elif call_type == 'ceil':
                    x = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op ceil {target_var} {x} 0")

                elif call_type == 'get_link':
                    arg_index = -1

                    link_num = get_var(last_func, arguments, functions, arg_index + 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f'getlink {target_var} {link_num}')

                elif call_type == 'pack_color':
                    arg_index = -1

                    red = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    green = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    blue = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    alpha = get_var(last_func, arguments, functions, arg_index + 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f'packcolor {target_var} {red} {green} {blue} {alpha}')

                elif call_type == 'lookup':
                    arg_index = -1

                    lookup_type = get_var(last_func, arguments, functions, arg_index := arg_index + 1)
                    target_num = get_var(last_func, arguments, functions, arg_index + 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"lookup {lookup_type} {target_var} {target_num}")

                elif call_type == 'read':
                    value_pos = get_var(last_func, arguments, functions, 0)
                    storage_type = arguments[1]
                    storage_id = get_var(last_func, arguments, functions, 2)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"read {target_var} {storage_type}{storage_id} {value_pos}")

                elif call_type == 'write':
                    data = get_target_var(last_func, arguments, functions)
                    value_pos = get_var(last_func, arguments, functions, 1)
                    storage_type = arguments[2]
                    storage_id = get_var(last_func, arguments, functions, 3)

                    parsed.append(f"write {data} {storage_type}{storage_id} {value_pos}")

                elif call_type == 'sin':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op sin {target_var} {value} 0")

                elif call_type == 'cos':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op cos {target_var} {value} 0")

                elif call_type == 'sqrt':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op sqrt {target_var} {value} 0")

                elif call_type == 'max':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op max {target_var} {value} {value_2}")

                elif call_type == 'min':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op min {target_var} {value} {value_2}")

                elif call_type == 'angle':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op angle {target_var} {value} {value_2}")

                elif call_type == 'angle_difference':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op angleDiff {target_var} {value} {value_2}")

                elif call_type == 'len':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op len {target_var} {value} {value_2}")

                elif call_type == 'noise':
                    value = get_var(last_func, arguments, functions, 0)
                    value_2 = get_var(last_func, arguments, functions, 1)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op noise {target_var} {value} {value_2}")

                elif call_type == 'absolute':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op abs {target_var} {value} 0")

                elif call_type == 'log':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op log {target_var} {value} 0")

                elif call_type == 'log10':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op log10 {target_var} {value} 0")

                elif call_type == 'random':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op rand {target_var} {value} 0")

                elif call_type == 'tan':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op tan {target_var} {value} 0")

                elif call_type == 'asin':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op asin {target_var} {value} 0")

                elif call_type == 'acos':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op acos {target_var} {value} 0")

                elif call_type == 'atan':
                    value = get_var(last_func, arguments, functions, 0)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f"op atan {target_var} {value} 0")

                elif call_type == 'idle':
                    parsed.append('ucontrol idle 0 0 0 0 0')

                elif call_type == 'stop':
                    parsed.append('ucontrol stop 0 0 0 0 0')

                elif call_type == 'pathfind':
                    pos_x = get_var(last_func, arguments, functions, 0)
                    pos_y = get_var(last_func, arguments, functions, 1)

                    parsed.append(f'ucontrol pathfind {pos_x} {pos_y} 0 0 0')

                elif call_type == 'automatic_pathfind':
                    parsed.append('ucontrol autoPathfind 0 0 0 0 0')

                elif call_type == 'boost':
                    boost_bool = get_var(last_func, arguments, functions, 0)

                    parsed.append(f'ucontrol boost {boost_bool} 0 0 0 0')

                elif call_type == 'target':
                    pos_x = get_var(last_func, arguments, functions, 0)
                    pos_y = get_var(last_func, arguments, functions, 1)
                    shoot = get_var(last_func, arguments, functions, 2)

                    parsed.append(f'ucontrol target {pos_x} {pos_y} {shoot} 0 0')

                elif call_type == 'predictive_target':
                    unit = get_var(last_func, arguments, functions, 0)
                    shoot = get_var(last_func, arguments, functions, 1)

                    parsed.append(f'ucontrol targetp {unit} {shoot} 0 0 0')

                elif call_type == 'drop_item':
                    destination = get_var(last_func, arguments, functions, 0)
                    amount = get_var(last_func, arguments, functions, 1)

                    parsed.append(f'ucontrol itemDrop {destination} {amount} 0 0 0')

                elif call_type == 'take_item':
                    target = get_var(last_func, arguments, functions, 0)
                    item = get_var(last_func, arguments, functions, 1)
                    amount = get_var(last_func, arguments, functions, 2)

                    parsed.append(f'ucontrol itemTake {target} {item} {amount} 0 0')

                elif call_type == 'drop_payload':
                    parsed.append(f'ucontrol payDrop 0 0 0 0 0')

                elif call_type == 'take_payload':
                    amount = get_var(last_func, arguments, functions, 0)

                    parsed.append(f'ucontrol payTake {amount} 0 0 0 0')

                elif call_type == 'enter_payload':
                    parsed.append(f'ucontrol payEnter 0 0 0 0 0')

                elif call_type == 'mine':
                    pos_x = get_var(last_func, arguments, functions, 0)
                    pos_y = get_var(last_func, arguments, functions, 1)

                    parsed.append(f'ucontrol mine {pos_x} {pos_y} 0 0 0')

                elif call_type == 'flag':
                    value = get_var(last_func, arguments, functions, 0)

                    parsed.append(f'ucontrol flag {value} 0 0 0 0')

                elif call_type == 'build':
                    pos_x = get_var(last_func, arguments, functions, 0)
                    pos_y = get_var(last_func, arguments, functions, 1)
                    block = get_var(last_func, arguments, functions, 2)
                    rotation = get_var(last_func, arguments, functions, 3)
                    config = get_var(last_func, arguments, functions, 4)

                    parsed.append(f'ucontrol build {pos_x} {pos_y} {block} {rotation} {config}')

                elif call_type == 'get_block':
                    pos_x = get_var(last_func, arguments, functions, 0)
                    pos_y = get_var(last_func, arguments, functions, 1)
                    block_type = get_var(last_func, arguments, functions, 2)
                    building = get_var(last_func, arguments, functions, 3)
                    floor = get_var(last_func, arguments, functions, 4)

                    parsed.append(f'ucontrol build {pos_x} {pos_y} {block_type} {building} {floor}')

                elif call_type == 'within':
                    pos_x = get_var(last_func, arguments, functions, 1)
                    pos_y = get_var(last_func, arguments, functions, 2)
                    radius = get_var(last_func, arguments, functions, 3)

                    for assignment in assignments:
                        target_var = get_target_var(last_func, [assignment], functions)
                        parsed.append(f'ucontrol within {pos_x} {pos_y} {radius} {target_var} 0')

                elif call_type == 'unbind':
                    parsed.append(f'ucontrol unbind 0 0 0 0 0')

                elif call_type == 'func_call':
                    # print(functions[func_name]['arguments'])
                    func_references += 1
                    parsed.append(f'FUNC---REFERENCE---{func_name}---["{'", "'.join(arguments)}"]---{last_func}')

                elif call_type == "return":
                    # return var;
                    line_split = line.strip().split(" ")
                    part_to_return = line_split[1].removesuffix(";")
                    full_to_return = f"set {last_func}_ret {last_func}_{part_to_return}"

                    parsed.append(full_to_return)

                elif call_type == 'import':
                    line_split = line.strip().split(" ")
                    file_to_import = line_split[1].removesuffix(";")
                    import_path = Path(f"{parent_path.__str__()}/{file_to_import}")
                    import_parent = import_path.parent

                    if not import_path.exists():
                        raise InvalidPath

                    with open(import_path, 'r') as fi:
                        import_content = fi.read()
                        compiled_import, exposed_funcs = parse(import_content, import_parent, True)
                        exposed_funcs: dict

                        for instruction in compiled_import:
                            parsed.append(instruction)
                        for exposed_func_name in exposed_funcs.keys():
                            functions[exposed_func_name] = exposed_funcs[exposed_func_name]

                elif call_type == "":
                    print(line)
                    print(call_type)
                    raise CallDoesNotExist

                break
            elif char == " " and not in_quotes and not in_assign_tuple:
                previous_word = current_word
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
            elif char == "," and not in_quotes:
                word = current_word.removeprefix(",").strip()
                current_word = ""

                if in_parentheses:
                    arguments.append(word)
                    continue
                in_assign_tuple = True
                assignments.append(word)

            elif char == "=" and not in_quotes and not in_assignment:
                assign_tuple = in_assign_tuple
                word = current_word.removeprefix(",").strip()
                in_assign_tuple = False
                current_word = ""
                in_assignment = True
                call_type = "var"

                if not assign_tuple and len(arguments) != 0:
                    assignments = arguments
                    arguments = []
                    continue
                elif not assign_tuple and len(arguments) == 0:
                    assignments.append(previous_word)
                    continue

                assignments.append(word)

            elif char == "{" and not in_quotes:
                if call_type == 'def':
                    line_split = line.split(" ")
                    function_name = line_split[1].split('(')[0]
                    # print(function_name)

                    functions[function_name] = {
                        'arguments': arguments,
                    }

                    if branch_call_queue['def'] == 0:
                        parsed.append('op add main_exit @counter 0')
                        parsed.append('jump main always')

                    last_func = function_name
                    parsed.append(f"START---OF---BLOCK---{call_type}---{index}---{function_name}---{arguments}")
                else:
                    parsed.append(f"START_OF_BLOCK_{call_type}_{index} {arguments[0]} {last_func}")

                branch_queue.append(f"{call_type}_{index}")

                branch_call_queue[call_type] += 1

            elif char == "}" and not in_quotes:
                parsed.append(f"END_OF_BLOCK_{branch_queue.pop(-1)}")

            current_word += char

    while func_references >= 1:
        # FUNC---REFERENCE---foo---(X, Y, Z)---main
        # 0      1           2     3           4
        start_index = index_starts_with("FUNC---REFERENCE---", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("---")
        # split_line[2] will look like this: foo-(X, Y, Z)
        func_name = split_line[2]

        args: tuple = json.loads(split_line[3])

        next_index = start_index
        ref_func_name = split_line[4]

        for index, arg_name in enumerate(functions[func_name]['arguments']):
            arg = get_target_var(ref_func_name, [args[index]], functions)
            parsed.insert(next_index := next_index + 1, f'set {func_name}_{arg_name} {arg}')

        parsed.insert(next_index := next_index + 1, f'op add {func_name}_exit @counter 1')
        parsed.insert(next_index + 1, f'jump {func_name} always')
        parsed.pop(start_index)

        func_references -= 1

    while branch_call_queue['def'] >= 1:
        # START---OF---BLOCK---def---1---foo---['arg_1', 'arg_2', 'arg_3']
        # 0       1    2       3     4   5     6
        # START_OF_BLOCK_def_1_foo ['arg_1', 'arg_2', 'arg_3']
        # 0     1  2     3   4 5         6        7        8
        # 0                        1
        start_index = index_starts_with("START---OF---BLOCK---def", parsed)
        sof_line: str = parsed[start_index]
        split_line = sof_line.split("---")
        block_id = split_line[4]
        end_index = parsed.index(f"END_OF_BLOCK_def_{block_id}")

        func_name = split_line[5]

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
    if expose_funcs:
        return parsed, functions

    return parsed
