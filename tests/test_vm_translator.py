"""
Test methods for main VMTranslator module
"""

from pytest import MonkeyPatch, raises
from VMTranslator import initialize_argparser, initialize_arguments, Namespace

monkeypatch = MonkeyPatch()
arg_parser = initialize_argparser()


def test_initialize_arguments():
    mock_filepath = "C:/File/Path.vm"

    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args", lambda _: Namespace(file_or_dir=mock_filepath)
    )

    args = initialize_arguments(arg_parser)

    assert args.file_or_dir == mock_filepath


def test_initialize_arguments_invalid_file():
    mock_filepath = "C:/File/Path.asm"

    monkeypatch.setattr(
        "argparse.ArgumentParser.parse_args", lambda _: Namespace(file_or_dir=mock_filepath)
    )

    with raises(SystemExit):
        initialize_arguments(arg_parser)
