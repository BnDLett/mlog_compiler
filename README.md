# mlog_compiler
A Python program that compiles a custom language into mlog.

# What is currently supported?
The custom language currently supports the following:
- print statements
- variable assignment
- comments

With much more planned to come.

# What is an example of it in use?
Here is an example of it in use:
```cpp
// Variable assignment
int variable = 3;
str example_str = "Hello, world!";
str another_str = "Hello, Discord!";
float balloon = 3.14159;

// Printing a variable
print(example_str, 1);
```
This compiles down to:
```mlog
set variable 3
set example_str "Hello, world!"
set another_str "Hello, Discord!"
set balloon 3.14159
print example_str
printflush message1
```

# I need your help.
## The situation
As of now, the language is still under heavy development. We're missing a lot of features.
## How can I help?
Recommending changes to the syntax would be greatly appreciated. Alongside that, suggestions for what the language
should be called would also be appreciated.

I would prefer if suggestions regarding the structure of compiler's code itself is kept to a minimal. This is entirely a
learning experience for me and I'd prefer to avoid having the code mangled in ways that can make it harder to develop.
Although, once I am ready to add changes to the compiler that optimizes development, then I will specify so here.
