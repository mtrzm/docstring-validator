class ValidationError:
    def __init__(self, code: str, text: str):
        self.code = code
        self.text = text
