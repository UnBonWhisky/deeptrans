from typing import Optional

class DeepLException(Exception):
    """Base exception for DeepL API errors."""
    def __init__(self, message: str, http_status_code: Optional[int] = None, should_retry: bool = False):
        super().__init__(message)
        self.http_status_code = http_status_code
        self.should_retry = should_retry


class AuthorizationException(DeepLException):
    """Exception raised when authentication fails."""
    pass


class QuotaExceededException(DeepLException):
    """Exception raised when the character limit is exceeded."""
    pass


class TooManyRequestsException(DeepLException):
    """Exception raised when too many requests are made."""
    pass