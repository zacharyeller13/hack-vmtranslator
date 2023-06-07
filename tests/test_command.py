"""
Test methods for Command class
"""

from pytest import raises

from command import Command
from constants import CType

valid_parsed_file = [
    "push constant 17",
    "push local 2",
    "add",
    "pop argument 1",
    "label TEST_LABEL",
    "goto TEST_LABEL",
    "if-goto TEST_LABEL",
]


# Command type tests
def test_command_type_push():
    assert Command(valid_parsed_file[0]).c_type == CType.PUSH


def test_command_type_arithmetic():
    assert Command(valid_parsed_file[2]).c_type == CType.ARITHMETIC


def test_command_type_pop():
    assert Command(valid_parsed_file[3]).c_type == CType.POP


def test_command_type_label():
    assert Command(valid_parsed_file[4]).c_type == CType.LABEL


def test_command_type_GOTO():
    assert Command(valid_parsed_file[5]).c_type == CType.GOTO


def test_command_type_IF():
    assert Command(valid_parsed_file[6]).c_type == CType.IF


def test_command_type_FUNCTION():
    assert Command("function SimpleFunc.test 0").c_type == CType.FUNCTION


# Arg tests
def test_command_arithmetic_arg1():
    assert Command("add").arg1 == "add"


def test_command_push_arg1():
    assert Command("push constant 17").arg1 == "constant"


def test_command_pop_arg1():
    assert Command("pop constant 17").arg1 == "constant"


def test_command_push_arg2():
    assert Command("push constant 17").arg2 == "17"


def test_command_label_arg1():
    assert Command("label TEST_LABEL").arg1 == "TEST_LABEL"


def test_command_goto_arg1():
    assert Command("goto TEST_LABEL").arg1 == "TEST_LABEL"


def test_command_if_goto_arg1():
    assert Command("if-goto TEST_LABEL").arg1 == "TEST_LABEL"


def test_command_arg1_return_raises_error():
    with raises(TypeError):
        _ = Command("return").arg1


def test_command_arg2_return_raises_error():
    with raises(TypeError):
        _ = Command("return").arg2


def test_command_arg2_label_raises_error():
    with raises(TypeError):
        _ = Command("label TEST_LABEL").arg2


def test_command_arg2_goto_raises_error():
    with raises(TypeError):
        _ = Command("goto TEST_LABEL").arg2


def test_command_arg2_if_goto_raises_error():
    with raises(TypeError):
        _ = Command("if-goto TEST_LABEL").arg2


# Arithmetic translation command tests
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


# Push/Pop translation command tests
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
        "@SP",
        "M=M+1",
    ]


def test_translate_pop_local_0():
    command = Command("pop local 0")
    command.translate()
    assert command.translation == [
        "// pop local 0",
        "@SP",
        "AM=M-1",
        "D=M",
        "@LCL",
        "A=M",
        "M=D",
    ]


def test_translate_pop_local():
    command = Command("pop local 1")
    command.translate()
    assert command.translation == [
        "// pop local 1",
        "@1",
        "D=A",
        "@LCL",
        "D=D+M",
        "@SP",
        "AM=M-1",
        "D=D+M",
        "A=D-M",
        "M=D-A",
    ]


def test_translate_pop_local_2():
    command = Command("pop local 2")
    command.translate()
    assert command.translation == [
        "// pop local 2",
        "@2",
        "D=A",
        "@LCL",
        "D=D+M",
        "@SP",
        "AM=M-1",
        "D=D+M",
        "A=D-M",
        "M=D-A",
    ]


def test_translate_pop_argument_0():
    command = Command("pop argument 0")
    command.translate()
    assert command.translation == [
        "// pop argument 0",
        "@SP",
        "AM=M-1",
        "D=M",
        "@ARG",
        "A=M",
        "M=D",
    ]


def test_translate_pop_argument_2():
    command = Command("pop argument 2")
    command.translate()
    assert command.translation == [
        "// pop argument 2",
        "@2",
        "D=A",
        "@ARG",
        "D=D+M",
        "@SP",
        "AM=M-1",
        "D=D+M",
        "A=D-M",
        "M=D-A",
    ]


def test_translate_pop_temp():
    command = Command("pop temp 2")
    command.translate()
    assert command.translation == [
        "// pop temp 2",
        "@2",
        "D=A",
        "@5",
        "D=D+A",
        "@SP",
        "AM=M-1",
        "D=D+M",
        "A=D-M",
        "M=D-A",
    ]


def test_translate_pop_pointer_0():
    command = Command("pop pointer 0")
    command.translate()
    assert command.translation == [
        "// pop pointer 0",
        "@SP",
        "AM=M-1",
        "D=M",
        "@THIS",
        "M=D",
    ]


def test_translate_pop_pointer_1():
    command = Command("pop pointer 1")
    command.translate()
    assert command.translation == [
        "// pop pointer 1",
        "@SP",
        "AM=M-1",
        "D=M",
        "@THAT",
        "M=D",
    ]


def test_translate_pop_static_1():
    command = Command("pop static 1")
    command.translate(filename="TestFile")
    assert command.translation == [
        "// pop static 1",
        "@SP",
        "AM=M-1",
        "D=M",
        "@TestFile.1",
        "M=D",
    ]


def test_translate_push_local_2():
    command = Command("push local 2")
    command.translate()
    assert command.translation == [
        "// push local 2",
        "@2",
        "D=A",
        "@LCL",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_push_argument_2():
    command = Command("push argument 2")
    command.translate()
    assert command.translation == [
        "// push argument 2",
        "@2",
        "D=A",
        "@ARG",
        "A=D+M",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_push_temp():
    command = Command("push temp 2")
    command.translate()
    assert command.translation == [
        "// push temp 2",
        "@5",
        "D=A",
        "@2",
        "A=D+A",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_push_pointer_0():
    command = Command("push pointer 0")
    command.translate()
    assert command.translation == [
        "// push pointer 0",
        "@THIS",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_push_pointer_1():
    command = Command("push pointer 1")
    command.translate()
    assert command.translation == [
        "// push pointer 1",
        "@THAT",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_push_static_1():
    command = Command("push static 1")
    command.translate(filename="TestFile")
    assert command.translation == [
        "// push static 1",
        "@TestFile.1",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


# Branch commands translation
def test_translate_label():
    command = Command("label TEST_LABEL")
    command.translate()
    assert command.translation == ["// label TEST_LABEL", "(TEST_LABEL)"]


def test_translate_label_in_function():
    command = Command("label TEST_LABEL")
    command._current_function = "testFunction"
    command.translate()
    assert command.translation == ["// label TEST_LABEL", "(testFunction$TEST_LABEL)"]


def test_translate_goto():
    command = Command("goto TEST_LABEL")
    command.translate()
    assert command.translation == ["// goto TEST_LABEL", "@TEST_LABEL", "0;JMP"]


def test_translate_if_goto():
    command = Command("if-goto TEST_LABEL")
    command.translate()
    assert command.translation == [
        "// if-goto TEST_LABEL",
        "@SP",
        "AM=M-1",
        "D=M",
        "@TEST_LABEL",
        "D;JNE",
    ]


# Function commands translation
def test_translate_function():
    command = Command("function SimpleFunc.test 0")
    command.translate()
    assert command.translation == ["// function SimpleFunc.test 0", "(SimpleFunc.test)"]
    assert command._current_function == "SimpleFunc.test"


def test_translate_function_n_vars():
    command = Command("function SimpleFunc.test 3")
    command.translate()
    assert command.translation == [
        "// function SimpleFunc.test 3",
        "(SimpleFunc.test)",
        "@0",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@0",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@0",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def test_translate_function_call():
    command = Command("call SimpleFunc.test 2")
    command.label_count = 2
    command.translate()
    assert command.translation == [
        "// call SimpleFunc.test 2",
        # push the return address
        "@RETURN_ADDRESS2",
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
        "@7",  # 2 + 5
        "D=D-A",
        "@ARG",
        "M=D",
        # Set LCL = SP
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        # goto function
        "@SimpleFunc.test",
        "0;JMP",
        "(RETURN_ADDRESS2)"
    ]
