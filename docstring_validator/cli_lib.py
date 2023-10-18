"""Library for handling CLI related operations for Docstring Validator."""

import argparse
import sys

import docstring_validator


def get_args(args) -> argparse.Namespace:
    """Parse input arguments passed to CLI.

    Args:
        args: list of arguments to parse

    Returns:
        Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Docstring Validator is a tool for validating function docstrings against defined schema"
    )

    parser.add_argument("filenames", help="Filename for validation", nargs="*")
    parser.add_argument(
        "-name_pattern",
        "-p",
        required=False,
        help="Optional: function name pattern to filter analyzed functions (regex pattern)",
    )
    parser.add_argument(
        "-s",
        "--staged",
        action="store_true",
        help="Perform validation on files staged for commit",
    )
    return parser.parse_args(args)


def run_cli():
    """CLI entry point for docstring-validator."""
    args = get_args(sys.argv[1:])
    if args.staged:
        report = docstring_validator.analyze_staged(".", args.name_pattern)
    else:
        report = docstring_validator.analyze_files(args.filenames, args.name_pattern)

    if report:
        print("Issues found in docstrings by Docstring Validator:\n")
        print("\n".join(report))
    sys.exit(bool(report))
