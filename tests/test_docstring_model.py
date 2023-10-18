from docstring_validator import chunks, docstring_model
from tests.static_data import VALID_DOCSTRING

ONE_LINER = """Simple docstring."""


def test_get_raw_chunks():
    chunks = docstring_model.Docstring._get_raw_chunks(VALID_DOCSTRING)

    assert len(chunks) == 6
    assert all([isinstance(chunk, list) for chunk in chunks])
    assert len(chunks[5]) == 3


def test_get_raw_chunks_oneliner():
    chunks = docstring_model.Docstring._get_raw_chunks(ONE_LINER)

    assert len(chunks) == 1
    assert chunks[0] == [ONE_LINER]


def test_parse_raw_chunks():
    expected_types = [
        chunks.DescriptionChunk,
        chunks.DescriptionChunk,
        chunks.StepsChunk,
        chunks.PassCriteriaChunk,
        chunks.FailCriteriaChunk,
        chunks.ReferencesChunk,
    ]

    docstring = docstring_model.Docstring(VALID_DOCSTRING)
    assert len(docstring.chunks) == len(expected_types)
    for chunk, type_ in zip(docstring.chunks, expected_types):
        assert isinstance(chunk, type_)
