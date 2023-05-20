"""
Parser module for parsing .vm file into its lexical components and providing access
to those components.
Ignores all whitespace and comments
"""

from command import Command
from constants import COMMENT, VAR_START


def parse_file(file: str) -> list[str]:
    """
    Read in a file and parse it into
    a list of commands without whitespace or comments

    Args:
        `file` (str): The filepath to the file to be parsed

    Returns:
        list[str]: The file parsed into a list of strings without
            whitespace or comments
    """

    with open(file, "r", encoding="UTF-8") as f:
        lines = f.read().split("\n")
        lines = [
            line.split(COMMENT)[0].strip()
            for line in lines
            if line != "" and line[:2] != COMMENT
        ]

        return lines


def parse_commands(base_commands: list[str]) -> list[Command]:
    """
    Parse list of commands in string representation into a list of Command objects
    with component parts

    Args:
        `base_commands` (list[str]): The list of string commands

    Returns:
        list[Command]: The same list of commands, but parsed into Command objects with
            necessary fields
    """

    return [Command(command) for command in base_commands]


# TODO: Arithemtic/Logic commands
# add, sub, neg, eq, gt, lt, and, or, not

# TODO: Memory access commands
# pop, push

# TODO: Branching Commands
# label, goto, if-goto

# TODO: Function commands
# function, call, return
