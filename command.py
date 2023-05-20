"""
Command module
"""


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

    def __init__(self, command: str) -> None:
        self.command: str = command
        self.c_type: str = self._set_type(command)
        self.translation: list[str] = []

    def __eq__(self, other) -> bool:
        return self.command == other.command and self.c_type == other.c_type

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

    def translate(self) -> None:
        """
        Translates a command from its VM code to its assembly code
        """

        raise NotImplementedError