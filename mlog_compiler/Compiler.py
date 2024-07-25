from typing import override
from BaseCompiler import BaseCompiler


def _main(compiler: BaseCompiler):
    @compiler.register_keyword('add', 3)
    def keyword_add(self, arguments: tuple[str]):
        variable = arguments[0]
        x = arguments[1]
        y = arguments[2]

        return f"op add {variable} {x} {y}"


class Compiler(BaseCompiler):
    @override
    def __init__(self, code: str | list):
        super().__init__(code)

        _main(self)


if __name__ == "__main__":
    code = "add(asd, 4, 2);"
    comp = Compiler(code)
    comp.compile_line(0)
    print(comp.compiled_result)
