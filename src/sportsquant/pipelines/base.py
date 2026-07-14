"""
Base pipeline abstractions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BasePipeline(ABC):
    """
    Base class for every pipeline.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Execute the pipeline.
        """
        raise NotImplementedError