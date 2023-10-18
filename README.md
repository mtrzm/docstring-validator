# Introduction

Doctring Validator is a tool to analyze docstrings against defined schema. It was developed with test functions in mind, that's why schema contains sections like `Test steps` and `Pass/Fail criteria`. It's configured to be used as [pre-commit](https://pre-commit.com/) hook.


# Usage examples
## pre-commit integration

To enable Docstring Validator in your pre-commit configuration it is required to extend `repos` section in `.pre-commit-config.yaml` with hook declaration:

```yaml
- repo: <TODO link to final repo>
  rev: 1.0.0
  hooks:
  - id: docstring-validator
    args: [-name_pattern=test_\w+, -s]
    pass_filenames: false
```

where `-name_pattern` is optional argument.

## CLI
After installation Docstring Validator is available under `docstring-validator` entry point in CLI. Example usage:
```
% docstring-validator -name_pattern test_\\w+ file1.py file2.py
```

If directory is provided then it will be recursively checked for `*.py` files.

### Staged files check
The `-s` flag can be used to analyze only files staged for commit in git repository. In this mode only functions staged for commit will be analyzed. This method uses current working directory, so should be run from root directory of git repository. Example usage:

```
% docstring-validator -name_pattern test_\\w+ -s
```

## Python package
Docstring Validator can be used as a python module. It provides two functions that represent both CLI modes: `analyze_files` and `analyze_staged`. Example:

### Analyze files
    >>> import pathlib
    >>> import docstring_validator
    >>> pattern = r"test_\w+"
    >>> path = [pathlib.Path("test_api.py"), pathlib.Path("test_backend.py")]
    >>> report = docstring.validator.analyze_files(path, pattern)

### Diff analysis
    >>> import pathlib
    >>> import docstring_validator
    >>> pattern = r"test_\w+"
    >>> path = pathlib.Path(".")
    >>> report = docstring.validator.analyze_staged(path, pattern)

## Installation
Currently Docstring Validator can be installed from source code:

    pip install docstring_validator/
