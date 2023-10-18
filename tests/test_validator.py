from pathlib import Path
from typing import Dict, Optional, Union

import pytest

from docstring_validator.code_parser import get_docstring
from docstring_validator.diff_util import find_func_names
from docstring_validator.docstring_validator import _analyze_docstring

REPO_PATH = Path(__file__).parent.parent.absolute()
DATA = REPO_PATH / "tests" / "dummy_module.py"


def docstrings() -> Dict[str, Dict[str, Optional[Union[int, str]]]]:
    module_content = DATA.read_text()
    functions = find_func_names(module_content.split("\n"), r"test_\w+")
    docstrings = {
        func: dict(docstring=get_docstring(DATA, func), errors=0) for func in functions
    }
    docstrings["test_BUG1701"]["errors"] = 3
    return docstrings


DOCSTRINGS = docstrings()


@pytest.mark.parametrize("docstring", DOCSTRINGS.values(), ids=DOCSTRINGS.keys())
def test_analyze_docstring(docstring):
    errors = _analyze_docstring(docstring["docstring"])
    assert len(errors) == docstring["errors"]
