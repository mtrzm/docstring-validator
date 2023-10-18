import pytest

from docstring_validator import docstring_model
from docstring_validator import validators


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

unordered_lists_ok = [
    [
        "Pass criteria:",
        "- Fail criteria #1 with",
        "multiline description",
        "- Fail criteria #2",
    ]
]

unordered_lists_nok = [["Fail criteria:", "No dash"], ["Pass criteria:"]]


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
    assert validators.validate_ordered_list(docstring) == []


@pytest.mark.parametrize("docstring", unordered_lists_ok)
def test_validate_unordered_ok(docstring):
    assert validators.validate_unordered_list(docstring) == []


@pytest.mark.parametrize("docstring", ordered_lists_nok)
def test_validate_ordered_nok(docstring):
    result = validators.validate_ordered_list(docstring)
    assert isinstance(result, list)
    assert len(result) == 1


@pytest.mark.parametrize("docstring", unordered_lists_nok)
def test_validate_unordered_nok(docstring):
    result = validators.validate_unordered_list(docstring)
    assert isinstance(result, list)
    assert len(result) == 1


def test_validate_chunk_occurences_ok():
    result = validators.validate_chunk_occurences(
        TEST_DOCSTRING.chunks, TEST_DOCSTRING.schema
    )
    assert result == []
