"""
Pipeline hook abstractions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class PipelineHook(ABC):
    """
    Base interface for pipeline execution hooks.

    Hooks provide extension points during pipeline execution
    without coupling infrastructure services directly to the
    PipelineExecutor.
    """

    @abstractmethod
    def before_run(self) -> None:
        """
        Called before pipeline execution begins.
        """
        raise NotImplementedError

    @abstractmethod
    def after_run(self) -> None:
        """
        Called after pipeline execution completes.
        """
        raise NotImplementedError