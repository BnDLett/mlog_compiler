from io import TextIOWrapper
import mlog_compiler

sample = """
// Variable assignment
str example_str = "Hello, world!";
sense(enabled, switch1, enabled);
num not_enabled = not enabled;

// Primary code
set_enabled(conveyor1, enabled);
if (enabled) {
    print("The button is enabled.", 1);
}
if (not_enabled) {
    print("The button is disabled.", 1);
}

// Wait testing. (Don't forget your semi-colons, kids)
// sense(button_enabled, switch2, enabled);
// num button_not_enabled = not button_enabled;

// set_enabled(switch2, button_not_enabled);
// Update: I forgot my semicolon on the wait. 😭
// wait(0.5);
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
