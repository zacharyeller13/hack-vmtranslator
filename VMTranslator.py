# pylint: disable=invalid-name
"""
Main VM Translator program. Does not conform to naming convention in order
to comply with submission rules of the Nand2Tetris course.
"""

from argparse import ArgumentParser, Namespace
import sys

from vm_parser import parse_commands, parse_file


def initialize_argparser() -> ArgumentParser:
    """
    Initialize the ArgumentParser for command-line-arguments
    """

    arg_parser = ArgumentParser(
        prog="VMTranslator", description="Translate .vm file into Hack assembly code."
    )
    arg_parser.add_argument(
        "file",
        metavar="file.vm",
        type=str,
        help="absolute filepath of the .vm file to be translated",
    )

    return arg_parser


def initialize_arguments(arg_parser: ArgumentParser) -> Namespace:
    """
    Parse command-line-arguments
    """

    arg_namespace = arg_parser.parse_args()

    if arg_namespace.file[-3:] != ".vm":
        arg_parser.print_usage()
        sys.exit()

    return arg_namespace


def main() -> None:
    args = initialize_argparser()
    file = initialize_arguments(args).file

    lines = parse_file(file)
    commands = parse_commands(lines)

    # for command in commands:
    #     command.translate()
    #     print(command.translation)


if __name__ == "__main__":
    main()
