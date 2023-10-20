from pathlib import Path

from docstring_validator import reporter
from docstring_validator.validation_error import ValidationError


ERRORS = {
    Path("tests/dummy_module.py"): {
        "test_BUG2042005": [
            ValidationError("E111", "Test Steps list elements are missing")
        ]
    },
    Path("tests/testing.py"): {
        "test_c": [
            ValidationError("E113", "Test Steps list elements have wrong numbering")
        ],
        "test_missing_docstring": [
            ValidationError("E211", "Test Steps section is missing")
        ],
    },
}


def test_report_errors():
    report = reporter.report_errors(ERRORS)
    assert isinstance(report, list)
    assert len(report) == 3
