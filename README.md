# mlog_compiler
A Python program that compiles a custom-syntax programming language into mlog.

# Note!
This is just me experimenting with abstract syntax trees and lexers to get a feel for them. I cannot guarantee that
this version will be the version that I go with. As such, don't expect regular updates or stability either. *(However,
I am not saying that I won't develop this further -- just that there is a possibility that I won't)*

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
