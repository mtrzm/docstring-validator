"""Validators for Docstring and Chunk objects.

There are two types validators:
* Docstring validators
* Chunk validators

Docstring validators must accept chunks list and schema dictionary from Docstring
object and return detected errors as a list.

Chunk validators must accept content of the chunk as a list of strings from Chunk object
and return detected errors as a list.
"""
import re
from typing import List, Optional, Sequence

from docstring_validator.validation_error import ValidationError


def validate_ordered_list(content: List[str], type_: str) -> Optional[ValidationError]:
    """Validates that each element in ordered list starts with subsequent number."""
    if len(content) < 2:
        return ValidationError("E111", f"{type_} list elements are missing")

    elements = content[1:]
    elements = _merge_multiline_elements(elements, "ordered")
    if elements is None:
        return ValidationError(
            "E112", f"{type_} first element in a list should start with 1."
        )

    for i, line in enumerate(elements, 1):
        if not line.strip().startswith(f"{i}. "):
            return ValidationError(
                "E113", f"{type_} list elements have wrong numbering"
            )


def validate_unordered_list(
    content: List[str], type_: str
) -> Optional[ValidationError]:
    """Validates that each element in unordered list starts with a dash."""
    if len(content) < 2:
        return ValidationError("E121", f"{type_} list elements are missing")

    elements = content[1:]
    elements = _merge_multiline_elements(elements, "unordered")
    if elements is None:
        return ValidationError(
            "E122", f"{type_} first element in a list should start with -"
        )

    for line in elements:
        if not line.strip().startswith("- "):
            return ValidationError(
                "E123", f"{type_} list elements should start with a dash ('-')"
            )


def validate_paragraph(content: List[str], type_: str) -> Optional[ValidationError]:
    # TODO probably nothing to check here ¯\_(ツ)_/¯
    return


def _merge_multiline_elements(elements: List[str], type_: str) -> Optional[List[str]]:
    types = dict(ordered=r"\d+\.", unordered="-")
    index = f"^\\s*{types[type_]} "

    first_element = elements.pop(0)
    first_element_ok = _validate_first_element(first_element, type_)
    if not first_element_ok:
        return None

    merged = [first_element]

    for line in elements:
        if re.search(index, line):
            merged.append(line)
        else:
            merged[-1] = f"{merged[-1]} {line}"
    return merged


def _validate_first_element(first_element: str, type_: str) -> bool:
    first_element_index = dict(ordered="1. ", unordered="-")[type_]
    return bool(re.search(first_element_index, first_element))


def validate_chunk_occurences(chunks: Sequence, schema: dict) -> List[ValidationError]:
    """Validates if number of chunks of given type is in ranges defined in schema."""
    errors = []
    chunk_count = _count_chunk_types(chunks, schema)

    for type_, ranges in schema.items():
        actual = chunk_count[type_]
        section = type_.chunk_type.value
        min = ranges["min"]
        max = ranges["max"]

        if min > 0 and actual == 0:
            errors.append(ValidationError("E211", f"{section} section is missing"))
            continue

        if actual > max:
            errors.append(
                ValidationError(
                    "E212",
                    f"Detected {section} section {actual} time(s), max allowed is {max}",
                )
            )
            continue

        if actual < min:
            errors.append(
                ValidationError(
                    "E213",
                    f"Detected {section} section {actual} time(s), min allowed is {min}",
                )
            )
            continue

    return errors


def _count_chunk_types(chunks: Sequence, schema: dict) -> dict:
    counter = {type_: 0 for type_ in schema.keys()}
    for chunk in chunks:
        counter[type(chunk)] += 1
    return counter
