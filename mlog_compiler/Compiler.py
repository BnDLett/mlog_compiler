from typing import override, Any
from BaseCompiler import BaseCompiler
from TypeCheck import TypeCheck


def _main(compiler: BaseCompiler):
    compiler.register_type("int", TypeCheck.ensure_int)
    compiler.register_type("str", TypeCheck.ensure_str)

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


if __name__ == "__main__":
    test_code = (
        "int asd;"
        "add(asd, -3.141, 2);"
        "str x = \"Lorem ipsum dolor sit amet.\";"
        "print(\"lorem ipsum\", 1);"
    )
    comp = Compiler(test_code)

    comp.compile_line(0)
    comp.compile_line(1)
    comp.compile_line(2)
    comp.compile_line(3)

    print(comp.compiled_result)
