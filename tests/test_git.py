from pathlib import Path

import pytest

from docstring_validator import diff_util

REPO_PATH = Path(__file__).parent.parent.absolute()


@pytest.mark.xfail
def test_get_diffs():
    """Test setup is not yet automated."""
    diffs = [*diff_util.iter_diffs(REPO_PATH)]
    assert len(diffs) == 1


def test_find_func_names():
    diff = '''+    - blabla
    +def test_BUG1701():
    +    """Simple docstring."""
    +    return "1701"
    +
    +
    +def dummy():
    +    pass
    +
    +
    +
    +
    +class A:
    +    def b():
    +        pass
    +
    +    def d():
    +        pass
    '''
    diff = diff.split("\n")

    names = diff_util.find_func_names(diff, r"test_\w+")
    assert len(names) == 1
    assert names == ["test_BUG1701"]
