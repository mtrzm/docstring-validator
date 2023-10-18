"""Utilities for human readable error report."""
from string import Template
from typing import List

from docstring_validator.code_parser import get_func_ranges

COLORS = {
    "bold": "\033[1m",
    "red": "\033[31m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "reset": "\033[m",
}

ERROR_FORMAT = Template(
    "$bold$file$reset$cyan:$reset"
    "$magenta$func$reset$cyan:$reset"
    "$row$cyan:$reset "
    "$bold$red$code$reset $error"
)


def report_errors(errors: dict) -> List[str]:
    """Prepares report from unformatted errors.

    The input dictionary should have structure:
    {
        file_path_1: {
            analyzed_function_name_1: [Docstring level errors],
            analyzed_function_name_2: [Docstring level errors],
            },
        file_path_2: {...}
        }
    }
    Args:
        errors: dictionary containing detected errors

    Returns:
        Formatted error report as a list of strings.
    """
    report = []
    for file_, file_errors in errors.items():
        for func, func_errors in file_errors.items():
            start_line, _ = get_func_ranges(file_, func)
            for error in func_errors:
                report.append(
                    ERROR_FORMAT.substitute(
                        file=file_,
                        func=func,
                        row=start_line,
                        code=error.code,
                        error=error.text,
                        **COLORS,
                    )
                )

    return report
