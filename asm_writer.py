"""
Module for functions to write all of the command translations out to file
"""

from __future__ import annotations

from command import Command
from constants import SYS_INIT


def write_init(directory: str) -> None:
    """
    Write bootstrap code that initializes the VM via .asm code.

    Args:
        `directory` (str): The directory being translated that will be the written filename

    Returns:
        list[list[str]]: A list of the initialization commands
    """

    sys_init = Command("call Sys.init 0")
    sys_init.translate()
    sys_init_commands = SYS_INIT #+ sys_init.translation

    with open(f"{directory}.asm", "w", encoding="UTF-8") as out_file:
        out_file.write("\n".join(sys_init_commands) + "\n")


def translate_commands(commands: list[Command]) -> None:
    """
    Translate all commands by calling the translate method on every command in the list.

    Args:
        `commands` (list[Command]): The list of Commands being translated
    """

    for command in commands:
        command.translate()


def write_translated_asm(in_filename: str, commands: list[Command]) -> None:
    """
    Write an output file with the same name as the `in_filename` but with the .asm filetype

    Args:
        `in_filename` (str): The filename (without extension) of the file being translated.
            Or the directory name which will be the out_file name
        `commands` (list[Command]): The list of Commands being translated and written
            to the .asm file
    """

    with open(f"{in_filename}.asm", "a", encoding="UTF-8") as out_file:
        for command in commands:
            out_file.write("\n".join(command.translation) + "\n")
