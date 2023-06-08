"""
Command module
"""

from __future__ import annotations

from constants import (
    ARITHMETIC_COMMANDS,
    COMMENT,
    CType,
    IF_GOTO,
    GOTO,
    LABEL,
    SEGMENTS,
)


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
        self._current_function: str = ""

    def __eq__(self, other) -> bool:
        return (self.command == other.command) and (self.c_type == other.c_type)

    def _set_type(self, command: str) -> str:
        if (command_start := command.split()[0]) in ARITHMETIC_COMMANDS.keys():
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
        elif self.c_type == CType.PUSH:
            self._translate_push(filename)
        elif self.c_type == CType.POP:
            self._translate_pop(filename)
        elif self.c_type == CType.LABEL:
            self._translate_label()
        elif self.c_type == CType.GOTO:
            self._translate_goto()
        elif self.c_type == CType.IF:
            self._translate_if_goto()
        elif self.c_type == CType.FUNCTION:
            self._translate_function()
        elif self.c_type == CType.CALL:
            self._translate_call()
        elif self.c_type == CType.RETURN:
            self._translate_return()
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
            @SP
            M=M+1

        Args:
            filename (str): Name of vm file being translated
        """

        # All push operations have arg1 and arg2, so go ahead and assign to local variables
        segment = self.arg1
        index = int(self.arg2)

        # Implementation of `push constant n`
        if segment == "constant":
            self.translation.extend(
                [f"@{index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            )

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

    def _translate_label(self) -> None:
        """
        Should be of form `(functionName$label)` for labels inside of a function.
        Will be plain `(label)` otherwise
        """

        if self._current_function:
            label = LABEL.format(f"{self._current_function}${self.arg1}")
        else:
            label = LABEL.format(self.arg1)

        self.translation.append(label)

    def _translate_goto(self) -> None:
        self.translation.extend([line.format(self.arg1) for line in GOTO])

    def _translate_if_goto(self) -> None:
        self.translation.extend([line.format(self.arg1) for line in IF_GOTO])

    def _translate_function(self) -> None:
        self.translation.append(LABEL.format(self.arg1))
        self._current_function = self.arg1

        # If nVars is > 0, initialize all local variables to 0
        # In other words, repeat self.arg2 times: push constant 0
        if self.arg2 != "0":
            self.translation.extend(
                int(self.arg2) * ["@0", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            )

    def _translate_call(self) -> None:
        n_args = int(self.arg2)
        self.translation.extend(
            [
                # push the return address
                f"@RETURN_ADDRESS{self.label_count}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                # push LCL
                "@LCL",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                # push ARG
                "@ARG",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                # push THIS
                "@THIS",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                # push THAT
                "@THAT",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                # Set ARG = SP - n - 5
                "@SP",
                "D=M",
                f"@{5 + n_args}",
                "D=D-A",
                "@ARG",
                "M=D",
                # Set LCL = SP
                "@SP",
                "D=M",
                "@LCL",
                "M=D",
            ]
        )

        # goto function
        self._translate_goto()

        # (return-address) - declare the return-address label; this does not happen on the stack,
        # this happens in the assembly code so we return just below where we 'goto' the function.
        # Use the current label count to make them unique
        self.translation.append(LABEL.format(f"RETURN_ADDRESS{self.label_count}"))
        self.label_count += 1

    def _translate_return(self) -> None:
        self.translation.extend(
            [
                # endFrame
                "@LCL",
                "D=M",
                # retAddr = endFrame - 5
                "@5",
                "D=D-A",
                "@R13",
                "M=D",  # D register is now free to use
                # *ARG = pop()
                "@SP",
                "AM=M-1",
                "D=M",
                "@ARG",
                "A=M",
                "M=D",
                # SP = ARG + 1
                "@ARG",
                "D=M+1",
                "@SP",
                "M=D",
                # restore THAT
                "@R13",
                "D=M+1",
                "@3",
                "A=D+A",
                "D=M",
                "@THAT",
                "M=D",
                # restore THIS
                "@R13",
                "D=M+1",
                "@2",
                "A=D+A",
                "D=M",
                "@THIS",
                "M=D",
                # restore ARG
                "@R13",
                "D=M+1",
                "@2",
                "A=D+A",
                "D=M",
                "@ARG",
                "M=D",
                # restore LCL
                "@R13",
                "D=M+1",
                "@2",
                "A=D+A",
                "D=M",
                "@LCL",
                "M=D",
                # goto retAddr
                "@R13",
                "A=M",
                "A=M",
                "0;JMP",
            ]
        )


# TODO: Function commands
# return
