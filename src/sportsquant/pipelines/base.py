"""
Base pipeline abstractions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from sportsquant.pipelines.config import PipelineConfig


class BasePipeline(ABC):
    """
    Base class for every pipeline.
    """

    def __init__(
        self,
        config: PipelineConfig | None = None,
    ) -> None:
        """
        Initialize the pipeline.

        Args:
            config:
                Pipeline execution configuration.
        """
        self._config = config or PipelineConfig()

    @property
    def config(self) -> PipelineConfig:
        """
        Return the pipeline configuration.
        """
        return self._config

    @abstractmethod
    def run(self) -> None:
        """
        Execute the pipeline.
        """
        raise NotImplementedError