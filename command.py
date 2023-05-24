"""
Command module
"""

from typing import Self

from constants import ARITHMETIC_COMMANDS, COMMENT, CType


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

        Start by appending the command itself as a comment, then use string formatting
            to append the current `label_count` to any labels/references to labels.
        """

        self.translation.append(f"{COMMENT} {self.command}")

        if self.c_type == CType.ARITHMETIC:
            self._translate_arithmetic()
            return
        elif self.c_type == CType.PUSH:
            self._translate_push()
            return
        elif self.c_type == CType.POP:
            self._translate_pop()
            return
        else:
            raise NotImplementedError

    def _translate_arithmetic(self):
        """
        Translate a command when its `CType` is arithmetic.


        """

        translation = ARITHMETIC_COMMANDS[self.arg1]

        self.translation.extend(
            [line.format(Command.label_count) for line in translation]
        )

        if self.arg1 in ("eq", "gt", "lt"):
            Command.label_count += 1

    def _translate_push(self):
        """
        Translate a command when its `CType` is push.

        Example:
            `push constant 17` ->
            // push constant 17
            @17
            D=A
            @SP
            A=M
            M=D
            M=M+1
        """

        # All push operations have arg1 and arg2, so go ahead and assign to local variables
        segment = self.arg1
        index = int(self.arg2)

        # Implementation of `push constant n`
        if segment == "constant":
            self.translation.extend([f"@{index}", "D=A", "@SP", "A=M", "M=D", "M=M+1"])

        # TODO: segment
        # - local
        # - argument
        # - this
        # - that
        # - constant
        # - static
        # - pointer
        # - temp
        # TODO: index

    def _translate_pop(self):
        """
        Translate a command when its `CType` is pop. "Constant" memory segment
            does not have a pop method.

        Example:
            `pop local 1` ->
            // pop local 1
            @SP
            AM=M-1
            D=M
            @LCL
            A=M
            A=A+1
            M=D
        """

        # Same as with push, all pop operations have arg1 and arg2; assign to local variables
        segment = self.arg1
        index = int(self.arg2)

        # implementation of `pop local n`
        if segment == "local":
            moves = ["A=A+1"] * index
            self.translation.extend(
                ["@SP", "AM=M-1", "D=M", "@LCL", "A=M", *moves, "M=D"]
            )

        # TODO: segment
        # - local
        # - argument
        # - this
        # - that
        # - static
        # - pointer
        # - temp
        # TODO: index
        # TODO: command push or pop
