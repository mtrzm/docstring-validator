"""Functions for analysing python files.

Extracts code information using AST.
"""

import ast
from pathlib import Path
from typing import Optional, Tuple, Union


def get_docstring(py_file: Union[Path, str], func_name: str) -> Optional[str]:
    """Gets doctring for requested function.

    This function was not tested with class methods and inner functions.

    Args:
        py_file: path to python file with function to be checked
        func_name: name of searched function

    Returns:
        Docstring for requested function if present. If docstring is not defined
        this will return None.

    Raises:
        ValueError: if func_name is not found in py_file.
    """
    func = _get_function(py_file, func_name)
    return ast.get_docstring(func)


def get_func_ranges(
    py_file: Union[Path, str], func_name: str
) -> Tuple[int, Optional[int]]:
    """Gets line numbers for beginning and and of function declaration.

    This function was not tested with class methods and inner functions.

    Args:
        py_file: path to python file with function to be checked
        func_name: name of searched function

    Returns:
        Tuple containing numbers for first and last lines for searched function

    Raises:
        ValueError: if func_name is not found in py_file.
    """
    func = _get_function(py_file, func_name)
    return func.lineno, getattr(func, "end_lineno", None)


def _get_function(py_file: Union[Path, str], func_name: str) -> ast.FunctionDef:
    py_file = Path(py_file).resolve()
    tree = ast.parse(py_file.read_text())
    functions = [
        func
        for func in ast.walk(tree)
        if isinstance(func, ast.FunctionDef) and func.name == func_name
    ]

    if len(functions) == 0:
        raise ValueError(f"Function {func_name} not found in {py_file.absolute()}")
        # TODO test for multiple functions with the same name

    return functions[0]
