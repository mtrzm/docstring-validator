"""Runners for different modes of operation for docstring validator."""
from pathlib import Path
from typing import Generator, List, Optional, Union

from docstring_validator import diff_util
from docstring_validator.code_parser import get_docstring
from docstring_validator.docstring_model import Docstring
from docstring_validator.reporter import report_errors
from docstring_validator.validation_error import ValidationError


def analyze_staged(
    path: Union[Path, str], func_name_filter: Optional[str] = None
) -> List[str]:
    """Finds new functions in staged files and analyzes docstrings.

    To filter functions to be analyzed `func_name_filter` must be provided.
    This is positive filter (only functions with names matching the pattern)
    will be analyzed. This argument has standard python regex format. For example
    to analyze only `test` functions (functions names starting with `test_`):

    >>> import pathlib
    >>> import docstring_validator
    >>> pattern = "test_\\w+"
    >>> path = pathlib.Path(".")
    >>> docstring.validator.analyze_staged(path, pattern)
    ...

    Args:
        path: repository root path
        func_name_filter: pattern for function names

    Returns:
        Text report from analysis
    """
    print(Path(path))
    print(Path(path).resolve())
    generator = diff_util.iter_diffs(
        Path(path).resolve(),
        pattern=r"\.py$",
        baseline_rev=diff_util.from_ref(),
        target_rev=diff_util.to_ref(),
    )
    return _analyze_files(generator, func_name_filter)


def analyze_files(
    path: List[Union[Path, str]], func_name_filter: Optional[str] = None
) -> List[str]:
    """Finds functions in files in provided location and analyzes docstrings.

    Path can be file name or directory. If directory is provided, then it will
    be recursively searched for python files.

    To filter functions to be analyzed `func_name_filter` must be provided.
    This is positive filter (only functions with names matching the pattern)
    will be analyzed. This argument has standard python regex format. For example
    to analyze only `test` functions (functions names starting with `test_`):

    >>> import pathlib
    >>> import docstring_validator
    >>> pattern = "test_\\w+"
    >>> path = [pathlib.Path("test_api.py"), pathlib.Path("test_backend.py")]
    >>> docstring.validator.analyze_files(path, pattern)
    ...

    Args:
        path: paths to files to be analyzed
        func_name_filter: pattern for function names

    Returns:
        Text report from analysis
    """
    generator = diff_util.iter_files(path)
    return _analyze_files(generator, func_name_filter)


def _analyze_files(
    generator: Generator, func_name_filter: Optional[str] = None
) -> List[str]:
    errors = {}
    for file in generator:
        func_names = diff_util.find_func_names(file.content, func_name_filter)
        print(func_names)

        file_errors = {}
        for func in func_names:
            result = _analyze_docstring(get_docstring(file.path, func))
            if result:
                file_errors[func] = result
        if file_errors:
            errors[file.path] = file_errors

    report = report_errors(errors)
    print(report)
    return report


def _analyze_docstring(
    raw_docstring: Optional[str],
) -> List[ValidationError]:
    """Checks if docstring adheres to schema."""
    print(raw_docstring)
    docstring = Docstring(raw_docstring)
    errors = docstring.validate()
    print(errors)
    return errors
