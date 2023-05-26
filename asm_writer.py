"""
Module for functions to write all of the command translations out to file
"""

from command import Command


def translate_commands(commands: list[Command]) -> None:
    """
    Translate all commands by calling the translate method on every command in the list.

    Args:
        `commands` (list[Command]): The list of Commands being translated
    """

    for command in commands:
        command.translate()


def write_output_file(in_filename: str, commands: list[Command]) -> None:
    """
    Write an output file with the same name as the `in_filename` but with the .asm filetype

    Args:
        `in_filename` (str): The filename (without extension) of the file being translated
        `commands` (list[Command]): The list of Commands being translated and written
            to the .asm file
    """

    with open(f"{in_filename}.asm", "w", encoding="UTF-8") as out_file:
        for command in commands:
            out_file.write("\n".join(command.translation) + "\n")
