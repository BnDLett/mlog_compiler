from io import TextIOWrapper
import mlog_compiler

sample = """
// Variable assignment
str example_str = "Hello, world!";
sense(enabled, switch1, enabled);
var not_enabled = enabled != 1;

// Primary code
set_enabled(conveyor1, enabled);
if (enabled) {
    print("The button is enabled.", 1);
}
if (not_enabled) {
    print("The button is disabled.", 1);
}

// Wait testing. (Don't forget your semi-colons, kids)
sense(button_enabled, switch2, enabled);
var button_not_enabled = not button_enabled;

set_enabled(switch2, button_not_enabled);
// Update: I forgot my semicolon on the wait. 😭
wait(0.5);
"""

sample_2 = """
// Variable retrieval
sense(reactor_temp, reactor1, heat);
sense(reactor_on, switch1, enabled);
var not_overheat = reactor_temp < 0.1;

var enable == not_overheat and reactor_on;
set_enabled(reactor1, enable);
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
    main(sample_2)
