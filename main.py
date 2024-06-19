from io import TextIOWrapper
from pathlib import Path
from sys import argv
from mlog_compiler.RunCompiler import mlog_compile

arguments = {
    'output': '',
    'terminal': False,
    'file': '',

}
truth_statements = ["true", "yes"]

for index, arg in enumerate(argv):
    arg = arg.lower()

    if len(argv) == 1:
        break

    index_next = len(argv) != (index + 1)
    next_arg = argv[index + index_next].lower()

    if arg in ['-o', '--output']:
        arguments['output'] = next_arg
    elif arg in ['-t', '--terminal']:
        arguments['terminal'] = True
    elif arg in ['-f', '--file']:
        arguments['file'] = next_arg


def main(args: dict[str: str | bool]) -> int:
    """
    Takes the args and appropriately executes the compiler based on it.

    The following status codes will be returned: \n
    0: No error. \n
    1: File argument is empty. \n
    2: No output destination was specified. \n

    :param args: The arguments to use.
    :return: int
    """
    if args['file'] == '':
        return 1

    path = Path(args['file'])

    with open(path, 'r') as fi:
        # For some reason, PyCharm thinks that open() returns TextIO despite the type hint specifying that it will
        # return a TextIOWrapper.
        fi: TextIOWrapper
        result = mlog_compile(fi, path.parent)

    result_str = "\n"

    # for line in result:
    #     buffer += f"{line}\n"
    result_str = result_str.join(result)

    if args['terminal']:
        print(result_str.removesuffix("\n"))
        return 0

    elif args['output'] != '':
        out_fi = open(args['output'], 'w')
        out_fi.write(result_str)
        return 0

    return 2


if __name__ == "__main__":
    # try:
    #     main()
    # except Exception:
    #     pass
    exit_code = main(arguments)
    exit(exit_code)
