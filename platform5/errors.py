class Platform5Error(Exception):
    def __init__(self, status_code: int, message: str, errors: str | None, request_id: str | None) -> None:
        self.status_code = status_code
        self.errors = errors
        self.request_id = request_id
        super().__init__(message)


class UnauthorizedError(Platform5Error):
    ...


class InsufficientBalanceError(Platform5Error):
    ...


class ForbiddenError(Platform5Error):
    ...


class NotFoundError(Platform5Error):
    ...


class ValidationError(Platform5Error):
    ...


class RateLimitError(Platform5Error):
    def __init__(self, status_code: int, message: str, errors: str | None, request_id: str | None, limit: int, remaining: int) -> None:
        self.limit = limit
        self.remaining = remaining
        super().__init__(status_code, message, errors, request_id)
