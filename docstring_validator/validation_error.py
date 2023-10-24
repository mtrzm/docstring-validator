"""Library with classes for representing validation errors."""


class ValidationError:
    """Representation of single validation error.

    Attributes:
        code: error code describing validation error
        text: description of discovered error
    """

    def __init__(self, code: str, text: str):
        self.code = code
        self.text = text
