# mlog_compiler
A Python program that compiles a custom-syntax programming language into mlog.

# Note!
## The Present Situation
Even though this branch says "oop_version," that doesn't mean that this version of the compiler supports the OOP
paradigm in the language. It just means that the compiler itself was written in OOP. I'd also highly advise against
using this version of the compiler as there are mistakes that I am not willing to go back and fix. As such, you're going
to have some issues with using this version. Especially given the lack of proper scopes (there is functionality in the
works for it; however, that functionality is not completed, and it likely won't be.)
## The future goal
The future goal as of now is to do something similar to this, but with a *lexer* and an *AST*. I'll likely do that in 
Java, which is an OOP language. Given that, it should work *extremely* well for my use case. Although, currently, this
lacks a proper lexer and AST. Therefore, it isn't on the same caliber as other compilers would be. I may also do Rust,
which would be great for a functional version of this compiler. Although, given the way that Rust is in terms of its
learning curve, it could be a no-go.

# What is currently supported?
Basic keywords and typing.

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

## 0/1.minor.patch
### Major Version 0
The first iteration of the compiler that was done in Python. It didn't include either a specific AST or a specific
lexer.
### Major Version 1
The second iteration of the compiler that was also done in Python; however, it took more of an OOP approach. Similar to
the first iteration (Major Version 0), it didn't include a specific lexer or AST.
### minor
A feature was added or a non-significant change was added. For example, a new set of keywords. Although, it should be
noted that non-backwards-compatible changes can be implemented on this field. If you wish to upgrade the minor field, then
you should check the history between your current version and the version that you wish to upgrade to in order to ensure
that a breaking change has not been implemented.

### patch
A patch, bug fix, or insignificant change was added. This should never include any non-backwards-compatible
changes that will affect source code. With that said, you can freely upgrade patch version without worry about breaking
changes to the syntax of the language.
