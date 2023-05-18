"""
Constants for both VM language and ASM language
"""

COMMENT = "//"
VAR_START = "@"

# Arithmetic/Logical Commands
# Dictionary containing list of ASM instructions to complete each VM arithmetic/logic command
ARITHMETIC_COMMANDS = {
    "add": ["@SP", "AM=A-1", "D=M", "A=A-1", "M=D+M"],
    "sub": ["@SP", "AM=A-1", "D=M", "A=A-1", "M=M-D"],
    "neg": ["@SP", "A=M-1", "M=-M"],
    "eq": [""],
    "get": [""],
    "lt": [""],
    "and": [""],
    "or": [""],
    "not": [""],
}
