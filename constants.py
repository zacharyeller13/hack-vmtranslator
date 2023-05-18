"""
Constants for both VM language and ASM language
"""

COMMENT = "//"
VAR_START = "@"

# Base Address Pointers - may not be necessary but will keep til later
SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4

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
        "@IF_EQ",
        "D;JEQ",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_EQ",
        "0;JMP",
        "(IF_EQ)",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_EQ)",
    ],
    "gt": [
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D ",
        "@IF_GT",
        "D;JGT",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_GT ",
        "0;JMP",
        "(IF_GT)",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_GT)",
    ],
    "lt": [
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D ",
        "@IF_GT",
        "D;JLT",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_GT ",
        "0;JMP",
        "(IF_GT)",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_GT)",
    ],
    "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
    "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
    "not": ["@SP", "AM=M-1", "M=!M"],
}
