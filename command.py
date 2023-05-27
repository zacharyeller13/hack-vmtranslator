"""
Command module
"""

from constants import ARITHMETIC_COMMANDS, COMMENT, CType, SEGMENTS


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

    def __eq__(self, other) -> bool:
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

    def translate(self, filename: str = "") -> None:
        """
        Translates a command from its VM code to its assembly code

        Start by appending the command itself as a comment, then use string formatting
            to append the current `label_count` to any labels/references to labels.

        Args:
            filename (str): The name of the vm file being translated
        """

        self.translation.append(f"{COMMENT} {self.command}")

        if self.c_type == CType.ARITHMETIC:
            self._translate_arithmetic()
            return
        elif self.c_type == CType.PUSH:
            self._translate_push(filename)
            return
        elif self.c_type == CType.POP:
            self._translate_pop(filename)
            return
        else:
            raise NotImplementedError

    def _translate_arithmetic(self) -> None:
        """
        Translate a command when its `CType` is arithmetic.
        """

        translation = ARITHMETIC_COMMANDS[self.arg1]

        self.translation.extend(
            [line.format(Command.label_count) for line in translation]
        )

        if self.arg1 in ("eq", "gt", "lt"):
            Command.label_count += 1

    def _translate_push(self, filename: str) -> None:
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

        Args:
            filename (str): Name of vm file being translated
        """

        # All push operations have arg1 and arg2, so go ahead and assign to local variables
        segment = self.arg1
        index = int(self.arg2)

        # Implementation of `push constant n`
        if segment == "constant":
            self.translation.extend([f"@{index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"])

        # Implementation of `push local/argument/this/that n`
        # Push item at LCL[index]/ARG[index]/THIS[index]/THAT[index] onto stack
        elif segment in SEGMENTS.keys():
            self.translation.extend(
                [
                    f"@{index}",
                    "D=A",
                    f"@{SEGMENTS[segment]}",
                    "A=D+M",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            )

        # Implementation of `push temp n`
        # Push item at RAM[5+index] onto stack
        elif segment == "temp":
            self.translation.extend(
                [
                    "@5",
                    "D=A",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            )

        # Implementation of `push pointer 0/1`
        # Push item at THIS or THAT onto stack
        elif segment == "pointer":
            if index == 0:
                self.translation.extend(
                    ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                )
            else:
                self.translation.extend(
                    ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                )

        # Implementation of `push static n`
        # Push item at Foo.i onto the stack where Foo is the vm filename
        # and i is the index
        elif segment == "static":
            self.translation.extend(
                [f"@{filename}.{index}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            )

    def _translate_pop(self, filename: str) -> None:
        """
        Translate a command when its `CType` is pop. "Constant" memory segment
            does not have a pop method.

        Example:
            `pop local 1` ->
            // pop local 1
            @1
            D=A
            @LCL
            D=D+M
            @SP
            AM=M-1
            D=D+M
            A=D-M
            M=D-A

        Args:
            filename (str): Name of vm file being translated
        """

        # Same as with push, all pop operations have arg1 and arg2; assign to local variables
        segment = self.arg1
        index = int(self.arg2)

        # Implementation of `pop local/argument/this/that n`
        # Pop last item from stack into LCL[index]/ARG[index]/THIS[index]/THAT[index]
        if segment in SEGMENTS.keys():
            if index > 0:
                self.translation.extend(
                    [
                        f"@{index}",
                        "D=A",
                        f"@{SEGMENTS[segment]}",
                        "D=D+M",
                        "@SP",
                        "AM=M-1",
                        "D=D+M",
                        "A=D-M",
                        "M=D-A",
                    ]
                )
            else:
                self.translation.extend(
                    ["@SP", "AM=M-1", "D=M", f"@{SEGMENTS[segment]}", "A=M", "M=D"]
                )

        # Implementation of `pop temp n`
        # Pop last item from stack into RAM[5+index]
        elif segment == "temp":
            self.translation.extend(
                [
                    f"@{index}",
                    "D=A",
                    "@5",
                    "D=D+A",
                    "@SP",
                    "AM=M-1",
                    "D=D+M",
                    "A=D-M",
                    "M=D-A",
                ]
            )

        # Implementation of `pop pointer 0/1`
        # Pop last item from stack into THIS or THAT
        elif segment == "pointer":
            if index == 0:
                self.translation.extend(["@SP", "AM=M-1", "D=M", "@THIS", "M=D"])
            else:
                self.translation.extend(["@SP", "AM=M-1", "D=M", "@THAT", "M=D"])

        # Implementation of `pop static n`
        # Pop last item from stack into variable Foo.i
        # where i is the index and Foo is the .vm filename
        elif segment == "static":
            self.translation.extend(
                ["@SP", "AM=M-1", "D=M", f"@{filename}.{index}", "M=D"]
            )
