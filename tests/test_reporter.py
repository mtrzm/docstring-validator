from pathlib import Path

from docstring_validator import reporter


ERRORS = {
    Path("tests/dummy_module.py"): {
        "test_BUG2042005x": [
            {"Test Steps": ["Line: 23. Missnumbered, expected iterator: 2"]}
        ]
    },
    Path("tests/testing.py"): {
        "test_c": [{"Test Steps": ["Line: 3. B, expected iterator: 2"]}],
        "test_missing_docstring": ["Missing/Empty docstring"],
    },
}


def test_report_errors():
    report = reporter.report_errors(ERRORS)
    assert len(report) == 13
    assert isinstance(report, list)
