"""
Execution configuration objects.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionConfig:
    """
    Configuration for execution infrastructure.

    Attributes:
        retries:
            Number of retry attempts after a failure.

        timeout:
            Timeout in seconds for execution tasks.

        retry_delay:
            Delay in seconds between retry attempts.
    """

    retries: int = 3
    timeout: float = 30.0
    retry_delay: float = 1.0