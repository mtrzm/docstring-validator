import pytest

from docstring_validator import docstring_model
from docstring_validator import validators
from docstring_validator.validation_error import ValidationError


ordered_lists_ok = [
    [
        "Test steps:",
        "1. First step",
        "2. Second test step with",
        "multiline description",
        "3. Third step",
        "4. Fourth",
        "5. Last step",
    ]
]

ordered_lists_nok = [
    [
        "Test steps:",
        "1. First step",
        "34. Second test step with",
        "multiline description",
        "3. Third step",
        "4. Fourth",
        "5. Last step",
    ],
    ["Test steps:"],
    ["Test steps:", "Not starting with number"],
]
ordered_lists_codes = ["E113", "E111", "E112"]

unordered_lists_ok = [
    [
        "Pass criteria:",
        "- Fail criteria #1 with",
        "multiline description",
        "- Fail criteria #2",
    ]
]

unordered_lists_nok = [["Fail criteria:", "No dash"], ["Pass criteria:"]]
unordered_lists_codes = ["E122", "E121"]


TEST_DOCSTRING = docstring_model.Docstring(
    """Verify device can boot up after seven power resets.

During field tests it was discovered that device cannot boot up after
6 power resets performed within 10 minutes.

Test steps:
1. Perform power reset on device 7 times within 5 minutes
2. Verify all processes are up after 7th reboot

Pass criteria:
- All processes are up after each reboot
- Processes are brought up within 20 seconds from reboot

Fail criteria:
- Device does not boot up after any power reset
- Boot up time exceeds 20 seconds

Reference:
- BUG2137
- BUG2042005
"""
)


@pytest.mark.parametrize("docstring", ordered_lists_ok)
def test_validate_ordered_ok(docstring):
    assert validators.validate_ordered_list(docstring, "Test steps") is None


@pytest.mark.parametrize("docstring", unordered_lists_ok)
def test_validate_unordered_ok(docstring):
    assert validators.validate_unordered_list(docstring, "Pass criteria") is None


@pytest.mark.parametrize(
    "docstring, error_code", zip(ordered_lists_nok, ordered_lists_codes)
)
def test_validate_ordered_nok(docstring, error_code):
    result = validators.validate_ordered_list(docstring, "Test steps")
    assert isinstance(result, ValidationError)
    assert result.code == error_code
    assert isinstance(result.text, str)


@pytest.mark.parametrize(
    "docstring, error_code", zip(unordered_lists_nok, unordered_lists_codes)
)
def test_validate_unordered_nok(docstring, error_code):
    result = validators.validate_unordered_list(docstring, "Fail criteria")
    assert isinstance(result, ValidationError)
    assert result.code == error_code
    assert isinstance(result.text, str)


def test_validate_chunk_occurences_ok():
    result = validators.validate_chunk_occurences(
        TEST_DOCSTRING.chunks, TEST_DOCSTRING.schema
    )
    assert result == []
