from pathlib import Path

from docstring_validator import code_parser

REPO_PATH = Path(__file__).parent.parent.absolute()
DUMMY_MODULE = REPO_PATH / "tests" / "dummy_module.py"

docstring_data = dict(
    test_ping=dict(start=7, end=28),
    test_BUG1701=dict(start=31, end=33),
    test_BUG2137=dict(start=36, end=56),
    test_BUG2042005=dict(start=84, end=106),
)


def test_func_ranges():
    ranges = code_parser.get_func_ranges(DUMMY_MODULE, "test_ping")
    assert ranges == (7, 27)


def test_get_docstring():
    docstrings = [
        code_parser.get_docstring(DUMMY_MODULE, f_name) for f_name in docstring_data
    ]
    assert len(docstrings) == 4

    lens = (546, 17, 529, 532)
    for docstring, expected_len in zip(docstrings, lens):
        docstring = "" if docstring is None else docstring
        assert len(docstring) == expected_len
