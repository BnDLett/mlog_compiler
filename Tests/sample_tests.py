from mlog_compiler.RunCompiler import mlog_compile

sample = """
// Variable assignment
str example_str = "Hello, world!";
sense(enabled, switch1, enabled);
var not_enabled = !enabled;

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
var button_not_enabled = !button_enabled;

set_enabled(switch2, button_not_enabled);
// Update: I forgot my semicolon on the wait. 😭
wait(0.5);
"""

sample_2 = """
// Variable retrieval
sense(reactor_temp, reactor1, heat);
sense(reactor_on, switch1, enabled);
var not_overheat = reactor_temp < 0.1;

// Primary operation
var enable = not_overheat && reactor_on;
set_enabled(reactor1, enable);
"""

sample_3 = """
// Variable retrieval
sense(item_amount, container1, totalItems);
var size = item_amount / 4.29;

// Control display
clear(0, 0, 0, 1);
rectangle(5, 5, size, 10, 1);
update(1);

// Message blocks
print("Total Items: ", 1, false);
print(item_amount, 1);

print("Created by: [#003ec8]BnDLett", 2);
"""

sample_4 = """
// Variable grabbing
var radius = 4;
sense(pos_x, point1, x);
sense(pos_y, point1, y);

// Binding
bind(poly);

// Controlling
approach(pos_x, pos_y, radius);
"""


if __name__ == "__main__":
    result = mlog_compile(sample_4)

    buffer = ""

    for line in result:
        buffer += f"{line}\n"
    print(buffer.removesuffix("\n"))