"""Data models for allowed sections of docstring.

Allowed section types:
* Description
* Test steps
* Pass criteria
* Fail criteria
* References

Each section can have one of data types:
* ordered list
* unordered list
* text paragraph
"""
import abc
import enum
from typing import List

from docstring_validator import validators
from docstring_validator.validation_error import ValidationError


class ChunkTypes(enum.Enum):
    """Types of docstring chunks."""

    DESCRIPTION = "Description"
    TEST_STEPS = "Test Steps"
    PASS_CRITERIA = "Pass Criteria"
    FAIL_CRITERIA = "Fail Criteria"
    REFERENCE = "References"

    @staticmethod
    def get_types():
        """Returns available chunk types."""
        return [
            ChunkTypes.DESCRIPTION,
            ChunkTypes.TEST_STEPS,
            ChunkTypes.PASS_CRITERIA,
            ChunkTypes.FAIL_CRITERIA,
            ChunkTypes.REFERENCE,
        ]


class ContentTypes(enum.Enum):
    """Types of data that can be stored in a chunk."""

    ORDERED_LIST = 1
    UNORDERED_LIST = 2
    PARAGRAPH = 3


class Chunk(abc.ABC):
    """Data model for Docstring section.

    Attributes:
        chunk_type: section name
        content: actual content of the section
        content_type: type of data stored in section
        validators: list of validation functions to check data integrity
    """

    content_type: ContentTypes
    validators = []
    chunk_type: ChunkTypes

    def __new__(cls, content: List[str], *args, **kwargs):
        if cls is Chunk:
            chunk_type = cls._identify_chunk(content)
            cls = type_map[chunk_type]
        return object.__new__(cls)

    def __init__(self, content: List[str]):
        self.content = content

    def validate(self) -> List[ValidationError]:
        """Runs validation functions for the chunk.

        Returns:
            List of errors detected by validation functions.
        """
        if self.validators is None:
            return []
        if self.content is None:
            return [ValidationError("E100", f"No value for {self.chunk_type.value}")]

        errors = []
        for validator in self.validators:
            result = validator(self.content, self.chunk_type.value)
            if result:
                errors.append(result)
        return errors

    @staticmethod
    def _identify_chunk(chunk: List[str]) -> ChunkTypes:
        """Returns chunk type based on header (first line)."""
        chunk_headers = {
            "Test steps": ChunkTypes.TEST_STEPS,
            "Pass criteria": ChunkTypes.PASS_CRITERIA,
            "Fail criteria": ChunkTypes.FAIL_CRITERIA,
            "Reference": ChunkTypes.REFERENCE,
        }

        header = chunk[0].split(":")[0]
        return chunk_headers.get(header, ChunkTypes.DESCRIPTION)


class DescriptionChunk(Chunk):
    """Description section of docstring.

    This is generic section containing unstructured paragraph of text.
    Each docstring must contain at least one description section, preferably
    one line summary at the beginning of the docstring.
    """

    chunk_type = ChunkTypes.DESCRIPTION
    content_type = ContentTypes.PARAGRAPH
    validators = [validators.validate_paragraph]


class StepsChunk(Chunk):
    """Test steps section of docstring."""

    chunk_type = ChunkTypes.TEST_STEPS
    content_type = ContentTypes.ORDERED_LIST
    validators = [validators.validate_ordered_list]


class PassCriteriaChunk(Chunk):
    """Pass criteria section of docstring."""

    chunk_type = ChunkTypes.PASS_CRITERIA
    content_type = ContentTypes.UNORDERED_LIST
    validators = [validators.validate_unordered_list]


class FailCriteriaChunk(Chunk):
    """Fail criteria section of docstring."""

    chunk_type = ChunkTypes.FAIL_CRITERIA
    content_type = ContentTypes.UNORDERED_LIST
    validators = [validators.validate_unordered_list]


class ReferencesChunk(Chunk):
    """References section of docstring."""

    chunk_type = ChunkTypes.REFERENCE
    content_type = ContentTypes.UNORDERED_LIST
    validators = [validators.validate_unordered_list]

    def __init__(self, content: List[str]):
        self.content = self._parse_reference(content)

    def _parse_reference(self, content: List[str]) -> List[str]:
        if len(content) == 1:
            header, elements = content[0].split(":")
            elements = elements.split(",")
            elements = [f"- {el.strip()}" for el in elements]
            content = [header] + elements
        return content


type_map = {
    ChunkTypes.DESCRIPTION: DescriptionChunk,
    ChunkTypes.TEST_STEPS: StepsChunk,
    ChunkTypes.PASS_CRITERIA: PassCriteriaChunk,
    ChunkTypes.FAIL_CRITERIA: FailCriteriaChunk,
    ChunkTypes.REFERENCE: ReferencesChunk,
}
