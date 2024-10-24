from typing import override
from BaseCompiler import BaseCompiler
from TypeCheck import TypeCheck


def _main(compiler: BaseCompiler):
    compiler.register_type("int", TypeCheck.ensure_int)
    compiler.register_type("str", TypeCheck.ensure_str)

    # Scope functionality isn't going to be supported.
    # compiler.register_scope_type('if', False, 1)

    @compiler.register_keyword('add', 3)
    def k_add(self: BaseCompiler, arguments: tuple[str], line_number: int):
        variable = arguments[0]
        x = arguments[1]
        y = arguments[2]

        return f"op add {variable} {x} {y}"

    @compiler.register_keyword('sub', 3)
    def k_sub(self: BaseCompiler, arguments: tuple[str], line_number: int):
        variable = arguments[0]
        x = arguments[1]
        y = arguments[2]

        return f"op sub {variable} {x} {y}"

    @compiler.register_keyword('div', 3)
    def k_mul(self: BaseCompiler, arguments: tuple[str], line_number: int):
        variable = arguments[0]
        x = arguments[1]
        y = arguments[2]

        return f"op mul {variable} {x} {y}"

    @compiler.register_keyword('div', 3)
    def k_div(self: BaseCompiler, arguments: tuple[str], line_number: int):
        variable = arguments[0]
        x = arguments[1]
        y = arguments[2]

        return f"op div {variable} {x} {y}"

    @compiler.register_keyword('print', 2)
    def k_print(self: BaseCompiler, arguments: tuple[str], line_number: int):
        to_print = arguments[0]
        message_block = arguments[1]

        TypeCheck.ensure_int(message_block)

        return f"print {to_print}", f"printflush message{message_block}"


class Compiler(BaseCompiler):
    @override
    def __init__(self, code: str | list):
        super(Compiler, self).__init__(code)

        _main(self)


def main(code: str):
    comp = Compiler(code)

    comp.compile_all()

    print(comp.unlinked_result)

# This is just here for bench marking
if __name__ == "__main__":
    import time

    test_code = (
        "int asd;"
        "add(asd, -3.141, 2);"
        "str x = \"Lorem ipsum dolor sit amet.\";"
        "print(\"lorem i\n\n\n"
        "psum\", 1);"
    )

    iterations = 1
    start = time.time_ns()
    for i in range(iterations):
        main(test_code)
    end = time.time_ns()

    duration = (end - start) / iterations
    print(f"Times ran: {iterations}\n"
          f"Lines compiled: {iterations * 4}\n"
          f"Duration (ns): {duration}\n"
          f"Duration (ms): {duration / (1 * 10**6)}\n"
          f"Duration (s): {duration / (1 * 10**9)}")
