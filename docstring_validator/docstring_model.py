"""Data model for docstring content."""
from typing import List, Optional

from docstring_validator import chunks, validators
from docstring_validator.validation_error import ValidationError


class Docstring:
    """Data model for docstring.

    Attributes:
        schema: schema what sections should be present in docstring with expected occurence numbers
        chunks: parsed sections of docstring
        validators: list of validation functions to check data integrity
    """

    validators = [validators.validate_chunk_occurences]
    schema = {
        chunks.DescriptionChunk: dict(min=1, max=float("inf")),
        chunks.StepsChunk: dict(min=1, max=1),
        chunks.PassCriteriaChunk: dict(min=1, max=1),
        chunks.FailCriteriaChunk: dict(min=1, max=1),
        chunks.ReferencesChunk: dict(min=0, max=1),
    }

    def __init__(self, raw_docstring: Optional[str]):
        self._raw = raw_docstring

        if self._raw is None:
            self.chunks = []
        else:
            raw_chunks = self._get_raw_chunks(self._raw)
            self.chunks = self._parse_raw_chunks(raw_chunks)

    @classmethod
    def parse_docstring(cls, docstring: str):
        """Parses docstring for validation."""
        return cls(docstring)

    def validate(self) -> List[ValidationError]:
        """Runs validation functions for docstring and all sections.

        Returns:
            List of errors detected by validation functions.
        """
        errors = []

        if len(self.chunks) == 0:
            errors.append(ValidationError("E300", "Missing/Empty docstring"))
            return errors

        for validator in self.validators:
            result = validator(self.chunks, self.schema)
            if result:
                errors.extend(result)

        for chunk in self.chunks:
            result = chunk.validate()
            if result:
                errors.extend(result)
        return errors

    @staticmethod
    def _get_raw_chunks(raw_docstring: str) -> List[List[str]]:
        """Splits docstring into chunks based on empty lines."""
        string_chunks = raw_docstring.split("\n\n")
        raw_chunks = []
        for chunk in string_chunks:
            raw_chunks.append([line.strip() for line in chunk.split("\n") if line])
        return raw_chunks

    def _parse_raw_chunks(self, raw_chunks: List[List[str]]) -> List[chunks.Chunk]:
        """Parses raw docstring chunks into Chunk objects."""
        parsed_chunks = []

        for chunk in raw_chunks:
            parsed_chunks.append(chunks.Chunk(chunk))

        return parsed_chunks
