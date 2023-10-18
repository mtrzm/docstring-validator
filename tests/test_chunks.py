import pytest

from docstring_validator import chunks
from tests.static_data import RAW_CHUNKS


VALID_REFERENCES = [
    ["Reference: BUG2137, BUG2042005"],
    ["Reference:", "- BUG2137,", "- BUG2042005"],
]


@pytest.mark.parametrize("expected_type, raw_chunk", RAW_CHUNKS.items())
def test_identify_chunk(expected_type, raw_chunk):
    chunk_type = chunks.Chunk._identify_chunk(raw_chunk)
    assert chunk_type == expected_type


@pytest.mark.parametrize("expected_type, raw_chunk", RAW_CHUNKS.items())
def test_chunk_constructor(expected_type, raw_chunk):
    chunk = chunks.Chunk(raw_chunk)
    assert isinstance(chunk, chunks.type_map[expected_type])
    assert chunk.content == raw_chunk


@pytest.mark.parametrize("chunk", VALID_REFERENCES)
def test_reference_chunk(chunk):
    ref = chunks.ReferencesChunk(chunk)
    assert len(ref.content) == 3
