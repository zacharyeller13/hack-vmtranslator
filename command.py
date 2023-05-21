"""
Command module
"""

from typing import Self

from constants import ARITHMETIC_COMMANDS, CType


class Command:
    """
    Holds a VM command with its full command, type, translation, and parts

    Attributes:
        `label_count` (int): class attribute that counts number of commands used with labels.
            To help create unique labels for each command.
        `command` (str): the full command
        `c_type` (CType): the type of the command.  Is one of:
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

    label_count: int = 0

    def __init__(self, command: str) -> None:
        self.command: str = command
        self.c_type: str = self._set_type(command)
        self.translation: list[str] = []

    def __eq__(self, other: Self) -> bool:
        return self.command == other.command and self.c_type == other.c_type

    def _set_type(self, command: str) -> str:
        if (command_start := command.split()[0]) not in (CType.POP, CType.PUSH):
            return CType.ARITHMETIC
        return command_start

    @property
    def arg1(self) -> str:
        """
        Returns the 1st argument to the command.  If `c_type` == "arithmetic", returns the command.
        Does not support `c_type` of "return"
        """

        if self.c_type == CType.RETURN:
            raise TypeError(f"Method not supported for Command of type {self.c_type}")

        if self.c_type == CType.ARITHMETIC:
            return self.command
        return self.command.split()[1]

    @property
    def arg2(self) -> str:
        """
        Returns the 2nd argument to the command.  Raises an error if `c_type` is not one of:
            - push
            - pop
            - function
            - call
        """

        if self.c_type not in (CType.PUSH, CType.POP, CType.FUNCTION, CType.CALL):
            raise TypeError(f"Method not supported for Command of type {self.c_type}.")

        return self.command.split()[2]

    def translate(self) -> None:
        """
        Translates a command from its VM code to its assembly code
        """

        if self.c_type == CType.ARITHMETIC:
            translation = ARITHMETIC_COMMANDS[self.arg1]

            self.translation = [
                line.format(Command.label_count) for line in translation
            ]

            if self.arg1 in ("eq", "gt", "lt"):
                Command.label_count += 1
            return
        raise NotImplementedError
