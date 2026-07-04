"""
Shared data models for the data layer.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RequestConfig:
    """
    Configuration for an HTTP request.
    """

    url: str
    timeout: int = 30
    retries: int = 3


@dataclass(slots=True)
class ResponseData:
    """
    Standard response returned by downloaders.
    """

    success: bool
    status_code: int
    data: Any