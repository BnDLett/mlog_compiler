# mlog_compiler
A Python program that compiles a custom language into mlog.

# Migration from 0.13.x to 0.14.x
A lot of functionality has changed in `0.14.x`. If you try to compile any `0.13.x` compatible code, then you may run into
issues. In order to make the code functional again, you may need to implement a main function. Examples of that are
shown in the "examples" folder. Every example in it works.

This is overall a major change to the structure of the compiled code, so do expect bugs. If you do encounter a bug, then
please do open an issue with it so that I (or anyone else) can squash it.

It should also be noted that some functions still run legacy arguments, so you may need to specify the functions name
before a variable if an argument is legacy. For example: `bind(main_unit);`, where `main_unit` would be a unit defined
by a variable.

## What is a legacy argument?
A legacy argument is an argument that does not automatically append the function's name at the start of the argument.
That may require you to manually append the function's name to the start of the argument if necessary.

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
- Functions
- And more!

With more planned to come.

# Versioning schemes
## Why is a scheme necessary?
I believe it will be helpful to contributors and users to understand what each version number means. Generally speaking,
the versioning is based around semantic versioning, but it will break semver standards. This is primarily because it is
more helpful (as far as I know) to have a more specialized scheme over a generalized scheme. 

## General rules
- Any time a higher level version is incremented, the lower level number must be reset to zero. For example, `0.14.4` 
will become `0.15.0` when minor is incremented.
- A number should only be incremented on per-commit basis. For example, if a commit implements a minor change, then only
the minor version should be incremented by one. 

## 0.minor.patch
### minor
A feature was added or a non-significant change was added. For example, a new set of keywords. Although, it should be
noted that non-backwards-compatible changes can be implemented on this field. If you wish to upgrade the x field, then
you should check the history between your current version and the version that you wish to upgrade to in order to ensure
that a breaking change has not been implemented.

### patch
A patch, bug fix, or insignificant feature was added. This should never include any non-backwards-compatible
changes that will affect source code. With that said, you can freely upgrade patch version without worry about breaking
changes to the syntax of the language.

# I need your help.
## The situation
Currently, the language has had little feedback -- the syntax is based only on my personal experience. Not only that,
but as the language has grown, it has also had less and less debugging ran (only the bare minimum for functions).
## How you can help
Providing feedback and reporting bugs in the issues tab would be greatly appreciated. Alongside that, but the language
has gone unnamed ever since it has begun development. Opening a new discussion with an idea for a name would also be
greatly appreciated. Although, be practical -- I personally prefer not to have a meme name.

I would prefer if suggestions regarding the structure of compiler's code itself is kept to a minimal. This is entirely a
learning experience for me and I'd prefer to avoid having the code mangled in ways that can make it harder to develop.
Although, once I am ready to add changes to the compiler that optimizes development, then I will specify so here.
