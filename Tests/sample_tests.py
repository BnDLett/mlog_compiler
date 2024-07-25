# from mlog_compiler.RunCompiler import mlog_compile
import sys

sample_1 = """
def main() {
    // Variable.py assignment
    str example_str = "Hello, world!";
    var enabled = sense(switch1, enabled);
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
    var button_enabled = sense(switch2, enabled);
    var button_not_enabled = !button_enabled;
    
    set_enabled(switch2, button_not_enabled);
    // Update: I forgot my semicolon on the wait. 😭
    wait(0.5);
}
"""

sample_2 = """
def main() {
    // Variable.py retrieval
    var reactor_temp = sense(reactor1, heat);
    var reactor_on = sense(switch1, enabled);
    var not_overheat = reactor_temp < 0.1;
    
    // Primary operation
    var enable = not_overheat && reactor_on;
    set_enabled(reactor1, enable);
}
"""

sample_3 = """
def main() {
    // Variable.py retrieval
    var item_amount = sense(container1, totalItems);
    var size = item_amount / 4.29;
    
    // Control display
    clear(0, 0, 0, 1);
    rectangle(5, 5, size, 10, 1);
    update(1);
    
    // Message blocks
    print("Total Items: ", 1, false);
    print(item_amount, 1);
    
    print("Created by: [#003ec8]BnDLett", 2);
}
"""

sample_4 = """
def main() {
    // Variable.py grabbing
    var radius = 10;
    var pos_x = sense(point1, x);
    var pos_y = sense(point1, y);
    
    unit_radar(unit, player, ally, any, distance, 1);
    var ally_x = sense(unit, x);
    var ally_y = sense(unit, y);
    
    floor(floored_x, ally_x);
    floor(floored_y, ally_y);
    
    var switch_enabled = sense(switch1, enabled);
    var not_enabled = !switch_enabled;
    
    var diff_x = floored_x - @thisx;
    var diff_y = floored_y - @thisy;
    floor(diff_x, diff_x);
    floor(diff_y, diff_y);
    
    // Binding
    bind(poly);
    
    // Controlling
    if (switch_enabled) {
        approach(floored_x, floored_y, radius);
    }
    if (not_enabled) {
        approach(pos_x, pos_y, radius);
    }
    
    // Data printing
    print("x: ", 1, 0);
    print(diff_x, 1, 0);
    print("\\n", 1, 0);
    
    print("y: ", 1, 0);
    print(diff_y, 1);
    
    print("Created by: [#003ec8]BnDLett", 2);
}
"""

sample_5 = """
def main() {
    var run = 1;
    var num = 0;
    while (run) {
        print(num, 1);
        var num = num + 1;
    }
    
    if (cond) {
        print(1, 2);
        if (cond_2) {
            print(2, 2);
        }
        print(3, 2);
    }
}
"""

sample_6 = """
def foo(x) {
    // <name>_ret is the function's return value
    var result = x + 2;
    return result;
}

def main() {
    foo(3);
    print(foo_ret, 1);
    var example = 4;
}
"""

sample_7 = """
def main() {
    var var_x = 9 != 2;
    var sensed = sense(block1, enabled);
}
"""

sample_to_run = sample_1

if __name__ == "__main__":
    print("This script is not ready for usage within the current version of this library.")
    sys.exit(1)

    # result = mlog_compile(sample_to_run)
    #
    # buffer = ""
    #
    # for index, line in enumerate(result):
    #     # buffer += f"[{str(index).rjust(3, '0')}] {line}\n"
    #     buffer += f"{line}\n"
    #
    # print(buffer.removesuffix("\n"))
