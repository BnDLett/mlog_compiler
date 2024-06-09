# mlog_compiler
A Python program that compiles a custom language into mlog.

# What is currently supported?
The custom language currently supports the following:
- Print statements
- Variable assignment
- Comments
- Enabling/disabling blocks
- If statements
- Sensing data from blocks
- Wait statements
- Logical comparative operations
- Mathematical operations
- Bitwise comparative operations
- Drawing on a display
- Unit binding and (basic) controlling. 

With much more planned to come.

# What is an example of it in use?
Here is an example of it in use:
```cpp
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
```
This compiles down to:
```mlog
set example_str "Hello, world!"
sensor enabled switch1 @enabled
op notEqual not_enabled enabled 1
control enabled conveyor1 enabled 0 0 0
jump 7 notEqual enabled 1
print "The button is enabled."
printflush message1
jump 10 notEqual not_enabled 1
print "The button is disabled."
printflush message1
end
```

# I need your help.
## The situation
As of now, the language is still under heavy development. We're missing a lot of features.
## How can you help.
Recommending changes to the syntax would be greatly appreciated. Alongside that, suggestions for what the language
should be called would also be appreciated.

I would prefer if suggestions regarding the structure of compiler's code itself is kept to a minimal. This is entirely a
learning experience for me and I'd prefer to avoid having the code mangled in ways that can make it harder to develop.
Although, once I am ready to add changes to the compiler that optimizes development, then I will specify so here.
