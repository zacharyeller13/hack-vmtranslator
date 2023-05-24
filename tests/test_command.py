"""
Test methods for Command class
"""

from pytest import raises

from command import Command
from constants import CType

valid_parsed_file = ["push constant 17", "push local 2", "add", "pop argument 1"]
valid_parsed_commands = [
    Command("push constant 17"),
    Command("push local 2"),
    Command("add"),
    Command("pop argument 1"),
]


def test_command_type_push():
    assert Command(valid_parsed_file[0]).c_type == CType.PUSH


def test_command_type_pop():
    assert Command(valid_parsed_file[-1]).c_type == CType.POP


def test_command_type_arithmetic():
    assert Command(valid_parsed_file[2]).c_type == CType.ARITHMETIC


def test_command_arithmetic_arg1():
    assert Command("add").arg1 == "add"


def test_command_push_arg1():
    assert Command("push constant 17").arg1 == "constant"


def test_command_pop_arg1():
    assert Command("pop constant 17").arg1 == "constant"


def test_command_push_arg2():
    assert Command("push constant 17").arg2 == "17"


# Currently fails as arg1() does not account for other types besides arithmetic and push/pop
def test_command_arg1_return_raises_error():
    with raises(TypeError):
        Command("return").arg1


def test_command_arg2_return_raises_error():
    with raises(TypeError):
        Command("return").arg2


def test_translate_arithmetic_no_label():
    command = Command("add")
    command.translate()
    assert command.translation == ["// add", "@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"]


def test_translate_arithmetic_label():
    command = Command("eq")
    command.translate()
    assert command.translation == [
        "// eq",
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D",
        "@IF_EQ0",
        "D;JEQ",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_EQ0",
        "0;JMP",
        "(IF_EQ0)",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_EQ0)",
    ]


def test_translate_arithmetic_multiple_labels():
    command = Command("eq")
    Command.label_count = 5
    command.translate()
    assert command.translation == [
        "// eq",
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "D=M-D",
        "@IF_EQ5",
        "D;JEQ",
        "@SP",
        "A=M-1",
        "M=0",
        "@END_IF_EQ5",
        "0;JMP",
        "(IF_EQ5)",
        "@SP",
        "A=M-1",
        "M=-1",
        "(END_IF_EQ5)",
    ]


def test_translate_push_constant():
    command = Command("push constant 17")
    command.translate()
    assert command.translation == [
        "// push constant 17",
        "@17",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "M=M+1",
    ]
