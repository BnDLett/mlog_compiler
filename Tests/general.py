from io import TextIOWrapper

import mlog_compiler

sample = """int variable = 3;
str example_str = "Hello, world!";
str another_str = "Hello, Discord!";
float balloon = 3.14159;
"""


def main(fi: TextIOWrapper | str = None):
    source = ""
    running = False

    if fi is None:
        running = True
    elif type(fi) is TextIOWrapper:
        source = fi.read()
    elif type(fi) is str:
        source = fi

    while running:
        result = input("> ")
        stripped_result = result.strip()

        if stripped_result == "exit()" or stripped_result == "":
            break

        source += f"{result}\n"

    result = mlog_compiler.parse(source.removesuffix("\n"))
    buffer = ""

    for line in result:
        buffer += f"{line}\n"
    print(buffer.removesuffix("\n"))


if __name__ == '__main__':
    main(sample)
