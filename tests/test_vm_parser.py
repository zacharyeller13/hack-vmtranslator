"""
Test methods for vm_parser module
"""

import os
from pytest import raises

from vm_parser import parse_file, Command


valid_parsed_file = ["push constant 17", "push local 2", "add", "pop argument 1"]


def test_parse_file_basic():
    parsed_file = parse_file(f"{os.path.dirname(__file__)}/parser_test_file.vm")
    assert parsed_file == valid_parsed_file


def test_parse_file_whitespace():
    parsed_file = parse_file(
        f"{os.path.dirname(__file__)}/parser_test_file_whitespace.vm"
    )
    assert parsed_file == valid_parsed_file


def test_parse_file_comments():
    parsed_file = parse_file(
        f"{os.path.dirname(__file__)}/parser_test_file_comments.vm"
    )
    assert parsed_file == valid_parsed_file


def test_command_type_push():
    assert Command(valid_parsed_file[0]).c_type == "push"


def test_command_type_pop():
    assert Command(valid_parsed_file[-1]).c_type == "pop"


def test_command_type_arithmetic():
    assert Command(valid_parsed_file[2]).c_type == "arithmetic"


def test_command_arithmetic_arg1():
    assert Command("add").arg1() == "add"


def test_command_push_arg1():
    assert Command("push constant 17").arg1() == "constant"


def test_command_pop_arg1():
    assert Command("pop constant 17").arg1() == "constant"


def test_command_push_arg2():
    assert Command("push constant 17").arg2() == "17"


# Currently fails as arg1() does not account for other types besides arithmetic and push/pop
def test_command_arg1_return_raises_error():
    with raises(TypeError):
        Command("return").arg1()


def test_command_arg2_return_raises_error():
    with raises(TypeError):
        Command("return").arg2()
