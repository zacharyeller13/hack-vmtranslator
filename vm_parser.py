"""
Parser module for parsing .vm file into its lexical components and providing access
to those components.
Ignores all whitespace and comments
"""

from __future__ import annotations
from glob import glob

from command import Command
from constants import COMMENT


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


def parse_directory(directory: str) -> list[str]:
    """
    Read in all files from a directory and return a list of the .vm files
    to be parsed

    Args:
        `directory` (str): The filepath to the directory to be parsed

    Returns:
        list[str]: All vm files in the directory
    """

    vm_files = glob(f"{directory}/*.vm")
    return vm_files


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
