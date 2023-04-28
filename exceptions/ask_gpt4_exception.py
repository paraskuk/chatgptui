class GPTException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code



