"""
Constants for both VM language and ASM language
"""

from enum import Enum


COMMENT = "//"
VAR_START = "@"
LABEL = "({})"
GOTO = ["@{}", "0;JMP"]
IF_GOTO = ["@SP", "AM=M-1", "D=M", "@{}", "D;JNE"]


class CType(str, Enum):
    """
    Command type constants

    Inherits from both str and Enum rather than the simple StrEnum as a workaround in Python3.8
        which the course grader uses
    """

    ARITHMETIC = "arithmetic"
    PUSH = "push"
    POP = "pop"
    LABEL = "label"
    GOTO = "goto"
    IF = "if-goto"
    FUNCTION = "function"
    RETURN = "return"
    CALL = "call"


# Base Address Pointers - may not be necessary but will keep til later
# Additionally, Temp is RAM[5]-RAM[12] and static is RAM[16]-RAM[255]
SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4

# Segment Abbreviations
SEGMENTS = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

# Arithmetic/Logical Commands
# Dictionary containing list of ASM instructions to complete each VM arithmetic/logic command
# Labels like "(IF_EQ)" will get appended with a number later on when there is more than 1
ARITHMETIC_COMMANDS = {
    "add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"],
    "sub": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"],
    "neg": ["@SP", "A=M-1", "M=-M"],
    "eq": [
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D",
        "@IF_EQ{}",
        "D;JEQ",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_EQ{}",
        "0;JMP",
        "(IF_EQ{})",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_EQ{})",
    ],
    "gt": [
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D ",
        "@IF_GT{}",
        "D;JGT",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_GT{}",
        "0;JMP",
        "(IF_GT{})",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_GT{})",
    ],
    "lt": [
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D ",
        "@IF_LT{}",
        "D;JLT",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_LT{}",
        "0;JMP",
        "(IF_LT{})",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_LT{})",
    ],
    "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
    "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
    "not": ["@SP", "A=M-1", "M=!M"],
}
