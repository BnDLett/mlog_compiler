import sys
from io import TextIOWrapper
from pathlib import Path

import mlog_compiler

print("This script is not ready for usage within the current version of this library.")
sys.exit(1)


# def mlog_compile(fi: TextIOWrapper | str = None, parent_path: str | Path = ""):
#     source = ""
#     running = False
#
#     if fi is None:
#         running = True
#     elif type(fi) is TextIOWrapper:
#         source = fi.read()
#     elif type(fi) is str:
#         source = fi
#     else:
#         raise TypeError(f"Unknown type {type(fi)}")
#
#     while running:
#         result = input("> ")
#         stripped_result = result.strip()
#
#         if stripped_result == "exit()" or stripped_result == "":
#             break
#
#         source += f"{result}\n"
#
#     parsed = mlog_compiler.parse(source.removesuffix("\n"), parent_path)
#     return parsed
#
#
# if __name__ == '__main__':
#     mlog_compile()
