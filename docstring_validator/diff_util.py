"""Library for iterating over possible inputs.

Iterating over file system or git diff output are supported.
"""
import os
import re
from pathlib import Path
from typing import Generator, List, NamedTuple, Optional, Sequence, Union

import git


class FileContent(NamedTuple):
    """Stores file path and content for analysis."""

    path: Path  # path of the modified file
    content: List[str]  # changed lines


def iter_diffs(
    path: Path,
    pattern: Optional[str] = None,
    baseline_rev: Optional[str] = None,
    target_rev: Optional[str] = None,
) -> Generator[FileContent, None, None]:
    """Yields git diffs for all modified files.

    Args:
        path: repository root path
        pattern: filter file types (regex)
        baseline_rev: git revision name for baseline or None for HEAD
        target_rev: git revision name for current or None for Index

    Yields:
        FileContent with path to file and added lines
    """
    repo = git.Repo(path)  # type: ignore

    baseline = repo.rev_parse(baseline_rev or "HEAD")
    target = repo.rev_parse(target_rev) if target_rev else git.Diffable.Index

    # equivalent to git diff --cached --unified=0 --patch
    for change in baseline.diff(target, unified=0, create_patch=True):
        # omit deleted files
        if change.b_path is None:
            continue
        if pattern is not None:
            if not re.search(pattern, change.b_path):
                continue

        file_path = path / change.b_path
        only_added_lines = _get_added_lines(change.diff.decode())

        result = FileContent(
            path=file_path,
            content=only_added_lines,
        )
        yield result


def iter_files(paths: List[Union[Path, str]]) -> Generator[FileContent, None, None]:
    """Yields python files with content for given directory.

    Args:
        paths: paths to files to be checked

    Yields:
        FileContent with path to file and full content
    """
    files = []
    for path in paths:
        path = Path(path).resolve()
        if path.is_file():
            files.append(path)
        else:
            files.extend(path.rglob("*.py"))
    files = set(files)

    for file_ in files:
        result = FileContent(path=file_, content=file_.read_text().split("\n"))
        yield result


def _get_added_lines(diff: str) -> List[str]:
    """Filters diff output to get only added lines."""
    return [line for line in diff.split("\n") if line.startswith("+")]


def find_func_names(
    diff: Sequence[str], func_name_pattern: Optional[str] = None
) -> List[str]:
    """Finds function names in diffs.

    Match is done for function declarations - `def <func_name_patter>`.
    Functions can be filtered using regex pattern.

    Args:
        diff: section to be analyzed
        func_name_pattern: regex pattern for function name

    Returns:
        List of detected function names
    """
    pattern = f"def ({func_name_pattern})"  # \W?def\s+(\w+) ?

    functions = []
    for line in diff:
        matches = re.search(pattern, line)
        if matches:
            functions.append(matches.group(1))
    return functions


def from_ref() -> Optional[str]:
    """Retrieves user provided --from-ref."""
    return os.environ.get("PRE_COMMIT_FROM_REF")


def to_ref() -> Optional[str]:
    """Retrieves user provided --to-ref."""
    return os.environ.get("PRE_COMMIT_TO_REF")
