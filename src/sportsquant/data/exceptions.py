"""
Custom exceptions for the data layer.
"""


class DataError(Exception):
    """Base exception for all data-related errors."""


class DownloadError(DataError):
    """Raised when data download fails."""


class ValidationError(DataError):
    """Raised when downloaded data is invalid."""


class CacheError(DataError):
    """Raised when cache operations fail."""