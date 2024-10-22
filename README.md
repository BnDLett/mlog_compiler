# mlog_compiler
A Python program that compiles a custom-syntax programming language into mlog.

# Note!
This version of the compiler is still in a rework stage. Expect *a lot* of breaking changes until this is pushed into
the master branch. There are also a lot of missing features, so don't expect a lot until this is further polished out.

# What is currently supported?
I'll work on this list later.

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
### minor
A feature was added or a non-significant change was added. For example, a new set of keywords. Although, it should be
noted that non-backwards-compatible changes can be implemented on this field. If you wish to upgrade the minor field, then
you should check the history between your current version and the version that you wish to upgrade to in order to ensure
that a breaking change has not been implemented.

### patch
A patch, bug fix, or insignificant change was added. This should never include any non-backwards-compatible
changes that will affect source code. With that said, you can freely upgrade patch version without worry about breaking
changes to the syntax of the language.
