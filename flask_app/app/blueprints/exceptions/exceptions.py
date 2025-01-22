class ValidationError(Exception):
    def __init__(self, errors, status_code=400):
        super().__init__(errors)
        self.errors = errors
        self.status_code = status_code
