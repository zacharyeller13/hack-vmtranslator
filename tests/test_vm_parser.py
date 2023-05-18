"""
Test methods for vm_parser module
"""

import os

from vm_parser import parse_file


valid_parsed_file = ["push constant 17", "push local 2", "add", "pop argument 1"]

def test_parse_file_basic():
    parsed_file = parse_file(f"{os.path.dirname(__file__)}/parser_test_file.vm")
    assert parsed_file == valid_parsed_file

def test_parse_file_whitespace():
    parsed_file = parse_file(f"{os.path.dirname(__file__)}/parser_test_file_whitespace.vm")
    assert parsed_file == valid_parsed_file


def test_parse_file_comments():
    parsed_file = parse_file(f"{os.path.dirname(__file__)}/parser_test_file_comments.vm")
    assert parsed_file == valid_parsed_file
