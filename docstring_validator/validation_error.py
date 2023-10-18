class ValidationError:
    def __init__(self, code: int, text: str):
        self.code = code
        self.text = text
