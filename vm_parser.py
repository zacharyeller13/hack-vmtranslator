"""
Parser module for parsing .vm file into its lexical components and providing access
to those components.
Ignores all whitespace and comments
"""

from dataclasses import dataclass

from constants import COMMENT, VAR_START


class Command:
    """
    Holds a VM command with its full command, type, translation, and parts

    Attributes:
        `command` (str): the full command
        `c_type` (str): the type of the command.  Is one of:
            - arithmetic
            - push
            - pop
            - label
            - goto
            - if
            - function
            - return
            - call
        `translation` (list[str]): the full translation of the command in multiple lines of
            ASM commands
    """

    def __init__(self, command) -> None:
        self.command: str = command
        self.c_type: str = self._set_type(command)
        self.translation: list[str] = []

    def _set_type(self, command: str) -> str:
        if (command_start := command.split()[0]) not in ("push", "pop"):
            return "arithmetic"
        return command_start

    def arg1(self) -> str:
        """
        Returns the 1st argument to the command.  If `c_type` == "arithmetic", returns the command
        """

        if self.c_type == "return":
            raise TypeError(f"Method not supported for Command of type {self.c_type}")

        if self.c_type == "arithmetic":
            return self.command
        return self.command.split()[1]

    def arg2(self) -> str:
        """
        Returns the 2nd argument to the command.  Should only run if `c_type` is in:
            - push
            - pop
            - function
            - call
        """

        if self.c_type not in ("push", "pop", "function", "call"):
            raise TypeError(f"Method not supported for Command of type {self.c_type}.")

        return self.command.split()[2]


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


# TODO: Arithemtic/Logic commands
# add, sub, neg, eq, gt, lt, and, or, not

# TODO: Memory access commands
# pop, push

# TODO: Branching Commands
# label, goto, if-goto

# TODO: Function commands
# function, call, return
