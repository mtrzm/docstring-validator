from setuptools import setup, find_packages

setup(
    name="docstring_validator",
    version="1.0.0",
    description="Pre-commit hook for validating function names against provided schema",
    packages=find_packages(),
    install_requires=["GitPython"],
    entry_points={
        "console_scripts": ["docstring-validator = docstring_validator.cli_lib:run_cli"]
    },
)
