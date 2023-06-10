# pylint: disable=invalid-name
"""
Main VM Translator program. Does not conform to naming convention in order
to comply with submission rules of the Nand2Tetris course.
"""

from argparse import ArgumentParser, Namespace
import os
import sys

from asm_writer import translate_commands, write_init, write_translated_asm
from vm_parser import parse_commands, parse_directory, parse_file


def initialize_argparser() -> ArgumentParser:
    """
    Initialize the ArgumentParser for command-line-arguments
    """

    arg_parser = ArgumentParser(
        prog="VMTranslator",
        description="Translate .vm file(s) into Hack assembly code.",
    )
    arg_parser.add_argument(
        "file_or_dir",
        metavar="file.vm or /dirname/",
        type=str,
        help="absolute filepath of the .vm file or directory to be translated",
    )

    return arg_parser


def initialize_arguments(arg_parser: ArgumentParser) -> Namespace:
    """
    Parse command-line-arguments
    """

    arg_namespace = arg_parser.parse_args()

    if arg_namespace.file_or_dir[-3:] != ".vm" and not os.path.isdir(
        arg_namespace.file_or_dir
    ):
        arg_parser.print_usage()
        sys.exit()

    return arg_namespace


def main() -> None:
    args = initialize_argparser()
    file_or_dir = initialize_arguments(args).file_or_dir

    if os.path.isdir(file_or_dir):
        out_file_name = f"{file_or_dir}/{os.path.basename(file_or_dir)}"
        write_init(out_file_name)
        files = parse_directory(file_or_dir)
        commands = []
        for file in files:
            lines = parse_file(file)
            commands.extend(parse_commands(lines, os.path.basename(file)))
    else:
        out_file_name = file_or_dir[:-3]
        lines = parse_file(file_or_dir)
        commands = parse_commands(lines, os.path.basename(file_or_dir))

    translate_commands(commands)
    write_translated_asm(out_file_name, commands)


if __name__ == "__main__":
    main()
